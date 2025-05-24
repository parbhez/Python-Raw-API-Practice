import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# আপনার চালাতে চাওয়া script গুলোর নাম এখানে দিন
SCRIPT_FILES = ["blog_api.py", "auto_background_worker.py"]

class ReloadHandler(FileSystemEventHandler):
    def __init__(self):
        
        self.processes = []
        self.start_all_scripts()

    def start_all_scripts(self):
        # আগের সব প্রসেস kill করে আবার শুরু করবে
        self.stop_all_scripts()
        self.processes = []
        for script in SCRIPT_FILES:
            print(f"Starting: {script}")
            p = subprocess.Popen(["python", script])
            self.processes.append(p)

    def stop_all_scripts(self):
        for process in self.processes:
            process.kill()


    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"🔁 Detected change in {event.src_path}, restarting all scripts...")
            self.start_all_scripts()

if __name__ == "__main__":
    path = "."
    event_handler = ReloadHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        event_handler.stop_all_scripts()

    observer.join()
