import json
from types import SimpleNamespace

from logger import LOGGER
from block import GENESIS_INDEX, block_to_string


class Node:
    """Node class.

    Attributes:
        node_id: ID of this node
        block_index: Index of last block
        blocks_array: Array of blocks contained in the node
    """

    def __init__(self, node_id):
        """Initializes the instance."""
        self.node_id = node_id
        self.block_index = None
        self.blocks_array = []

    def handle_block(self, received_block_json):
        """Handler of received block."""
        block = json.loads(received_block_json, object_hook=lambda d: SimpleNamespace(**d))
        if block.index == GENESIS_INDEX:
            self.blocks_array.append(block)
            self.block_index = 0
            LOGGER.debug(block_to_string(block))
            return True

        last_block = json.loads(self.blocks_array[-1], object_hook=lambda d: SimpleNamespace(**d))
        if block.index > last_block.index:
            self.blocks_array.append(block)
            self.block_index = block.index
            if self.node_id != block.node_id:
                LOGGER.debug(block_to_string(block))
            return True

        return False
