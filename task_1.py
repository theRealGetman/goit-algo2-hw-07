import random
import time
from collections import OrderedDict

# from functools import lru_cache

# --- Налаштування ---
N = 100_000  # розмір масиву
Q = 50_000  # кількість запитів
CACHE_SIZE = 1000  # розмір LRU-кешу


# --- Функції без кешу ---
def range_sum_no_cache(array, L, R):
    return sum(array[L : R + 1])


def update_no_cache(array, index, value):
    array[index] = value


# --- Простий LRU-кеш ---
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)  # робимо найновішим
            return self.cache[key]
        return None

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # видаляємо найстаріший

    def invalidate_ranges_with_index(self, index):
        keys_to_delete = [k for k in self.cache if k[0] <= index <= k[1]]
        for k in keys_to_delete:
            del self.cache[k]


# --- Функції з кешем ---
cache = LRUCache(CACHE_SIZE)

# @lru_cache(maxsize=1000)
# def cached_range_sum(L, R, array_tuple):
#     return sum(array_tuple[L : R + 1])


# def range_sum_with_cache(array, L, R):
#     return cached_range_sum(L, R, tuple(array))


# def update_with_cache(array, index, value):
#     array[index] = value
#     cached_range_sum.cache_clear()


def range_sum_with_cache(array, L, R):
    key = (L, R)
    cached = cache.get(key)
    if cached is not None:
        return cached
    result = sum(array[L : R + 1])
    cache.put(key, result)
    return result


def update_with_cache(array, index, value):
    array[index] = value
    cache.invalidate_ranges_with_index(index)


# --- Генерація даних ---
def generate_test_data(N, Q):
    array = [random.randint(1, 100) for _ in range(N)]
    queries = []
    for _ in range(Q):
        if random.random() < 0.5:
            L = random.randint(0, N - 1)
            R = random.randint(L, N - 1)
            queries.append(("Range", L, R))
        else:
            idx = random.randint(0, N - 1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
    return array, queries


# --- Вимірювання часу ---
def run_without_cache(array, queries):
    arr = array[:]
    start = time.time()
    for q in queries:
        if q[0] == "Range":
            range_sum_no_cache(arr, q[1], q[2])
        else:
            update_no_cache(arr, q[1], q[2])
    return time.time() - start


def run_with_cache(array, queries):
    arr = array[:]
    global cache
    cache = LRUCache(CACHE_SIZE)
    start = time.time()
    for q in queries:
        if q[0] == "Range":
            range_sum_with_cache(arr, q[1], q[2])
        else:
            update_with_cache(arr, q[1], q[2])
    return time.time() - start


# --- Запуск програми ---
if __name__ == "__main__":
    array, queries = generate_test_data(N, Q)

    t1 = run_without_cache(array, queries)
    t2 = run_with_cache(array, queries)

    print(f"Час виконання без кешування: {t1:.2f} секунд")
    print(f"Час виконання з LRU-кешем: {t2:.2f} секунд")
