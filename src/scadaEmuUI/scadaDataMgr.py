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

from collections import OrderedDict

import scadaGobal as gv
import modbusTcpCom

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

    def getPlcHRegsData(self, plcid, startIdx, endIdx):
        if plcid in self.regsDict.keys():
            return self.regsDict[plcid][startIdx:endIdx]
        return None

    def getPlcCoilsData(self, plcid, startIdx, endIdx):
        if plcid in self.coilsDict.keys():
            return self.coilsDict[plcid][startIdx:endIdx]
        return None
