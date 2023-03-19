import hazelcast

def get_hz_q():
    hz = hazelcast.HazelcastClient(cluster_name='dev')
    queue = hz.get_queue('tiny_queue').blocking()
    return hz, queue
