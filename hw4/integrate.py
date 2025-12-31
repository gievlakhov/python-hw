import os
import math
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def integrate_chunk(f, a, step, start, end):
    acc = 0
    for i in range(start, end):
        acc += f(a + i * step) * step

    return acc

def integrate(f, a, b, *, n_jobs=1, n_iter=10_000_000, executor_type='thread'):
    step = (b - a) / n_iter
    chunk_size = n_iter // n_jobs

    ranges = []
    for i in range(n_jobs):
        start = chunk_size * i
        end = chunk_size * (i + 1) if i < n_jobs - 1 else n_iter
        ranges.append((start, end))

    if executor_type == "thread":
        Executor = ThreadPoolExecutor
    elif executor_type == "process":
        Executor = ProcessPoolExecutor
    else:
        raise ValueError(f"unknown executor type: {executor_type}")

    acc = 0
    with Executor(max_workers=n_jobs) as executor:
        futures = [
            executor.submit(integrate_chunk, f, a, step, start, end) 
            for start, end in ranges
        ]

        for future in futures:
            acc += future.result()

    return acc

def main():
    results = []
    for n_jobs in range(1, os.cpu_count() * 2 + 1):
        start = time.perf_counter()
        integrate(math.cos, 0, math.pi / 2, n_jobs=n_jobs, n_iter=10_000_000, executor_type='thread')
        thread_time = time.perf_counter() - start

        start = time.perf_counter()
        integrate(math.cos, 0, math.pi / 2, n_jobs=n_jobs, n_iter=10_000_000, executor_type='process')
        process_time = time.perf_counter() - start

        results.append((n_jobs, thread_time, process_time))

    with open("artifacts/task2/result.txt", "w") as file:
        for n_jobs, thread_time, process_time in results:
            file.write(f"jobs number: {n_jobs}, thread time: {thread_time:.4f} seconds, process time: {process_time:.4f} seconds\n")


if __name__ == "__main__":
    main()
