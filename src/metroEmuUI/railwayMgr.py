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
        self._initTT()
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
        self.trains = {}

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
        self.trains['weTrains'] = self.trackATrains

        # Init NS Line and the trains on it.
        self.trackB = {
            'name' : 'NS Line',
            'color': wx.Colour(233, 0, 97),
            'type': gv.RAILWAY_TYPE_CYCLE,
            'points': [(300, 50), (1200, 50), (1200, 600), (1100, 600), 
                       (1100, 100), (400, 100), (400, 450), (300, 450)]
        }
        trackBTrainCfg = [  {'id': 'ns01', 'head': (700, 50), 'nextPtIdx': 1, 'len': 4},
                            {'id': 'ns02', 'head': (320, 450), 'nextPtIdx': 7, 'len': 4},
                            {'id': 'ns03', 'head': (600, 100), 'nextPtIdx': 5, 'len': 4}]

        self.trackBTrains = self._getTrainsList(trackBTrainCfg, self.trackB['points'])
        self.trains['nsTrains'] = self.trackBTrains

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
        self.trains['ccTrains'] = self.trackCTrains

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
    
    def periodic(self , now):
        """ Periodicly call back function."""
        # update the trains position.
        for key, val in self.trains.items():
            frontTrain = val[-1]
            for train in val:
                train.updateTrainPos()
                train.checkClashFt(frontTrain)
                frontTrain = train
