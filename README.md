# simple_kafka_search

python script for fast search messages from kafka.

You have variables for filter:
  - message - json deserialized message to python dict
  - offset - integer offset value 

## Options:
  - -h, --help                                                      
    show help message and exit
  
  - -s BOOTSTRAP_SERVERS --bootstrap_servers=BOOTSTRAP_SERVERS

  - -t TOPIC, --topic=TOPIC

  - -f FILTER, --filter=FILTER                                      
    set 'True' for output all messages

  - -n NUMBER, --number=NUMBER                                      
    limit on the number of output messages

  - -w SHOW_WARNINGS, --show_warnings=SHOW_WARNINGS                 
    't' or 'f', default = 'f'      

  - -H HOSTNAME, --hostname=HOSTNAME                                
    set the hostname for used one consumer group id in a docker, because hostname in a docker everybody random or used --network host


## usage

python3 main.py -s {kafka-ip:port} -t {topic-name} -f {filter}


docker run --rm -it jammywork1/simple_kafka_search -H \`hostname\` -s {kafka-ip:port} -t {topic-name} -f {filter}

## examples
python3 main.py -s localhost:9092 -t test -f 'message.get("b") == 2'

docker run --rm -it --network host jammywork1/simple_kafka_search -s localhost:9092 -t test -f 'message["b"] == 2'

docker run --rm -it jammywork1/simple_kafka_search  -H \`hostname\` -s localhost:9092 -t test -w t -f 'message["b"] == 2' 

docker run --rm -it jammywork1/simple_kafka_search  -H 'vasya01_pc' -s localhost:9092 -t test -n 10 -f 'message["b"] == 2' 


