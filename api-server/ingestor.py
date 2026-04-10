import subprocess
import json
import sys
import os
from database import SessionLocal, LogRecord, init_db

# Path to compiled C++ binary
if sys.platform == "win32":
    BINARY_PATH = os.path.join("..", "build", "device-simulator", "Debug", "device_simulator.exe")
else:
    BINARY_PATH = os.path.join("..", "build", "device-simulator", "device_simulator")

def run():
    init_db()
    print(f"[ingestor] Starting binary: {BINARY_PATH}")

    process = subprocess.Popen(
        [BINARY_PATH],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    db = SessionLocal()
    try:
        for line in process.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                record = LogRecord(
                    timestamp = data["timestamp"],
                    device_id = data["device_id"],
                    severity  = data["severity"],
                    message   = data["message"]
                )
                db.add(record)
                db.commit()
                print(f"[ingestor] Stored: {data['severity']} | {data['device_id']} | {data['message']}")
            except json.JSONDecodeError:
                print(f"[ingestor] Skipping non-JSON line: {line}")
    finally:
        db.close()
        process.terminate()

if __name__ == "__main__":
    run()