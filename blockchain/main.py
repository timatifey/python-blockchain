import argparse
import time

from block import GENESIS_BLOCK
from server import Server
from node import Node
from gevent import monkey


def main():
    monkey.patch_all()

    parser = argparse.ArgumentParser()
    parser.add_argument('node_id', nargs='?')
    node_id = int(parser.parse_args().node_id)

    node = Node(node_id)
    server = Server(node)
    server.start()

    if node_id == 1:
        time.sleep(3)
        server.send_block(GENESIS_BLOCK)


if __name__ == '__main__':
    main()
