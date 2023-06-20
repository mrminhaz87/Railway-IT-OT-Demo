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
# Version:     v0.2
# Created:     2023/05/29
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

import os
import time
import json
import threading
from datetime import datetime
from collections import OrderedDict

import plcSimGlobal as gv
import Log
import udpCom
import modbusTcpCom

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

class tFlipFlopLadderLogic(modbusTcpCom.ladderLogic):

    def __init__(self, parent) -> None:
        super().__init__(parent)

    def initLadderInfo(self):
        self.holdingRegsInfo['address'] = 0
        self.holdingRegsInfo['offset'] = 39
        self.srcCoilsInfo['address'] = 0
        self.srcCoilsInfo['offset'] = 19
        self.destCoilsInfo['address'] = 0
        self.destCoilsInfo['offset'] = 19

        # Init the flipflop coils and register config:
        weIdxOffSet, nsIdxOffset, ccIdxOffset = 0, 17, 25

        self.ffConfig = [
            # Init all the weline signals flipflop:
            {'coilIdx': 0, 'onRegIdx':(ccIdxOffset+12,), 'offRegIdx':(ccIdxOffset+13,)},
            {'coilIdx': 1, 'onRegIdx':(ccIdxOffset+12,), 'offRegIdx':(ccIdxOffset+13,)},
            {'coilIdx': 2, 'onRegIdx':(ccIdxOffset+10,), 'offRegIdx':(ccIdxOffset+11,)},
            {'coilIdx': 3, 'onRegIdx':(ccIdxOffset+10,), 'offRegIdx':(ccIdxOffset+11,)},
            {'coilIdx': 4, 'onRegIdx':(ccIdxOffset+8,), 'offRegIdx':(ccIdxOffset+9,)},
            {'coilIdx': 5, 'onRegIdx':(ccIdxOffset+8,), 'offRegIdx':(ccIdxOffset+9,)},
            {'coilIdx': 6, 'onRegIdx':(ccIdxOffset+6,), 'offRegIdx':(ccIdxOffset+7,)},
            {'coilIdx': 7, 'onRegIdx':(ccIdxOffset+6,), 'offRegIdx':(ccIdxOffset+7,)},
            # Init all the nsline signals flipflop:
            {'coilIdx': 8, 'onRegIdx':(ccIdxOffset+0,), 'offRegIdx':(ccIdxOffset+1,)},
            {'coilIdx': 9, 'onRegIdx':(ccIdxOffset+0,), 'offRegIdx':(ccIdxOffset+1,)},
            {'coilIdx': 10, 'onRegIdx':(ccIdxOffset+2,), 'offRegIdx':(ccIdxOffset+3,)},
            {'coilIdx': 11, 'onRegIdx':(ccIdxOffset+4,), 'offRegIdx':(ccIdxOffset+5,)},
            # Init all the ccline signal flipflop:
            {'coilIdx': 12, 'onRegIdx': (nsIdxOffset+0, nsIdxOffset+6), 'offRegIdx': (nsIdxOffset+1, nsIdxOffset+7)},
            {'coilIdx': 13, 'onRegIdx': (nsIdxOffset+4,), 'offRegIdx': (nsIdxOffset+5,)},
            {'coilIdx': 14, 'onRegIdx': (nsIdxOffset+2,), 'offRegIdx': (nsIdxOffset+3,)},
            {'coilIdx': 15, 'onRegIdx': (weIdxOffSet+7, weIdxOffSet+9), 'offRegIdx': (weIdxOffSet+8, weIdxOffSet+10)},
            {'coilIdx': 16, 'onRegIdx': (weIdxOffSet+5, weIdxOffSet+11), 'offRegIdx': (weIdxOffSet+6, weIdxOffSet+12)},
            {'coilIdx': 17, 'onRegIdx': (weIdxOffSet+3, weIdxOffSet+13), 'offRegIdx': (weIdxOffSet+4, weIdxOffSet+14)},
            {'coilIdx': 18, 'onRegIdx': (weIdxOffSet+1, weIdxOffSet+15), 'offRegIdx': (weIdxOffSet+2, weIdxOffSet+16)}
        ]

#-----------------------------------------------------------------------------
    def _tfligFlogRun(self, coilState, toggleOnList, toggleOffList):
        """ function to simulate a normal t-flip-flop latching replay.
            Args:
                coilState (_type_): Current output State
                toggleOnList (_type_): input 
                toggleOffList (_type_): _description_

            Returns:
                _type_: _description_
        """
        if coilState:
            for regs in toggleOffList:
                if regs: return False 
        else:
            for regs in toggleOnList:
                if regs: return True
        return coilState

