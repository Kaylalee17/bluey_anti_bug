import subprocess
import time
import sys

WORKER_SCRIPT = "main.py"
RESTART_DELAY = 5          # seconds to wait before restarting
MAX_RAPID_CRASHES = 5      # if it crashes this many times quickly, stop auto-restarting
CRASH_WINDOW = 60          # "quickly" = within this many seconds

crash_times = []

while True:
    print(f"[watcher] Starting {WORKER_SCRIPT}...")
    start = time.time()

    result = subprocess.run([sys.executable, WORKER_SCRIPT])

    end = time.time()
    print(f"[watcher] Worker exited with code {result.returncode} after {end - start:.1f}s")

    if result.returncode == 0:
        print("[watcher] Clean exit, not restarting.")
        break

    # crash-loop detection
    crash_times.append(end)
    crash_times = [t for t in crash_times if end - t < CRASH_WINDOW]

    if len(crash_times) >= MAX_RAPID_CRASHES:
        print(f"[watcher] {MAX_RAPID_CRASHES} crashes within {CRASH_WINDOW}s. Stopping auto-restart.")
        print("[watcher] Check worker.log for the last message processed before investigating.")
        break

    print(f"[watcher] Restarting in {RESTART_DELAY}s...")
    time.sleep(RESTART_DELAY)