#-----------------------------------------------------------------------------
# Name:        railwayAgent.py
#
# Purpose:     This module is the agents module to init different items in the 
#              railway system. All the items on the Map are agent object, each 
#              agent's update() function is a self-driven function to update the 
#              item's state.
# 
# Author:      Yuancheng Liu
#
# Version:     v0.1
# Created:     2023/05/26
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

import math
import metroEmuGobal as gv

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AgentTarget(object):
    """ Create a agent target to generate all the elements in the metro system, 
        all the other 'things' in the system will be inheritance from this module.
    """
    def __init__(self, parent, tgtID, pos, tType):
        self.parent = parent
        self.id = tgtID
        self.pos = pos      # target init position on the map.
        self.tType = tType  # 2 letter agent types.<railwayGlobal.py>

#--AgentTarget-----------------------------------------------------------------
    def getID(self):
        return self.id

#--AgentTarget-----------------------------------------------------------------
    def getPos(self):
        return self.pos

#--AgentTarget-----------------------------------------------------------------
    def getType(self):
        return self.tType

#--AgentTarget-----------------------------------------------------------------
    def checkNear(self, posX, posY, threshold):
        """ Check whether a point is near the selected point with the 
            input threshold value (unit: pixel).
        """
        dist = math.sqrt((self.pos[0] - posX)**2 + (self.pos[1] - posY)**2)
        return dist <= threshold

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AgentSensors(AgentTarget):
    """ The sensors set to show the sensors detection state."""
    def __init__(self, parent, idx, pos):
        AgentTarget.__init__(self, parent, idx, pos, gv.SENSOR_TYPE)
        self.sensorsCount = len(self.pos)
        self.stateList = [0]*self.sensorsCount # elements state: 1-triggered, 0-not triggered.

#-----------------------------------------------------------------------------
    def getSensorCount(self):
        return self.sensorsCount

#-----------------------------------------------------------------------------
    def getActiveIndex(self):
        idxList = []
        for i, val in enumerate(self.pos):
            if val: idxList.append(i)
        return idxList

#-----------------------------------------------------------------------------
    def getSensorState(self, idx):
        return self.stateList[idx]

#-----------------------------------------------------------------------------
    def getSensorsState(self):
        return self.stateList

#-----------------------------------------------------------------------------
    def setSensorState(self, idx, state):
        """ Set one sensor's state with a index in the sensor list.
            Args:
                idx (int): sensor index.
                state (int): 0/1
        """
        if idx >= self.sensorsCount: return False
        self.stateList[idx] = state
        return True

#-----------------------------------------------------------------------------
    def updateActive(self, trainList):
        """ Update the sensor triggered state based on the trains position.

            Args:
                trainList (list(<AgentTrain>)): _description_
        """
        for i in range(self.sensorsCount):
            self.stateList[i] = 0
            x, y = self.pos[i]
            for trainObj in trainList:
                (u, d, l, r) = trainObj.getTrainArea()
                if l <= x <= r and u <= y <= d: 
                    self.stateList[i] = 1
                    break
        
#-----------------------------------------------------------------------------
class AgentStation(AgentTarget):
    def __init__(self, parent, tgtID, pos, layout=gv.LAY_U):
        super().__init__(parent, tgtID, pos, gv.STATION_TYPE)
        self.dockCount = 10 # default the train will dock in the station.
        self.trainList = []
    
    def bindTrains(self, TrainList):
        self.trainList = TrainList

    def updateTrainSDock(self):
        if len(self.trainList) == 0: return
        for train in self.trainList:
            midPt = train.getTrainPos(idx=2)
            if self.checkNear(midPt[0], midPt[1], 5):
                if train.getDockCount() == 0: train.setDockCount(self.dockCount)
                break

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AgentSignal(AgentTarget):
    def __init__(self, parent, tgtID, pos, dir=0, tType=gv.SINGAL_TYPE):
        """ One signal object to control whether a train can pass/be-blocked at 
            the intersection. 
        Args:
            parent (_type_): _description_
            tgtID (_type_): _description_
            pos (_type_): _description_
            dir (int, optional): _description_. Defaults to 0-up, 1-down, 2-left, 3 right.
            tType (_type_, optional): _description_. Defaults to gv.SINGAL_TYPE.
        """
        super().__init__(parent, tgtID, pos, tType)
        self.signalOn = False # signal on (True): train stop, signal off(False): train pass  
        self.dir = dir # signal indicator's direction on map. 0-up, 1-down, 2-left, 3-right
        self.triggerOnSenAgent = None
        self.triggerOnIdx = None
        self.triggerOffSenAgent = None
        self.triggerOffIdx = None