#-----------------------------------------------------------------------------
    def runLadderLogic(self, regsList, coilList=None):
        coilsRsl = []
        if len(regsList) != 39 or coilList is None or len(coilList)!=19:
            print('runLadderLogic(): input not valid')
            print(regsList)
            print(coilList)
        else:
            for item in self.ffConfig:
               coilState = coilList[item['coilIdx']]
               onRegListState = [regsList[i] for i in item['onRegIdx']]
               offRegListState = [regsList[i] for i in item['offRegIdx']]
               coilsRsl.append(self._tfligFlogRun(coilState, onRegListState, offRegListState) ) 
        gv.gDebugPrint('Finished calculate all coils: %s' %str(coilsRsl), logType=gv.LOG_INFO)
        return coilsRsl
        
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class modBusService(threading.Thread):

    def __init__(self, parent, threadID, name):
        threading.Thread.__init__(self)
        hostIp = 'localhost'
        hostPort = 502
        self.dataMgr = modbusTcpCom.plcDataHandler(allowRipList=gv.ALLOW_R_L, allowWipList=gv.ALLOW_W_L)
        self.server = modbusTcpCom.modbusTcpServer(hostIp=hostIp, hostPort=hostPort, dataHandler=self.dataMgr)
        serverInfo = self.server.getServerInfo()
        self.dataMgr.initServerInfo(serverInfo)
        self.dataMgr.addLadderLogic('T_flipflop_logic_set', gv.iLadderLogic)
        self.dataMgr.setAutoUpdate(True)
        gv.iMBhandler = self.dataMgr
        self.daemon = True

    def run(self):
        """ Start the udp server's main message handling loop."""
        print("ModbusTCP service thread run() start.")
        self.server.startServer()
        print("Server thread run() end.")
        self.threadName = None # set the thread name to None when finished.

    def stop(self):
        self.server.stopServer()

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
        #self.ladderDict = OrderedDict()
        self.LadderPiority = {
            'weline': ('ccline',),
            'nsline': ('ccline',),
            'ccline': ('weline', 'nsline')
        }
        # self._initLadderLogic()
        gv.iLadderLogic = tFlipFlopLadderLogic(self)

        self.realwordInfo= {
            'ip': realworldIP[0],
            'port': realworldIP[1]
        }
        self.rwConnector = udpCom.udpClient((self.realwordInfo['ip'], self.realwordInfo['port']))

        self.recoonectCount = 30
        self.realwordOnline = self._loginRealWord()
        
        if self.realwordOnline:
            gv.gDebugPrint('Login the realworld successfully', logType=gv.LOG_INFO)
        else:
            gv.gDebugPrint('Cannot connect to the realworld emulator', logType=gv.LOG_INFO)
        
        # create the local modbus TCP server
        gv.iMBservice = modBusService(self, 1, 'ModbusService')
        gv.iMBservice.start()

        self.terminate = False

