#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        trainDataMgr.py
#
# Purpose:     Data manager module used to control all the data processing 
#              modules and store the interprocess/result data.
#
# Author:      Yuancheng Liu
#
# Created:     2023/06/13
# Version:     v0.1.2
# Copyright:   Copyright (c) 2023 LiuYuancheng
# License:     MIT License  
#-----------------------------------------------------------------------------

import time
from collections import OrderedDict
from random import randint

import trainCtrlGlobal as gv
import modbusTcpCom

# flag to identify whether the train's data will be added a slight random change 
# before show up on the UI to simulate the real-world scenario.
RANDOM_FLG = True 

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class TrainAgent(object):
    """ Agent class to store a trains' information and generate the adjusted 
        random data if needed.
    """
    def __init__(self, trainID, designVoltage, dataRandFlg=True) -> None:
        """ Init example: train = TrainAgent(1, 750)
            Args:
                trainID (str): train ID
                designVoltage (int): trains operating voltage.
        """
        self.id = trainID
        self.speed = 0 if not gv.TEST_MD else 1
        self.current = 0
        self.designVoltage = designVoltage
        self.powerFlag = False if not gv.TEST_MD else True
        self.dataRanFlg = dataRandFlg

#-----------------------------------------------------------------------------
# Define all the get() function here

    def getTrainInfo(self):
        """ Return the adjusted train information dictionary. Example: 
            {
                'id': self.id,
                'speed': 0,
                'current': o,
                'voltage': self.designVoltage + randint(0,50) if self.dataRanFlg else 0,
                'power': self.powerFlag
            }
        """
        result = None
        if not self.powerFlag:
            result = {
                'id': self.id,
                'speed': 0,
                'current': 0,
                'voltage': self.designVoltage + randint(0, 50) if self.dataRanFlg  else 0,
                'power': self.powerFlag
            }
        else:
            if self.speed == 0:
                result = {
                    'id': self.id,
                    'speed': randint(0, 5) if self.dataRanFlg  else 0,
                    'current': randint(10, 30) if self.dataRanFlg  else 10,
                    'voltage': int(self.designVoltage - randint(0, 20)) if self.dataRanFlg else self.designVoltage,
                    'power': self.powerFlag
                }
            else:
                result = {
                    'id': self.id,
                    'speed': randint(56, 100) if self.dataRanFlg  else 78,
                    'current': randint(150, 200) if self.dataRanFlg  else 150,
                    'voltage': int(self.designVoltage - randint(20, 50)) if self.dataRanFlg else self.designVoltage,
                    'power': self.powerFlag
                }
        return result

#-----------------------------------------------------------------------------
# Define all the set function() here.
    def setSpeed(self, speed):
        self.speed = speed

    def setPower(self, state):
        self.powerFlag = state

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class MapManager(object):
    """ UI manager module to control all the UI components."""
    def __init__(self, parent) -> None:
        self.parent = parent
        self.trainsAgentDict = OrderedDict() # each element is a list of train agents.
        self._initTrains()
        gv.gDebugPrint("Finished init map manager: %s" %str(self.trainsAgentDict), 
                       prt=False, logType=gv.LOG_INFO)

#-----------------------------------------------------------------------------
    def _initTrain(self, trackID, trainNum, designVoltage):
        """ Init one train agent on a tracks and add them in the related trains
            agents list of <self.trainsAgentDict>
        """
        self.trainsAgentDict[trackID] = []
        for i in range(trainNum):
            trainID = '-'.join((trackID, str(i)))
            train = TrainAgent(trainID, designVoltage, dataRandFlg=RANDOM_FLG)
            self.trainsAgentDict[trackID].append(train)

#-----------------------------------------------------------------------------
    def _initTrains(self):
        # init all the weline trains
        trackID, trainNum, designVoltage = 'weline', 4, 750
        self._initTrain(trackID, trainNum, designVoltage)
        # init all the nsline trains
        trackID, trainNum, designVoltage = 'nsline', 3, 750
        self._initTrain(trackID, trainNum, designVoltage)
        # init all the ccline Trains
        trackID, trainNum, designVoltage = 'ccline', 3, 750
        self._initTrain(trackID, trainNum, designVoltage)

