from flask import Flask, request
import time
import threading
import grequests
import logging
import sys

from block import Block, build_block_from_json
from node import Node

BLOCK_GENERATOR_DELAY = 0.2
START_PORT = 5000
NODES_COUNT = 3


class Server:
    def __init__(self, node: Node):
        self.host = 'localhost'
        self.urls = [f'http://{self.host}:{START_PORT + offset}/' for offset in range(NODES_COUNT)]
        self.current_port = START_PORT + node.node_id - 1
        self.node: Node = node

        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        logging.getLogger('werkzeug').disabled = True
        logging.getLogger('urllib3.connectionpool').disabled = True
        self.logger = logging.getLogger(f"NODE_{node.node_id}")

    def send_block(self, block: Block):
        async_requests = (grequests.post(url, json=block.as_json) for url in self.urls)
        grequests.map(async_requests)

    def blocks_generator(self):
        while True:
            new_block = self.node.generate_next_block()
            if new_block is not None and new_block.index > self.node.block_index:
                self.send_block(new_block)
            time.sleep(BLOCK_GENERATOR_DELAY)

    def start(self):
        server = Flask(__name__)

        @server.route("/", methods=['POST'])
        def server_handler():
            block = build_block_from_json(request.get_json())
            self.logger.debug(f"Received block from Node[{block.node_id}]: index = {block.index}")

            block_handled = self.node.handle_block(block)
            msg = f"{'Append' if block_handled else 'Ignored'} block from Node[{block.node_id}]: index = {block.index}"
            self.logger.debug(msg)

            if block_handled:
                self.logger.debug(str(block))
            return msg

        server_thread = threading.Thread(target=server.run, args=(self.host, self.current_port), daemon=False)
        blocks_generator_thread = threading.Thread(target=self.blocks_generator, daemon=False)

        server_thread.start()
        blocks_generator_thread.start()
