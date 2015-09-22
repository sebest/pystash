===============================
pystash
===============================

A proxy for python logging UDP/TCP to logstash/redis

* Free software: BSD license

You can use PyStash in 2 ways:
1/ using the PyStash as a proxy server
2/ using the pystash.handlers as a library for python logging

The big picture of use case 1 is:

Your Python app -- TCP or UDP --> PyStash --  TCP --> Redis -- TCP --> LogStash

So as you can see PyStash does not use the TCP handler of logstash but
use the redis input plugin, the reason is that the TCP handler of
logstash does not have a queuing mechanism, thats's why the logstash
team recommend using redis.

The advantage to use UDP with PyStash is that UDP is not blocking so
it won't impact your Python App but you can loose some logs is PyStash
is stopped.

So i recommend using UDP is your logs are not criticals.

I also recommend to install PyStash on the same servers as you Python
app, so you log on localhost and PyStash proxy your logs to Redis

You need to have logstash with the redis input plugin for handling the
queuing, which is the recommended setup for logstash.

The configuration on logstash is:
input {
    redis {
        codec => json {
            charset => "UTF-8"
        }
        data_type => "list"
        key => "logstash"
        threads => 12
    }
}

for information about the redis input plugin:
http://logstash.net/docs/1.3.2/inputs/redis

For the usecase 2, using pystash as a library:
you can import le logging handlers from
 - pystash.handlers
 - you have LogstashTCPHandler, LogstashUDPHandler and RedisHandler
These handlers support the logstsh input plugin, tcp, udp and redis.
The pystash proxy internally use the RedisHandler

You have an example usage at the end of the file pystash/handlers.py

In this use case the big picture is:
Python App -- UDP or TCP -->  Logstash
or
Python App -- TCP --> Redis -- TCP --> Logstash

About the logstash configuration the default UDP or TCP configuration
should work.
The handlers in pystash have the correct python logging formatter to
generate the messages that Logstash expect.

The formatter is in pystash/formatter.py and is a classic python
logging formatter.
