#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey; monkey.patch_all()

import cPickle
import struct
import redis
import logging
import logging.handlers
import gevent
from gevent.server import DatagramServer, StreamServer
from .formatter import LogstashFormatter

DEFAULT_UDP = logging.handlers.DEFAULT_UDP_LOGGING_PORT
DEFAULT_TCP = logging.handlers.DEFAULT_TCP_LOGGING_PORT

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Server(object):

    def __init__(self, bind_ip='0.0.0.0', tcp_port=DEFAULT_TCP, udp_port=DEFAULT_UDP, redis_host='localhost', redis_port=6379, redis_queue='logstash'):
        self.redis = redis.Redis(redis_host, redis_port)
        self.formatter = LogstashFormatter()
        self.udp_server = DatagramServer('%s:%s' % (bind_ip, udp_port), self.udp_handle)
        self.tcp_server = StreamServer('%s:%s' % (bind_ip, tcp_port), self.tcp_handle)
        logging.info('Listening on %s (udp=%s tcp=%s) sending to %s:%s.', bind_ip, udp_port, tcp_port, redis_host, redis_port)

    def obj_to_redis(self, obj):
        record = logging.makeLogRecord(obj)
        payload = self.formatter.format(record)
        self.redis.rpush(redis_queue, payload)

    def udp_handle(self, data, address):
        slen = struct.unpack('>L', data[:4])[0]
        obj = cPickle.loads(data[4:slen+4])
        self.obj_to_redis(obj)

    def tcp_handle(self, socket, address):
        fileobj = socket.makefile()
        while True:
            chunk = fileobj.read(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack(">L", chunk)[0]
            chunk = fileobj.read(slen)
            while len(chunk) < slen:
                chunk = chunk + fileobj.read(slen - len(chunk))
            fileobj.flush()
            obj = self.unPickle(chunk)
            self.obj_to_redis(obj)

    def start(self):
        self.udp_server.start()
        self.tcp_server.start()
        gevent.wait()
