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
# Define all the get() functions here:

    def getID(self):
        return self.id

    def getPos(self):
        return self.pos

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
class agentEnv(AgentTarget):
    """ The environment Item shown on the map such as building, IOT, camera.
    """
    def __init__(self, parent, tgtID, pos, wxBitMap, size ,tType=gv.ENV_TYPE):
        super().__init__(parent, tgtID, pos, tType)
        # build Icon: https://www.freepik.com/premium-vector/isometric-modern-supermarket-buildings-set_10094282.htm
        self.bitmap = wxBitMap
        self.size = size

#-----------------------------------------------------------------------------
# Define all the get() functions here:

    def getSize(self):
        return self.size

    def getWxBitmap(self):
        return self.bitmap

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AgentSensors(AgentTarget):
    """ The sensors set to show the sensors detection state."""
    def __init__(self, parent, idx, pos):
        AgentTarget.__init__(self, parent, idx, pos, gv.SENSOR_TYPE)
        self.sensorsCount = len(self.pos)
        self.stateList = [0]*self.sensorsCount # elements state: 1-triggered, 0-not triggered.

#-----------------------------------------------------------------------------
# Define all the get() functions here:

    def getActiveIndex(self):
        """ Return a list of all the actived sensors' index."""
        idxList = []
        for i, val in enumerate(self.pos):
            if val: idxList.append(i)
        return idxList

    def getSensorCount(self):
        return self.sensorsCount

    def getSensorState(self, idx):
        return self.stateList[idx]

    def getSensorsState(self):
        return self.stateList

#-----------------------------------------------------------------------------
# Define all the set() functions here:

    def setSensorState(self, idx, state):
        """ Set one sensor's state with an index in the sensor list.
            Args:
                idx (int): sensor index.
                state (int): 0/1
        """
        if idx >= self.sensorsCount: return False
        self.stateList[idx] = state
        return True

#-----------------------------------------------------------------------------
    def updateActive(self, trainList):
        """ Update the sensor triggered state based on the input trains position.
            Args:
                trainList (list(<AgentTrain>)): a list of AgentTrain obj.
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
    """ One train station obj. TODO: this agent is just for testing as it can only 
        sense/check on pos on one line. Will add sense multiple point on different 
        tracks later.
    """
    def __init__(self, parent, tgtID, pos, layout=gv.LAY_U):
        super().__init__(parent, tgtID, pos, gv.STATION_TYPE)
        self.dockCount = 10 # default the train will dock in the station in 10 refresh cycle.
        self.trainList = []
        self.dockState = False
    
    def bindTrains(self, TrainList):
        self.trainList = TrainList

#-----------------------------------------------------------------------------
# Define all the get() functions here:

    def getDockState(self):
        return self.dockState

#-----------------------------------------------------------------------------
    def updateTrainSDock(self):
        if len(self.trainList) == 0: return
        for train in self.trainList:
            midPt = train.getTrainPos(idx=2)
            if self.checkNear(midPt[0], midPt[1], 5):
                self.dockState = True
                if train.getDockCount() == 0: train.setDockCount(self.dockCount)
                return
        self.dockState = False

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AgentSignal(AgentTarget):
    def __init__(self, parent, tgtID, pos, dir=gv.LAY_U, tType=gv.SINGAL_TYPE):
        """ One signal object to control whether a train can pass / be-blocked at 
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
# Define all the get() functions here:
    def getState(self):
        return self.signalOn

#-----------------------------------------------------------------------------
# Define all the set() functions here:

    def setTriggerOnSensors(self, sensorAgent, idxList):
        self.triggerOnSenAgent = sensorAgent
        self.triggerOnIdx = idxList

    def setTriggerOffSensors(self, sensorAgent, idxList):
        self.triggerOffSenAgent = sensorAgent
        self.triggerOffIdx = idxList

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
    """ Create a train object with its init railway (track) array.

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
            railwayPts (_type_): the track path train will follow.
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
        self.trainDestList = self._getDestList(initPos)
        self.trainSpeed = trainSpeed    # train speed: pixel/periodic loop
        self.dockCount = 0              # refersh cycle number of a train to stop in the station.
        self.emgStop = False            # emergency stop.

#-----------------------------------------------------------------------------
    def _getDestList(self, initPos):
        """ Get the idx list of the target points on the track based on current 
            train pos.
        """
        (x0, y0) = initPos
        for idx in range(len(self.railwayPts)-1):
            x1, y1 = self.railwayPts[idx]
            x2, y2 = self.railwayPts[idx+1]
            if x1 == x0 == x2 or y1 == y0 == y2: return [idx+1]*len(self.pos)
        return [0]*len(self.pos)
            
#-----------------------------------------------------------------------------
    def _getDirc(self, srcPt, destPt):
        """ Get the moving direction. (vector from src point to dest point)"""
        x = destPt[0] - srcPt[0]
        y = destPt[1] - srcPt[1]
        return math.pi-math.atan2(x, y) 

#-----------------------------------------------------------------------------
    def initDir(self, nextPtIdx):
        """ Init every train carriage's direction.(Currently not used)"""
        if nextPtIdx < len(self.railwayPts):
            self.trainDestList = [nextPtIdx]*len(self.pos)
            nextPt = self.railwayPts[nextPtIdx]
            for i in range(len(self.pos)):
                self.dirs[i] = self._getDirc(self.pos[i], nextPt)

