import streamlit as st
import os
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
from streamlit_chat import message
import pandas as pd
from data_manager import DataManager
from ai_query_engine import AIQueryEngine

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Dumroo AI Admin Panel",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="auto"
)

# Responsive CSS for all devices
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: clamp(1rem, 4vw, 2rem);
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        font-size: clamp(1.5rem, 5vw, 2.5rem) !important;
        margin: 0 !important;
    }
    .main-header p {
        font-size: clamp(0.9rem, 3vw, 1.2rem) !important;
    }
    .metric-card {
        background: white;
        padding: clamp(1rem, 3vw, 1.5rem);
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        min-height: 100px;
    }
    .metric-card h2 {
        color: #333 !important;
        font-size: clamp(1.2rem, 4vw, 2rem) !important;
    }
    .metric-card h3 {
        font-size: clamp(0.8rem, 2.5vw, 1rem) !important;
    }
    .admin-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: clamp(0.8rem, 3vw, 1rem);
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: clamp(0.4rem, 2vw, 0.5rem) clamp(1rem, 4vw, 2rem);
        font-weight: bold;
        width: 100%;
        font-size: clamp(0.8rem, 2.5vw, 1rem);
    }
    .stSelectbox > div > div {
        font-size: clamp(0.8rem, 2.5vw, 1rem);
    }
    .stTextInput > div > div > input {
        font-size: clamp(0.8rem, 2.5vw, 1rem);
    }
    @media (max-width: 768px) {
        .main-header {
            padding: 1rem;
        }
        .metric-card {
            padding: 1rem;
            margin: 0.5rem 0;
        }
        .admin-card {
            padding: 0.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'selected_admin' not in st.session_state:
    st.session_state.selected_admin = 'A001'
if 'conversation_context' not in st.session_state:
    st.session_state.conversation_context = []


def create_analytics_dashboard(data_manager, admin_id):
    """Create analytics dashboard with real metrics from admin's scope only"""
    filtered_data = data_manager.filter_data_by_scope(admin_id)
    
    if filtered_data.empty:
        st.warning("No data available for your scope")
        return
    
    # Responsive metrics layout
    if len(filtered_data) > 0:
        # Use 2 columns on mobile, 4 on desktop
        try:
            # Check if mobile by screen width (approximate)
            cols = st.columns([1, 1, 1, 1])
            mobile_layout = False
        except:
            mobile_layout = True
        
        if mobile_layout:
            # Mobile: 2x2 grid
            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)
        else:
            # Desktop: 1x4 grid
            col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_students = len(filtered_data)
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #667eea; margin: 0;">My Students</h3>
            <h2 style="margin: 0.5rem 0;">{total_students}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        homework_submitted = len(filtered_data[filtered_data['homework_submitted'] == True])
        homework_rate = (homework_submitted / total_students * 100) if total_students > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #667eea; margin: 0;">Homework Rate</h3>
            <h2 style="margin: 0.5rem 0;">{homework_rate:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_score = filtered_data['quiz_score'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #667eea; margin: 0;">Avg Quiz Score</h3>
            <h2 style="margin: 0.5rem 0;">{avg_score:.1f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        low_performers = len(filtered_data[filtered_data['quiz_score'] < 75])
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #667eea; margin: 0;">Need Support</h3>
            <h2 style="margin: 0.5rem 0;">{low_performers}</h2>
        </div>
        """, unsafe_allow_html=True)

    # Responsive data tables
    st.markdown("### 📊 Your Students Overview")
    
    # Stack tables vertically on mobile
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**Students by Performance Level**")
        high_perf = len(filtered_data[filtered_data['quiz_score'] >= 85])
        med_perf = len(filtered_data[(filtered_data['quiz_score'] >= 75) & (filtered_data['quiz_score'] < 85)])
        low_perf = len(filtered_data[filtered_data['quiz_score'] < 75])
        
        perf_data = pd.DataFrame({
            'Performance Level': ['High (85+)', 'Medium (75-84)', 'Low (<75)'],
            'Count': [high_perf, med_perf, low_perf]
        })
        st.dataframe(perf_data, use_container_width=True)
    
    with col2:
        st.markdown("**Homework Status by Class**")
        homework_summary = filtered_data.groupby('class').agg({
            'homework_submitted': ['sum', 'count']
        }).round(1)
        homework_summary.columns = ['Submitted', 'Total']
        homework_summary['Rate %'] = (homework_summary['Submitted'] / homework_summary['Total'] * 100).round(1)
        st.dataframe(homework_summary, use_container_width=True)
    
    # Student list with action items
    st.markdown("### 📋 Student Details")
    display_data = filtered_data[['student_name', 'class', 'quiz_score', 'homework_submitted']].copy()
    display_data.columns = ['Student Name', 'Class', 'Quiz Score', 'Homework Done']
    st.dataframe(display_data, use_container_width=True)


def main():
    # Load configuration
    with open("../data/config.json", 'r') as f:
        config = json.load(f)
    app_config = config["app_config"]
    
    # Header
    st.markdown(f"""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2.5rem;">🎓 {app_config['title']}</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">{app_config['subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar navigation
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; color: white;">
            <h2>🎓 Admin Portal</h2>
        </div>
        """, unsafe_allow_html=True)

        page_names = [page["name"] for page in app_config["pages"]]
        page_icons = [page["icon"] for page in app_config["pages"]]
        
        selected_page = option_menu(
            menu_title=None,
            options=page_names,
            icons=page_icons,
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "white", "font-size": "18px"},
                "nav-link": {"color": "white", "font-size": "16px", "text-align": "left", "margin": "0px"},
                "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"},
            }
        )

        st.markdown("---")

        # Load admin data from JSON
        with open("../data/admin_roles.json", 'r') as f:
            admin_json_data = json.load(f)
        
        admin_options = {admin["admin_id"]: admin["admin_name"] for admin in admin_json_data}
        
        admin_details = {
            admin["admin_id"]: {
                "role": f"{', '.join(admin['access_scope']['grades'])} Coordinator",
                "region": ', '.join(admin['access_scope']['regions']),
                "classes": ', '.join(admin['access_scope']['classes'])
            } for admin in admin_json_data
        }
        
        # Admin selection with access code
        st.markdown("**👤 Admin Profile**")

        selected_admin = st.selectbox(
            "Select Profile:",
            options=list(admin_options.keys()),
            format_func=lambda x: admin_options[x],
            key="admin_selector"
        )
        
        # Access code verification
        if 'current_admin' not in st.session_state or st.session_state.current_admin != selected_admin:
            access_code = st.text_input("Enter Access Code:", type="password", key=f"code_{selected_admin}")
            st.caption("💡 Hint: Access code is 0000")
            
            if access_code:
                admin_data = next((admin for admin in admin_json_data if admin['admin_id'] == selected_admin), None)
                if admin_data and access_code == admin_data.get('access_code', ''):
                    st.session_state.current_admin = selected_admin
                    st.success("✅ Access granted")
                else:
                    st.error("❌ Invalid access code")
                    st.stop()
            else:
                st.warning("🔒 Please enter access code")
                st.stop()

        # Admin info card - only show own scope
        admin_info = admin_details[selected_admin]
        st.markdown(f"""
        <div class="admin-card">
            <h4>{admin_options[selected_admin]}</h4>
            <p><strong>Role:</strong> {admin_info['role']}</p>
            <p><strong>My Region:</strong> {admin_info['region']}</p>
            <p><strong>My Classes:</strong> {admin_info['classes']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.session_state.selected_admin = selected_admin

    # Initialize components
    try:
        data_manager = DataManager(
            students_file="../data/students_data.json",
            admins_file="../data/admin_roles.json"
        )

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("⚠️ OpenAI API key not found. Please check your .env file.")
            return

        ai_engine = AIQueryEngine(api_key)

        # Page content based on selection  
        if selected_page == "AI Assistant":
            st.markdown("## 🤖 AI Assistant")

            # Quick action buttons
            st.markdown("**⚡ Quick Actions:**")
            cols = st.columns(len(app_config["quick_actions"]))
            
            for i, action in enumerate(app_config["quick_actions"]):
                with cols[i]:
                    if st.button(action["label"], use_container_width=True, key=f"quick_{i}"):
                        # Execute query immediately
                        with st.spinner("🤖 Processing..."):
                            response = ai_engine.execute_query(data_manager, selected_admin, action["query"])
                            st.session_state.chat_history.append({
                                "query": action["query"],
                                "response": response,
                                "admin": admin_options[selected_admin],
                                "timestamp": datetime.now().strftime("%H:%M:%S")
                            })
                            st.rerun()

            st.markdown("---")

            # Chat interface
            st.markdown("**💬 Conversation with AI Assistant**")

            # Display chat history with better formatting
            if st.session_state.chat_history:
                st.markdown("**💬 Recent Conversations:**")
                for i, chat in enumerate(st.session_state.chat_history[-3:]):
                    with st.expander(f"Q: {chat['query'][:50]}...", expanded=(i == len(st.session_state.chat_history[-3:])-1)):
                        st.markdown(f"**Query:** {chat['query']}")
                        # Format response for better display
                        response = chat['response']
                        if '**' in response and '=' in response:
                            # It's a formatted table response
                            lines = response.split('\n')
                            title_line = next(
                                (line for line in lines if '**' in line), '')
                            if title_line:
                                st.markdown(f"**{title_line}**")

                            # Find table content
                            table_start = -1
                            for i, line in enumerate(lines):
                                if any(col in line.lower() for col in ['student name', 'grade', 'class']):
                                    table_start = i
                                    break

                            if table_start >= 0:
                                # Extract table data
                                table_lines = []
                                for i in range(table_start, len(lines)):
                                    if lines[i].strip() and not lines[i].startswith('📈'):
                                        table_lines.append(lines[i])
                                    elif lines[i].startswith('Summary:'):
                                        break

                                if table_lines:
                                    st.code('\n'.join(table_lines))

                                # Show summary if exists
                                summary_line = next(
                                    (line for line in lines if 'Summary:' in line), '')
                                if summary_line:
                                    st.info(summary_line)
                            else:
                                st.code(response)
                        else:
                            st.code(response)
                        if 'timestamp' in chat:
                            st.caption(f"Asked at {chat['timestamp']}")

            # Enhanced query input
            st.markdown("**🎯 Ask Your Question:**")

            suggestions = app_config["suggestions"]

            selected_suggestion = st.selectbox(
                "Quick suggestions:",
                ["Type your own question..."] + suggestions
            )

            query_value = selected_suggestion if selected_suggestion != "Type your own question..." else st.session_state.get(
                'quick_query', '')

            query = st.text_input(
                "Your question:",
                value=query_value,
                placeholder="e.g., Show me students with quiz scores below 80"
            )

            # Clear quick query after use
            if 'quick_query' in st.session_state:
                query = st.session_state.quick_query
                del st.session_state.quick_query

            # Responsive button layout
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                if st.button("🚀 Ask AI Assistant", type="primary", use_container_width=True):
                    if query:
                        with st.spinner("🤖 Processing your question..."):
                            response = ai_engine.execute_query(
                                data_manager, selected_admin, query)

                            # Add to chat history
                            st.session_state.chat_history.append({
                                "query": query,
                                "response": response,
                                "admin": admin_options[selected_admin],
                                "timestamp": datetime.now().strftime("%H:%M:%S")
                            })

                            st.success("✅ Query processed successfully!")
                            st.rerun()

            with col2:
                if st.button("🗑️ Clear Chat", use_container_width=True):
                    st.session_state.chat_history = []
                    st.rerun()

            with col3:
                if st.button("💾 Export Chat", use_container_width=True):
                    if st.session_state.chat_history:
                        chat_df = pd.DataFrame(st.session_state.chat_history)
                        csv = chat_df.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )

            # Example queries from config
            with st.expander("💡 Example Queries"):
                for i, example in enumerate(app_config["example_queries"]):
                    if st.button(f"➡️ {example}", key=f"example_{i}"):
                        # Execute query immediately
                        with st.spinner("🤖 Processing..."):
                            response = ai_engine.execute_query(data_manager, selected_admin, example)
                            st.session_state.chat_history.append({
                                "query": example,
                                "response": response,
                                "admin": admin_options[selected_admin],
                                "timestamp": datetime.now().strftime("%H:%M:%S")
                            })
                            st.rerun()

        elif selected_page == "My Students":
            st.markdown("## 👥 My Students Dashboard")
            create_analytics_dashboard(data_manager, selected_admin)
            
            # Export only admin's data
            filtered_data = data_manager.filter_data_by_scope(selected_admin)
            if not filtered_data.empty:
                st.markdown("### 💾 Export My Data")
                col1, col2 = st.columns(2)
                with col1:
                    csv = filtered_data.to_csv(index=False)
                    st.download_button(
                        label="Download My Students (CSV)",
                        data=csv,
                        file_name=f"my_students_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    json_data = filtered_data.to_json(orient='records', indent=2)
                    st.download_button(
                        label="Download My Students (JSON)",
                        data=json_data,
                        file_name=f"my_students_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json"
                    )

        elif selected_page == "Data Explorer":
            st.markdown("## 🗃️ Data Explorer")

            filtered_data = data_manager.filter_data_by_scope(selected_admin)

            if not filtered_data.empty:
                # Data summary
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**📊 Data Summary**")
                    st.write(f"Total Records: {len(filtered_data)}")
                    st.write(
                        f"Grades: {', '.join(filtered_data['grade'].unique())}")
                    st.write(
                        f"Classes: {', '.join(filtered_data['class'].unique())}")
                    st.write(
                        f"Regions: {', '.join(filtered_data['region'].unique())}")

                with col2:
                    st.markdown("**🔍 Filter Data**")
                    selected_grade = st.selectbox(
                        "Filter by Grade:", ["All"] + list(filtered_data['grade'].unique()))
                    selected_class = st.selectbox(
                        "Filter by Class:", ["All"] + list(filtered_data['class'].unique()))

                # Apply filters
                display_data = filtered_data.copy()
                if selected_grade != "All":
                    display_data = display_data[display_data['grade']
                                                == selected_grade]
                if selected_class != "All":
                    display_data = display_data[display_data['class']
                                                == selected_class]

                # Data table
                st.markdown("**📄 Student Data**")
                st.dataframe(display_data, use_container_width=True)

                # Export options
                col1, col2 = st.columns(2)
                with col1:
                    csv = display_data.to_csv(index=False)
                    st.download_button(
                        label="💾 Download as CSV",
                        data=csv,
                        file_name=f"student_data_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )

                with col2:
                    json_data = display_data.to_json(
                        orient='records', indent=2)
                    st.download_button(
                        label="💾 Download as JSON",
                        data=json_data,
                        file_name=f"student_data_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json"
                    )
            else:
                st.warning("⚠️ No data available for your access scope.")

        elif selected_page == "Settings":
            st.markdown("## ⚙️ Settings")

            # Admin scope display
            scope = data_manager.get_admin_scope(selected_admin)
            st.markdown("**🔒 Your Access Scope**")
            st.json(scope)

            st.markdown("---")

            # System information
            st.markdown("**💻 System Information**")
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"Current Admin: {admin_options[selected_admin]}")
                st.write(
                    f"Session Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                st.write(
                    f"Total Queries: {len(st.session_state.chat_history)}")

            with col2:
                st.write(f"API Status: ✅ Connected")
                st.write(f"Data Source: JSON Files")
                st.write(f"AI Model: GPT-3.5-turbo")

            st.markdown("---")

            # Advanced options
            st.markdown("**🔧 Advanced Options**")

            if st.button("🔄 Reset All Data"):
                st.session_state.chat_history = []
                st.session_state.conversation_context = []
                st.success("✅ All data has been reset!")
                st.rerun()

            if st.button("📊 Generate System Report"):
                report_data = {
                    "admin_id": selected_admin,
                    "admin_name": admin_options[selected_admin],
                    "total_queries": len(st.session_state.chat_history),
                    "accessible_students": len(data_manager.filter_data_by_scope(selected_admin)),
                    "session_time": datetime.now().isoformat()
                }

                st.json(report_data)

                report_json = pd.DataFrame([report_data]).to_json(
                    orient='records', indent=2)
                st.download_button(
                    label="💾 Download Report",
                    data=report_json,
                    file_name=f"system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

    except Exception as e:
        st.error(f"❌ Error initializing application: {str(e)}")
        st.markdown(
            "⚠️ Please ensure all data files are present and properly formatted.")

        # Debug information
        with st.expander("🔧 Debug Information"):
            st.code(f"Error Details: {str(e)}")
            st.code(f"Current Directory: {os.getcwd()}")
            st.code(
                f"API Key Present: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")

# Footer


def show_footer():
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #666;">
        <p>🎓 <strong>Dumroo AI Admin Panel</strong> - Empowering Education Through AI</p>
        <p>Built with ❤️ using Streamlit, LangChain & OpenAI | Version 2.0</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
    show_footer()
