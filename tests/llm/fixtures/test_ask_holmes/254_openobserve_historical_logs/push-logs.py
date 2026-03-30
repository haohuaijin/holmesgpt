#!/usr/bin/env python3
"""Push test logs to OpenObserve for eval test 254.

Generates logs within the last 4 hours (OpenObserve default allows last 5 hours).
The incident period is placed ~2 hours ago and lasts 30 minutes.
"""
import json
import random
import sys
import urllib.error
import urllib.request
import base64
from datetime import datetime, timedelta, timezone

random.seed(254)

BATCH_SIZE = 200


def push_batch(url, user, password, records, max_retries=10):
    """Push a batch of log records to OpenObserve with retry on transient errors."""
    import time as _time

    credentials = base64.b64encode(f"{user}:{password}".encode()).decode()
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                f"{url}/api/default/default/_json",
                data=json.dumps(records).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Basic {credentials}",
                },
            )
            response = urllib.request.urlopen(req, timeout=30)
            if response.status != 200:
                raise Exception(f"OpenObserve returned status {response.status}")
            body = json.loads(response.read())
            for status in body.get("status", []):
                if status.get("failed", 0) > 0:
                    error_msg = status.get("error", "unknown")
                    if "being deleted" in error_msg and attempt < max_retries - 1:
                        print(f"Stream being deleted, retrying in 3s (attempt {attempt + 1})...")
                        _time.sleep(3)
                        break  # retry
                    raise Exception(f"OpenObserve ingestion error: {error_msg}")
            else:
                return  # success
        except urllib.error.HTTPError as e:
            if e.code == 400 and attempt < max_retries - 1:
                print(f"Got 400, retrying in 3s (attempt {attempt + 1})...")
                _time.sleep(3)
                continue
            raise
    raise Exception(f"Failed to push batch after {max_retries} retries")


def generate_logs():
    """Generate logs within the last 4 hours including an incident period."""
    logs = []

    now = datetime.now(timezone.utc)

    # Incident window: 2.5 hours ago to 2 hours ago (30 min window)
    problem_start = now - timedelta(hours=2, minutes=30)
    problem_end = now - timedelta(hours=2)

    # Generate logs from 4 hours ago to now
    current_time = now - timedelta(hours=4)

    while current_time < now:
        ts_micro = int(current_time.timestamp() * 1e6)

        if random.random() < 0.1:
            logs.append({
                "_timestamp": ts_micro,
                "level": "INFO",
                "message": "Payment processed successfully",
                "service": "payment-api",
                "pod_name": "payment-api-254-6b8f9d7c4-xk2m9",
                "namespace": "app-254",
                "payment_id": f"PAY-{random.randint(1000, 9999)}",
                "amount": round(random.uniform(10, 1000), 2),
                "processing_time_ms": random.randint(100, 500),
            })

        if random.random() < 0.05:
            logs.append({
                "_timestamp": ts_micro,
                "level": "INFO",
                "message": "User authenticated",
                "service": "payment-api",
                "pod_name": "payment-api-254-6b8f9d7c4-xk2m9",
                "namespace": "app-254",
                "user_id": f"USER-{random.randint(100, 999)}",
                "method": "oauth2",
            })

        if random.random() < 0.2:
            query_time = random.randint(10, 100)
            if problem_start <= current_time <= problem_end:
                query_time = random.randint(1000, 5000)

            logs.append({
                "_timestamp": ts_micro,
                "level": "DEBUG",
                "message": "Database query executed",
                "service": "payment-api",
                "pod_name": "payment-api-254-6b8f9d7c4-xk2m9",
                "namespace": "app-254",
                "duration_ms": query_time,
            })

        if problem_start <= current_time <= problem_end:
            if random.random() < 0.3:
                logs.append({
                    "_timestamp": ts_micro,
                    "level": "ERROR",
                    "message": "Failed to acquire database connection - pool exhausted",
                    "service": "payment-api",
                    "pod_name": "payment-api-254-6b8f9d7c4-xk2m9",
                    "namespace": "app-254",
                    "pool_size": 20,
                    "active_connections": 20,
                    "waiting_requests": random.randint(5, 50),
                    "wait_time_ms": random.randint(5000, 30000),
                })

            if random.random() < 0.2:
                logs.append({
                    "_timestamp": ts_micro,
                    "level": "ERROR",
                    "message": "ConnectionPoolExhausted: All connections in use",
                    "service": "payment-api",
                    "pod_name": "payment-api-254-6b8f9d7c4-xk2m9",
                    "namespace": "app-254",
                    "error_code": "DB_CONN_001",
                })

            if random.random() < 0.1:
                logs.append({
                    "_timestamp": ts_micro,
                    "level": "ERROR",
                    "message": "Health check failed - database unreachable",
                    "service": "payment-api",
                    "pod_name": "payment-api-254-6b8f9d7c4-xk2m9",
                    "namespace": "app-254",
                    "endpoint": "/healthz",
                    "status_code": 503,
                })

        current_time += timedelta(seconds=random.randint(5, 30))

    # Print incident window for the test prompt
    print(f"Incident window: {problem_start.strftime('%H:%M')} - {problem_end.strftime('%H:%M')} UTC")

    return logs


def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <openobserve_url> <username> <password>")
        sys.exit(1)

    url, user, password = sys.argv[1], sys.argv[2], sys.argv[3]

    print("Generating logs...")
    logs = generate_logs()
    print(f"Generated {len(logs)} log records")

    # Push in batches
    for i in range(0, len(logs), BATCH_SIZE):
        batch = logs[i:i + BATCH_SIZE]
        push_batch(url, user, password, batch)
        print(f"Pushed {min(i + BATCH_SIZE, len(logs))}/{len(logs)} logs")

    print("All logs pushed successfully")


if __name__ == "__main__":
    main()
