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
import modbusTcpCom
count = 0 
hostIp = '127.0.0.1'
hostPort = 502

client = modbusTcpCom.modbusTcpClient(hostIp)
print('Try to connect to the target victim PLC: %s' %str(hostIp))
print('Start PLC read request thread')
print('Start pLC write request thread')
timeVal = time.time()
while not client.checkConn():
    count +=1
    print('Try connect to the PLC')
    reuslt = client.getCoilsBits(0, 4)
    if not reuslt: print("connection rejected")
    if count == 100:
        timeInt = time.time() - timeVal
        print("PLC request sending frequency: %s" %str(100/timeInt))
        timeVal = time.time()
