from block import GENESIS_INDEX, build_new_block, Block


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

    def handle_block(self, block: Block):
        """Handler of received block."""
        if block.index == GENESIS_INDEX:
            self.blocks_array.append(block)
            self.block_index = 0
            return True

        if not self.blocks_array:
            return False

        last_block = self.blocks_array[-1]
        if block.index > last_block.index:
            self.blocks_array.append(block)
            self.block_index = block.index
            return True

        return False

    def generate_next_block(self):
        """Generates next block."""
        new_block = None
        if self.blocks_array:
            last_block = self.blocks_array[-1]
            new_block = build_new_block(
                index=self.block_index + 1,
                prev_hash=last_block.hash,
                nonce_type=self.node_id,
                node_id=self.node_id
            )
        return new_block