#-----------------------------------------------------------------------------
    def changedir(self):
        """ Change the train running direction."""
        #print(self.trainDestList)
        self.traindir = -self.traindir
        for i in range(len(self.trainDestList)):
            element = self.trainDestList[i]
            self.trainDestList[i] = (element+self.traindir) % len(self.railwayPts)
        #print(self.trainDestList)        

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
    def checkCollFt(self, frontTrain, threshold = 40):
        """ Check whether their is possible collision to the front train.
            Args:
                frontTrain (_type_): _description_
                threshold (int, optional): collision detection distance. Defaults to 40.
        """
        ftTail = frontTrain.getTrainPos()[-1] # front train tail position.
        if self.checkNear(ftTail[0], ftTail[1], threshold):
            if self.trainSpeed > 0 and self.dockCount==0:
                ftDockCount = frontTrain.getDockCount()
                # temp add make the behing train wait 
                self.setDockCount(ftDockCount+10)

#--AgentTrain------------------------------------------------------------------
    def checkSignal(self, signalList):
        """ Check whether the train reach the signal position, if the signal is 
            on, stop the train to wait.
        """
        for singalObj in signalList:
            x, y = singalObj.getPos()
            if self.checkNear(x, y, 20) and not self.emgStop:
                self.emgStop = singalObj.getState()
                break

#-----------------------------------------------------------------------------
# Define all the get() functions here:
    
    def getDirs(self):
        return self.dirs 

    def getDockCount(self):
        return self.dockCount

    def getTrainArea(self):
        """ Get the area train covered on the map."""
        h, t = self.pos[0], self.pos[-1]
        left, right = min(h[0], t[0])-5, max(h[0], t[0])+5
        up, down = min(h[1], t[1])-5, max(h[1], t[1])+5
        return (up, down, left, right)

    def getTrainLength(self):
        return self.trainLen
    
    def getTrainPos(self, idx=None):
        if isinstance(idx, int) and idx < self.trainLen: return self.pos[idx]
        return self.pos

#-----------------------------------------------------------------------------
# Define all the set() functions here:
    def setDockCount(self, count):
        self.dockCount = count

    def setEmgStop(self, emgStop):
        self.emgStop = emgStop

    def setNextPtIdx(self, nextPtIdx):
        if nextPtIdx < len(self.railwayPts): 
            self.trainDestList = [nextPtIdx]*len(self.pos)

    def setRailWayPts(self, railwayPts):
        """ change the train's railway points list.(before train pass the fork)"""
        self.railwayPts = railwayPts

    def setTrainSpeed(self, speed):
        self.trainSpeed = speed

#--AgentTrain------------------------------------------------------------------
    def updateTrainPos(self):
        """ Update the current train positions on the map. This function will be 
            called periodicly.
        """
        if self.emgStop: return
        # if dockCount == 1 also move the train to simulate the train start.
        if self.dockCount == 0 or self.dockCount ==1:
            # Train running on the railway:
            for i, trainPt in enumerate(self.pos):
                # The next railway point idx train going to approch.
                nextPtIdx = self.trainDestList[i]
                nextPt = self.railwayPts[nextPtIdx]
                dist = math.sqrt((trainPt[0] - nextPt[0])**2 + (trainPt[1] - nextPt[1])**2)
                if dist < self.trainSpeed:
                    # Go to the next check point if the distance is less than 1 speed unit.
                    trainPt[0], trainPt[1] = nextPt[0], nextPt[1]
                    # Update the next train distination if the train already get its next dist.
                    nextPtIdx = self.trainDestList[i] = (nextPtIdx + self.traindir) % len(self.railwayPts)
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
