# 🎓 Dumroo AI Admin Panel

**AI-Powered Educational Admin System with Natural Language Querying & Role-Based Access Control**

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org) [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io) [![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com) [![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)

## 📋 Project Overview

This project demonstrates an AI-powered admin panel built for Dumroo.ai that allows educational administrators to query student data using natural language. The system implements strict role-based access control, ensuring admins can only access data within their assigned scope (grade, class, region).

### 🎯 Key Features Implemented

✅ **Natural Language Processing** - Ask questions in plain English  
✅ **Role-Based Access Control** - Admins see only their scope data  
✅ **AI-Powered Query Engine** - LangChain + OpenAI GPT-3.5-turbo  
✅ **Professional Web Interface** - Streamlit with responsive design  
✅ **Agent-Style Conversations** - Context-aware follow-up questions  
✅ **Real-time Analytics** - Interactive dashboards and metrics  
✅ **Modular Architecture** - Database-ready, scalable design  
✅ **Access Code Protection** - Secure admin profile switching  

## 🚀 Live Demo

![Live App Demo](live_app/dashboard.png)

### 📱 Responsive Design
| Desktop View | Mobile View |
|--------------|-------------|
| ![Desktop](live_app/desktop_view.png) | ![Mobile](live_app/mobile_view.png) |

### 🤖 AI Assistant in Action
![AI Chat Interface](live_app/ai_chat.png)



## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Dumroo AI Admin Panel                    │
├─────────────────────────────────────────────────────────────┤
│  Frontend Layer (Streamlit)                                │
│  ├── Multi-page Interface                                  │
│  ├── Responsive Design                                     │
│  ├── Real-time Chat                                        │
│  └── Analytics Dashboard                                   │
├─────────────────────────────────────────────────────────────┤
│  AI Processing Layer                                        │
│  ├── AIQueryEngine (LangChain + OpenAI)                   │
│  ├── Intent Recognition                                     │
│  ├── Context Management                                     │
│  └── Response Formatting                                   │
├─────────────────────────────────────────────────────────────┤
│  Business Logic Layer                                       │
│  ├── DataManager (Role-based filtering)                   │
│  ├── Access Control                                        │
│  ├── Query Processing                                      │
│  └── Analytics Generation                                  │
├─────────────────────────────────────────────────────────────┤
│  Data Layer                                                 │
│  ├── students_data.json (8 student records)               │
│  ├── admin_roles.json (3 admin profiles)                  │
│  └── config.json (UI configuration)                       │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Tech Stack

### Core Technologies

| Category | Technology | Purpose |
|----------|------------|---------|
| **Backend** | Python 3.x | Core programming language |
| **AI Framework** | LangChain | AI agent orchestration |
| **AI Model** | OpenAI GPT-3.5-turbo | Natural language processing |
| **Data Processing** | Pandas | Data manipulation and analysis |
| **Frontend** | Streamlit | Web interface and UI components |
| **Navigation** | streamlit-option-menu | Multi-page navigation |
| **Charts** | Plotly | Interactive analytics |
| **Environment** | python-dotenv | Configuration management |

### Architecture Patterns
- **Modular Design**: Separated concerns across multiple files
- **Role-Based Access Control**: Strict data isolation by admin scope
- **Agent-Style AI**: Context-aware conversational interface
- **Database-Ready**: Easily adaptable to SQL databases

## 📁 Project Structure

```
Dumroo ai/
├── src/                          # Core application code
│   ├── streamlit_app.py         # Main UI application
│   ├── ai_query_engine.py       # AI processing engine
│   └── data_manager.py          # Data management & filtering
├── data/                        # Dataset and configuration
│   ├── students_data.json       # Student records (8 students)
│   ├── admin_roles.json         # Admin profiles (3 admins)
│   └── config.json              # UI configuration

├── live_app/                    # Application screenshots

├── requirements.txt             # Python dependencies
├── .env                         # API keys (create this)
├── run_app.py                   # Application launcher
└── README.md                    # This documentation
```

## ⚡ Quick Start

### 1. Clone Repository
```bash
git clone <repository-url>
cd "Dumroo ai"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
Create `.env` file in root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Launch Application
```bash
python run_app.py
```

The application will open in your browser at `http://localhost:8501`

## 🔐 Admin Profiles & Access Control

### Available Admin Profiles

| Admin | Grade | Region | Classes | Access Code |
|-------|-------|--------|---------|-------------|
| **John Admin** | Grade 8 | North | 8A, 8B | 0000 |
| **Sarah Manager** | Grade 7 | South | 7A, 7B | 0000 |
| **Mike Supervisor** | Grade 9 | East | 9A, 9B | 0000 |
| **Hydra** | Grade 7 | South | 7A, 7B | 0000 |

### Security Features
- **Access Code Protection**: Required when switching admin profiles
- **Scope Isolation**: Admins can only see their assigned students
- **Session Management**: Secure admin session handling

## 🎯 Example Queries

### Basic Queries
```
"Which students haven't submitted their homework yet?"
"Show me the best performing student"
"What's the average quiz score in my classes?"
"List all students in my scope"
```

### Advanced Queries
```
"Show me students with quiz scores below 75"
"Which students need academic support?"
"Display performance data for my region"
"Who are the top performers in Grade 8?"
```

### Analytics Queries
```
"Generate a summary of homework completion rates"
"Show me upcoming quiz schedules"
"Compare performance across my classes"
"Identify students requiring intervention"
```

## 📊 Features Demonstration

### 1. Natural Language Processing
![NLP Demo](live_app/nlp_processing.png)

The AI engine processes natural language queries and converts them into structured data operations:

- **Intent Recognition**: Identifies query type (homework, performance, analytics)
- **Entity Extraction**: Extracts grades, dates, score thresholds
- **Context Awareness**: Maintains conversation history for follow-ups

### 2. Role-Based Data Access
![Access Control](live_app/access_control.png)

Each admin sees only their assigned data:
- John Admin: 4 Grade 8 students in North region
- Sarah Manager: 2 Grade 7 students in South region  
- Mike Supervisor: 2 Grade 9 students in East region

### 3. Interactive Analytics Dashboard
![Analytics](live_app/analytics_dashboard.png)

Real-time metrics and insights:
- Student count and homework completion rates
- Average quiz scores and performance trends
- Students requiring academic support
- Class-wise performance breakdowns

### 4. Agent-Style Conversations
![Conversation](live_app/conversation_flow.png)

Context-aware follow-up handling:
- Maintains conversation history
- Understands references to previous queries
- Provides contextual responses and recommendations

## 🔧 Configuration

### Customizing Admin Roles
Edit `data/admin_roles.json`:
```json
{
  "admin_id": "A005",
  "admin_name": "New Admin",
  "access_code": "1234",
  "access_scope": {
    "grades": ["Grade 10"],
    "classes": ["10A", "10B"],
    "regions": ["West"]
  }
}
```

### Adding Student Data
Edit `data/students_data.json`:
```json
{
  "student_id": "S009",
  "student_name": "New Student",
  "grade": "Grade 10",
  "class": "10A",
  "region": "West",
  "quiz_score": 85,
  "homework_submitted": true,
  "upcoming_quiz": "Math Quiz",
  "upcoming_quiz_date": "2024-01-20"
}
```

### UI Customization
Modify `data/config.json` for:
- Application title and branding
- Navigation pages and icons
- Quick action buttons
- Example queries and suggestions

## 🚀 Deployment Options

### Local Development
```bash
streamlit run src/streamlit_app.py
```

### Production Deployment
1. **Streamlit Cloud**: Direct GitHub integration
2. **Heroku**: Web app deployment
3. **AWS/GCP**: Cloud hosting with auto-scaling
4. **Docker**: Containerized deployment

### Environment Variables for Production
```env
OPENAI_API_KEY=your_production_api_key
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## 🔄 Database Migration Ready

The system is designed for easy database integration:

### Current JSON Structure → SQL Tables
```sql
-- Students table
CREATE TABLE students (
    student_id VARCHAR(10) PRIMARY KEY,
    student_name VARCHAR(100),
    grade VARCHAR(20),
    class VARCHAR(10),
    region VARCHAR(50),
    quiz_score INTEGER,
    homework_submitted BOOLEAN,
    upcoming_quiz VARCHAR(100),
    upcoming_quiz_date DATE
);

-- Admins table  
CREATE TABLE admins (
    admin_id VARCHAR(10) PRIMARY KEY,
    admin_name VARCHAR(100),
    access_code VARCHAR(10),
    grades JSON,
    classes JSON,
    regions JSON
);
```

### Migration Steps
1. Replace `DataManager` JSON file operations with SQL queries
2. Update connection string in environment variables
3. Implement database connection pooling
4. Add data validation and constraints

## 🧪 Testing

### Manual Testing Scenarios
1. **Access Control**: Try switching admin profiles with wrong codes
2. **Data Isolation**: Verify each admin sees only their scope
3. **Query Processing**: Test various natural language queries
4. **Error Handling**: Test with invalid queries and API failures
5. **Responsive Design**: Test on mobile and desktop devices

### Example Test Queries
```python
# Test role-based access
admin_data = data_manager.filter_data_by_scope("A001")  # John Admin
assert len(admin_data) == 4  # Should see 4 Grade 8 students

# Test query processing
response = ai_engine.execute_query(data_manager, "A001", "best student")
assert "Alice Johnson" in response  # Highest scorer in John's scope
```

## 🎯 Assignment Requirements Fulfilled

### ✅ Core Requirements
- [x] **Dataset Created**: JSON files with student data (name, class, submission status, quiz scores, dates)
- [x] **AI-Powered System**: Natural language query interface with filtered results
- [x] **LangChain Integration**: Used for query parsing and data fetching
- [x] **Role-Based Access**: Admins restricted to their assigned scope only

### ✅ Bonus Features Completed
- [x] **Streamlit Interface**: Professional multi-page web application
- [x] **Agent-Style Handling**: Context-aware follow-up questions and conversation history
- [x] **Modular Code**: Database-ready architecture with separated concerns
- [x] **Advanced Features**: Analytics dashboard, export capabilities, access code protection

### 🏆 Additional Enhancements
- [x] **Responsive Design**: Mobile-friendly interface with adaptive layouts
- [x] **Real-time Analytics**: Interactive charts and performance metrics
- [x] **Professional UI**: Modern styling with gradient themes and animations
- [x] **Error Handling**: Graceful fallbacks for API quota exceeded scenarios
- [x] **Configuration Management**: JSON-driven UI and admin setup

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Make changes and test thoroughly
4. Commit changes: `git commit -m "Add new feature"`
5. Push to branch: `git push origin feature/new-feature`
6. Create Pull Request

### Code Standards
- Follow PEP 8 Python style guidelines
- Add docstrings for all functions and classes
- Maintain modular architecture patterns
- Test role-based access control thoroughly

## 📞 Support & Contact

For questions, issues, or feature requests:

- **GitHub Issues**: [Create an issue](https://github.com/your-repo/issues)
- **Email**: support@dumroo.ai
- **Documentation**: [Full API Documentation](docs/api.md)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for Dumroo.ai - Empowering Education Through AI**

*Demonstrating advanced AI integration, role-based security, and professional web development for educational technology solutions.*