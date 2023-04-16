import threading
import time

from blockchain.node import Node
from blockchain.server import Server
from blockchain.block import GENESIS_BLOCK


def test_server():
    node_id = 1
    node = Node(node_id)
    server = Server(node)

    new_server = threading.Thread(target=server.start, daemon=True)
    new_server.start()

    server.send_block(GENESIS_BLOCK)

    while node.block_index is None:
        time.sleep(0.1)

    assert len(node.blocks_array) == 1
    last_block = node.blocks_array[-1]

    assert last_block.prev_hash == 'GENESIS'
    assert last_block.index == 0


def test_valid_blockchain():
    block_count = 5
    nodes = [Node(node_id) for node_id in range(1, 3 + 1)]
    servers = [Server(node) for node in nodes]
    servers_threads = [threading.Thread(target=server.start, daemon=True) for server in servers]

    for server_thread in servers_threads:
        server_thread.start()

    servers[0].send_block(GENESIS_BLOCK)

    while any(len(node.blocks_array) < block_count for node in nodes):
        time.sleep(0.1)

    for i in range(block_count):
        blocks_from_nodes = [node.blocks_array[i] for node in nodes]
        for node_index in range(len(nodes) - 1):
            assert blocks_from_nodes[node_index] == blocks_from_nodes[node_index + 1]
