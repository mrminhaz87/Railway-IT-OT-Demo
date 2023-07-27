#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        trainDataMgr.py
#
# Purpose:     Data manager module used to control all the other data processing 
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

# flag to identify whether the train's data will be done a slight change before 
# show up on the UI 
RANDOM_FLG = True 

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class TrainAgent(object):
    """ Agent class to store a trains' information and generate the adjusted 
        data.
    """
    def __init__(self, trainID, designVoltage) -> None:
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

#-----------------------------------------------------------------------------
# Define all the get() function here

    def getTrainInfo(self):
        """ Return the adjusted train information dictionary. Example: 
            {
                'id': self.id,
                'speed': 0,
                'current': o,
                'voltage': self.designVoltage + randint(0,50) if RANDOM_FLG else 0,
                'power': self.powerFlag
            }
        """
        result = None
        if not self.powerFlag:
            result = {
                'id': self.id,
                'speed': 0,
                'current': 0,
                'voltage': self.designVoltage + randint(0,50) if RANDOM_FLG else 0,
                'power': self.powerFlag
            }
        else:
            if self.speed == 0:
                result = {
                    'id': self.id,
                    'speed': randint(0, 5) if RANDOM_FLG else 0,
                    'current': randint(10, 30) if RANDOM_FLG else 10,
                    'voltage': int(self.designVoltage - randint(0,20)) if RANDOM_FLG else self.designVoltage,
                    'power': self.powerFlag
                }
            else:
                result = {
                    'id': self.id,
                    'speed': randint(56, 100) if RANDOM_FLG else 78,
                    'current': randint(150, 200) if RANDOM_FLG else 150,
                    'voltage': int(self.designVoltage - randint(20, 50)) if RANDOM_FLG else self.designVoltage,
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
    """ Train data manager to store all the trains agent. """

    def __init__(self, parent) -> None:
        self.trainInfoDict = OrderedDict()
        self._initTrains()
        gv.gDebugPrint("Finished the Trains Agent Mangage: %s" %str(self.trainInfoDict), 
                       prt=False, logType=gv.LOG_INFO)

#-----------------------------------------------------------------------------
    def _initTrain(self, trackID, trainNum, designVoltage):
        """ Init the train agents on a tracks and add them in the <self.trainInfoDict>"""
        self.trainInfoDict[trackID] = []
        for i in range(trainNum):
            trainID = '-'.join((trackID, str(i)))
            train = TrainAgent(trainID, designVoltage)
            self.trainInfoDict[trackID].append(train)

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
        if trackID in self.trainInfoDict.keys():
            idxRange = min(len(speedList), len(self.trainInfoDict[trackID]))
            for idx in range(idxRange):
                train = self.trainInfoDict[trackID][idx]
                train.setSpeed(speedList[idx])

#-----------------------------------------------------------------------------
    def updateTrainsPwr(self, trackID, speedList):
        if trackID in self.trainInfoDict.keys():
            idxRange = min(len(speedList), len(self.trainInfoDict[trackID]))
            for idx in range(idxRange):
                train = self.trainInfoDict[trackID][idx]
                train.setPower(speedList[idx])

#-----------------------------------------------------------------------------
    def getTrainsInfo(self, trackID):
        """ Collect data from all the train agtens in <self.trainInfoDict> and 
            build a list of data.
        """
        result = []
        if trackID in self.trainInfoDict.keys():
            for train in self.trainInfoDict[trackID]:
                result.append(train.getTrainInfo())
        return result

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class DataManager(object):
    """ The data manager is a module running parallel with the main thread to 
        handle the data-IO with dataBase and the monitor hub's data fetching/
        changing request.
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
                gv.gDebugPrint('DataManager: Connected to PLC', logType=gv.LOG_INFO)
            else:
                gv.gDebugPrint('DataManager: Fail to connect to PLC', logType=gv.LOG_INFO)
            self.regsDict[key] = []
            self.coilsDict[key] = []
        gv.gDebugPrint('ScadaMgr inited', logType=gv.LOG_INFO)

    #-----------------------------------------------------------------------------
    def periodic(self, now):
        """ Call back every periodic time."""
        gv.gDebugPrint('DataManager: get PLC information', logType=gv.LOG_INFO)
        for key, val in self.plcClients.items():
            hRegsAddr, hRegsNum = self.plcInfo[key]['hRegsInfo']
            self.regsDict[key] = self.plcClients[key].getHoldingRegs(hRegsAddr, hRegsNum)
            coilsAddr, coilsNum = self.plcInfo[key]['coilsInfo']
            self.coilsDict[key] = self.plcClients[key].getCoilsBits(coilsAddr, coilsNum)

    #-----------------------------------------------------------------------------
    def setPlcCoilsData(self, plcid, idx, val):
        if plcid in self.plcClients.keys():
            gv.gDebugPrint('DataManager: set PLC coil:%s' %str((plcid, idx, val)), logType=gv.LOG_INFO)
            self.plcClients[plcid].setCoilsBit(idx, val)
            time.sleep(0.1)

    #-----------------------------------------------------------------------------
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
        """ Combine all the coids data in to one list and return it."""
        result = []
        for val in self.coilsDict.values():
            if val is None: continue
            result += val
        return result