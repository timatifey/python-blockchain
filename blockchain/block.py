from __future__ import annotations
import json
import random
import string
from hashlib import sha256


class Block:
    """Block of blockchain.

    Attributes:
        hash: Hash of the current block
        data: Data in the form of a string of 256 characters
        index: Ascending number of the current block
        node_id: Node ID
        prev_hash: Hash of the previous block
        nonce: Addition to fulfill the hashing requirement
    """

    def __init__(self, index, prev_hash, nonce_type, node_id):
        """Initializes the instance."""
        self.index = index
        self.prev_hash = prev_hash
        self.node_id = node_id
        self.nonce = 1

        self.data = self.generate_random_string(256)
        self.hash = self.generate_hash(nonce_type)

    def generate_hash(self, nonce_type):
        """Generating the current Hash taking into account that the last 4 characters == 0000."""
        current_encoded_hash = self.encoded_string_hash

        while not self.valid_hash(current_encoded_hash):
            self.update_nonce(nonce_type)
            current_encoded_hash = self.encoded_string_hash

        return current_encoded_hash.hexdigest()

    def update_nonce(self, nonce_type):
        """Update Addition to fulfill the hashing requirement."""
        nonce_additional = {
            1: random.randint(1, 10),
            2: random.randint(11, 20)
        }
        default_nonce_additional = random.randint(21, 30)
        self.nonce += nonce_additional.get(nonce_type, default_nonce_additional)

    @property
    def string_hash(self):
        return f'{self.index}{self.prev_hash}{self.data}{self.nonce}'

    @property
    def encoded_string_hash(self):
        return sha256(self.string_hash.encode('utf-8'))

    @property
    def as_json(self):
        json_dictionary = {
            'node': self.node_id,
            'index': self.index,
            'hash': self.hash,
            'prev_hash': self.prev_hash,
            'data': self.data,
            'nonce': self.nonce
        }
        return json.dumps(json_dictionary)

    @staticmethod
    def valid_hash(encoded_hash):
        return encoded_hash.hexdigest()[-4:] == '0000'

    @staticmethod
    def generate_random_string(length: int):
        """Generating a random string of input count characters."""
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for _ in range(length))
        return random_string


def build_block(index, prev_hash, nonce_type, node_id):
    """Build new block."""
    return Block(index, prev_hash, nonce_type, node_id)


GENESIS_BLOCK = build_block(index=0, prev_hash='GENESIS', nonce_type=1, node_id=-1)
