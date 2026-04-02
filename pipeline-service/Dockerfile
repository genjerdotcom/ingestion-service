FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Langsung copy file (tanpa apt-get agar tidak error network)
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Setup user keamanan
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

ENV PATH="/home/appuser/.local/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--proxy-headers"]