#-----------------------------------------------------------------------------
    def updateTrainsSpeed(self, trackID, speedList):
        if trackID in self.trainsAgentDict.keys():
            idxRange = min(len(speedList), len(self.trainsAgentDict[trackID]))
            for idx in range(idxRange):
                train = self.trainsAgentDict[trackID][idx]
                train.setSpeed(speedList[idx])

#-----------------------------------------------------------------------------
    def updateTrainsPwr(self, trackID, speedList):
        if trackID in self.trainsAgentDict.keys():
            idxRange = min(len(speedList), len(self.trainsAgentDict[trackID]))
            for idx in range(idxRange):
                train = self.trainsAgentDict[trackID][idx]
                train.setPower(speedList[idx])

#-----------------------------------------------------------------------------
    def getTrainsInfo(self, trackID):
        """ Collect data from all the train agtens in <self.trainsAgentDict> and 
            build a list of data.
        """
        result = []
        if trackID in self.trainsAgentDict.keys():
            for train in self.trainsAgentDict[trackID]:
                result.append(train.getTrainInfo())
        return result

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class DataManager(object):
    """ The data manager is a module running parallel with the main thread to 
        connect to PLCs module to do the data communication with modbus TCP.
    """
    def __init__(self, parent, plcInfo) -> None:
        self.parent = parent
        self.plcClients = OrderedDict()
        self.regsDict = {}
        self.coilsDict = {}
        self.plcInfo = plcInfo
        for key, val in plcInfo.items():
            plcIpaddr = val['ipaddress']
            plcPort = val['port']
            self.plcClients[key] = modbusTcpCom.modbusTcpClient(plcIpaddr, tgtPort=plcPort)
            if self.plcClients[key].checkConn():
                gv.gDebugPrint('DataManager: Connected to PLC.', logType=gv.LOG_INFO)
            else:
                gv.gDebugPrint('DataManager: Failed to connect to PLC.', logType=gv.LOG_INFO)
            self.regsDict[key] = []
            self.coilsDict[key] = []
        gv.gDebugPrint('TrainsHMI dataMgr inited', logType=gv.LOG_INFO)

    #-----------------------------------------------------------------------------
    def periodic(self, now):
        """ Call back every periodic time."""
        gv.gDebugPrint('DataManager: try to get PLC information', logType=gv.LOG_INFO)
        for key, val in self.plcClients.items():
            hRegsAddr, hRegsNum = self.plcInfo[key]['hRegsInfo']
            self.regsDict[key] = self.plcClients[key].getHoldingRegs(hRegsAddr, hRegsNum)
            coilsAddr, coilsNum = self.plcInfo[key]['coilsInfo']
            self.coilsDict[key] = self.plcClients[key].getCoilsBits(coilsAddr, coilsNum)

    #-----------------------------------------------------------------------------
    # define all the get() function here.
    def getPlcHRegsData(self, plcid, startIdx, endIdx):
        if plcid in self.regsDict.keys():
            if not self.regsDict[plcid] is None:
                return self.regsDict[plcid][startIdx:endIdx]
        return None

    #-----------------------------------------------------------------------------
    def getPlcCoilsData(self, plcid, startIdx, endIdx):
        if plcid in self.coilsDict.keys():
            if not self.coilsDict[plcid] is None:
                return self.coilsDict[plcid][startIdx:endIdx]
        return None

    #-----------------------------------------------------------------------------
    def getConntionState(self, plcID):
        if plcID in self.plcClients.keys():
            return self.plcClients[plcID].checkConn()
        return False

    #-----------------------------------------------------------------------------
    def getAllPlcRegsData(self):
        """ Combine all the registers data into one list and return it."""
        result = []
        for val in self.regsDict.values():
            if val is None: continue
            result += val
        return result
    
    #-----------------------------------------------------------------------------
    def getAllPlcCoisData(self):
        """ Combine all the coils data in to one list and return it."""
        result = []
        for val in self.coilsDict.values():
            if val is None: continue
            result += val
        return result
    
    #-----------------------------------------------------------------------------
    def setPlcCoilsData(self, plcid, idx, val):
        """ Set the PLC coils state
            Args:
                plcid (str): PLC ID
                idx (int): coils address index.
                val (bool): coil on/off state.
        """
        if plcid in self.plcClients.keys():
            gv.gDebugPrint('DataManager: set PLC coil:%s' %str((plcid, idx, val)), 
                           logType=gv.LOG_INFO)
            self.plcClients[plcid].setCoilsBit(idx, val)
            time.sleep(0.1)