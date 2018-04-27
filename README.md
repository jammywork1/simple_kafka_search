# simple_kafka_search

python script for fast search messages from kafka.

You have variables for filter:
  - message - json deserialized message to python dict
  - offset - integer offset value 

## Options:
  - -h, --help                    show this help message and exit
  - -s BOOTSTRAP_SERVERS --bootstrap_servers=BOOTSTRAP_SERVERS
  - -t TOPIC, --topic=TOPIC
  - -f FILTER, --filter=FILTER
  - -n NUMBER, --number=NUMBER    limit on the number of output messages
  - -w SHOW_WARNINGS, --show_warnings=SHOW_WARNINGS

## usage

python3 main.py -s {kafka-ip:port} -t {topic-name} -f {filter}


docker run --rm -it jammywork1/simple_kafka_search -s {kafka-ip:port} -t {topic-name} -f {filter}

## examples
python3 main.py -s localhost:9092 -t test -f 'message.get("b") == 2'

docker run --rm -it --network host jammywork1/simple_kafka_search -s localhost:9092 -t test -f 'message["b"] == 2'


