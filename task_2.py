import timeit
from functools import lru_cache
import matplotlib.pyplot as plt


# --------- Реалізація Splay Tree ---------
class SplayNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class SplayTree:
    def __init__(self):
        self.root = None

    def _zig(self, x):
        return x.left, x.right

    def _splay(self, root, key):
        if not root or root.key == key:
            return root

        if key < root.key:
            if not root.left:
                return root
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._rotate_left(root.left)
            return self._rotate_right(root) if root.left else root
        else:
            if not root.right:
                return root
            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._rotate_right(root.right)
            return self._rotate_left(root) if root.right else root

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def insert(self, key, value):
        if not self.root:
            self.root = SplayNode(key, value)
            return
        self.root = self._splay(self.root, key)
        if self.root.key == key:
            return
        node = SplayNode(key, value)
        if key < self.root.key:
            node.right = self.root
            node.left = self.root.left
            self.root.left = None
        else:
            node.left = self.root
            node.right = self.root.right
            self.root.right = None
        self.root = node

    def get(self, key):
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            return self.root.value
        return None


# --------- Фібоначчі з LRU ---------
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


# --------- Фібоначчі з Splay Tree ---------
def fibonacci_splay(n, tree):
    cached = tree.get(n)
    if cached is not None:
        return cached
    if n < 2:
        tree.insert(n, n)
        return n
    val = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, val)
    return val


# --------- Основна логіка ---------
def main():
    results = []
    ns = list(range(0, 1000, 50))

    for n in ns:
        # LRU Cache
        fibonacci_lru.cache_clear()
        lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=1)

        # Splay Tree
        tree = SplayTree()
        splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=1)

        results.append((n, lru_time, splay_time))

    # Виведення таблиці
    print(f"{'n':<10}{'LRU Cache Time (s)':<25}{'Splay Tree Time (s)':<25}")
    print("-" * 60)
    for n, lru_t, splay_t in results:
        print(f"{n:<10}{lru_t:<25.10f}{splay_t:<25.10f}")

    # Побудова графіка
    xs = [r[0] for r in results]
    lru_times = [r[1] for r in results]
    splay_times = [r[2] for r in results]

    plt.plot(xs, lru_times, label="LRU Cache", marker="o")
    plt.plot(xs, splay_times, label="Splay Tree", marker="x")
    plt.xlabel("Число Фібоначчі (n)")
    plt.ylabel("Середній час виконання (секунди)")
    plt.title("Порівняння часу виконання для LRU Cache та Splay Tree")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
