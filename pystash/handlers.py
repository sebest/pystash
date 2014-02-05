import redis
from logging import Handler
from logging.handlers import DatagramHandler, SocketHandler


class LogstashTCPHandler(SocketHandler):

    def makePickle(self, record):
        return self.format(record)


class LogstashUDPHandler(DatagramHandler):

    def makePickle(self, record):
        return self.format(record)


class RedisHandler(Handler):

    def __init__(self, host='localhost', port=6379, db=0, key='logstash'):
        Handler.__init__(self)
        self._key = key
        self.r_server = redis.Redis(host)

    def emit(self, record):
        try:
            self.r_server.rpush(self._key, self.format(record))
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


if __name__ == '__main__':
    import logging
    from .formatter import LogstashFormatter

    lsip = '127.0.0.1'
    
    logger = logging.getLogger()
    handler_tcp = LogstashTCPHandler(lsip, 9020)
    handler_udp = LogstashUDPHandler(lsip, 9021)
    handler_redis = RedisHandler(host=lsip)
    
    formatter = LogstashFormatter()
    
    handler_tcp.setFormatter(formatter)
    handler_udp.setFormatter(formatter)
    handler_redis.setFormatter(formatter)

    logger.addHandler(handler_tcp)
    logger.addHandler(handler_udp)
    logger.addHandler(handler_redis)

    logger.error('hello carlos')
