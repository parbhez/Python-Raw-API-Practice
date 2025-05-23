import subprocess
import time
import signal
import sys

# চালাতে চাওয়া স্ক্রিপ্টগুলো
SCRIPT_FILES = ["blog_api.py", "auto_background_worker.py"]
processes = []

def start_all_scripts():
    for script in SCRIPT_FILES:
        print(f"✅ Starting: {script}")
        p = subprocess.Popen(["python", script])
        processes.append(p)

def stop_all_scripts():
    for p in processes:
        print(f"🛑 Stopping: PID {p.pid}")
        p.terminate()
        try:
            p.wait(timeout=5)
        except subprocess.TimeoutExpired:
            p.kill()

def signal_handler(sig, frame):
    print("\n✋ Interrupt received. Shutting down all scripts...")
    stop_all_scripts()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    start_all_scripts()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)
