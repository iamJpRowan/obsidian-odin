import os
import dotenv

f = dotenv.find_dotenv()
if not f:
    f = dotenv.find_dotenv('template.env')
dotenv.load_dotenv(f)

# LLM Provider: 'openai' or 'ollama'
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "ollama")

# OpenAI Configuration (if using OpenAI)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Ollama Configuration (if using Ollama)
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")

MEMGRAPH_HOST = os.environ.get("MEMGRAPH_HOST", "127.0.0.1")
MEMGRAPH_PORT = os.environ.get("MEMGRAPH_PORT", "7687")
MEMGRAPH_PORT = int(MEMGRAPH_PORT)

CHROMA_DATA_DIR = os.environ.get("CHROMA_DATA_DIR")
CHROMA_VECTOR_SPACE = os.environ.get("CHROMA_VECTOR_SPACE")

# Embedding configuration
EMBEDDING_PROVIDER = os.environ.get("EMBEDDING_PROVIDER", "local")  # 'openai' or 'local'
EMBEDDING_MODEL_NAME = os.environ.get(
    "EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")  # For local: sentence-transformers model name

# LLM model configuration
LLM_MODEL_NAME = os.environ.get("LLM_MODEL_NAME", "llama3.1:8b")  # For Ollama: model name
LLM_MODEL_TEMPERATURE = os.environ.get("LLM_MODEL_TEMPERATURE", "0.2")
LLM_MODEL_TEMPERATURE = float(LLM_MODEL_TEMPERATURE)

MOCK = (os.environ.get("MOCK", 'False') == 'True')
