import hazelcast
from box import Box

from time import time

from multiprocessing import Process


def get_hz_map():
    hz = hazelcast.HazelcastClient(cluster_name="dev")
    map = hz.get_map("map").blocking()
    return hz, map

def perfrom_loop(add_to_val_in_map, cfg):
    hz, map = get_hz_map()
    for _ in range(cfg.steps):
        add_to_val_in_map(map, cfg.key, to_add=1)

    hz.shutdown()


def without_lock(map, key, to_add):
    val = map.get(key)
    val += to_add
    map.put(key, val)

def pessimistic_lock(map, key, to_add):
    map.lock(key)
    try:
        val = map.get(key)
        val += to_add
        map.put(key, val)
    finally:
        map.unlock(key)

def optimistic_lock(map, key, to_add):

    while True:
        val = map.get(key)
        new_val = val
        new_val += to_add
        if map.replace_if_same(key, val, new_val):
            break

if __name__ == "__main__":
    cfg = Box({
        'key': 'flex',
        'num_clients': 3,
        'steps': 1000,
    })

    methods = [without_lock, pessimistic_lock, optimistic_lock]
   
    processes = []
    for method in methods:
        print(f'test: {method.__name__}')
        hz, map = get_hz_map()
        map.put(cfg.key, 0)

        processes = []
        time_begin = time()
        for idx in range(cfg.num_clients):
            p = Process(target=perfrom_loop, args=(method, cfg))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        print(f'Time taken: {time() - time_begin:.3f}')
        print(f'resulted value {map.get(cfg.key)}\n{"#"*39}\n')
        hz.shutdown()
