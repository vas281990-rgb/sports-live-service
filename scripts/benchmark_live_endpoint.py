import statistics
import time

import requests

URL = "http://localhost:8000/api/v1/sport/football/events/live"
REQUESTS_COUNT = 100


def percentile(values: list[float], percentile_value: float) -> float:
    # Simple percentile calculation without external dependencies.
    sorted_values = sorted(values)
    index = int((len(sorted_values) - 1) * percentile_value)
    return sorted_values[index]


def main():
    latencies_ms = []
    for _ in range(REQUESTS_COUNT):
        # Start a high-resolution timer
        start = time.perf_counter()
        # Perform the GET request with a 5-second timeout
        response = requests.get(URL, timeout=5)
        response.raise_for_status()
        # End the timer and calculate duration in milliseconds
        end = time.perf_counter()
        latencies_ms.append((end - start) * 1000)

    # Calculate median (P50) and 95th percentile (P95) latencies
    p50 = statistics.median(latencies_ms)
    p95 = percentile(latencies_ms, 0.95)

    # Print the performance results
    print(f"Requests: {REQUESTS_COUNT}")
    print(f"P50 latency: {p50:.2f} ms")
    print(f"P95 latency: {p95:.2f} ms")


if __name__ == "__main__":
    main()