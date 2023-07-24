#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        scadaDataMgr.py
#
# Purpose:     Data manager module used to control all the other data processing 
#              modules and store the interprocess/result data.
#
# Author:      Yuancheng Liu
#
# Created:     2023/06/13
# Version:     v_0.1
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------

import time
from collections import OrderedDict
from random import randint

import trainCtrlGlobal as gv
import modbusTcpCom

RANDOM_FLG = True

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class TrainAgent(object):

    def __init__(self, trainID, designVoltage) -> None:
        self.id = trainID
        self.speed = 0 if not gv.TEST_MD else 1
        self.current = 0 
        self.designVoltage = designVoltage
        self.powerFlag = False if not gv.TEST_MD else True

    def setSpeed(self, speed):
        self.speed = speed

    def setPower(self, state):
        self.powerFlag = state

    def getTrainInfo(self):
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
#-----------------------------------------------------------------------------
class MapManager(object):

    def __init__(self, parent) -> None:
        self.trainInfoDict = OrderedDict()
        self._initTrains()
        print(self.trainInfoDict)

    def _initTrains(self):
        # init all the weline trains
        trackID, trainNum, designVoltage = 'weline', 4, 750
        self._initTrain(trackID, trainNum, designVoltage)

        # init all the nsline trains
        trackID, trainNum, designVoltage = 'nsline', 3, 750
        self._initTrain(trackID, trainNum, designVoltage)

        # init all the cclineTrains
        trackID, trainNum, designVoltage = 'ccline', 3, 750
        self._initTrain(trackID, trainNum, designVoltage)

    def _initTrain(self, trackID, trainNum, designVoltage):
        self.trainInfoDict[trackID] = []
        for i in range(trainNum):
            trainID = '-'.join((trackID, str(i)))
            train = TrainAgent(trainID, designVoltage)
            self.trainInfoDict[trackID].append(train)

    def updateTrainsSpeed(self, trackID, speedList):
        if trackID in self.trainInfoDict.keys():
            idxRange = min(len(speedList), len(self.trainInfoDict[trackID]))
            for idx in range(idxRange):
                train = self.trainInfoDict[trackID][idx]
                train.setSpeed(speedList[idx])
                
    def updateTrainsPwr(self, trackID, speedList):
        if trackID in self.trainInfoDict.keys():
            idxRange = min(len(speedList), len(self.trainInfoDict[trackID]))
            for idx in range(idxRange):
                train = self.trainInfoDict[trackID][idx]
                train.setPower(speedList[idx])

    def getTrainsInfo(self, trackID):
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

    #--UIFrame---------------------------------------------------------------------
    def periodic(self, now):
        """ Call back every periodic time."""
        gv.gDebugPrint('DataManager: get PLC information', logType=gv.LOG_INFO)
        for key, val in self.plcClients.items():
            hRegsAddr, hRegsNum = self.plcInfo[key]['hRegsInfo']
            self.regsDict[key] = self.plcClients[key].getHoldingRegs(hRegsAddr, hRegsNum)
            coilsAddr, coilsNum = self.plcInfo[key]['coilsInfo']
            self.coilsDict[key] = self.plcClients[key].getCoilsBits(coilsAddr, coilsNum)

    def setPlcCoilsData(self, plcid, idx, val):
        if plcid in self.plcClients.keys():
            gv.gDebugPrint('DataManager: set PLC coil:%s' %str((plcid, idx, val)), logType=gv.LOG_INFO)
            self.plcClients[plcid].setCoilsBit(idx, val)
            time.sleep(0.1)

    def getPlcHRegsData(self, plcid, startIdx, endIdx):
        if plcid in self.regsDict.keys():
            return self.regsDict[plcid][startIdx:endIdx]
        return None

    def getPlcCoilsData(self, plcid, startIdx, endIdx):
        if plcid in self.coilsDict.keys():
            return self.coilsDict[plcid][startIdx:endIdx]
        return None

    def getAllPlcRegsData(self):
        result = []
        for val in self.regsDict.values():
            result += val
        return result
    
    def getAllPlcCoisData(self):
        result = []
        for val in self.coilsDict.values():
            result += val
        return result