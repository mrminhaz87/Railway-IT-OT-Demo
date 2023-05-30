#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        railwayMgr.py
#
# Purpose:     This function is the railway function manager to connect the 
#              agent element with their control panel.
#
# Author:      Yuancheng Liu
#
# Created:     2019/07/29
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     
#-----------------------------------------------------------------------------
import wx
import metroEmuGobal as gv
import railwayAgent as agent

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class MapMgr(object):
    """ Map Manager to init/control differet elements in the map."""
    def __init__(self, parent):
        """ Init all the element on the map. All the parameters are public to 
            other module.
        """
        self.trains = {}
        self.sensors = {}
        self.signals = {}

        self._initTT()
        self._initSensors()
        self._initSignal()
        #headPosA = (50, 200)
        #self.trainA = agent.AgentTrain(self, 0, headPosA, self.trackA['points'])
        #self.trainA.setNextPtIdx(1)
        #self.trainA.changedir()
        #self.trainA.initDir(1)

#-----------------------------------------------------------------------------
    def _initTT(self):
        """ This is a private Train&Tracks data init function. Will be replaced by 
            loading a config file before the how program init.(load to a gv.gxx
            parameter)
        """

        # Init WE Line and the trains on it.
        self.trackA = {
            'name' : 'WE Line',
            'color': wx.Colour(52, 169, 129),
            'type': gv.RAILWAY_TYPE_CYCLE,
            'points': [(50, 200), (100, 200), (100, 600), (600, 600), (600, 800), 
                       (900, 800),(900, 400), (1550, 400), (1550, 450), (950, 450), 
                       (950, 850), (550, 850), (550, 650),(50, 650)]
            }
        trackATrainCfg = [  {'id': 'we01', 'head': (50, 200), 'nextPtIdx': 1, 'len': 5}, 
                            {'id': 'we02', 'head': (1500, 400),'nextPtIdx': 7, 'len': 5},
                            {'id': 'we03', 'head': (460, 600), 'nextPtIdx': 3, 'len': 5},
                            {'id': 'we03', 'head': (800, 850), 'nextPtIdx': 11, 'len': 5}]
        
        self.trackATrains = self._getTrainsList(trackATrainCfg, self.trackA['points'])
        self.trains['weline'] = self.trackATrains

        # Init NS Line and the trains on it.
        self.trackB = {
            'name' : 'NS Line',
            'color': wx.Colour(233, 0, 97),
            'type': gv.RAILWAY_TYPE_CYCLE,
            'points': [(300, 50), (1200, 50), (1200, 300), (800, 300), (800, 600), (700, 600), 
                       (700, 100), (400, 100), (400, 450), (300, 450)]
        }
        trackBTrainCfg = [  {'id': 'ns01', 'head': (400, 50), 'nextPtIdx': 1, 'len': 4},
                            {'id': 'ns02', 'head': (1100, 300), 'nextPtIdx': 3, 'len': 4},
                            {'id': 'ns03', 'head': (600, 100), 'nextPtIdx': 7, 'len': 4}]

        self.trackBTrains = self._getTrainsList(trackBTrainCfg, self.trackB['points'])
        self.trains['nsline'] = self.trackBTrains

        # Init CC Line and the trains on it.
        self.trackC = {
            'name' : 'CC Line',
            'color': wx.Colour(255, 136, 0),
            'type': gv.RAILWAY_TYPE_CYCLE,
            'points': [(200, 200), (1400, 200), (1400, 700), (200, 700)]
        }
        trackCTrainCfg = [  {'id': 'cc01', 'head': (800, 200), 'nextPtIdx': 1, 'len': 6},
                            {'id': 'cc02', 'head': (300, 700), 'nextPtIdx': 3, 'len': 6},
                            {'id': 'cc03', 'head': (1300, 700), 'nextPtIdx': 3, 'len': 6}]
        self.trackCTrains = self._getTrainsList(trackCTrainCfg, self.trackC['points'])
        self.trains['ccline'] = self.trackCTrains

#-----------------------------------------------------------------------------
    def _initSensors(self):
        trackAsensorPos= [
            (50, 200), (170, 600), (270, 600), (600, 670), (600, 770), (900, 730),
            (900, 630), (1370, 400), (1470, 400), (1430, 450), (1330, 450), 
            (950, 670), (950, 770), (550, 730), (550, 650), (230, 650), (130, 650)
            ]
        self.tAsensors = agent.AgentSensors(self, 'we', trackAsensorPos)
        self.sensors['weline'] = self.tAsensors

        trackBsensorPos = [
            (300, 230), (300, 130), (1200, 170), (1200, 270), (700, 230), (700, 130),
            (400, 170), (400, 270)
            ]
        self.tBsensors = agent.AgentSensors(self, 'ns', trackBsensorPos)
        self.sensors['nsline'] = self.tBsensors

        trackCsensroPos = [
            (270, 200), (480, 200), (670, 200), (770, 200), 
            (1170, 200), (1270, 200), (1400, 370), (1400, 500), 
            (980, 700), (830, 700), (630, 700), (460, 700),
            (200, 700), (200, 530)
            ]
        self.tCsensors = agent.AgentSensors(self, 'cc', trackCsensroPos)
        self.sensors['ccline'] = self.tCsensors

