from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time

class ReloadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py"):  # Surveiller les fichiers .py
            print("Changements détectés, redémarrage...")
            os.system("python /home/nathan/Documents/PROJECT/Reconnaissace_Facial/connect.py")  # Exécuter ton script

if __name__ == "__main__":
    path = "."  # Dossier courant
    event_handler = ReloadHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
