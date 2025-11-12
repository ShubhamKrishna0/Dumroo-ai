import os
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_core.messages import HumanMessage, AIMessage
import pandas as pd
from typing import Dict, Any, List
import re
import json

class AIQueryEngine:
    def __init__(self, api_key: str):
        os.environ["OPENAI_API_KEY"] = api_key
        self.llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
        # Simple conversation context management
        self.max_context_length = 5
        self.conversation_context = []
    
    def parse_query_intent(self, query: str, context: List[Dict] = None) -> Dict[str, Any]:
        """Enhanced query parsing with context awareness"""
        query_lower = query.lower()
        
        intent_mapping = {
            "homework": ["homework", "assignment", "submit", "turn in", "hand in"],
            "performance": ["performance", "score", "grade", "result", "achievement", "progress"],
            "quiz": ["quiz", "test", "exam", "upcoming", "scheduled", "assessment"],
            "analytics": ["average", "mean", "statistics", "summary", "report", "analysis"],
            "support": ["help", "support", "struggling", "difficulty", "improve", "below"],
            "comparison": ["compare", "versus", "vs", "difference", "better", "worse"]
        }
        
        # Extract entities with improved patterns
        grade_match = re.search(r'grade\s*(\d+)', query_lower)
        grade = f"Grade {grade_match.group(1)}" if grade_match else None
        
        # Enhanced time extraction
        time_patterns = {
            "last week": "2024-W02",
            "this week": "2024-W03", 
            "next week": "2024-W04",
            "recent": "2024-W02"
        }
        
        week = None
        for pattern, value in time_patterns.items():
            if pattern in query_lower:
                week = value
                break
        
        # Score threshold extraction
        score_match = re.search(r'(below|under|less than|above|over|more than)\s*(\d+)', query_lower)
        score_threshold = None
        score_operator = None
        if score_match:
            operator = score_match.group(1)
            threshold = int(score_match.group(2))
            score_threshold = threshold
            score_operator = "<" if operator in ["below", "under", "less than"] else ">"
        
        # Determine intent with priority
        intent = "general"
        confidence = 0
        for key, keywords in intent_mapping.items():
            matches = sum(1 for keyword in keywords if keyword in query_lower)
            if matches > confidence:
                intent = key
                confidence = matches
        
        # Context-aware intent refinement
        if context and len(context) > 0:
            last_intent = context[-1].get("intent", "")
            if "follow" in query_lower or "also" in query_lower or "what about" in query_lower:
                intent = last_intent  # Continue previous conversation thread
        
        return {
            "intent": intent,
            "grade": grade,
            "week": week,
            "score_threshold": score_threshold,
            "score_operator": score_operator,
            "confidence": confidence,
            "original_query": query,
            "context_aware": bool(context and len(context) > 0)
        }
    
    def generate_contextual_response(self, data_result: pd.DataFrame, query_info: Dict, admin_id: str) -> str:
        """Generate intelligent, contextual responses"""
        intent = query_info["intent"]
        
        if data_result.empty:
            return self._generate_empty_response(intent, query_info)
        
        # Intent-specific response generation
        if intent == "homework":
            return self._format_homework_response(data_result, query_info)
        elif intent == "performance":
            return self._format_performance_response(data_result, query_info)
        elif intent == "quiz":
            return self._format_quiz_response(data_result, query_info)
        elif intent == "analytics":
            return self._format_analytics_response(data_result, query_info)
        elif intent == "support":
            return self._format_support_response(data_result, query_info)
        else:
            return self._format_general_response(data_result, query_info)
    
    def _generate_empty_response(self, intent: str, query_info: Dict) -> str:
        """Generate appropriate responses for empty results"""
        responses = {
            "homework": "Great news! All students in your scope have submitted their homework.",
            "performance": "No performance data found matching your criteria.",
            "quiz": "No quizzes found matching your search criteria.",
            "analytics": "Insufficient data to generate analytics for your request.",
            "support": "All students appear to be performing well based on available data."
        }
        return responses.get(intent, "No data found matching your query criteria.")
    
    def _format_homework_response(self, data: pd.DataFrame, query_info: Dict) -> str:
        """Format homework-related responses"""
        if 'homework_submitted' in data.columns:
            missing = data[data['homework_submitted'] == False]
            if not missing.empty:
                return self._format_as_table(missing[['student_name', 'grade', 'class']], 
                                           f"Students Missing Homework ({len(missing)} out of {len(data)})")
        return "All students have submitted their homework."
    
    def _format_performance_response(self, data: pd.DataFrame, query_info: Dict) -> str:
        """Format performance-related responses"""
        if 'quiz_score' in data.columns:
            threshold = query_info.get('score_threshold')
            operator = query_info.get('score_operator')
            
            if threshold and operator:
                if operator == '<':
                    filtered_data = data[data['quiz_score'] < threshold]
                    title = f"Students with Quiz Scores Below {threshold}"
                elif operator == '>':
                    filtered_data = data[data['quiz_score'] > threshold]
                    title = f"Students with Quiz Scores Above {threshold}"
                else:
                    filtered_data = data
                    title = "Performance Analysis"
            else:
                filtered_data = data
                title = "Performance Analysis"
            
            if filtered_data.empty:
                return f"No students found matching your criteria."
            
            avg_score = filtered_data['quiz_score'].mean()
            summary = f"Average: {avg_score:.1f} | Total: {len(filtered_data)} students"
            
            return self._format_as_table(filtered_data[['student_name', 'grade', 'class', 'quiz_score']], 
                                       title, summary)
        return "Performance data processed successfully."
    
    def _format_quiz_response(self, data: pd.DataFrame, query_info: Dict) -> str:
        """Format quiz-related responses"""
        if 'upcoming_quiz' in data.columns:
            quiz_data = data[['student_name', 'grade', 'class', 'upcoming_quiz', 'upcoming_quiz_date']].drop_duplicates()
            unique_quizzes = data['upcoming_quiz'].nunique()
            summary = f"Total Unique Quizzes: {unique_quizzes}"
            return self._format_as_table(quiz_data, "Upcoming Quizzes", summary)
        return "Quiz data processed successfully."
    
    def _format_analytics_response(self, data: pd.DataFrame, query_info: Dict) -> str:
        """Format analytics responses with insights"""
        insights = []
        
        if 'quiz_score' in data.columns:
            avg_score = data['quiz_score'].mean()
            min_score = data['quiz_score'].min()
            max_score = data['quiz_score'].max()
            insights.append(f"Quiz Score Analytics:")
            insights.append(f"   • Average: {avg_score:.1f}")
            insights.append(f"   • Range: {min_score} - {max_score}")
        
        if 'homework_submitted' in data.columns:
            homework_rate = (data['homework_submitted'].sum() / len(data) * 100)
            insights.append(f"Homework Completion: {homework_rate:.1f}%")
        
        return "\n".join(insights) if insights else "Analytics generated successfully."
    
    def _format_support_response(self, data: pd.DataFrame, query_info: Dict) -> str:
        """Format support-focused responses"""
        if 'quiz_score' in data.columns:
            threshold = query_info.get('score_threshold', 75)
            operator = query_info.get('score_operator', '<')
            
            if operator == '<':
                struggling = data[data['quiz_score'] < threshold]
                if not struggling.empty:
                    recommendation = "Recommendation: Consider additional tutoring or review sessions."
                    return self._format_as_table(struggling[['student_name', 'grade', 'class', 'quiz_score']], 
                                               f"Students Needing Support (scores < {threshold})", recommendation)
                else:
                    return f"Excellent! All students have quiz scores of {threshold} or above."
            else:
                excelling = data[data['quiz_score'] > threshold]
                if not excelling.empty:
                    recommendation = "Recommendation: Consider advanced challenges or peer tutoring opportunities."
                    return self._format_as_table(excelling[['student_name', 'grade', 'class', 'quiz_score']], 
                                               f"High-Performing Students (scores > {threshold})", recommendation)
                else:
                    return f"No students found with scores above {threshold}."
        
        return "Support analysis completed."
    
    def _format_general_response(self, data: pd.DataFrame, query_info: Dict) -> str:
        """Format general responses"""
        return self._format_as_table(data, "Query Results", f"Total Records: {len(data)}")
    
    def _format_as_table(self, data: pd.DataFrame, title: str, summary: str = None) -> str:
        """Format DataFrame as a clean table with title and summary"""
        if data.empty:
            return f"{title}: No data found"
        
        # Create clean column headers
        clean_data = data.copy()
        clean_data.columns = [col.replace('_', ' ').title() for col in clean_data.columns]
        
        # Format the table
        table_str = clean_data.to_string(index=False, justify='left')
        
        # Build response
        response_parts = [f"** {title} **", "=" * (len(title) + 6), table_str]
        
        if summary:
            response_parts.extend(["", f"Summary: {summary}"])
        
        return "\n".join(response_parts)
    
    def execute_query(self, data_manager, admin_id: str, query: str) -> str:
        """Enhanced query execution with context awareness and agent-style handling"""
        # Parse query with conversation context
        parsed = self.parse_query_intent(query, self.conversation_context)
        
        try:
            # Add current query to context
            self.conversation_context.append({
                "query": query,
                "intent": parsed["intent"],
                "timestamp": pd.Timestamp.now().isoformat()
            })
            
            # Keep only last 5 interactions for context
            if len(self.conversation_context) > 5:
                self.conversation_context = self.conversation_context[-5:]
            
            # Execute based on intent
            if parsed["intent"] == "homework":
                df = data_manager.get_students_without_homework(admin_id)
                return self.generate_contextual_response(df, parsed, admin_id)
            
            elif parsed["intent"] == "performance":
                df = data_manager.get_performance_data(admin_id, parsed["grade"], parsed["week"])
                return self.generate_contextual_response(df, parsed, admin_id)
            
            elif parsed["intent"] == "support" or (parsed.get("score_threshold") and parsed.get("score_operator")):
                df = data_manager.filter_data_by_scope(admin_id)
                return self.generate_contextual_response(df, parsed, admin_id)
            
            elif parsed["intent"] == "quiz":
                df = data_manager.get_upcoming_quizzes(admin_id)
                return self.generate_contextual_response(df, parsed, admin_id)
            
            elif parsed["intent"] == "analytics":
                df = data_manager.filter_data_by_scope(admin_id)
                return self.generate_contextual_response(df, parsed, admin_id)
            
            elif parsed["intent"] == "support":
                df = data_manager.filter_data_by_scope(admin_id)
                return self.generate_contextual_response(df, parsed, admin_id)
            
            else:
                # Enhanced pandas agent with context
                filtered_df = data_manager.filter_data_by_scope(admin_id)
                if filtered_df.empty:
                    return "No data available in your access scope."
                
                # Create context-aware prompt
                context_prompt = self._build_context_prompt(query, parsed)
                
                agent = create_pandas_dataframe_agent(
                    self.llm,
                    filtered_df,
                    verbose=False,
                    allow_dangerous_code=True
                )
                
                result = agent.run(context_prompt)
                return f"AI Analysis:\n\n{result}"
                
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "429" in error_msg:
                # Try fallback for quota exceeded
                fallback_response = self._try_fallback_query(query, data_manager, admin_id)
                if fallback_response:
                    return fallback_response
                return "API quota exceeded. Please check your OpenAI billing or try basic queries like 'best student' or 'homework status'."
            return f"Error processing query: {error_msg}\n\nTry rephrasing your question or use one of the example queries."
    
    def _build_context_prompt(self, query: str, parsed: Dict) -> str:
        """Build context-aware prompt for the pandas agent"""
        context_info = ""
        if self.conversation_context:
            recent_queries = [ctx["query"] for ctx in self.conversation_context[-3:]]
            context_info = f"Previous queries in this conversation: {', '.join(recent_queries)}. "
        
        enhanced_prompt = f"""
        {context_info}Current query: {query}
        
        Please analyze the student data and provide insights. Focus on:
        - Clear, actionable information
        - Relevant statistics and summaries
        - Educational context and recommendations
        
        Format your response professionally with appropriate emojis and structure.
        """
        
        return enhanced_prompt
    
    def reset_context(self):
        """Reset conversation context"""
        self.conversation_context = []
    
    def _try_fallback_query(self, query: str, data_manager, admin_id: str) -> str:
        """Handle basic queries without OpenAI API"""
        query_lower = query.lower()
        
        try:
            df = data_manager.filter_data_by_scope(admin_id)
            if df.empty:
                return "No data available in your scope."
            
            # Best student query
            if any(word in query_lower for word in ['best', 'top', 'highest', 'excellent']):
                if 'quiz_score' in df.columns:
                    best_student = df.loc[df['quiz_score'].idxmax()]
                    return f"**Best Performing Student**\n\nName: {best_student['student_name']}\nGrade: {best_student['grade']}\nClass: {best_student['class']}\nQuiz Score: {best_student['quiz_score']}"
            
            # Homework status
            if 'homework' in query_lower:
                if 'homework_submitted' in df.columns:
                    missing = df[df['homework_submitted'] == False]
                    if missing.empty:
                        return "All students have submitted their homework."
                    return self._format_as_table(missing[['student_name', 'grade', 'class']], "Students Missing Homework")
            
            # Average score
            if any(word in query_lower for word in ['average', 'mean']):
                if 'quiz_score' in df.columns:
                    avg = df['quiz_score'].mean()
                    return f"Average quiz score in your scope: {avg:.1f}"
            
            # List all students
            if any(word in query_lower for word in ['list', 'show', 'all students']):
                return self._format_as_table(df[['student_name', 'grade', 'class', 'quiz_score']], "All Students in Your Scope")
            
            return None
            
        except Exception:
            return None
    
    def get_conversation_summary(self) -> Dict:
        """Get summary of current conversation"""
        return {
            "total_queries": len(self.conversation_context),
            "recent_intents": [ctx["intent"] for ctx in self.conversation_context[-5:]],
            "conversation_length": len(self.conversation_context)
        }