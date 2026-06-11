FROM python:3.14-slim AS builder

WORKDIR /code

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY pyproject.toml ./
COPY uv.lock ./
COPY README.md ./

RUN uv sync --frozen --no-dev

FROM python:3.14-slim

WORKDIR /code

COPY --from=builder /code/.venv /code/.venv
COPY app ./app

ENV PATH="/code/.venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]