# Learning Assistant Backend

This is the backend service for the Learning Assistant application, built with FastAPI and Google's Agent Development Kit (ADK). The service provides an intelligent learning planning system that helps create personalized study plans.

## Features

- FastAPI-based REST API
- Google ADK integration for intelligent agent-based responses
- Session management for user interactions
- Study plan generation

## Prerequisites

- Python 3.8+
- Google Gemini API credentials

## Installation

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
GOOGLE_API_KEY=your_google_api_key
```

## Project Structure

```
backend/
├── app/
│   ├── agents/         # AI agent implementations
│   ├── callbacks/      # Callback handlers
│   ├── models/         # Database models
│   ├── prompts/        # AI prompt templates
│   ├── tools/          # Utility tools and helpers
│   └── main.py         # FastAPI application entry point
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## API Endpoints

### `GET /new-session`
Creates a new session for user interaction.
- Returns: Session information

### `GET /list-sessions`
Lists all active sessions for a user.
- Returns: List of sessions

### `POST /chat`
Processes user messages and generates study plans.
- Request Body:
  ```json
  {
    "text": "string",
    "session_id": "string",
    "user_id": "string"
  }
  ```
- Returns: Generated study plan or response

## Running the Application

1. Start the development server:
```bash
uvicorn app.main:app --reload
```

2. The API will be available at `http://localhost:8000`

## Development

- The application uses FastAPI for the web framework
- SQLAlchemy for database operations
- Alembic for database migrations
- Google ADK for AI agent functionality

## Dependencies

Key dependencies include:
- FastAPI
- Google ADK
- Pydantic
- Python-jose (for JWT)
- Passlib (for password hashing)

- Environment variable configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

Copyright (c) 2024 Learning Assistant

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 