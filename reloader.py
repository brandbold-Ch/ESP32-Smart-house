import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PySide6.QtCore import QProcess, QCoreApplication
import os


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, process):
        super().__init__()
        self.process = process

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f'{event.src_path} ha sido modificado. Reiniciando el script...')
            self.process.kill()
            self.process.waitForFinished()
            self.process.start(sys.executable, ["main.py"])


def main() -> None:
    app = QCoreApplication(sys.argv)

    process = QProcess()
    process.start(sys.executable, ["main.py"])

    event_handler = ChangeHandler(process)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(os.path.abspath(__file__)), recursive=True)
    observer.start()

    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
