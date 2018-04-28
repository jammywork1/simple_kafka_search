#!/usr/bin/python3
# -*- coding: utf-8 -*-

from optparse import OptionParser
from datetime import datetime
from pprint import pprint
import json
from socket import gethostname
from confluent_kafka import Consumer, KafkaError, TopicPartition, OFFSET_BEGINNING, TIMESTAMP_NOT_AVAILABLE 


def _bytes2string(msg):
    return msg.decode('utf-8')

def _json2dict_deserialize(json_str):
    return json.loads(json_str)

def _json_pprint(dct):
    p_json = json.dumps(dct, indent=4, sort_keys=True, ensure_ascii=False)
    print(p_json)

def main(options):
    if options.hostname:
        hostname = options.hostname
    else:
        hostname = gethostname()
    group_id = f'python_search@{hostname}'
    print(f'group_id = {group_id}')
    c = Consumer({
        'bootstrap.servers': options.bootstrap_servers,
        'group.id': group_id,
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
        message_string = _bytes2string(msg.value())
        try:
            message = _json2dict_deserialize(message_string)
        except json.decoder.JSONDecodeError:
            if options.show_warnings:
                print('-> offset {0} : deserialize error'.format(offset)) 
        else:
            ts_type, ts_ms_value = msg.timestamp()
            if ts_type != TIMESTAMP_NOT_AVAILABLE and ts_ms_value:
                ts_value = int(ts_ms_value / 1000)
                recieved = datetime.fromtimestamp(ts_value)
            else:
                recieved = None
            try:
                criteria = eval(options.filter)
            except (KeyError, TypeError) as e:
                criteria = False
                if options.show_warnings:
                    print(f'-> offset {offset} : {e}')
            if criteria == True:
                if recieved:
                    print(f'-> offset {offset}, recieved {recieved:%d-%m-%Y %H:%M:%S}')
                else:
                    print(f'-> offset {offset}')
                _json_pprint(message)
                # pprint(message)
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
parser.add_option("-H", "--hostname")

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

