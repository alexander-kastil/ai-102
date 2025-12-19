# Student AI RAG Application - Python Version

This is a Python port of the C# ASP.NET RAG application, converted to use Flask.

## Features

- Web-based student Q&A interface
- RAG (Retrieval Augmented Generation) functionality
- SQLite database for storing questions and answers
- Student context tracking
- Interactive chat interface

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables in `.env`:
   - `DEPLOYMENT_MODEL`: Your AI model deployment name
   - `ENDPOINT`: Your Azure AI endpoint URL
   - `API_KEY`: Your Azure AI API key
   - `DATABASE_URL`: SQLite database path (default: "sqlite:///app.db")
   - `SECRET_KEY`: Flask secret key for sessions

## Usage

1. Run the Flask application:
   ```bash
   python app.py
   ```

2. Open your browser to `http://localhost:5000`

3. Enter your name and start asking questions

## Features

- **Ask Questions**: Students can ask educational questions
- **View History**: Load previous questions and answers
- **Contextual Responses**: AI provides educational, helpful responses
- **Persistent Storage**: Questions and answers are saved to database

## Note

This Python version uses Flask instead of ASP.NET Core, and SQLAlchemy instead of Entity Framework for database operations.