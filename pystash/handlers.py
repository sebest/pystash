import redis
from logging import Handler
from logging.handlers import DatagramHandler, SocketHandler
from . import formatter


class LogstashTCPHandler(SocketHandler):

    def __init__(self, host, port=5959, message_type='logstash', fqdn=False, version=1):
        SocketHandler.__init__(self, host, port)
        if version == 1:
            self.formatter = formatter.LogstashFormatterVersion1(message_type, [], fqdn)
        else:
            self.formatter = formatter.LogstashFormatterVersion0(message_type, [], fqdn)

    def makePickle(self, record):
        return self.formatter.format(record)


class LogstashUDPHandler(DatagramHandler):

    def __init__(self, host, port=5959, message_type='logstash', fqdn=False, version=1):
        DatagramHandler.__init__(self, host, port)
        if version == 1:
            self.formatter = formatter.LogstashFormatterVersion1(message_type, [], fqdn)
        else:
            self.formatter = formatter.LogstashFormatterVersion0(message_type, [], fqdn)

    def makePickle(self, record):
        return self.formatter.format(record)


class RedisHandler(Handler):

    def __init__(self, host='localhost', port=6379, db=0, key='logstash'):
        Handler.__init__(self)
        self._key = key
        self.r_server = redis.Redis(host)
        if version == 1:
            self.formatter = formatter.LogstashFormatterVersion1(message_type, [], fqdn)
        else:
            self.formatter = formatter.LogstashFormatterVersion0(message_type, [], fqdn)

    def emit(self, record):
        try:
            self.r_server.rpush(self._key, self.formatter.format(record))
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


if __name__ == '__main__':
    import logging

    lsip = '127.0.0.1'
    
    logger = logging.getLogger()
    handler_tcp = LogstashTCPHandler(lsip, 9020)
    handler_udp = LogstashUDPHandler(lsip, 9021)
    handler_redis = RedisHandler(host=lsip)
    
    logger.addHandler(handler_tcp)
    logger.addHandler(handler_udp)
    logger.addHandler(handler_redis)

    logger.error('hello carlos')
