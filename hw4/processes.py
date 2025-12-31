import sys
import time
import codecs
import threading
import multiprocessing
from queue import Empty
from datetime import datetime

STOP_SIGNAL = "\0"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

def A(queue_in, queue_out):
    buffer = []
    last_sent = time.time()
    while True:
        try:
            buffer.append(queue_in.get(timeout=0.1).lower())
        except Empty:
            pass

        if buffer and (time.time() - last_sent >= 5):
            msg = buffer.pop(0)
            queue_out.put(msg)
            last_sent = time.time()
            if msg == STOP_SIGNAL:
                break

def B(queue_in, queue_out):
    while True:
        try:
            msg = queue_in.get(timeout=0.1)
            if msg == STOP_SIGNAL:
                break 

            msg = codecs.encode(msg, "rot_13")
            timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
            sys.stdout.write(f"{msg}\n")
            sys.stdout.flush()
            queue_out.put((timestamp, msg))
        except Empty:
            pass

def reader(queue_in, file):
    while True:
        try:
            msg = input()
            timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
            file.write(f"[IN] \t{timestamp}\t{msg}\n")
            file.flush()
            queue_in.put(msg)
        except EOFError:
            queue_in.put(STOP_SIGNAL)
            break

def main():
    queue_A = multiprocessing.Queue()
    queue_B = multiprocessing.Queue()
    queue_main = multiprocessing.Queue()

    process_A = multiprocessing.Process(target=A, args=(queue_A, queue_B))
    process_B = multiprocessing.Process(target=B, args=(queue_B, queue_main))

    process_A.start()
    process_B.start()

    with open("artifacts/task3/result.txt", "w") as file:
        reader_thread = threading.Thread(target=reader, args=(queue_A, file))
        reader_thread.start()

        while reader_thread.is_alive() or not queue_main.empty():
            try:
                timestamp, msg = queue_main.get(timeout=0.1)
                file.write(f"[OUT] \t{timestamp}\t{msg}\n")
                file.flush()
            except Empty:
                continue

        reader_thread.join()
    
    process_A.join()
    process_B.join()

if __name__ == "__main__":
    main()
