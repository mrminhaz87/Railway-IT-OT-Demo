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
        
        self.inputState = {
            'weline': [],
            'nsline': [],
            'ccline': [] }
        
        self.coilState = {
            'weline': [0, 0, 0, 0, 0, 0, 0, 0 ],
            'nsline': [0, 0, 0, 0],
            'ccline': [0, 0, 0, 0, 0, 0, 0]
        }
        # Init the ladder logic.
        self.ladderDict = {}
        self._initLadderLogic()
        
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

#-----------------------------------------------------------------------------
    def _initLadderLogic(self):
        """ This is a temp test function to implement the ladder logic of PLC, the ladder diagram 
            logic will be replaced by real ladder config file.
        """
        self.ladderDict['weline'] = [
            {'id': 'we-0', 'tiggerS': 'ccline', 'onIdx':(13,), 'offIdx':(12,) }, 
            {'id': 'we-1', 'tiggerS': 'ccline', 'onIdx':(13,), 'offIdx':(12,) },
            {'id': 'we-2', 'tiggerS': 'ccline', 'onIdx':(11,), 'offIdx':(10,) },
            {'id': 'we-3', 'tiggerS': 'ccline', 'onIdx':(11,), 'offIdx':(10,) },
            {'id': 'we-4', 'tiggerS': 'ccline', 'onIdx':(9,), 'offIdx':(8,) },
            {'id': 'we-5', 'tiggerS': 'ccline', 'onIdx':(9,), 'offIdx':(8,) },
            {'id': 'we-6', 'tiggerS': 'ccline', 'onIdx':(7,), 'offIdx':(6,) },
            {'id': 'we-7', 'tiggerS': 'ccline', 'onIdx':(7,), 'offIdx':(6,) }
        ]

        self.ladderDict['nsline'] = [
            {'id': 'ns-0', 'tiggerS': 'ccline', 'onIdx':(1,), 'offIdx':(0,) },
            {'id': 'ns-1', 'tiggerS': 'ccline', 'onIdx':(1,), 'offIdx':(0,) },
            {'id': 'ns-2', 'tiggerS': 'ccline', 'onIdx':(3,), 'offIdx':(2,) },
            {'id': 'ns-3', 'tiggerS': 'ccline', 'onIdx':(5,), 'offIdx':(4,) }
        ]

        self.ladderDict['ccline'] = [
            {'id': 'cc-0', 'tiggerS': 'nsline', 'onIdx':(1, 7), 'offIdx':(0, 6) },
            {'id': 'cc-1', 'tiggerS': 'nsline', 'onIdx':(5,), 'offIdx':(4,) },
            {'id': 'cc-2', 'tiggerS': 'nsline', 'onIdx':(3,), 'offIdx':(2,) },
            {'id': 'cc-3', 'tiggerS': 'weline', 'onIdx':(8,10), 'offIdx':(7,9) },
            {'id': 'cc-4', 'tiggerS': 'weline', 'onIdx':(6,12), 'offIdx':(5,11) },
            {'id': 'cc-5', 'tiggerS': 'weline', 'onIdx':(4,14), 'offIdx':(3,13) },
            {'id': 'cc-6', 'tiggerS': 'weline', 'onIdx':(2, 16), 'offIdx':(1,15) }
        ]

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
                resp = self.rwConnector.sendMsg(rqst, resp=response)
                if resp:
                    #gv.gDebugPrint('===> resp:%s' %str(resp), logType=gv.LOG_INFO)
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
    
    def changeSignalCoil(self):
        rqstKey = 'POST'
        rqstType = 'signals'
        rqstDict = self.coilState
        result = self._queryToRW(rqstKey, rqstType, rqstDict)
        return result
    
#-----------------------------------------------------------------------------
    def periodic(self, now):
        result = self.getSensorsInfo()
        time.sleep(0.1)
        for key in result[2].keys():
            self.inputState[key] = result[2][key]
        self.updateCoilOutput()
        rst = self.changeSignalCoil()
        print(rst)

#-----------------------------------------------------------------------------
    def updateCoilOutput(self):
        """ update the coil output based in the input and ladder logic
        """
        for key in self.ladderDict.keys():
            for i, ladder in enumerate(self.ladderDict[key]):
                sensorTp = ladder['tiggerS']
                triggerOnSensorIdx = ladder['onIdx']
                triggerOffSensorIdx = ladder['offIdx']
                # check signal 'On' state:
                if self.coilState[key][i]:
                    for idx in triggerOnSensorIdx:
                        try:
                            if self.inputState[sensorTp][idx]:
                                self.coilState[key][i] = 0
                                break
                        except:
                            gv.gDebugPrint(str(sensorTp)+str(idx), logType=gv.LOG_ERR)
                else:
                    for idx in triggerOffSensorIdx:
                        try:
                            if self.inputState[sensorTp][idx]:
                                self.coilState[key][i] = 1
                                break
                        except:
                            gv.gDebugPrint(str(sensorTp)+str(idx), logType=gv.LOG_ERR)

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
