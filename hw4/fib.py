import time
import threading
import multiprocessing

def fib(n: int) -> int:
    if n <= 1:
        return n

    return fib(n - 1) + fib(n - 2)

def run_sync(n: int, runs: int) -> float:
    start = time.perf_counter()
    for _ in range(runs):
        fib(n)

    return time.perf_counter() - start

def run_threading(n: int, runs: int) -> float:
    start = time.perf_counter()

    threads = []
    for _ in range(runs):
        thread = threading.Thread(target=fib, args=(n,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return time.perf_counter() - start

def run_multiprocessing(n: int, runs: int) -> float:
    start = time.perf_counter()
    
    processes = []
    for _ in range(runs):
        process = multiprocessing.Process(target=fib, args=(n,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    return time.perf_counter() - start

def main():
    n = 36
    runs = 10

    sync_time = run_sync(n, runs)
    threading_time = run_threading(n, runs)
    multiprocessing_time = run_multiprocessing(n, runs)

    with open("artifacts/task1/result.txt", "w") as file:
        file.write(f"Sync time: {sync_time:.4f} seconds\n")
        file.write(f"Threading time: {threading_time:.4f} seconds\n")
        file.write(f"Multiprocessing time: {multiprocessing_time:.4f} seconds\n")

if __name__ == "__main__":
    main()
