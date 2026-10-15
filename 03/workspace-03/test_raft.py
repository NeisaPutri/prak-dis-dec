import time
import random
from raft import RaftNode, State

def simulate_raft():
    node_ids = [1, 2, 3]
    nodes = [RaftNode(i, node_ids) for i in node_ids]

    for step in range(20):
        time.sleep(0.5)
        print(f"\n--- Step {step + 1} ---")

        leaders = [n for n in nodes if n.state == State.LEADER]
        if leaders:
            leader = random.choice(leaders)
            for node in nodes:
                if node.id != leader.id:
                    node.on_heartbeat(leader.current_term)

            if step % 5 == 0:
                leader.append_entry(f"command-{step}")

        for node in nodes:
            node.tick()

        for node in nodes:
            print(f"Node {node.id}: {node.state.name} | Term {node.current_term} | Log len ({len(node.log)})")

if __name__ == "__main__":
    print("Simulating Raft Consensus for Drone Swarm Coordination\n")
    simulate_raft()