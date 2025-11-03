# Python Environment Options

This project requires **Python 3.9.16** for the backend. Here are different ways to set it up.

## Option 1: Conda (Default/Recommended)

### What is Conda?
- Package + environment manager
- Handles Python versions and dependencies
- Good at managing C/C++ dependencies

### Installation
```bash
# Install Miniconda (lightweight, ~400MB)
# macOS Intel:
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
bash Miniconda3-latest-MacOSX-x86_64.sh

# macOS Apple Silicon (M1/M2):
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
bash Miniconda3-latest-MacOSX-arm64.sh
```

### Usage
```bash
# Create environment
conda create -n odin_backend python=3.9.16
conda activate odin_backend

# Install dependencies
cd packages/backend
pip install -e .

# Use the development scripts
./scripts/start-dev.sh
```

**Pros:**
- ✅ Easiest to get exact Python version (3.9.16)
- ✅ Well-tested with this project
- ✅ Scripts use it by default

**Cons:**
- ⚠️ Large download (~400MB)
- ⚠️ Another tool to learn

---

## Option 2: pyenv + venv

### What is pyenv?
- Python version manager only
- Lightweight
- Uses standard venv for environments

### Installation
```bash
# Install pyenv
brew install pyenv

# Add to shell (for bash/zsh)
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
```

### Usage
```bash
# Install Python 3.9.16
pyenv install 3.9.16

# Set for this project
cd /path/to/obsidian-odin/packages/backend
pyenv local 3.9.16

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .
```

### Modify start-dev.sh for pyenv
Replace:
```bash
conda run -n odin_backend uvicorn ...
```

With:
```bash
source packages/backend/venv/bin/activate
uvicorn core.restapi.api:app --reload ...
```

**Pros:**
- ✅ Lightweight (~50MB per Python version)
- ✅ Standard Python tools (venv)
- ✅ Easy to switch Python versions

**Cons:**
- ⚠️ Manual modification of scripts needed
- ⚠️ Less tested with this project

---

## Option 3: Docker Only (No Local Python)

### What is it?
Run backend in Docker, but with volume mounting for development.

### Usage
```bash
# Modified docker-compose.yml to reload on changes
docker compose up

# Backend code changes trigger reload inside container
```

### For this to work well, modify docker-compose.yml:
```yaml
backend:
  # ... existing config ...
  volumes:
    - ./packages/backend:/usr/src/bor
  command: >
    conda run --no-capture-output -n bor_env
    uvicorn core.restapi.api:app --reload --host 0.0.0.0 --port 8000
```

**Pros:**
- ✅ No local Python setup needed
- ✅ Exact match to production environment

**Cons:**
- ⚠️ Slower iteration (still 3-5 seconds vs < 1 second)
- ⚠️ Harder to debug
- ⚠️ Doesn't get the "hybrid" workflow benefits

---

## Option 4: System Python (If You Have 3.9.x)

### Check Your Version
```bash
python3 --version
# If output is Python 3.9.x (any 3.9 version), you can use this
```

### Usage
```bash
cd packages/backend

# Create virtual environment with system Python
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .
```

**Pros:**
- ✅ No additional tools needed
- ✅ Simplest setup

**Cons:**
- ⚠️ Only works if you already have Python 3.9.x
- ⚠️ Most modern systems have 3.10+ (won't work)
- ⚠️ May break if you update system Python

---

## Comparison Table

| Method | Setup Complexity | Disk Space | Auto-reload Speed | Recommended? |
|--------|------------------|------------|-------------------|--------------|
| **Conda** | Easy | ~400MB | < 1 sec | ✅ Yes (default) |
| **pyenv + venv** | Medium | ~100MB | < 1 sec | ✅ Yes (if prefer lighter) |
| **Docker only** | Easy | ~2GB | 3-5 sec | 🤷 OK (but slower) |
| **System Python** | Very Easy | ~50MB | < 1 sec | ⚠️ Only if 3.9.x |

---

## Why Python 3.9.16 Specifically?

The project requires Python 3.9.x because:

1. **pymgclient compatibility** - The Memgraph Python client was built/tested with 3.9
2. **Dependency constraints** - Some libraries may not support Python 3.10+
3. **Stability** - 3.9.16 was the stable version when the project was created

### Can I Use Python 3.10 or 3.11?

**Maybe**, but not recommended:
- Some dependencies might fail to install
- Untested - you'd be the guinea pig
- Could work, but if you hit issues, you'll need to downgrade

---

## Switching Between Options

You can switch freely:

```bash
# From conda to pyenv
conda deactivate
pyenv local 3.9.16
python -m venv venv
source venv/bin/activate
pip install -e .

# From pyenv to conda
deactivate  # Exit venv
rm -rf venv
conda create -n odin_backend python=3.9.16
conda activate odin_backend
pip install -e .
```

---

## My Recommendation

**Start with conda** (Option 1):
- It's what the scripts use
- It's what the documentation assumes
- It's the path of least resistance

**Switch to pyenv later** if:
- You want something lighter weight
- You're comfortable modifying the scripts
- You prefer standard Python tools

**Use Docker only** if:
- You don't want to install Python at all
- You're okay with slower iteration
- You want exact production parity

---

## Quick Start Commands

### Conda
```bash
conda create -n odin_backend python=3.9.16
conda activate odin_backend
cd packages/backend && pip install -e .
```

### pyenv
```bash
pyenv install 3.9.16
cd packages/backend
pyenv local 3.9.16
python -m venv venv
source venv/bin/activate
pip install -e .
```

### Docker Only
```bash
docker compose up
# That's it!
```

Choose the one that fits your preference and existing setup!

