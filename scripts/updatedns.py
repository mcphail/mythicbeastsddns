#! /usr/bin/python3

import os
import configparser
import urllib3

CONFIG_FILE=os.environ['SNAP_DATA'] + '/config'
config = configparser.ConfigParser()
config.read(CONFIG_FILE)
http = urllib3.PoolManager()

try:
    config.getboolean('User', 'updateipv4')
    if config['User']['domain'] == '' or config['User']['password'] == '' or config['User']['ipv4hostname'] == '':
        raise ValueError
except ValueError:
    config['User']['updateipv4'] = 'false'

try:
    config.getboolean('User', 'updateipv6')
    if config['User']['domain'] == '' or config['User']['password'] == '' or config['User']['ipv6hostname'] == '':
        raise ValueError
except ValueError:
    config['User']['updateipv6'] = 'false'

if config.getboolean('User', 'updateipv4') == True:
    value = { 'domain' : config['User']['domain'],
            'password' : config['User']['password'],
            'command' : 'REPLACE ' + config['User']['ipv4hostname'] + ' 5 A DYNAMIC_IP' }
    try:
        http.request('GET', 'https://dnsapi4.mythic-beasts.com', fields=value)
    except Exception:
        pass

if config.getboolean('User', 'updateipv6') == True:
    value = { 'domain' : config['User']['domain'],
            'password' : config['User']['password'],
            'command' : 'REPLACE ' + config['User']['ipv6hostname'] + ' 5 AAAA DYNAMIC_IP' }
    try:
        http.request('GET', 'https://dnsapi6.mythic-beasts.com', fields=value)
    except Exception:
        pass
