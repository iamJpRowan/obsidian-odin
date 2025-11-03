#!/bin/bash
# Run the FastAPI server with virtual environment activated

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source "$BACKEND_DIR/venv/bin/activate"

# Check if venv is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

echo "✅ Virtual environment activated: $VIRTUAL_ENV"
echo ""
echo "🚀 Starting FastAPI server..."
echo "   Using local LLM (Ollama)"
echo "   Your data stays private! 🔒"
echo ""

# Run the server
cd "$BACKEND_DIR"
python -m uvicorn core.restapi.api:app --reload --host 0.0.0.0 --port 8000

