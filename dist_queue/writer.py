from time import time
from get_queue import get_hz_q


if __name__ == '__main__':
    hz, queue = get_hz_q()

    time_base = time()
    for i in range(15):
        # queue.put(i)
        queue.offer(i, timeout=1.)
        print(f'Writed {i:>2}: time to prev: {time()-time_base:.2e}, capacity left: {queue.remaining_capacity():>2}')
        time_base = time()

    queue.put(-1)
    hz.shutdown()