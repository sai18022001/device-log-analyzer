from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_get_logs_returns_list():
    r = client.get("/logs")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_filter_by_severity_error():
    r = client.get("/logs?severity=ERROR")
    assert r.status_code == 200
    for log in r.json():
        assert log["severity"] == "ERROR"

def test_filter_by_severity_info():
    r = client.get("/logs?severity=INFO")
    assert r.status_code == 200
    for log in r.json():
        assert log["severity"] == "INFO"

def test_filter_by_device():
    r = client.get("/logs?device_id=dev_01")
    assert r.status_code == 200
    for log in r.json():
        assert log["device_id"] == "dev_01"

def test_limit_param():
    r = client.get("/logs?limit=5")
    assert r.status_code == 200
    assert len(r.json()) <= 5

def test_summary_returns_list():
    r = client.get("/logs/summary")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_summary_structure():
    r = client.get("/logs/summary")
    assert r.status_code == 200
    for item in r.json():
        assert "device_id" in item
        assert "INFO" in item
        assert "WARN" in item
        assert "ERROR" in item

def test_summary_counts_are_non_negative():
    r = client.get("/logs/summary")
    for item in r.json():
        assert item["INFO"] >= 0
        assert item["WARN"] >= 0
        assert item["ERROR"] >= 0