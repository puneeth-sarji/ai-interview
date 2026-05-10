# AI-Powered Coding Interview Platform

A real-time, highly scalable coding interview platform supporting collaborative code editing, secure isolated execution environments, and automated AI evaluation workflows using the Google Gemini API.

## 🚀 Features

- **Real-Time Collaboration**: Low-latency collaborative coding rooms powered by WebSockets.
- **Secure Code Execution**: Isolated, Docker-in-Docker multi-language code execution engine.
- **AI-Powered Analysis**: Instant feedback, bug detection, and time/space complexity evaluation via Google Gemini 1.5 Pro.
- **Scalable Architecture**: Built with FastAPI, PostgreSQL, and async SQLAlchemy.
- **Premium UI**: A stunning, responsive dark mode interface featuring glassmorphism and real-time syncing.

## 🛠️ Tech Stack

- **Backend**: Python 3.11, FastAPI
- **Database**: PostgreSQL, SQLAlchemy (async), asyncpg
- **Real-Time**: WebSockets
- **Code Engine**: Docker SDK for Python
- **AI Integration**: Google Generative AI (Gemini API)
- **Frontend**: Vanilla HTML/CSS/JS (Dark Theme + Glassmorphism)

## 📦 Local Development Setup

### Prerequisites
- Docker and Docker Compose
- A Google Gemini API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/puneeth-sarji/ai-interview.git
   cd ai-interview
   ```

2. **Set your environment variables**
   Export your Gemini API Key in your terminal:
   ```bash
   export GEMINI_API_KEY="your-gemini-api-key-here"
   ```

3. **Start the application using Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   Open your browser and navigate to:
   [http://localhost:8000](http://localhost:8000)

## 📁 Project Structure

```
.
├── app/
│   ├── api/            # API routers (to be added)
│   ├── core/           # Configuration
│   ├── services/
│   │   ├── ai.py       # Gemini API integration
│   │   └── execution.py# Docker code execution
│   ├── database.py     # Async DB connection setup
│   ├── main.py         # FastAPI & WebSocket entry point
│   └── models.py       # SQLAlchemy ORM models
├── frontend/
│   ├── index.html      # Glassmorphism UI
│   ├── script.js       # WebSocket logic
│   └── style.css       # Premium styles
├── docker-compose.yml  # Infrastructure setup
├── Dockerfile          # Backend container definition
└── requirements.txt    # Python dependencies
```

## 🔒 Security
The platform securely executes untrusted code by spawning isolated Alpine Linux containers via the Docker SDK with disabled networking and strict memory limits.

## 📝 License
This project is for demonstration and portfolio purposes.
