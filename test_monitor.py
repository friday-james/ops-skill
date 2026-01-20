#!/usr/bin/env python3
import time
import sys
from datetime import datetime

def main():
    print("Starting monitored process...", flush=True)
    counter = 0

    while True:
        counter += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if counter % 5 == 0:
            print(f"[{timestamp}] WARNING: Counter reached {counter}", flush=True)
        else:
            print(f"[{timestamp}] INFO: Iteration {counter} - Process running normally", flush=True)

        # Simulate some work
        time.sleep(10)

        # Add an error every 20 iterations for testing
        if counter % 20 == 0:
            print(f"[{timestamp}] ERROR: Simulated error at iteration {counter}", flush=True)

if __name__ == "__main__":
    main()