#-----------------------------------------------------------------------------
    def getState(self):
        return self.signalOn

#-----------------------------------------------------------------------------
    def setTriggerOnSensors(self, sensorAgent, idxList):
        self.triggerOnSenAgent = sensorAgent
        self.triggerOnIdx = idxList

#-----------------------------------------------------------------------------
    def setTriggerOffSensors(self, sensorAgent, idxList):
        self.triggerOffSenAgent = sensorAgent
        self.triggerOffIdx = idxList

#-----------------------------------------------------------------------------
    def setState(self, state):
        self.signalOn = state

#-----------------------------------------------------------------------------
    def updateSingalState(self):
        if self.signalOn:
            for idx in self.triggerOnIdx:
                if self.triggerOffSenAgent.getSensorState(idx): 
                    self.signalOn = False
                    break
        else:
            for idx in self.triggerOffIdx:
                if self.triggerOffSenAgent.getSensorState(idx):
                    self.signalOn =True
                    break

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AgentTrain(AgentTarget):
    """ Create a train object with its init railway(track) array.

        input:  pos - The init position of the train head.
                railwayPts - list of railway points.(train will also run under 
                the list sequence.)
    """
    def __init__(self, parent, trainID, initPos, railwayPts, trainLen=5, trainSpeed=10, railwayType=gv.RAILWAY_TYPE_CYCLE):
        """ Init the train control agent object.
        Args:
            parent (_type_): parent object.
            trainID (_type_): train ID.
            pos (_type_): train initiate position. 
            railwayPts (_type_): the track train will follow.
            trainLen (int, optional): _description_. Defaults to 5.
            railwayType (_type_, optional): _description_. Defaults to gv.RAILWAY_TYPE_CYCLE.
        """
        AgentTarget.__init__(self, parent, trainID, initPos, railwayType)
        self.railwayPts = railwayPts
        self.railwayType = railwayType
        self.trainLen = trainLen
        # Init the train head and tail points at the horizontal position.
        self.pos = [[initPos[0] + 10*i, initPos[1]] for i in range(self.trainLen)]
        self.dirs = [0]*5
        self.traindir = 1   # follow the railway point with increase order.
        # self.pos = [pos[0]]*5
        # The train next distination index for each train body.
        # self.trainDistList = [0]*len(self.pos) # destination idx for each train body.
        self.trainDistList = self._getDestList(initPos)
        self.trainSpeed = trainSpeed    # train speed: pixel/periodic loop
        self.dockCount = 0      # time to stop in the station.
        self.emgStop = False    # emergency stop.

#-----------------------------------------------------------------------------
    def _getDestList(self, initPos):
        """ Get the target points index automatically based on current train pos.
            Returns:
                _type_: _description_
        """
        (x0, y0) = initPos
        for idx in range(len(self.railwayPts)-1):
            x1, y1 = self.railwayPts[idx]
            x2, y2 = self.railwayPts[idx+1]
            if x1 == x0 == x2 or y1 == y0 == y2:
                return [idx+1]*len(self.pos)
        return [0]*len(self.pos)
            
#-----------------------------------------------------------------------------
    def _getDirc(self, srcPt, destPt):
        x = destPt[0] - srcPt[0]
        y = destPt[1] - srcPt[1]
        return math.pi-math.atan2(x, y) 

#-----------------------------------------------------------------------------
    def initDir(self, nextPtIdx):
        if nextPtIdx < len(self.railwayPts): 
            self.trainDistList = [nextPtIdx]*len(self.pos)
            nextPt = self.railwayPts[nextPtIdx]
            for i in range(len(self.pos)):
                self.dirs[i] = self._getDirc(self.pos[i], nextPt)
        print(self.dirs)

#-----------------------------------------------------------------------------
    def getDirs(self):
        return self.dirs 

#-----------------------------------------------------------------------------
    def setNextPtIdx(self, nextPtIdx):
        if nextPtIdx < len(self.railwayPts): 
            self.trainDistList = [nextPtIdx]*len(self.pos)

