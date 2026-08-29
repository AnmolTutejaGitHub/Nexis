#!/usr/bin/env bash

set -e

command -v uv || {
    echo "Please install uv first: https://docs.astral.sh/uv/"
    exit 1
}

[ -f .env ] || cp .env.sample .env

uv sync
uv pip install -e .

echo "Run:  uv run agent.py"
echo "Or from anywhere:  source $(pwd)/.venv/bin/activate && nexis"
