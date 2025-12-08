from time import perf_counter

def time_it(code):
    start_time = perf_counter()
    code()
    end_time = perf_counter()
    duration_ms = (end_time - start_time) * 1000
    print(f"Duration: {duration_ms:.2f} ms")