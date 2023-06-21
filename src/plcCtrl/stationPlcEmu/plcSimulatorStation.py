#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        plcSimulatorStation.py
#
# Purpose:     A simple plc simulation module to connect and control the real-world 
#              emulator via UDP (to simulate the eletrical signals change) and handle
#              SCADA system Modbus TCP request.
# 
# Author:      Yuancheng Liu
#
# Version:     v0.2
# Created:     2023/05/29
# Copyright:   
# License:     
#-----------------------------------------------------------------------------
""" 
    Program design:
        We want to create a PLC simulator which can simulate a PLC set (Master[slot-0], 
        Slave[slot-1], Slave[slot-2]) with thress 16-in 8-out PLCs. The PLC sets will
        take 22 input signal and provide 22 output signal to implement the railway station
        control system.
"""

import os
import time
import json
import threading
from datetime import datetime
from collections import OrderedDict

import plcSimGlobalStation as gv
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
class directConnLadderLogic(modbusTcpCom.ladderLogic):
    """ A Direct connection ladder logic diagram set
    """
    def __init__(self, parent) -> None:
        super().__init__(parent)

    def initLadderInfo(self):
        self.holdingRegsInfo['address'] = 0
        self.holdingRegsInfo['offset'] = 22
        self.srcCoilsInfo['address'] = None
        self.srcCoilsInfo['offset'] = None
        self.destCoilsInfo['address'] = 0
        self.destCoilsInfo['offset'] = 22
        # Init the flipflop coils and registers config:
        # For total 39 holding registers connected addresses
        # address: 0 - 9: weline stations
        # address: 10 - 15: nsline stations
        # address: 16 - 21: ccline sensors.

#-----------------------------------------------------------------------------
    def runLadderLogic(self, regsList, coilList=None):
        coilsRsl = []
        if len(regsList) != 22:
            gv.gDebugPrint('runLadderLogic(): input not valid', logType=gv.LOG_WARN)
            gv.gDebugPrint("Input registers list: %s" %str(regsList))
        else:
            # direct connection copy the register state to coil directly:
            coilsRsl = list(regsList).copy()
        gv.gDebugPrint('Finished calculate all coils: %s' %str(coilsRsl), logType=gv.LOG_INFO)
        return coilsRsl
        
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class modBusService(threading.Thread):
    """ mod bus service hold one datahandler, on databank and one Modbus server 
        to handler the SCADA system's modbus request.
    """
    def __init__(self, parent, threadID, name):
        threading.Thread.__init__(self)
        hostIp = 'localhost'
        hostPort = 503
        # Init the data handler with a databank. 
        self.dataMgr = modbusTcpCom.plcDataHandler(allowRipList=gv.ALLOW_R_L, allowWipList=gv.ALLOW_W_L)
        # Init the modbus TCP server.
        self.server = modbusTcpCom.modbusTcpServer(hostIp=hostIp, hostPort=hostPort, dataHandler=self.dataMgr)
        # load the server info into the 
        serverInfo = self.server.getServerInfo()
        self.dataMgr.initServerInfo(serverInfo)
        # passed in the ladder logic inside the handler.
        self.dataMgr.addLadderLogic('direct_logic_set', gv.iLadderLogic)
        # set auto update to true to make the data bank can auto execute  the ladder logic when register state changes.
        self.dataMgr.setAutoUpdate(True)
        gv.iMBhandler = self.dataMgr
        self.daemon = True

    def run(self):
        """ Start the udp server's main message handling loop."""
        gv.gDebugPrint("ModbusTCP service thread run() start.", logType=gv.LOG_INFO)
        self.server.startServer()
        gv.gDebugPrint("ModbusTCP service thread run() end.", logType=gv.LOG_INFO)
        self.threadName = None # set the thread name to None when finished.

    def stop(self):
        self.server.stopServer()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class plcSimulator(object):
    """ A PlC simulator to provide below functions: 
        - Create a modbus service running in subthread to handle the SCADA system's 
            modbus requirment.
        - Connect to the real world emulator to fetch the sensor state and calculate 
            the output coils state based on the ladder logic. 
        - Send the signal setup request to the real world emulator to change the signal.
    """
    def __init__(self, parent, plcID, realworldIP):
        self.parent = parent
        self.id = plcID
        self.realworld = realworldIP
        # input sensors state from real world emulator: 
        self.inputState = {
            'weline': [],
            'nsline': [],
            'ccline': [] }
        # out put coils state to real world emulator:
        self.coilState = {
            'weline': [0]*10,
            'nsline': [0]*6,
            'ccline': [0]*6
        }
        # Init the ladder logic.
        self.LadderPiority = {
            'weline': ('ccline',),
            'nsline': ('ccline',),
            'ccline': ('weline', 'nsline')
        }
        gv.iLadderLogic = directConnLadderLogic(self)
        # Init the UDP connector to connect to the realworld and test the connection. 
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
        # Init the modbus TCP service
        gv.iMBservice = modBusService(self, 1, 'ModbusService')
        gv.iMBservice.start()

        self.terminate = False

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
                rqstType (str): request type string.
                rqstDict (doct): request detail dictionary.
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
    def getStationsInfo(self):
        """ Get sensors state from the real-world simulator. """
        rqstKey = 'GET'
        rqstType = 'stations'
        rqstDict = {'weline': None,
                    'nsline': None,
                    'ccline': None}
        result = self._queryToRW(rqstKey, rqstType, rqstDict)
        return result

