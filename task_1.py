import random
import time
from functools import lru_cache


def range_sum_no_cache(array, L, R):
    return sum(array[L : R + 1])


def update_no_cache(array, index, value):
    array[index] = value


@lru_cache(maxsize=1000)
def range_sum_with_cache(array, L, R):
    return sum(array[L : R + 1])


def update_with_cache(array, index, value):
    array[index] = value
    range_sum_with_cache.cache_clear()


# --- Вимірювання часу ---
def run_no_cache(array, queries):
    temp_array = array[:]
    start = time.time()
    for q in queries:
        if q[0] == "Range":
            range_sum_no_cache(temp_array, q[1], q[2])
        else:
            update_no_cache(temp_array, q[1], q[2])
    return time.time() - start


def run_with_cache(array, queries):
    temp_array = array[:]
    start = time.time()
    for q in queries:
        if q[0] == "Range":
            range_sum_with_cache(temp_array, q[1], q[2])
        else:
            update_with_cache(temp_array, q[1], q[2])
    return time.time() - start


if __name__ == "__main__":
    # Масив
    N = 100_000
    array = [random.randint(1, 100) for _ in range(N)]

    # Запити
    Q = 50_000
    queries = []
    for _ in range(Q):
        if random.random() < 0.5:  # 50% Range, 50% Update
            L = random.randint(0, N - 1)
            R = random.randint(L, N - 1)
            queries.append(("Range", L, R))
        else:
            index = random.randint(0, N - 1)
            value = random.randint(1, 100)
            queries.append(("Update", index, value))

    t1 = run_no_cache(array=array, queries=queries)
    t2 = run_with_cache(array=array, queries=queries)
    print(f"Час виконання без кешування: {t1:.2f} секунд")
    print(f"Час виконання з LRU-кешем: {t2:.2f} секунд")
