from time import time
from multiprocessing import Process

from get_queue import get_hz_q

def queue_reader(reader_id):
    hz, queue = get_hz_q()
    time_base = time()
    while True:
        item = queue.poll(timeout=2.)
        if item is None:
            print(f'Reader #{reader_id}; get no item in prev {time()-time_base:.2f}s')
            continue
        print(f'Reader #{reader_id}; get: {item:>2}; time to prev: {time()-time_base:.2e}')
        time_base = time()
        if item == -1:
            queue.put(-1)
            print(f"Reader #{reader_id} finished")
            break
    
    hz.shutdown()


if __name__ == "__main__":
    hz, queue = get_hz_q()
    queue.clear()

    num_readers = 2
    processes = []
    for i in range(num_readers):
        process = Process(target=queue_reader, args=[i])
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    hz.shutdown()
