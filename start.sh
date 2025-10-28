#!/bin/bash

# ScriptMyIdeas - Development Startup Script

echo "🚀 Starting ScriptMyIdeas Development Environment..."

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Warning: backend/.env not found!"
    echo "   Copy backend/.env.example to backend/.env and configure it."
    exit 1
fi

# Start backend
echo "📦 Starting Backend (FastAPI)..."
cd backend
if [ ! -d "venv" ]; then
    echo "   Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

echo "   Backend starting on http://localhost:8000"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

cd ..

# Start frontend
echo "🎨 Starting Frontend (React + Vite)..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "   Installing dependencies..."
    npm install
fi

echo "   Frontend starting on http://localhost:3000"
npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo "✅ ScriptMyIdeas is running!"
echo ""
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/api/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Trap Ctrl+C and kill both processes
trap "echo ''; echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT

# Wait for processes
wait