#-----------------------------------------------------------------------------
    def getTrainArea(self):
        """ Get the area train covered area on the map."""
        h, t = self.pos[0], self.pos[-1]
        left, right = min(h[0], t[0])-5, max(h[0], t[0])+5
        up, down = min(h[1], t[1])-5, max(h[1], t[1])+5
        return (up, down, left, right)

#--AgentTrain------------------------------------------------------------------
    def changedir(self):
        """ Change the train running direction."""
        #self.railwayPts = self.railwayPts[::-1]
        #self.trainDistList = self.trainDistList[::-1]
        print(self.trainDistList)
        self.traindir = -self.traindir
        for i in range(len(self.trainDistList)):
            element = self.trainDistList[i]
            self.trainDistList[i] = (element+self.traindir)% len(self.railwayPts)
        print(self.trainDistList)        

#--AgentTrain------------------------------------------------------------------
    def checkNear(self, posX, posY, threshold):
        """ Overwrite the parent checknear function to check whether a point
            is near the train.
        """
        for pos in self.pos:
            dist = math.sqrt((pos[0] - posX)**2 + (pos[1] - posY)**2)
            if dist <= threshold: return True
        return False

#--AgentTrain------------------------------------------------------------------
    def checkClashFt(self, frontTrain, threshold = 40):
        ftTail = frontTrain.getTrainPos()[-1]
        if self.checkNear(ftTail[0], ftTail[1], threshold):
            if self.trainSpeed > 0:
                ftDockCount = frontTrain.getDockCount()
                # temp add make the behing train wait
                self.setDockCount(ftDockCount+10)

#--AgentTrain------------------------------------------------------------------
    def checkSignal(self, signalList):
        for singalObj in signalList:
            x, y = singalObj.getPos()
            if self.checkNear(x, y, 20):
                self.emgStop = singalObj.getState()
                break

    def getTrainLength(self):
        return self.trainLen

#--AgentTrain------------------------------------------------------------------
    def getTrainPos(self, idx=None):
        if isinstance(idx, int) and idx < self.trainLen: return self.pos[idx]
        return self.pos

#--AgentTrain------------------------------------------------------------------
    def getDockCount(self):
        return self.dockCount

#--AgentTrain------------------------------------------------------------------
    def setDockCount(self, count):
        self.dockCount = count

#--AgentTrain------------------------------------------------------------------
    def setTrainSpeed(self, speed):
        self.trainSpeed = speed

#--AgentTrain------------------------------------------------------------------
    def setRailWayPts(self, railwayPts):
        """ change the train's railway points list.(before train pass the fork)"""
        self.railwayPts = railwayPts

#--AgentTrain------------------------------------------------------------------
    def setEmgStop(self, emgStop):
        self.emgStop = emgStop

#--AgentTrain------------------------------------------------------------------
    def updateTrainPos(self):
        """ Update the current train positions on the map."""
        if self.emgStop: return
        if self.dockCount == 0 or self.dockCount ==1:
            # Train running on the railway:
            for i, trainPt in enumerate(self.pos):
                # The next railway point idx train going to approch.
                nextPtIdx = self.trainDistList[i]
                nextPt = self.railwayPts[nextPtIdx]
                dist = math.sqrt((trainPt[0] - nextPt[0])**2 + (trainPt[1] - nextPt[1])**2)
                if dist < self.trainSpeed:
                    # Go to the next check point if the distance is less than 1 speed unit.
                    trainPt[0], trainPt[1] = nextPt[0], nextPt[1]
                    # Update the next train distination if the train already get its next dist.
                    nextPtIdx = self.trainDistList[i] = (nextPtIdx + self.traindir) % len(self.railwayPts)
                    nextPt = self.railwayPts[nextPtIdx]
                    #self.dirs[i] = self._getDirc(trainPt, nextPt)
                else:
                    # Move one speed unit.
                    scale = float(self.trainSpeed)/float(dist)
                    trainPt[0] += int((nextPt[0]-trainPt[0])*scale)
                    trainPt[1] += int((nextPt[1]-trainPt[1])*scale)
            if self.dockCount == 1: self.dockCount -= 1

        else:  # Train stop at the station.
            self.dockCount -= 1
