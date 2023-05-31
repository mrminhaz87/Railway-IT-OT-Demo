#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        railwayMgr.py
#
# Purpose:     The management module to control all the components on the map 
#              and update the components state. 
# 
# Author:      Yuancheng Liu
#
# Version:     v0.1
# Created:     2023/05/29
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

import os
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
        self.tracks = {}
        self.trains = {}
        self.sensors = {}
        self.signals = {}
        self.stations = {}
        self.envItems = []

        self._initTT()
        self._initSensors()
        self._initSignal()
        self._initStation()
        self._initEnv()

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
        self.tracks['weline'] = self.trackA
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
        self.tracks['nsline'] = self.trackB
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
        self.tracks['ccline'] = self.trackC
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
            {'id': 'we-0', 'pos':(160, 600), 'dir': gv.LAY_U, 'tiggerS': self.tCsensors, 'onIdx':(13,), 'offIdx':(12,) }, 
            {'id': 'we-1', 'pos':(240, 650), 'dir': gv.LAY_U, 'tiggerS': self.tCsensors, 'onIdx':(13,), 'offIdx':(12,) },
            {'id': 'we-3', 'pos':(600, 660), 'dir': gv.LAY_R, 'tiggerS': self.tCsensors, 'onIdx':(11,), 'offIdx':(10,) },
            {'id': 'we-4', 'pos':(550, 740), 'dir': gv.LAY_L, 'tiggerS': self.tCsensors, 'onIdx':(11,), 'offIdx':(10,) },
            {'id': 'we-5', 'pos':(900, 740), 'dir': gv.LAY_L, 'tiggerS': self.tCsensors, 'onIdx':(9,), 'offIdx':(8,) },
            {'id': 'we-6', 'pos':(950, 660), 'dir': gv.LAY_R, 'tiggerS': self.tCsensors, 'onIdx':(9,), 'offIdx':(8,) },
            {'id': 'we-7', 'pos':(1360, 400), 'dir': gv.LAY_U, 'tiggerS': self.tCsensors, 'onIdx':(7,), 'offIdx':(6,) },
            {'id': 'we-8', 'pos':(1440, 450), 'dir': gv.LAY_U, 'tiggerS': self.tCsensors, 'onIdx':(7,), 'offIdx':(6,) },
        ]
        self.tAsignals = []
        for info in trackASignalConfig:
            signal = agent.AgentSignal(self, info['id'], info['pos'], dir=info['dir'])
            signal.setTriggerOnSensors(info['tiggerS'], info['onIdx'])
            signal.setTriggerOffSensors(info['tiggerS'], info['offIdx'])
            self.tAsignals.append(signal)
        self.signals['weline'] = self.tAsignals
        
        # Set all the signal on trackB
        trackBSignalConfig = [
            {'id': 'ns-0', 'pos':(300, 240), 'dir': gv.LAY_L, 'tiggerS': self.tCsensors, 'onIdx':(1,), 'offIdx':(0,) },
            {'id': 'ns-2', 'pos':(400, 160), 'dir': gv.LAY_R, 'tiggerS': self.tCsensors, 'onIdx':(1,), 'offIdx':(0,) },
            {'id': 'ns-3', 'pos':(700, 240), 'dir': gv.LAY_R, 'tiggerS': self.tCsensors, 'onIdx':(3,), 'offIdx':(2,) },
            {'id': 'ns-4', 'pos':(1200, 160), 'dir': gv.LAY_R, 'tiggerS': self.tCsensors, 'onIdx':(5,), 'offIdx':(4,) },

        ]
        self.tBsignals = []
        for info in trackBSignalConfig:
            signal = agent.AgentSignal(self, info['id'], info['pos'], dir=info['dir'])
            signal.setTriggerOnSensors(info['tiggerS'], info['onIdx'])
            signal.setTriggerOffSensors(info['tiggerS'], info['offIdx'])
            self.tBsignals.append(signal)
        self.signals['nsline'] = self.tBsignals

        # set all the signal on trackC
        trackCSignalConfig = [
            {'id': 'cc-0', 'pos':(260, 200), 'dir': gv.LAY_U, 'tiggerS': self.tBsensors, 'onIdx':(1, 7), 'offIdx':(0, 2) },
            {'id': 'cc-1', 'pos':(660, 200), 'dir': gv.LAY_U, 'tiggerS': self.tBsensors, 'onIdx':(5,), 'offIdx':(4,) },
            {'id': 'cc-2', 'pos':(1160, 200), 'dir': gv.LAY_U, 'tiggerS': self.tBsensors, 'onIdx':(3,), 'offIdx':(2,) },
            {'id': 'cc-3', 'pos':(1400, 360), 'dir': gv.LAY_R, 'tiggerS': self.tAsensors, 'onIdx':(8,10), 'offIdx':(7,9) },
            {'id': 'cc-4', 'pos':(990, 700), 'dir': gv.LAY_U, 'tiggerS': self.tAsensors, 'onIdx':(6,12), 'offIdx':(5,11) },
            {'id': 'cc-5', 'pos':(640, 700), 'dir': gv.LAY_U, 'tiggerS': self.tAsensors, 'onIdx':(4,14), 'offIdx':(3,13) },
            {'id': 'cc-6', 'pos':(210, 700), 'dir': gv.LAY_U, 'tiggerS': self.tAsensors, 'onIdx':(2, 16), 'offIdx':(1,15) },
        ]
        self.tCsignals = []
        for info in trackCSignalConfig:
            signal = agent.AgentSignal(self, info['id'], info['pos'], dir=info['dir'])
            signal.setTriggerOnSensors(info['tiggerS'], info['onIdx'])
            signal.setTriggerOffSensors(info['tiggerS'], info['offIdx'])
            self.tCsignals.append(signal)
        self.signals['ccline'] = self.tCsignals

