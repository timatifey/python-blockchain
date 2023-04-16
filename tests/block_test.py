import json
import random

from blockchain.block import build_new_block, GENESIS_BLOCK


def test_block_init():
    for _ in range(10):
        block_index = random.randint(1, 100000)
        nonce_type = random.randint(1, 3)
        prev_hash = 'This is old TEST block'
        node_id = random.randint(1, 3)

        new_block = build_new_block(block_index, prev_hash, node_id, nonce_type)

        assert new_block is not None

        assert new_block.hash is not None
        assert new_block.data is not None
        assert new_block.index is not None
        assert new_block.node_id is not None
        assert new_block.prev_hash is not None
        assert new_block.nonce is not None


def test_generate_random_data():
    for _ in range(10):
        block_index = 1
        prev_hash = 'Old_data'
        nonce_type = 1
        node_id = 1
        current_block = build_new_block(block_index, prev_hash, node_id, nonce_type)

        old_value_data = current_block.data
        old_value_length = len(current_block.data)
        new_value_length = random.randint(0, 255)

        current_block.data = current_block.generate_random_string(new_value_length)

        assert type(current_block.data) == str
        assert old_value_length != len(current_block.data)
        assert old_value_data != current_block.data
        assert len(current_block.data) == new_value_length


def test_generate_hash():
    for _ in range(10):
        block_index = 1
        prev_hash = 'Old_Hash'
        nonce_type = 1
        node_id = 1
        current_block = build_new_block(block_index, prev_hash, node_id, nonce_type)

        assert type(current_block.hash) == str
        assert current_block.hash[-4:] == '0000'
        assert current_block.prev_hash == 'Old_Hash'


def test_block_to_json():
    for _ in range(10):
        block_index = random.randint(1, 100000)
        prev_hash = 'This is old Json block'
        nonce_type = random.randint(1, 3)
        node_id = random.randint(1, 3)

        new_block = build_new_block(block_index, prev_hash, node_id, nonce_type)

        json_block = new_block.as_json
        assert type(json_block) == str

        json_dict = json.loads(json_block)

        index = int(json_dict['index'])
        cur_hash = json_dict['hash']
        prev_hash = json_dict['prev_hash']
        data = json_dict['data']
        nonce = int(json_dict['nonce'])

        assert index == new_block.index
        assert cur_hash == new_block.hash
        assert prev_hash == new_block.prev_hash
        assert data == new_block.data
        assert nonce == new_block.nonce


def test_create_genesis():
    assert GENESIS_BLOCK is not None
    assert GENESIS_BLOCK.node_id == -1
    assert GENESIS_BLOCK.index == 0
    assert GENESIS_BLOCK.hash[-4:] == '0000'
    assert GENESIS_BLOCK.prev_hash == 'GENESIS'
    assert len(GENESIS_BLOCK.data) == 256
