#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        plcSimulator.py
#
# Purpose:     A simple plc simulation module to connect and control the real-world 
#              emulator via UDP (to simulate the eletrical signal change) and reply
#              SCADA system with Modbus TCP.
# 
# Author:      Yuancheng Liu
#
# Version:     v0.1
# Created:     2023/05/29
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

import os
import time
import json
from datetime import datetime

import plcSimGlobal as gv
import Log
import udpCom

# Define all the module local untility functions here:
#-----------------------------------------------------------------------------
def parseIncomeMsg(msg):
    """ parse the income message to tuple with 3 element: request key, type and jsonString
        Args: msg (str): example: 'GET;dataType;{"user":"<username>"}'
    """
    req = msg.decode('UTF-8') if not isinstance(msg, str) else msg
    reqKey = reqType = reqJsonStr= None
    try:
        reqKey, reqType, reqJsonStr = req.split(';', 2)
    except Exception as err:
        Log.error('parseIncomeMsg(): The income message format is incorrect.')
        Log.exception(err)
    return (reqKey.strip(), reqType.strip(), reqJsonStr)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class plcAgent(object):
    """ Map manager to init/control differet elements state on the map."""
    def __init__(self, parent, plcID, realworldIP):
        self.parent = parent
        self.id = plcID
        self.realworld = realworldIP
        self.realwordInfo= {
            'ip': realworldIP[0],
            'port': realworldIP[1]
        }
        self.rwConnector = udpCom.udpClient((self.realwordInfo['ip'], self.realwordInfo['port']))
        if self._loginRealWord():
            gv.gDebugPrint('Login the realworld successfully', logType=gv.LOG_INFO)
        else:
            gv.gDebugPrint('Cannot connect to the realworld emulator', logType=gv.LOG_INFO)
        self.terminate = False

    def _initLadderLogic(self):
        """ This is a temp test function, the ladder diagram logic will be replaced by real ladder 
            config file.
        """
        



#-----------------------------------------------------------------------------
    def _loginRealWord(self):
        """ Try to connect to the realworld emulator."""
        gv.gDebugPrint("Try to connnect to the  [%s]..." %str(self.realworld), logType=gv.LOG_INFO)
        rqstKey = 'GET'
        rqstType = 'login'
        rqstDict = {'plcID': self.id}
        result = self._queryToRW(rqstKey, rqstType, rqstDict)
        if result:
            gv.gDebugPrint("Scheduler online, state: ready", logType=gv.LOG_INFO)
            return True
        return False

#-----------------------------------------------------------------------------
    def _queryToRW(self, rqstKey, rqstType, rqstDict, response=True):
        """ Query message to realword emulator
            Args:
                rqstKey (str): request key (GET/POST/REP)
                rqstType (_type_): request type string.
                rqstDict (_type_): request detail dictionary.
                dataOnly (bool, optional): flag to indentify whether only return the 
                    data. Defaults to True. return (responseKey, responseType, responseJson) if set
                    to False.
        Returns:
            _type_: refer to <dataOnly> flag's explaination.
        """
        k = t = result = None
        if rqstKey and rqstType and rqstDict:
            rqst = ';'.join((rqstKey, rqstType, json.dumps(rqstDict)))
            if self.rwConnector:
                resp = self.rwConnector.sendMsg(rqst, resp=True)
                if resp:
                    k, t, data = parseIncomeMsg(resp)
                    if k != 'REP': gv.gDebugPrint('The msg reply key %s is invalid' % k, logType=gv.LOG_WARN)
                    if t != rqstType: gv.gDebugPrint('The reply type doesnt match.%s' %str((rqstType, t)), logType=gv.LOG_WARN)
                    try:
                        result = json.loads(data)
                        self.lastUpdateT = datetime.now()
                    except Exception as err:
                        Log.exception('Exception: %s' %str(err))
                        return None
                else:
                    return None
        else:
            Log.error("queryBE: input missing: %s" %str(rqstKey, rqstType, rqstDict))
        return (k, t, result)

#-----------------------------------------------------------------------------
    def getSensorsInfo(self):
        rqstKey = 'GET'
        rqstType = 'sensors'
        rqstDict = {'weline': None,
                    'nsline': None,
                    'ccline': None}
        result = self._queryToRW(rqstKey, rqstType, rqstDict)
        return result



#-----------------------------------------------------------------------------
    def periodic(self, now):
        result = self.getSensorsInfo()
        print(result[2])

#-----------------------------------------------------------------------------
    def run(self):
        while not self.terminate:
            now = time.time()
            self.periodic(now)
            time.sleep(gv.gInterval)

#-----------------------------------------------------------------------------
    def stop(self):
        self.terminate = True

def main():
    plc = plcAgent(None, 'plc1', gv.gRealWordIP)
    plc.run()

if __name__ == "__main__":
    main()
