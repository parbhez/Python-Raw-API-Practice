import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time

class ReloadHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = subprocess.Popen(["python", "blog_api.py"])

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"Detected change in {event.src_path}, restarting server...")
            self.process.kill()
            self.process = subprocess.Popen(["python", "blog_api.py"])

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
        event_handler.process.kill()

    observer.join()