#-----------------------------------------------------------------------------
    def _initStation(self):
        """ Init all the stations

        Returns:
            _type_: _description_
        """
        # Init station on weline.
        trackAStationCfg = [ {'id':'Tuas_Link', 'pos': (80, 200)}, 
                             {'id':'Junrong_East', 'pos': (360, 600)}, 
                             {'id':'Outram_Park', 'pos': (750, 800)}, 
                             {'id':'City_Hall', 'pos': (900, 500)}, 
                             {'id':'Paya_Leba', 'pos': (1250, 400)}, 
                             {'id':'Changgi_Airport', 'pos': (1550, 450)}, 
                             {'id':'Lavender', 'pos': (1100, 450)}, 
                             {'id':'Raffles_Place', 'pos': (850, 850)}, 
                             {'id':'Cliementi', 'pos': (430, 650)}, 
                             {'id':'Boon_Lay', 'pos': (50, 450)}]
        self.tAStations = []
        for info in trackAStationCfg:
            station = agent.AgentStation(self, info['id'], info['pos'])
            station.bindTrains(self.trackATrains)
            self.tAStations.append(station)
        self.stations['weline'] = self.tAStations


        trackBStationCfg = [ {'id':'Junrong_East', 'pos': (360, 450)}, 
                             {'id':'Wood_Land', 'pos': (430, 50)},
                             {'id':'Yishun', 'pos': (1040, 50)}, 
                             {'id':'Orchard', 'pos': (980, 300)},
                             {'id':'City_Hall', 'pos': (750, 600)},
                             {'id':'BiShan', 'pos': (550, 100)}]
        self.tBStations = []
        for info in trackBStationCfg:
            station = agent.AgentStation(self, info['id'], info['pos'])
            station.bindTrains(self.trackBTrains)
            self.tBStations.append(station)
        self.stations['nsline'] = self.tBStations

        trackCStationCfg = [ {'id':'Buona_Vsta', 'pos': (320, 700)}, 
                             {'id':'Farrer Road', 'pos': (200, 300)}, 
                             {'id':'Serangoon', 'pos': (930, 200)}, 
                             {'id':'Nicoll Highway', 'pos': (1400, 600)}, 
                             {'id':'Bayfront', 'pos': (1160, 700)},
                             {'id':'HarbourFront', 'pos': (710, 700)}]
        self.tCStations = []
        for info in trackCStationCfg:
            station = agent.AgentStation(self, info['id'], info['pos'])
            station.bindTrains(self.trackCTrains)
            self.tCStations.append(station)
        self.stations['ccline'] = self.tCStations
#-----------------------------------------------------------------------------
    def _initEnv(self):

        envCfg = [ {'id':'Tuas Industry Area', 'img':'factory_0.png', 'pos':(80, 80) ,  'size':(120, 120)},
                   {'id':'Changgi Airport', 'img':'airport.jpg', 'pos':(1500, 240) ,  'size':(160, 100)},
                   {'id':'JurongEast-Jem', 'img':'city_0.png', 'pos':(360, 520) ,  'size':(80, 80)},
                   {'id':'CityHall-01', 'img':'city_2.png', 'pos':(750, 520) ,  'size':(90, 80)},
                   {'id':'CityHall-02', 'img':'city_1.png', 'pos':(850, 500) ,  'size':(80, 60)}]
        for info in envCfg:
            imgPath = os.path.join(gv.IMG_FD, info['img'])
            if os.path.exists(imgPath):
                bitmap = wx.Bitmap(imgPath)
                building = agent.agentEnv(self, info['id'], info['pos'], bitmap, info['size'] )
                self.envItems.append(building)

#-----------------------------------------------------------------------------
    def _getTrainsList(self, trainCfg, trackPts):
        trainList = []
        for trainInfo in trainCfg:
            trainID = trainInfo['id']
            headPos = trainInfo['head']
            tLength = trainInfo['len']
            trainObj = agent.AgentTrain(self, trainID, headPos, trackPts, trainLen=tLength)
            #trainObj.setNextPtIdx(trainInfo['nextPtIdx'])
            trainList.append(trainObj)
        return trainList

#-----------------------------------------------------------------------------

    def getEnvItems(self):
        return self.envItems

    def getTracks(self, trackID=None):
        if trackID and trackID in self.tracks.keys(): return self.tracks[trackID]
        return self.tracks

    def getTrains(self, trackID=None):
        if trackID and trackID in self.trains.keys(): return self.trains[trackID]
        return self.trains

    def getSignals(self, trackID=None):
        if trackID and trackID in self.signals.keys(): return self.signals[trackID]
        return self.signals

    def getSensors(self, trackID=None):
        if trackID and trackID in self.sensors.keys(): return self.sensors[trackID]
        return self.sensors
    
    def selfStations(self, trackID=None):
        if trackID and trackID in self.stations.keys(): return self.stations[trackID]
        return self.stations

#-----------------------------------------------------------------------------
    def periodic(self , now):
        """ Periodicly call back function."""
        # update the trains position.
        for key, val in self.trains.items():
            
            frontTrain = val[-1]
            for train in val:
                # Check the signal 1st 
                train.checkSignal(self.signals[key])
                train.checkClashFt(frontTrain)
                train.updateTrainPos()
                frontTrain = train                
                # update the sensor state
            if key == 'weline':
                self.tAsensors.updateActive(val)
            elif key == 'nsline':
                self.tBsensors.updateActive(val)
            elif key == 'ccline':
                self.tCsensors.updateActive(val)
        # update the station train's docking state
        for key, val in self.stations.items():
            for station in val:
                station.updateTrainSDock()

        # Update the signal state
        for key, val in self.signals.items():
            for signal in val:
                signal.updateSingalState()