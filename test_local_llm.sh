#!/bin/bash
# Quick test script for local LLM setup

echo "========================================="
echo "Testing Obsidian Odin Local LLM Setup"
echo "========================================="
echo ""

# Test 1: Ollama service
echo "1. Testing Ollama service..."
if ollama list > /dev/null 2>&1; then
    echo "   ✅ Ollama is running"
    ollama list | head -2
else
    echo "   ❌ Ollama is not running. Start it with: ollama serve"
    exit 1
fi
echo ""

# Test 2: Model exists
echo "2. Testing llama3.1:8b model..."
if ollama list | grep -q "llama3.1:8b"; then
    echo "   ✅ Model is installed"
else
    echo "   ❌ Model not found. Install with: ollama pull llama3.1:8b"
    exit 1
fi
echo ""

# Test 3: Quick inference test
echo "3. Testing model inference..."
echo "   (This should respond in a few seconds)"
RESPONSE=$(ollama run llama3.1:8b "Say 'Hello from Ollama!' and nothing else." 2>&1 | head -1)
if [ -n "$RESPONSE" ]; then
    echo "   ✅ Model responds: $RESPONSE"
else
    echo "   ❌ Model did not respond"
    exit 1
fi
echo ""

# Test 4: Python environment
echo "4. Testing Python dependencies..."
cd /Users/jprowan/Repos/obsidian-odin-local-llm/packages/backend
if python3 -c "import sentence_transformers; import langchain_community" 2>/dev/null; then
    echo "   ✅ Python dependencies installed"
else
    echo "   ⚠️  Python dependencies not installed"
    echo "      Install with: pip install -r requirements.txt"
fi
echo ""

# Test 5: .env file
echo "5. Checking .env file..."
if [ -f "/Users/jprowan/Repos/obsidian-odin-local-llm/packages/backend/.env" ]; then
    echo "   ✅ .env file exists"
    if grep -q 'LLM_PROVIDER="ollama"' /Users/jprowan/Repos/obsidian-odin-local-llm/packages/backend/.env; then
        echo "   ✅ Configured for Ollama"
    else
        echo "   ⚠️  Check LLM_PROVIDER setting in .env"
    fi
else
    echo "   ⚠️  .env file not created yet"
    echo "      Create with: cp template.env .env"
fi
echo ""

echo "========================================="
echo "Test Summary"
echo "========================================="
echo "If all tests passed, you're ready to go!"
echo "Start the backend with:"
echo "  cd packages/backend/core && ./run_server.sh"
echo ""
echo "Your vault data will stay 100% private! 🔒"

