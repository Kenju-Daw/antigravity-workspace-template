import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rag.ingest import IngestionPipeline
import asyncio

class DropHandler(FileSystemEventHandler):
    def __init__(self, pipeline: IngestionPipeline, loop):
        self.pipeline = pipeline
        self.loop = loop

    def on_created(self, event):
        if event.is_directory:
            print(f"New folder detected: {event.src_path}")
            # Schedule the async ingestion in the running loop
            asyncio.run_coroutine_threadsafe(
                self.pipeline.process_folder(event.src_path),
                self.loop
            )

class Watcher:
    def __init__(self, watch_dir: str):
        self.watch_dir = watch_dir
        self.pipeline = IngestionPipeline(watch_dir)
        self.observer = Observer()

    def start(self):
        loop = asyncio.get_running_loop()
        event_handler = DropHandler(self.pipeline, loop)
        self.observer.schedule(event_handler, self.watch_dir, recursive=False)
        self.observer.start()
        print(f"Watcher started on {self.watch_dir}")

    def stop(self):
        self.observer.stop()
        self.observer.join()
