# Local LLM Setup with Ollama

This guide explains how to run ODIN with local LLM models for complete privacy. Your vault data never leaves your machine.

## Why Local LLM?

### Privacy Benefits
- ✅ **All data stays on your machine** - No external API calls
- ✅ **HIPAA/GDPR compliant** - Full data sovereignty  
- ✅ **Works offline** - No internet required
- ✅ **No API costs** - Free after initial setup
- ✅ **No data retention** - Nothing stored on external servers

### Performance on Apple Silicon
On M4 MacBook Air with 24 GB RAM:
- **Speed**: 30-50 tokens/second (instant feel)
- **Memory**: ~14-15 GB during active use
- **Models**: 8B-70B parameters supported

## Quick Start

### Prerequisites
- macOS with Apple Silicon (M1/M2/M3/M4) or Linux
- 16 GB RAM minimum (24 GB recommended)
- 10 GB free disk space

### 1. Install Ollama

**macOS:**
```bash
brew install ollama
# OR download from https://ollama.com/download
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Pull the Model

```bash
# Start Ollama service
ollama serve

# In a new terminal, pull the model
ollama pull llama3.1:8b

# Verify it works
ollama run llama3.1:8b "Hello!"
```

### 3. Setup Python Environment

```bash
cd packages/backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure for Local LLM

```bash
cd packages/backend

# Copy template if you haven't already
cp template.env .env

# Edit .env - it should already have these settings:
# LLM_PROVIDER="ollama"
# EMBEDDING_PROVIDER="local"
# LLM_MODEL_NAME="llama3.1:8b"
# EMBEDDING_MODEL_NAME="all-MiniLM-L6-v2"
```

For local development (non-Docker), also update:
```bash
MEMGRAPH_HOST="127.0.0.1"
CHROMA_DATA_DIR="/path/to/local/chroma/storage"
```

### 5. Start Services

**Terminal 1 - Memgraph:**
```bash
cd packages/backend/core
./run_memgraph_290.sh
```

**Terminal 2 - Backend:**
```bash
cd packages/backend/core
./run_server_venv.sh
```

**Terminal 3 - Open Obsidian** with the ODIN plugin enabled.

## Configuration

### Available Models

You can use any Ollama model. Popular choices:

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| `llama3.1:8b` | 5 GB | ⚡⚡⚡ | ⭐⭐⭐ | General use, fast responses |
| `llama3.1:70b` | 40 GB | ⚡ | ⭐⭐⭐⭐⭐ | Best quality, needs 48GB+ RAM |
| `mistral:7b` | 4 GB | ⚡⚡⚡ | ⭐⭐⭐ | Alternative, very capable |
| `mixtral:8x7b` | 26 GB | ⚡⚡ | ⭐⭐⭐⭐ | Balanced quality/speed |

To switch models:
```bash
ollama pull mistral:7b
# Update .env: LLM_MODEL_NAME="mistral:7b"
# Restart backend
```

### Embedding Models

Local embedding models (via sentence-transformers):

| Model | Dimensions | Speed | Quality | Size |
|-------|------------|-------|---------|------|
| `all-MiniLM-L6-v2` | 384 | ⚡⚡⚡ | ⭐⭐⭐ | 100 MB |
| `all-mpnet-base-v2` | 768 | ⚡⚡ | ⭐⭐⭐⭐ | 450 MB |
| `bge-large-en-v1.5` | 1024 | ⚡ | ⭐⭐⭐⭐⭐ | 1.3 GB |

Update in `.env`:
```bash
EMBEDDING_MODEL_NAME="all-mpnet-base-v2"
```

**Note:** Changing embedding models requires re-initializing your knowledge base as vector dimensions differ.

### Switching Between Local and Cloud

Edit `.env` to switch providers:

**Local (Private):**
```bash
LLM_PROVIDER="ollama"
EMBEDDING_PROVIDER="local"
LLM_MODEL_NAME="llama3.1:8b"
EMBEDDING_MODEL_NAME="all-MiniLM-L6-v2"
```

**OpenAI (Cloud):**
```bash
LLM_PROVIDER="openai"
EMBEDDING_PROVIDER="openai"
OPENAI_API_KEY="sk-your-key-here"
LLM_MODEL_NAME="gpt-4"
EMBEDDING_MODEL_NAME="text-embedding-ada-002"
```

