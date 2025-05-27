# Learning Assistant Application

A comprehensive learning assistant that generates personalized study plans and detailed lesson content using AI. The application leverages Google ADK (AI Development Kit) with FastAPI backend and React frontend, implementing robust guardrails and rate limiting for production-grade AI interactions.

## Architecture

```mermaid
graph TD
    subgraph Frontend
        A[React App] --> B[User Interface]
    end

    subgraph Backend
        C[FastAPI Server]
        C1[Study Planner Agent]
        C2[Study Content Generator Agent]
        C3[Quiz Generator Agent]
        C -->|Invokes| C1
        C1 -->|Invokes| C2
        C2 -->|Invokes| C3
    end

    subgraph AI
        D[Google ADK + GenAI]
        D1[Rate Limiter]
        D2[Guardrails]
        D3[Callbacks]
        D -->|Enforces| D1
        D -->|Validates| D2
        D -->|Monitors| D3
    end

    B -->|User sends request| A
    A -->|HTTP request| C
    C1 -->|Uses| D
    C2 -->|Uses| D
    C3 -->|Uses| D
    C -->|Aggregated AI Response| A
    A -->|Renders Study Plan, Content, Quizzes| B
```

## Features

### Frontend
- Modern, responsive UI built with React and Material-UI
- Real-time study plan generation
- Interactive session management
- Detailed lesson plan visualization
- Loading states and error handling

### Backend
- FastAPI backend with Google ADK integration
- Multi-agent architecture for specialized tasks
- RESTful API endpoints for chat and session management
- Session-based conversation tracking
- Comprehensive error handling and logging

### AI Integration & Safety Features
- Google ADK integration for production-grade AI
- Rate limiting to prevent API abuse
- Guardrails for content safety and quality
- Callback system for monitoring AI responses
- Multi-agent orchestration for complex tasks
- Content validation and filtering

## Project Structure

```
learning_assistant/
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── App.js         # Main application component
│   │   └── ...
│   └── package.json
│
└── backend/               # FastAPI backend application
    ├── app/
    │   ├── main.py       # Main application entry point
    │   ├── models/       # Data models
    │   ├── services/     # Business logic
    │   │   ├── agents/   # AI agent implementations
    │   │   └── callbacks/ # AI monitoring callbacks
    │   ├── utils/        # Utility functions
    │   └── config/       # Configuration files
    └── requirements.txt
```

## Getting Started

### Prerequisites
- Node.js (v14 or higher)
- Python 3.8 or higher
- pip (Python package manager)
- Google Cloud account with ADK access
- API credentials for Google ADK

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure Google ADK credentials:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
```

5. Start the backend server:
```bash
uvicorn app.main:app --reload --port 8082
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8082

## API Endpoints

### Backend API

- `GET /new-session`: Create a new chat session
- `POST /chat`: Generate a study plan based on user input
  - Request body: `{ "text": string, "session_id": string, "user_id": string }`
  - Response: Study plan with detailed lesson content

### Rate Limiting
- Default rate limit: 100 requests per minute per user
- Customizable limits per endpoint
- Rate limit headers included in responses

### Callbacks
- Response validation callbacks
- Content safety monitoring
- Usage tracking and analytics
- Error logging and reporting

## Usage

1. Open the application in your browser
2. Enter your learning request in the input field
3. Click "Generate Study Plan"
4. View your personalized study plan with:
   - Daily topics and durations
   - Detailed lesson content
   - Practice problems
   - Key takeaways

## Error Handling

The application includes comprehensive error handling for:
- API connection issues
- Invalid user inputs
- Session management errors
- Study plan generation failures
- Rate limit exceeded
- Content safety violations
- AI model errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- React and Material-UI for the frontend framework
- FastAPI for the backend framework
- Google ADK for AI capabilities
- OpenAI for additional AI model integration 