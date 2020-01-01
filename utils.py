import threading
from datetime import datetime
from pathlib import Path


last_completed = 0

def format_size(path_size):
    index = 0
    cases = ["Bytes", "KB", "MB", "GB"]
    while path_size > 1024:
        path_size = path_size / 1024
        index+=1
    return (f'{path_size:.4g}'+" "+cases[index])


def threaded_dir_size(base_path, string_var):
    def get_dir_size(path, string_var):
        global last_completed
        sent = datetime.timestamp(datetime.now())
        try:
            base_path_size = sum(f.stat().st_size for f in path.glob('**/*') \
                             if f.is_file())
        except OSError as e:
            print(e)
            base_path_size = -1

        if sent>last_completed or last_completed == 0:
            last_completed = datetime.timestamp(datetime.now())
            if base_path_size>=0:
                string_var.set(format_size(base_path_size))
            else: string_var.set("Permission Error")



    my_thread = threading.Thread(target=get_dir_size,
                                 name="Size_Calc",
                                 args=(Path(base_path),string_var,))

    my_thread.setDaemon(True)
    my_thread.start()









def main():
    print(format_size(1024*8347.3234))
    print("test")

if __name__ == "__main__":
    main()