**Hybrid (Local LLM, Cloud Embeddings):**
```bash
LLM_PROVIDER="ollama"
EMBEDDING_PROVIDER="openai"
OPENAI_API_KEY="sk-your-key-here"
LLM_MODEL_NAME="llama3.1:8b"
EMBEDDING_MODEL_NAME="text-embedding-ada-002"
```

## Performance Tuning

### Memory Management

Ollama keeps models loaded for 5 minutes by default. Configure with:

```bash
# Keep loaded for 30 minutes
OLLAMA_KEEP_ALIVE=30m ollama serve

# Unload immediately after use (saves memory)
OLLAMA_KEEP_ALIVE=0 ollama serve

# Keep loaded indefinitely (fastest)
OLLAMA_KEEP_ALIVE=-1 ollama serve
```

### Monitoring

**Check model status:**
```bash
ollama ps
```

**View memory usage:**
- macOS: Activity Monitor
- Install `stats` menu bar app: `brew install stats`

**Expected memory:**
- 8B model: ~5-6 GB
- 13B model: ~8-10 GB
- 70B model: ~40 GB

## Troubleshooting

### Ollama not connecting
```bash
# Check if running
ollama list

# If not, start it
ollama serve
```

### Model not found
```bash
# Verify model exists
ollama list

# Pull if missing
ollama pull llama3.1:8b
```

### Python module errors
```bash
# Make sure venv is activated
cd packages/backend
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Slow performance
- Ensure Ollama is using Metal (GPU) on macOS
- Try smaller model (`llama3.1:8b` vs `70b`)
- Check memory pressure in Activity Monitor
- Close other memory-intensive applications

### "Agent error" messages
Ollama doesn't support OpenAI's function calling API. The code automatically uses `STRUCTURED_CHAT` agent type for Ollama. If you see errors, verify `LLM_PROVIDER="ollama"` in `.env`.

## Comparison with OpenAI

| Aspect | Local (Ollama) | OpenAI |
|--------|----------------|--------|
| **Privacy** | ✅ Complete | ❌ Data sent to cloud |
| **Cost** | ✅ Free | 💰 API charges |
| **Speed** | ⚡ Fast on M4 | ⚡ Very fast |
| **Quality (8B)** | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent |
| **Quality (70B)** | ⭐⭐⭐⭐ Very good | ⭐⭐⭐⭐⭐ Excellent |
| **Offline** | ✅ Yes | ❌ No |
| **Setup** | ⚙️ More involved | ⚙️ Just API key |
| **Compliance** | ✅ HIPAA/GDPR OK | ⚠️ Depends on use case |

## Advanced Configuration

### Using Custom Models

Train or fine-tune your own model and use it:

```bash
# Create Modelfile
echo 'FROM ./my-model.gguf' > Modelfile

# Create Ollama model
ollama create my-custom-model -f Modelfile

# Use in .env
LLM_MODEL_NAME="my-custom-model"
```

### Running Ollama Remotely

Run Ollama on a server and connect from your machine:

```bash
# On server
OLLAMA_HOST=0.0.0.0:11434 ollama serve

# In .env
OLLAMA_BASE_URL="http://server-ip:11434"
```

### Docker Setup

Coming soon: Docker Compose setup with Ollama included.

## Migration Notes

### Switching from OpenAI to Local

1. **Embeddings**: You'll need to re-initialize your knowledge base as embedding dimensions differ (OpenAI: 1536, local: 384-1024)

2. **Quality**: Test with mock data first. Some complex Cypher queries may need larger models (70B) or prompt tuning.

3. **Speed**: Local models are fast on Apple Silicon but may be slower on older hardware.

### Switching Between Local Models

Switching LLM models (e.g., llama3.1:8b to mistral:7b) doesn't require re-indexing. Just update `.env` and restart.

Switching embedding models requires re-initialization if dimensions differ.

## Getting Help

- **Test setup**: Run `test_local_llm.sh` in the repo root
- **View logs**: Backend logs show detailed error messages
- **Check model**: `ollama ps` shows what's loaded
- **Community**: Open an issue on GitHub

## See Also

- **[Development Log](../devlog/2025-11-03-local-llm-implementation.md)** - Implementation details
- **[Quickstart Guide](quickstart.md)** - General ODIN setup
- **[Contributing Guide](contributing.md)** - Development setup
- **[Ollama Documentation](https://ollama.com)** - Model management
- **[Sentence Transformers](https://www.sbert.net/)** - Embedding models

