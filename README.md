# Pipeline Service and Mock Server

This repository contains the Pipeline Service and Mock Server infrastructure. This guide covers the system requirements, environment setup, and how to orchestrate the services using Docker Compose.

---

## Requirements

Before starting, ensure your environment meets the following specifications:

- Docker 20.x or higher
- Docker Compose 1.29.x or higher
- Python 3.10 or higher (for local script execution)

---

### Environment Variables Setup

Copy the provided `.env-example` to a new `.env` file in each directory:

# Pipeline Service
```bash
cp pipeline-service/.env-example pipeline-service/.env
```

# Mock Server
```bash
cp mock-server/.env-example mock-server/.env
```

## Running with Docker Compose

To build and start all services, navigate to the project root (where `docker-compose.yml` is located) and run:
```bash
docker-compose up -d 
Or
docker-compose up
```

### Useful Commands:

- **View Logs**: Monitor real-time logs for all services.
```bash
docker-compose logs -f
```

- **Stop Services**: Stop and remove containers.
```bash
docker-compose down
```

- **Rebuild**: Use this if you make changes to the Dockerfiles.
```bash
docker-compose up -d --build
```

------------------------------------------------------------------------------------

## Running manual (Development)

### mock-server

go to directory
```bash
cd mock-server
```

Create Virtual Environtment

```bash
python -m venv venv
```

Linux / Mac
```bash
source venv/bin/activate
```

Windows
```bash
venv\Scripts\activate
```
Install dependencies

```bash
pip install -r requirements.txt
```

Run Application
```bash
flask run --debug
```


### pipeline-service

go to directory
```bash
cd pipeline-service
```

change environtment `.env`
```bash
python -m venv venv
```

Create Virtual Environtment

```bash
DB_HOST=localhost
FLASK_HOST=localhost
FASTAPI_HOST=localhost
```

Linux / Mac
```bash
source venv/bin/activate
```

Windows
```bash
venv\Scripts\activate
```
Install dependencies

```bash
pip install -r requirements.txt
```

Run Application
```bash
uvicorn main:app --reload
```