# AI Chat Interface with Ollama

## Overview
A simple AI chat interface that uses local Ollama for AI responses. The application consists of an HTML frontend and Python Flask backend that automatically installs and configures Ollama on startup.

## Recent Changes
- **November 10, 2025**: Initial project setup
  - Created Flask backend with Ollama integration
  - Built HTML chat interface with real-time messaging
  - Configured automatic Ollama installation via Nix
  - Set up auto-download of llama3.2:1b model (1.3GB, optimized for Replit's memory constraints)
  - Added response filtering for concise AI answers

## Project Architecture

### Backend (app.py)
- **Flask Server**: Runs on port 5000, serves the chat interface
- **Ollama Integration**: 
  - Auto-starts Ollama server on application launch
  - Downloads llama3.2:1b model automatically (1.3GB, balanced quality and performance)
  - Response filtering to keep answers concise and focused
- **API Endpoints**:
  - `/`: Serves the main HTML interface
  - `/chat`: POST endpoint for sending messages to AI
  - `/health`: GET endpoint to check if Ollama is ready

### Frontend (static/index.html)
- Simple, clean chat interface
- Real-time message display
- Loading indicators during AI response
- Health check polling to detect when Ollama is ready
- Error handling and display

### Dependencies
- Python 3.11
- Flask (web framework)
- Requests (HTTP client)
- Ollama (installed via Nix)

## Running the Application
The workflow is configured to automatically:
1. Start the Flask server
2. Launch Ollama server in background
3. Download the AI model
4. Make the chat interface available on port 5000

No manual setup required - just run and start chatting!
