import argparse
from server import Server
from node import Node
from gevent import monkey

monkey.patch_all()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('node_id', nargs='?')
    node_id = int(parser.parse_args().node_id)

    node = Node(node_id)
    server = Server(node)
    server.start()


if __name__ == '__main__':
    main()
