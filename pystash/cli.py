import argparse

from . import __version__
from .server import Server

def main():
    parser = argparse.ArgumentParser(description='Proxy for python logging UDP/TCP to logstash/redis', version=__version__)
    parser.add_argument('--bind-ip', metavar='IP', help='IP address to listen on', default='0.0.0.0')
    parser.add_argument('--tcp-port', metavar='PORT', help='TCP port to listen on', default=9020, type=int)
    parser.add_argument('--udp-port', metavar='PORT', help='UDP port to listen on', default=9021, type=int)
    parser.add_argument('--redis-host', metavar='HOST', help='IP address of the redis server', default='localhost')
    parser.add_argument('--redis-port', metavar='PORT', help='Port number of the redis server', default=6379, type=int)
    parser.add_argument('--redis-queue', metavar='NAME', help='Name of the queue on the redis server', default='logstash')
    args = parser.parse_args()
    Server(bind_ip=args.bind_ip, tcp_port=args.tcp_port, udp_port=args.udp_port, \
               redis_host=args.redis_host, redis_port=args.redis_port, redis_queue=args.redis_queue).start()
