import redis
from logging import Formatter, Handler
from logging.handlers import DatagramHandler, SocketHandler


class LogstashTCPHandler(SocketHandler):

    def makePickle(self, record):
        return self.format(record)


class LogstashUDPHandler(DatagramHandler):

    def makePickle(self, record):
        return self.format(record)


class RedisHandler(Handler):

    def __init__(self, host='localhost', port=6379, db=0, data_type='list', key='logstash'):
        Handler.__init__(self)
        self._data_type = data_type
        self._key = key

        self.r_server = redis.Redis(host)
        self.formatter = Formatter("%(asctime)s - %(message)s")

    def emit(self, record):
        if self._data_type == 'list':
            try:
                self.r_server.rpush(self._key, self.format(record))
            except Exception, e:
                print e
