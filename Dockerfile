FROM python:3.12-slim

WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT=/app/.venv \
    PATH="/app/.venv/bin:/root/.local/bin:${PATH}" \
    PYTHONPATH=/app \
    PYTHONUNBUFFERED=1

# Install uv (no pip) so we can sync dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies first for better layer caching
COPY uv.lock pyproject.toml ./
RUN uv sync --frozen --no-dev

# Bring in the rest of the app
COPY . .

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
