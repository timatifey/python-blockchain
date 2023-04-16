import random

from blockchain.block import GENESIS_BLOCK, build_new_block
from blockchain.node import Node


def test_node_init():
    for _ in range(10):
        node_id = random.randint(1, 3)
        new_node = Node(node_id)

        assert new_node is not None

        assert new_node.node_id == node_id
        assert new_node.block_index is None
        assert len(new_node.blocks_array) == 0


def test_block_handler_genesis():
    node_id = random.randint(1, 3)
    current_node = Node(node_id)
    genesis_block = GENESIS_BLOCK

    assert current_node.node_id == node_id
    assert current_node.block_index is None
    assert len(current_node.blocks_array) == 0

    current_node.handle_block(genesis_block)

    assert current_node.node_id == node_id
    assert current_node.block_index == 0
    assert len(current_node.blocks_array) == 1


def test_block_handler_not_genesis():
    node_id = random.randint(1, 3)
    current_node = Node(node_id)

    for _ in range(10):
        block_node_id = random.randint(1, 3)
        last_index = random.randint(1, 1000)
        prev_hash = 'This is Last block in Node'
        nonce_type = random.randint(1, 3)

        last_block = build_new_block(last_index, prev_hash, block_node_id, nonce_type)

        current_node.block_index = last_index
        current_node.blocks_array.append(last_block)

        answer_false = current_node.handle_block(last_block)
        assert answer_false is False

        array_length = len(current_node.blocks_array)

        new_index = random.randint(1, 1000)
        new_prev_hash = 'This is new Received block'
        received_block = build_new_block(new_index, new_prev_hash, block_node_id, nonce_type)

        block_handler_result = current_node.handle_block(received_block)

        if new_index > last_index:
            assert block_handler_result is True
            assert current_node.block_index == new_index
            assert len(current_node.blocks_array) == array_length + 1
        else:
            assert block_handler_result is False
            assert current_node.block_index == last_index
            assert len(current_node.blocks_array) == array_length
