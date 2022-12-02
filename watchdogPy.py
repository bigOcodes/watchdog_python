import os, sys, time

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler

class monitorFolder(FileSystemEventHandler):
    """
    watchdog to continuously monitor a folder to check for any new files or
    when an existing file is modified or deleted.
    When the size of the folder exceeds a certain limit, then take some action
    
    install watchdog ->
        $pip install watchdog
 
    """
    FILE_SIZE = 1000
    
    def on_created(self, event):
        print(event.src_path, event.event_type)
        self.checkFolderSize(event.src_path)
        
    def on_modified(self, event):
        print(event.src_path, event.event_type)
        self.checkFolderSize(event.src_path)
        
    def checkFolderSize(self, src_path):
        if os.path.isdir(src_path):
            if os.path.getsize(src_path) > self.FILE_SIZE:
                print("Time to backup the dir")
                
        else:
            if os.path.getsize(src_path) > self.FILE_SIZE:
                print("File is too big")
                
if __name__ == "__main__":
    src_path = sys.argv[1]

    event_handler = monitorFolder()
    observer = Observer()
    observer.schedule(event_handler, path=src_path, recursive = True)
    print("Monitoring Started")
    observer.start()
    
    try:
        while(True):
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()