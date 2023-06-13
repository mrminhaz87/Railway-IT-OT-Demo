#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        DataMgr.py
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
import scadaGobal as gv

import modbusTcpCom

class DataManager(object):
    """ The data manager is a module running parallel with the main thread to 
        handle the data-IO with dataBase and the monitor hub's data fetching/
        changing request.
    """
    def __init__(self, hostIp) -> None:
        self.plcClient = modbusTcpCom.modbusTcpClient(hostIp)
        if self.plcClient.checkConn():
            gv.gDebugPrint('DataManager: Connected to PLC', logType=gv.LOG_INFO)
        else:
            gv.gDebugPrint('DataManager: Fail to connect to PLC', logType=gv.LOG_INFO)
        self.regsList = []
        self.coilsList = []

    #--UIFrame---------------------------------------------------------------------
    def periodic(self, now):
        """ Call back every periodic time."""
        gv.gDebugPrint('DataManager: get PLC information', logType=gv.LOG_INFO)
        self.regsList = self.plcClient.getHoldingRegs(0, 39)
        self.coilsList = self.plcClient.getCoilsBits(0, 17)

    def getPLCInfo(self, plcName):
        if plcName == 'plc1':
            if len(self.regsList) > 0 and len(self.coilsList)>0: 
                return (self.regsList[0:15], self.coilsList[0:6])
        elif plcName == 'plc2':
            if len(self.regsList) > 0 and len(self.coilsList)>0:
                return (self.regsList[15:30], self.coilsList[6:12])
        elif plcName == 'plc3':
            if len(self.regsList) > 0 and len(self.coilsList)>0:
                return (self.regsList[30:39], self.coilsList[12:17])
        return None