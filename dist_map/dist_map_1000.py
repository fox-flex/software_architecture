from tqdm import tqdm
import hazelcast
# from hazelcast.client import HazelcastClient


if __name__ == "__main__":
    # Start the Hazelcast Client and connect to an already running Hazelcast Cluster on 127.0.0.1
    hz = hazelcast.HazelcastClient(cluster_name="dev")
    
    # Get the Distributed Map from Cluster.
    map = hz.get_map("tm").blocking()
    # Standard Put and Get
    for i in tqdm(range(1000)):
        map.put(i, str(i))
    
    # Shutdown this Hazelcast Client
    hz.shutdown()
