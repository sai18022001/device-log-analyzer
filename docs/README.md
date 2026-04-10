# Device Log Analyzer

A full-stack embedded log analysis system built with C++, Python, and SQLite.

## Architecture

A C++ simulator generates realistic device telemetry logs (JSON over stdout).
A Python ingestor reads the stream and stores logs into a SQLite database.
A FastAPI REST API exposes endpoints to query and summarize the logs.

## Tech Stack

- C++17 — embedded device log simulator
- Python 3 + FastAPI — REST API layer
- SQLAlchemy + SQLite — database
- CMake — build system
- Git — version control

## Setup & Run

### 1. Build C++ simulator

```bash
cmake -S . -B build
cmake --build build
```

### 2. Install Python dependencies

```bash
cd api-server
pip install -r requirements.txt
```

### 3. Start the ingestor (Terminal 1)

```bash
cd api-server
python ingestor.py
```

### 4. Start the API server (Terminal 2)

```bash
cd api-server
python -m uvicorn main:app --reload
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/logs` | Fetch all logs. Filter by `severity`, `device_id`, `limit` |
| GET | `/logs/summary` | Count of INFO/WARN/ERROR grouped by device |
| GET | `/health` | Health check |

### Example requests