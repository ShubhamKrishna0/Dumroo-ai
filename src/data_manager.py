import json
import pandas as pd
from typing import Dict, List, Any
from datetime import datetime, timedelta

class DataManager:
    def __init__(self, students_file: str, admins_file: str):
        self.students_df = pd.read_json(students_file)
        with open(admins_file, 'r') as f:
            self.admin_roles = json.load(f)
    
    def get_admin_scope(self, admin_id: str) -> Dict[str, List[str]]:
        """Get access scope for specific admin"""
        for admin in self.admin_roles:
            if admin['admin_id'] == admin_id:
                return admin['access_scope']
        return {}
    
    def filter_data_by_scope(self, admin_id: str) -> pd.DataFrame:
        """Filter student data based on admin's access scope"""
        scope = self.get_admin_scope(admin_id)
        if not scope:
            return pd.DataFrame()
        
        filtered_df = self.students_df.copy()
        
        # Apply filters based on admin scope
        if 'grades' in scope:
            filtered_df = filtered_df[filtered_df['grade'].isin(scope['grades'])]
        if 'classes' in scope:
            filtered_df = filtered_df[filtered_df['class'].isin(scope['classes'])]
        if 'regions' in scope:
            filtered_df = filtered_df[filtered_df['region'].isin(scope['regions'])]
            
        return filtered_df
    
    def get_students_without_homework(self, admin_id: str) -> pd.DataFrame:
        """Get students who haven't submitted homework within admin scope"""
        filtered_df = self.filter_data_by_scope(admin_id)
        return filtered_df[filtered_df['homework_submitted'] == False]
    
    def get_performance_data(self, admin_id: str, grade: str = None, week: str = None) -> pd.DataFrame:
        """Get performance data filtered by admin scope"""
        filtered_df = self.filter_data_by_scope(admin_id)
        
        if grade:
            filtered_df = filtered_df[filtered_df['grade'] == grade]
        if week:
            filtered_df = filtered_df[filtered_df['performance_week'] == week]
            
        return filtered_df[['student_name', 'grade', 'class', 'quiz_score', 'quiz_date']]
    
    def get_upcoming_quizzes(self, admin_id: str) -> pd.DataFrame:
        """Get upcoming quizzes within admin scope"""
        filtered_df = self.filter_data_by_scope(admin_id)
        return filtered_df[['student_name', 'grade', 'class', 'upcoming_quiz', 'upcoming_quiz_date']].drop_duplicates()
    
    def get_students_by_score_threshold(self, admin_id: str, threshold: int, operator: str = '<') -> pd.DataFrame:
        """Get students based on score threshold"""
        filtered_df = self.filter_data_by_scope(admin_id)
        
        if operator == '<':
            return filtered_df[filtered_df['quiz_score'] < threshold]
        elif operator == '>':
            return filtered_df[filtered_df['quiz_score'] > threshold]
        elif operator == '=':
            return filtered_df[filtered_df['quiz_score'] == threshold]
        else:
            return filtered_df
    
    def get_class_analytics(self, admin_id: str) -> Dict[str, Any]:
        """Get comprehensive analytics for admin's classes"""
        filtered_df = self.filter_data_by_scope(admin_id)
        
        if filtered_df.empty:
            return {}
        
        analytics = {
            'total_students': len(filtered_df),
            'average_quiz_score': filtered_df['quiz_score'].mean(),
            'homework_completion_rate': (filtered_df['homework_submitted'].sum() / len(filtered_df) * 100),
            'grade_distribution': filtered_df['grade'].value_counts().to_dict(),
            'class_distribution': filtered_df['class'].value_counts().to_dict(),
            'upcoming_quiz_count': filtered_df['upcoming_quiz'].nunique(),
            'score_statistics': {
                'min': filtered_df['quiz_score'].min(),
                'max': filtered_df['quiz_score'].max(),
                'median': filtered_df['quiz_score'].median(),
                'std': filtered_df['quiz_score'].std()
            }
        }
        
        return analytics
    
    def get_students_needing_support(self, admin_id: str, score_threshold: int = 75) -> pd.DataFrame:
        """Identify students who may need additional support"""
        filtered_df = self.filter_data_by_scope(admin_id)
        
        # Students with low scores OR missing homework
        support_needed = filtered_df[
            (filtered_df['quiz_score'] < score_threshold) | 
            (filtered_df['homework_submitted'] == False)
        ]
        
        return support_needed[['student_name', 'grade', 'class', 'quiz_score', 'homework_submitted']]
    
    def get_high_performers(self, admin_id: str, score_threshold: int = 90) -> pd.DataFrame:
        """Identify high-performing students"""
        filtered_df = self.filter_data_by_scope(admin_id)
        
        high_performers = filtered_df[
            (filtered_df['quiz_score'] >= score_threshold) & 
            (filtered_df['homework_submitted'] == True)
        ]
        
        return high_performers[['student_name', 'grade', 'class', 'quiz_score']]
    
    def export_filtered_data(self, admin_id: str, format: str = 'csv') -> str:
        """Export filtered data in specified format"""
        filtered_df = self.filter_data_by_scope(admin_id)
        
        if format.lower() == 'csv':
            return filtered_df.to_csv(index=False)
        elif format.lower() == 'json':
            return filtered_df.to_json(orient='records', indent=2)
        else:
            return filtered_df.to_string(index=False)
    
    def get_admin_info(self, admin_id: str) -> Dict[str, Any]:
        """Get detailed admin information"""
        for admin in self.admin_roles:
            if admin['admin_id'] == admin_id:
                scope = admin['access_scope']
                filtered_data = self.filter_data_by_scope(admin_id)
                
                return {
                    'admin_id': admin_id,
                    'admin_name': admin['admin_name'],
                    'access_scope': scope,
                    'accessible_students': len(filtered_data),
                    'grades_managed': scope.get('grades', []),
                    'classes_managed': scope.get('classes', []),
                    'regions_managed': scope.get('regions', [])
                }
        return {}
    
    # Database-ready methods for future integration
    def _build_sql_filter(self, admin_id: str) -> str:
        """Build SQL WHERE clause for database integration"""
        scope = self.get_admin_scope(admin_id)
        conditions = []
        
        if 'grades' in scope and scope['grades']:
            grades = "', '".join(scope['grades'])
            conditions.append(f"grade IN ('{grades}')")
        
        if 'classes' in scope and scope['classes']:
            classes = "', '".join(scope['classes'])
            conditions.append(f"class IN ('{classes}')")
        
        if 'regions' in scope and scope['regions']:
            regions = "', '".join(scope['regions'])
            conditions.append(f"region IN ('{regions}')")
        
        return " AND ".join(conditions) if conditions else "1=1"
    
    def get_database_query(self, admin_id: str, table_name: str = 'students') -> str:
        """Generate SQL query for database integration"""
        where_clause = self._build_sql_filter(admin_id)
        return f"SELECT * FROM {table_name} WHERE {where_clause}"