import argparse

from . import __version__
from .server import Server

def main():
    parser = argparse.ArgumentParser(description='Proxy for python logging UDP/TCP to logstash/redis', version=__version__)
    parser.add_argument('--bind-ip', metavar='IP', help='IP address to listen on', default='127.0.0.1')
    parser.add_argument('--tcp-port', metavar='PORT', help='TCP port to listen on', default=9020, type=int)
    parser.add_argument('--udp-port', metavar='PORT', help='UDP port to listen on', default=9021, type=int)
    parser.add_argument('--redis-host', metavar='HOST', help='IP address of the redis server', default='localhost')
    parser.add_argument('--redis-port', metavar='PORT', help='Port number of the redis server', default=6379, type=int)
    parser.add_argument('--redis-queue', metavar='NAME', help='Name of the queue on the redis server', default='logstash')
    parser.add_argument('--message-type', metavar='TYPE', help='Type in the event message', default='pystash')
    parser.add_argument('--fqdn', action='store_true', help='Use the fully qualified domain name')
    parser.add_argument('--logstash-version', metavar='VERSION', help='Version of logstash event message', default=1, type=int)
    parser.add_argument('--logstash-tags', metavar='TAG1 TAG2', help='Tags for the logstash event message', nargs='+')
    args = parser.parse_args()
    Server(bind_ip=args.bind_ip, tcp_port=args.tcp_port, udp_port=args.udp_port, \
               redis_host=args.redis_host, redis_port=args.redis_port, redis_queue=args.redis_queue, \
               message_type=args.message_type, fqdn=args.fqdn, logstash_version=args.logstash_version, \
               logstash_tags=args.logstash_tags).start()
