#!/bin/bash

set -e  # Exit on error

# STEP 1: System deps (if needed)
echo "🔧 Installing system dependencies..."
apt update && apt install -y wget curl git make build-essential \
  libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
  libsqlite3-dev libncursesw5-dev libgdbm-dev liblzma-dev \
  libffi-dev uuid-dev libdb-dev libexpat1-dev libmpdec-dev \
  libgmp-dev tk-dev

# STEP 2: Install Python 3.10.0
echo "🐍 Installing Python 3.10.0..."
cd /usr/src
wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz
tar xzf Python-3.10.0.tgz
cd Python-3.10.0
./configure --enable-optimizations
make -j$(nproc)
make altinstall
cd ~

# STEP 3: Clone repo
if [ ! -d "ollama-rag-fastapi-engine" ]; then
  echo "📦 Cloning your repo..."
  git clone https://github.com/BapanBigData/ollama-rag-fastapi-engine.git
fi

cd ollama-rag-fastapi-engine

# STEP 4: Set up Python virtual environment
echo "📦 Setting up Python environment..."
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# STEP 5: Pull Ollama models if not already pulled
echo "⬇️ Pulling Ollama models (if not already present)..."
ollama list | grep -q mxbai-embed-large || ollama pull mxbai-embed-large:latest
ollama list | grep -q llama3.1 || ollama pull llama3.1:8b

# STEP 6: Start FastAPI
echo "🚀 Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