#-----------------------------------------------------------------------------
    def _initSignal(self):
        # Set all the signal on track A
        trackASignalConfig = [
            {'id': 'we-0', 'pos':(160, 600), 'dir': 0, 'tiggerS': self.tCsensors, 'onIdx':13, 'offIdx':12 }, 
            {'id': 'we-1', 'pos':(240, 650), 'dir': 0, 'tiggerS': self.tCsensors, 'onIdx':13, 'offIdx':12 },
            {'id': 'we-3', 'pos':(600, 660), 'dir': 3, 'tiggerS': self.tCsensors, 'onIdx':11, 'offIdx':10 },
            {'id': 'we-4', 'pos':(550, 740), 'dir': 2, 'tiggerS': self.tCsensors, 'onIdx':11, 'offIdx':10 },
            {'id': 'we-5', 'pos':(900, 740), 'dir': 2, 'tiggerS': self.tCsensors, 'onIdx':9, 'offIdx':8 },
            {'id': 'we-6', 'pos':(950, 660), 'dir': 3, 'tiggerS': self.tCsensors, 'onIdx':9, 'offIdx':8 },
            {'id': 'we-7', 'pos':(1360, 400), 'dir': 0, 'tiggerS': self.tCsensors, 'onIdx':7, 'offIdx':6 },
            {'id': 'we-8', 'pos':(1440, 450), 'dir': 0, 'tiggerS': self.tCsensors, 'onIdx':7, 'offIdx':6 },
        ]
        self.tAsignals = []
        for Info in trackASignalConfig:
            signal = agent.AgentSignal(self, Info['id'], Info['pos'], dir=Info['dir'])
            signal.setTriggerOnSensors(Info['tiggerS'], Info['onIdx'])
            signal.setTriggerOffSensors(Info['tiggerS'], Info['offIdx'])
            self.tAsignals.append(signal)
        self.signals['weline'] = self.tAsignals
        
        # Set all the signal on trackB
        trackBSignalConfig = [
            {'id': 'we-0', 'pos':(160, 600), 'dir': 0, 'tiggerS': self.tCsensors, 'onIdx':13, 'offIdx':12 },

        ]
        self.tAsignals = []
        for Info in trackASignalConfig:
            signal = agent.AgentSignal(self, Info['id'], Info['pos'], dir=Info['dir'])
            signal.setTriggerOnSensors(Info['tiggerS'], Info['onIdx'])
            signal.setTriggerOffSensors(Info['tiggerS'], Info['offIdx'])
            self.tAsignals.append(signal)
        self.signals['weline'] = self.tAsignals



#-----------------------------------------------------------------------------
    def getSignals(self):
        return self.signals

#-----------------------------------------------------------------------------
    def getSensors(self):
        return self.sensors

#-----------------------------------------------------------------------------
    def _getTrainsList(self, trainCfg, trackPts):
        trainList = []
        for trainInfo in trainCfg:
            trainID = trainInfo['id']
            headPos = trainInfo['head']
            tLength = trainInfo['len']
            trainObj = agent.AgentTrain(self, trainID, headPos, trackPts, trainLen=tLength)
            trainObj.setNextPtIdx(trainInfo['nextPtIdx'])
            trainList.append(trainObj)
        return trainList

#-----------------------------------------------------------------------------
    def getTrains(self):
        return self.trains

    def getTrackA(self):
        return self.trackA
        
    def getTrackB(self):
        return self.trackB
    
    def getTrackC(self):
        return self.trackC
    
#-----------------------------------------------------------------------------
    def periodic(self , now):
        """ Periodicly call back function."""
        # update the trains position.
        for key, val in self.trains.items():
            frontTrain = val[-1]
            for train in val:
                train.updateTrainPos()
                train.checkClashFt(frontTrain)
                frontTrain = train                
                # update the sensor state
            if key == 'weline':
                self.tAsensors.updateActive(val)
            elif key == 'nsline':
                self.tBsensors.updateActive(val)
            elif key == 'ccline':
                self.tCsensors.updateActive(val)
        
        for key, val in self.signals.items():
            for signal in val:
                signal.updateSingalState()