#-----------------------------------------------------------------------------
    def changeStationSignalCoil(self):
        """ Set the signal state to the real-world simulator. """
        rqstKey = 'POST'
        rqstType = 'stations'
        rqstDict = self.coilState
        result = self._queryToRW(rqstKey, rqstType, rqstDict)
        return result
    
#-----------------------------------------------------------------------------
    def periodic(self, now):
        sensorInfo = self.getStationsInfo()
        if sensorInfo is None:
            gv.gDebugPrint("Lost connection to the real-world emulator.", logType=gv.LOG_WARN)
            self.realwordOnline = False
            return 
        (_, _, result) = sensorInfo
        time.sleep(0.1)
        for key in result.keys():
            self.inputState[key] = result[key]
        # Update PLC holding registers.
        self.updateHoldingRegs()
        time.sleep(0.1)
        self.updateCoilOutput()
        # update the output coils state:
        self.changeStationSignalCoil()

#-----------------------------------------------------------------------------
    def updateHoldingRegs(self):
        checkSeq = ('weline', 'nsline', 'ccline')
        holdingRegs = []
        for key in checkSeq:
            holdingRegs += self.inputState[key]
        gv.gDebugPrint("updateModBusInfo(): update holding registers: %s" %str(holdingRegs), logType=gv.LOG_INFO)
        gv.iMBhandler.updateHoldingRegs(0, holdingRegs)

#-----------------------------------------------------------------------------
    def updateCoilOutput(self):
        result = gv.iMBhandler.getCoilState(0, 22)
        self.coilState['weline'] = result[0:10]
        self.coilState['nsline'] = result[10:16]
        self.coilState['ccline'] = result[16:22]

#-----------------------------------------------------------------------------
    def run(self):
        while not self.terminate:
            now = time.time()
            if self.realwordOnline:
                self.periodic(now)
            else:
                self.recoonectCount -=1
                if self.recoonectCount == 0:
                    gv.gDebugPrint('Try to reconnect to the realworld.', logType=gv.LOG_INFO)
                    self.realwordOnline = self._loginRealWord()
                    if not self.realwordOnline: self.recoonectCount = 30
            time.sleep(gv.gInterval)

#-----------------------------------------------------------------------------
    def stop(self):
        self.terminate = True

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    gv.gDebugPrint("Start Init the PLC: %s" %str(gv.PCL_NAME), logType=gv.LOG_INFO)
    plc = plcSimulator(None, gv.PCL_NAME, gv.gRealWordIP)
    plc.run()

if __name__ == "__main__":
    main()