#-----------------------------------------------------------------------------
    def _initLadderLogic(self):
        """ This is a temp test function to implement the ladder logic of PLC, the ladder diagram 
            logic will be replaced by real ladder config file.
        """
        self.ladderDict['weline'] = [
            {'id': 'we-0', 'tiggerS': 'ccline', 'onIdx':(12,), 'offIdx':(13,) }, 
            {'id': 'we-1', 'tiggerS': 'ccline', 'onIdx':(12,), 'offIdx':(13,) },
            {'id': 'we-2', 'tiggerS': 'ccline', 'onIdx':(10,), 'offIdx':(11,) },
            {'id': 'we-3', 'tiggerS': 'ccline', 'onIdx':(10,), 'offIdx':(11,) },
            {'id': 'we-4', 'tiggerS': 'ccline', 'onIdx':(8,), 'offIdx':(9,) },
            {'id': 'we-5', 'tiggerS': 'ccline', 'onIdx':(8,), 'offIdx':(9,) },
            {'id': 'we-6', 'tiggerS': 'ccline', 'onIdx':(6,), 'offIdx':(7,) },
            {'id': 'we-7', 'tiggerS': 'ccline', 'onIdx':(6,), 'offIdx':(7,) }
        ]

        self.ladderDict['nsline'] = [
            {'id': 'ns-0', 'tiggerS': 'ccline', 'onIdx':(0,), 'offIdx':(1,) },
            {'id': 'ns-1', 'tiggerS': 'ccline', 'onIdx':(0,), 'offIdx':(1,) },
            {'id': 'ns-2', 'tiggerS': 'ccline', 'onIdx':(2,), 'offIdx':(3,) },
            {'id': 'ns-3', 'tiggerS': 'ccline', 'onIdx':(4,), 'offIdx':(5,) }
        ]

        self.ladderDict['ccline'] = [
            {'id': 'cc-0', 'tiggerS': 'nsline', 'onIdx':(0, 6), 'offIdx':(1, 7) },
            {'id': 'cc-1', 'tiggerS': 'nsline', 'onIdx':(4,), 'offIdx':(5,) },
            {'id': 'cc-2', 'tiggerS': 'nsline', 'onIdx':(2,), 'offIdx':(3,) },
            {'id': 'cc-3', 'tiggerS': 'weline', 'onIdx':(7,9), 'offIdx':(8,10) },
            {'id': 'cc-4', 'tiggerS': 'weline', 'onIdx':(5,11), 'offIdx':(6,12) },
            {'id': 'cc-5', 'tiggerS': 'weline', 'onIdx':(3,13), 'offIdx':(4,14) },
            {'id': 'cc-6', 'tiggerS': 'weline', 'onIdx':(1, 15), 'offIdx':(2,16) }
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
        (_, _, result) = self.getSensorsInfo()
        time.sleep(0.1)
        for key in result.keys():
            self.inputState[key] = result[key]
        # Update PLC holding registers.
        self.updateHoldingRegs()
        time.sleep(0.1)
        self.updateCoilOutput()
        # update the modbus data
        # self.updateModBusInfo()
        rst = self.changeSignalCoil()
        #print(rst)

    def updateHoldingRegs(self):
        checkSeq = ('weline', 'nsline', 'ccline')
        holdingRegs = []
        for key in checkSeq:
            holdingRegs += self.inputState[key]
        gv.gDebugPrint("updateModBusInfo(): update holding registers: %s" %str(holdingRegs), logType=gv.LOG_INFO)
        gv.iMBhandler.updateHoldingRegs(0, holdingRegs)


    def updateCoilOutput(self):
        result = gv.iMBhandler.getCoilState(0, 19)
        self.coilState['weline'] = result[0:8]
        self.coilState['nsline'] = result[8:12]
        self.coilState['nsline'] = result[12:19]

#-----------------------------------------------------------------------------
    def updateCoilOutput_old(self):
        """ update the coil output based in the input and ladder logic
        """
        for key in self.ladderDict.keys():
            for i, ladder in enumerate(self.ladderDict[key]):
                sensorTp = ladder['tiggerS']
                triggerOnSensorIdx = ladder['onIdx']
                triggerOffSensorIdx = ladder['offIdx']
                # check signal 'On' state:
                if self.coilState[key][i]:
                    for idx in triggerOffSensorIdx:
                        try:
                            if self.inputState[sensorTp][idx]:
                                self.coilState[key][i] = 0
                                break
                        except:
                            gv.gDebugPrint(str(sensorTp)+str(idx), logType=gv.LOG_ERR)
                else:
                    for idx in triggerOnSensorIdx:
                        try:
                            if self.inputState[sensorTp][idx]:
                                self.coilState[key][i] = 1
                                break
                        except:
                            gv.gDebugPrint(str(sensorTp)+str(idx), logType=gv.LOG_ERR)

#-----------------------------------------------------------------------------
    def updateModBusInfo(self):
        checkSeq = ('weline', 'nsline', 'ccline')
        holdingRegs = []
        coils = []
        for key in checkSeq:
            holdingRegs += self.inputState[key]
            coils += self.coilState[key]
        gv.gDebugPrint("updateModBusInfo(): update holding registers: %s" %str(holdingRegs), logType=gv.LOG_INFO)
        gv.iMBhandler.updateHoldingRegs(0, holdingRegs)

        gv.gDebugPrint("updateModBusInfo(): update coils: %s" %str(coils), logType=gv.LOG_INFO)
        gv.iMBhandler.updateOutPutCoils(0, coils)


#-----------------------------------------------------------------------------
    def run(self):
        while not self.terminate:
            now = time.time()
            if self.realwordOnline:
                self.periodic(now)
            else:
                self.recoonectCount -=1
                if self.recoonectCount == 0:
                    gv.gDebugPrint('Try to reconnect to the realword.', logType=gv.LOG_INFO)
                    self.realwordOnline = self._loginRealWord()
                    if not self.realwordOnline: self.recoonectCount = 30
            time.sleep(gv.gInterval)

#-----------------------------------------------------------------------------
    def stop(self):
        self.terminate = True

def main():
    plc = plcAgent(None, 'plc1', gv.gRealWordIP)
    plc.run()

if __name__ == "__main__":
    main()
