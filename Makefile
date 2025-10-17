.PHONY: install dev run lint test format

PY=.venv/Scripts/python
PIP=./.venv/Scripts/pip

install:
	@echo "📦 Installing dependencies..."
	uv pip install -r requirements.txt

dev:
	@echo "🚀 Starting development server..."
	$(PY) -m uvicorn app.main:app --reload

start:
	@echo "🚀 Starting server..."
	$(PY) -m uvicorn app.main:app

format:
	@echo "🎨 Formatting code with Black..."
	$(PY) -m black app

lint:
	@echo "🔍 Linting code with Ruff..."
	$(PY) -m ruff check app

lint-fix:
	@echo "🔧 Fixing lint issues with Ruff..."
	$(PY) -m ruff check app --fix