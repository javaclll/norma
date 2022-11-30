from libbaghchal import Baghchal, GameStatus
from bagchal import Bagchal as BaghchalOld
import time


def bench():
    bagchal = Baghchal.default()

    start_time = time.time()
    for _ in range(10000):
        bagchal.get_possible_moves()

    elapsed = time.time() - start_time
    print(f"New Time Taken: {time.time() - start_time}s")
    return elapsed


def bench_old():
    bagchal = BaghchalOld.new()

    start_time = time.time()
    for _ in range(10000):
        bagchal.get_possible_moves()

    elapsed = time.time() - start_time
    print(f"Old Time Taken: {elapsed} s")
    return elapsed


if __name__ == "__main__":
    print(f"Speedup: {bench_old()/bench():.1f}X")
    # bench()
    # bench_old()
