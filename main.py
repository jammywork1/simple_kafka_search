#!/usr/bin/python3
# -*- coding: utf-8 -*-

from optparse import OptionParser
from datetime import datetime
from pprint import pprint
import json
from socket import gethostname
from confluent_kafka import Consumer, KafkaError, TopicPartition, OFFSET_BEGINNING

def _bytes2dict_deserialize(msg):
    return json.loads(msg.decode('utf-8'))

def main(options):
    c = Consumer({
        'bootstrap.servers': options.bootstrap_servers,
        'group.id': 'python_search@{0}'.format(gethostname()),
    })
    
    tp = TopicPartition(options.topic, 0, 0) #OFFSET_BEGINNING)
    c.assign([tp])
    c.seek(tp) 


    printed = 0
    print('begin')
    while True:
        msg = c.poll()
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                break
            else:
                print(msg.error())
                return
        offset = msg.offset()
        try:
            message = _bytes2dict_deserialize(msg.value()) 
        except json.decoder.JSONDecodeError:
            if options.show_warnings:
                print('-> offset {0} : Json Deserialize Error'.format(offset)) 
        else:
            # ts_type, timestamp_value = msg.timestamp()
            # recieved = datetime.fromtimestamp(timestamp_value)
            try:
                criteria = eval(options.filter)
            except (KeyError, TypeError) as e:
                criteria = False
                if options.show_warnings:
                    print(f'-> offset {offset} : {e}')
            if criteria == True:
                # print('-> offset {0}, recieved {1:%d-%m-%Y %H:%M:%S}'.format(offset, recieved))
                print('-> offset {0}'.format(offset))
                pprint(message)
                printed += 1
                if options.number and printed >= options.number:
                    break
        print('{0}'.format(offset), end='\r')
    c.close()
    print('end             ')

parser = OptionParser()
parser.add_option("-s", "--bootstrap_servers")
parser.add_option("-t", "--topic")
parser.add_option("-f", "--filter")
parser.add_option("-w", "--show_warnings", default='f')
parser.add_option("-n", "--number", type="int")

(options, args) = parser.parse_args()

if not options.bootstrap_servers:
    parser.error("options bootstrap_servers cant be empty")
if not options.topic:
    parser.error("options topic cant be empty")
if not options.filter:
    parser.error("options filter cant be empty")
if options.show_warnings not in ('f', 't'):
    parser.error("options show_warnings maybe only 't' or 'f'")
if options.show_warnings == 'f':
    options.show_warnings = False
else:
    options.show_warnings = True
if __name__ == "__main__":
    main(options)

