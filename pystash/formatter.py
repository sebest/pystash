# https://github.com/vklochan/python-logstash/blob/master/logstash/formatter.py
import traceback
import logging
import socket
import sys
from datetime import datetime
try:
    import json
except ImportError:
    import simplejson as json


class LogstashFormatterBase(logging.Formatter):
    def __init__(self, message_type='Logstash', tags=None, fqdn=False):
        self.message_type = message_type
        self.tags = tags if tags is not None else []
        self.extra_tags = []

        if fqdn:
            self.host = socket.getfqdn()
        else:
            self.host = socket.gethostname()

    def get_extra_fields(self, record):
        # The list contains all the attributes listed in
        # http://docs.python.org/library/logging.html#logrecord-attributes
        skip_list = [
            'asctime', 'created', 'exc_info', 'exc_text', 'filename', 'args',
            'funcName', 'id', 'levelname', 'levelno', 'lineno', 'module', 'msg',
            'msecs', 'msecs', 'message', 'name', 'pathname', 'process',
            'processName', 'relativeCreated', 'thread', 'threadName', 'extra']

        if sys.version_info < (3, 0):
            easy_types = (basestring, bool, dict, float, int, list, type(None))
        else:
            easy_types = (str, bool, dict, float, int, list, type(None))

        fields = {}

        if record.args:
            fields['msg'] = record.msg

        self.extra_tags = []
        for key, value in record.__dict__.items():
            if key not in skip_list:
                if key == 'tags' and isinstance(value, list):
                    self.extra_tags = value
                elif isinstance(value, easy_types):
                    fields[key] = value
                else:
                    fields[key] = repr(value)

        return fields

    def get_debug_fields(self, record):
        if record.exc_info:
            exc_info = self.format_exception(record.exc_info)
        else:
            exc_info = record.exc_text
        return {
            'exc_info': exc_info,
            'filename': record.filename,
            'lineno': record.lineno,
            }

    @classmethod
    def format_source(cls, message_type, host, path):
        return "%s://%s/%s" % (message_type, host, path)

    @classmethod
    def format_timestamp(cls, time):
        return datetime.utcfromtimestamp(time).isoformat() + 'Z'

    @classmethod
    def format_exception(cls, exc_info):
        return ''.join(traceback.format_exception(*exc_info)) if exc_info else ''

    @classmethod
    def serialize(cls, message):
        if sys.version_info < (3, 0):
            return json.dumps(message)
        else:
            return bytes(json.dumps(message), 'utf-8')

class LogstashFormatterVersion0(LogstashFormatterBase):
    version = 0

    def format(self, record):
        # Create message dict
        message = {
            '@timestamp': self.format_timestamp(record.created),
            '@message': record.getMessage(),
            '@source': self.format_source(self.message_type, self.host,
                                          record.pathname),
            '@source_host': self.host,
            '@source_path': record.pathname,
            '@tags': self.tags[:],
            '@type': self.message_type,
            '@fields': {
                'levelname': record.levelname,
                'logger': record.name,
            },
        }

        # Add extra fields
        message['@fields'].update(self.get_extra_fields(record))

        # Add extra tags
        if self.extra_tags:
            message['@tags'].extend(self.extra_tags)

        # If exception, add debug info
        if record.exc_info or record.exc_text:
            message['@fields'].update(self.get_debug_fields(record))

        return self.serialize(message)


class LogstashFormatterVersion1(LogstashFormatterBase):
    def format(self, record):
        # Create message dict
        message = {
            '@timestamp': self.format_timestamp(record.created),
            '@version': 1,
            'message': record.getMessage(),
            'host': self.host,
            'path': record.pathname,
            'tags': self.tags[:],
            'type': self.message_type,

            # Extra Fields
            'levelname': record.levelname,
            'logger': record.name,
        }

        # Add extra fields
        message.update(self.get_extra_fields(record))

        # Add extra tags
        if self.extra_tags:
            message['tags'].extend(self.extra_tags)

        # If exception, add debug info
        if record.exc_info or record.exc_text:
            message.update(self.get_debug_fields(record))

        return self.serialize(message)
