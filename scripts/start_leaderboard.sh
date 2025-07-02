#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 Starting Spectral Hub Leaderboard..."
echo "📁 Project root: $PROJECT_ROOT"

cd "$PROJECT_ROOT"

echo "📦 Checking Gradio..."
if ! python -c "import gradio" 2>/dev/null; then
    echo "❌ Gradio not found. Installing..."
    pip install gradio pandas
    echo "✅ Dependencies installed"
else
    echo "✅ Gradio found"
fi

cd leaderboard/gradio
python app.py