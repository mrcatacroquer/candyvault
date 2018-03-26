import sys
import socket
import ntplib
import time
import requests

def add_reward():
    s = get_api_session()
    reward_data = dict(rewardowner='xxyy@yahoo.es')
    r = s.post('http://candyvault:5000/addreward', data=reward_data)
    return r


def get_api_session():
    s = requests.session()
    login_data = dict(loginemail='xxyy@gmail.com', loginpassword='123456')
    s.post('http://candyvault:5000/httplogin', data=login_data)
    return s

print str(add_reward())