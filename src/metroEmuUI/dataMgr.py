#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        DataMgr.py
#
# Purpose:     Data manager module used to control all the other data processing 
#              modules and store the interprocess/result data.
#
# Author:      Yuancheng Liu
#
# Created:     2023/06/07
# Version:     v_0.1
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------

import os
import time
import json
import threading
from datetime import datetime

import metroEmuGobal as gv
import Log
import udpCom

# Define all the local untility functions here:
#-----------------------------------------------------------------------------
def parseIncomeMsg(msg):
    """ parse the income message to tuple with 3 elements: request key, type and jsonString
        Args: msg (str): example: 'GET;dataType;{"user":"<username>"}'
    """
    req = msg.decode('UTF-8') if not isinstance(msg, str) else msg
    try:
        reqKey, reqType, reqJsonStr = req.split(';', 2)
        return (reqKey.strip(), reqType.strip(), reqJsonStr)
    except Exception as err:
        Log.error('parseIncomeMsg(): The income message format is incorrect.')
        Log.exception(err)
        return('','',json.dumps({}))

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class DataManager(threading.Thread):
    """ The data manager is a module running parallel with the main thread to 
        handle the data-IO with dataBase and the monitor hub's data fetching/
        changing request.
    """
    def __init__(self, parent) -> None:
        threading.Thread.__init__(self)
        self.parent = parent
        self.terminate = False
        self.server = udpCom.udpServer(None, gv.UDP_PORT)
        self.lastUpdate = datetime.now()
        self.daemon = True
        # init the local sensors data record dictionary
        self.sensorsDict = {
            'weline': None,
            'nsline': None, 
            'ccline': None
        }
        # init the local station data record dictionary
        self.stationsDict ={
            'weline': None,
            'nsline': None, 
            'ccline': None
        }

    #-----------------------------------------------------------------------------
    def updateSensorsData(self):
        if gv.iMapMgr:
            for key in self.sensorsDict.keys():
                sensorAgent = gv.iMapMgr.getSensors(trackID=key)
                self.sensorsDict[key] = sensorAgent.getSensorsState()

    #-----------------------------------------------------------------------------
    def updateStationsData(self):
        if gv.iMapMgr:
            for key in self.stationsDict.keys():
                self.stationsDict[key] = []
                for stationAgent in gv.iMapMgr.getStations(trackID=key):
                    state = 1 if stationAgent.getDockState() else 0
                    self.stationsDict[key].append(state)
                
    #-----------------------------------------------------------------------------
    def run(self):
        """ Thread run() function will be called by start(). """
        time.sleep(1)
        gv.gDebugPrint("datamanager started.", logType=gv.LOG_INFO)
        self.server.serverStart(handler=self.msgHandler)
        gv.gDebugPrint("DataManager running finished.", logType=gv.LOG_INFO)

    #-----------------------------------------------------------------------------
    def msgHandler(self, msg):
        """ Function to handle the data-fetch/control request from the monitor-hub.
            Args:
                msg (str/bytes): _description_
            Returns:
                bytes: message bytes reply to the monitor hub side.
        """
        gv.gDebugPrint("Incomming message: %s" % str(msg), logType=gv.LOG_INFO)
        # request message format: 
        # data fetch: GET:<key>:<val1>:<val2>...
        # data set: POST:<key>:<val1>:<val2>...
        resp = b'REP;deny;{}'
        (reqKey, reqType, reqJsonStr) = parseIncomeMsg(msg)
        if reqKey=='GET':
            if reqType == 'login':
                resp = ';'.join(('REP', 'login', json.dumps({'state':'ready'})))
            elif reqType == 'sensors':
                respStr = self.fetchSensorInfo(reqJsonStr)
                resp =';'.join(('REP', 'sensors', respStr))
            elif reqType == 'stations':
                respStr = self.fetchStationInfo(reqJsonStr)
                resp =';'.join(('REP', 'stations', respStr))
            pass
        elif reqKey=='POST':
            if reqType == 'signals':
                respStr = self.setSignals(reqJsonStr)
                resp =';'.join(('REP', 'signals', respStr))
            elif reqType == 'stations':
                respStr = self.setStationSignals(reqJsonStr)
                resp =';'.join(('REP', 'stations', respStr))
            pass
            # TODO: Handle all the control request here.
        if isinstance(resp, str): resp = resp.encode('utf-8')
        #gv.gDebugPrint('reply: %s' %str(resp), logType=gv.LOG_INFO )
        return resp
    
    #-----------------------------------------------------------------------------
    def fetchSensorInfo(self, reqJsonStr):
        reqDict = json.loads(reqJsonStr)
        self.updateSensorsData()
        respStr= json.dumps({'result': 'failed'})
        try:
            for key in reqDict.keys():
                if key in self.sensorsDict.keys():
                    reqDict[key] = self.sensorsDict[key]
            respStr = json.dumps(reqDict)
        except Exception as err:
            gv.gDebugPrint("fetchSensorInfo() Error: %s" %str(err), logType=gv.LOG_EXCEPT)
        return respStr

    #-----------------------------------------------------------------------------
    def fetchStationInfo(self, reqJsonStr):
        reqDict = json.loads(reqJsonStr)
        self.updateStationsData()
        respStr= json.dumps({'result': 'failed'})
        try:
            for key in reqDict.keys():
                if key in self.stationsDict.keys():
                    reqDict[key] = self.stationsDict[key]
            respStr = json.dumps(reqDict)
        except Exception as err:
            gv.gDebugPrint("fetchStationInfo() Error: %s" %str(err), logType=gv.LOG_EXCEPT)
        return respStr

    #-----------------------------------------------------------------------------
    def setSignals(self, reqJsonStr):
        reqDict = json.loads(reqJsonStr)
        respStr = json.dumps({'result': 'failed'})
        try:
            if gv.iMapMgr:
                for key, val in reqDict.items():
                    gv.iMapMgr.setSingals(key, val)
                respStr = json.dumps({'result': 'success'})
            respStr = json.dumps(reqDict)
        except Exception as err:
            gv.gDebugPrint("setSignals() Error: %s" %str(err), logType=gv.LOG_EXCEPT)
        return respStr

    #-----------------------------------------------------------------------------
    def setStationSignals(self, reqJsonStr):
        reqDict = json.loads(reqJsonStr)
        respStr = json.dumps({'result': 'failed'})
        try:
            if gv.iMapMgr:
                for key, val in reqDict.items():
                    gv.iMapMgr.setStationSignal(key, val)
                respStr = json.dumps({'result': 'success'})
            respStr = json.dumps(reqDict)
        except Exception as err:
            gv.gDebugPrint("setStationSignals() Error: %s" %str(err), logType=gv.LOG_EXCEPT)
        return respStr

    #-----------------------------------------------------------------------------
    def stop(self):
        """ Stop the thread."""
        self.terminate = True
        if self.server: self.server.serverStop()
        endClient = udpCom.udpClient(('127.0.0.1', gv.UDP_PORT))
        endClient.disconnect()
        endClient = None
