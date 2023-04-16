from flask import Flask, request
import time
import threading
import logging
import grequests
from block import build_block, GENESIS_BLOCK, Block

BLOCK_GENERATOR_DELAY = 0.2


class Server:
    def __init__(self, current_node):
        self.node_id = current_node.node_id
        logging.getLogger('werkzeug').disabled = True

        node_id_to_ports = {
            1: (5000, 5001, 5002),
            2: (5001, 5000, 5002)
        }
        default_node_id_to_ports = (5002, 5000, 5001)
        ports = node_id_to_ports.get(self.node_id, default_node_id_to_ports)
        self.host = 'localhost'
        self.urls = (f'http://{self.host}:{port}/' for port in ports)
        self.current_port = ports[0]
        self.current_node = current_node

    def send_block(self, block: Block):
        async_requests = (grequests.post(url, json=block.as_json) for url in self.urls)
        grequests.map(async_requests)

    def blocks_generator(self):
        while True:
            if self.current_node.blocks_array:
                last_block = self.current_node.blocks_array[-1]

                new_block = build_block(
                    index=self.current_node.block_index + 1,
                    prev_hash=last_block.hash,
                    nonce_type=self.current_node.node_id,
                    node_id=self.node_id
                )
                if new_block.index > self.current_node.block_index:
                    self.send_block(new_block)

            time.sleep(BLOCK_GENERATOR_DELAY)

    def start(self):
        server = Flask(__name__)

        @server.route("/", methods=['POST'])
        def server_handler():
            received_block = request.get_json()
            block_handled = self.current_node.handle_block(received_block)
            return "Received new block" if block_handled else "Block Error"

        server = threading.Thread(target=server.run, args=(self.host, self.current_port))
        blocks_generator_thread = threading.Thread(target=self.blocks_generator)

        server.daemon = False
        blocks_generator_thread.daemon = False

        server.start()
        blocks_generator_thread.start()

        if self.node_id == 1:
            time.sleep(1)
            self.send_block(GENESIS_BLOCK)
