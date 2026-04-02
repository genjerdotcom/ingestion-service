FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production

WORKDIR /app

# Langsung copy file
COPY . .

# Install dependencies (tambahkan gunicorn)
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Setup user keamanan
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

ENV PATH="/home/appuser/.local/bin:$PATH"

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]