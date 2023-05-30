#-----------------------------------------------------------------------------
# Name:        railwayAgentPLC.py
#
# Purpose:     This module is the agent module to init different items in the 
#              railway system or create the interface to connect to the hardware. 
# Author:      Yuancheng Liu
#
# Created:     2019/07/02
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------
import math
import metroEmuGobal as gv

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AgentTarget(object):
    """ Create a agent target to generate all the element in the railway system, 
        all the other 'things' in the system will inheritance from this module.
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
    """ Creat the sensors set to show the sensors detection state."""
    def __init__(self, parent, idx, pos, plc=None):
        AgentTarget.__init__(self, parent, idx, pos, gv.SENSOR_TYPE)
        self.sensorsCount = len(self.pos)
        self.stateList = [0]*self.sensorsCount

    def getSensorCount(self):
        return self.sensorsCount

#-----------------------------------------------------------------------------
    def getActiveIndex(self):
        idxList = []
        for i, val in enumerate(self.pos):
            if val: idxList.append(i)
        return idxList

#-----------------------------------------------------------------------------
    def updateActive(self, trainList):
        for i in range(self.sensorsCount):
            self.stateList[i] = 0
            x, y = self.pos[i]
            for trainObj in trainList:
                (u, d, l, r) = trainObj.getTrainArea()
                if l <= x <= r and u <= y <= d:self.stateList[i] = 1
        
#--AgentSensor-----------------------------------------------------------------
    def setSensorState(self, idx, state):
        """ Set sensor status, flag(int) 0-OFF 1~9 ON"""
        self.stateList[idx] = state

    def getSensorState(self, idx):
        return self.stateList[idx]

#--AgentSensor-----------------------------------------------------------------
    def getSensorsState(self):
        return self.stateList


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AgentSignal(AgentTarget):
    def __init__(self, parent, tgtID, pos, dir=0, tType=gv.SINGAL_TYPE):
        """_summary_
        Args:
            parent (_type_): _description_
            tgtID (_type_): _description_
            pos (_type_): _description_
            dir (int, optional): _description_. Defaults to 0-up, 1-down, 2-left, 3 right.
            tType (_type_, optional): _description_. Defaults to gv.SINGAL_TYPE.
        """
        super().__init__(parent, tgtID, pos, tType)
        self.signalOn = False
        self.dir = dir # direction on map.
        self.triggerOnSenAgent = None
        self.triggerOnIdx= None
        self.triggerOffSenAgent = None
        self.triggerOffIdx=None

    def setTriggerOnSensors(self, sensorAgent, idxList):
        self.triggerOnSenAgent = sensorAgent
        self.triggerOnIdx = idxList

    def setTriggerOffSensors(self, sensorAgent, idxList):
        self.triggerOffSenAgent = sensorAgent
        self.triggerOffIdx = idxList

    def setState(self, state):
        self.signalOn = state

    def getState(self):
        return self.signalOn

    def updateSingalState(self):
        if self.signalOn:
            for idx in self.triggerOnIdx:
                if self.triggerOffSenAgent.getSensorState(idx):
                    self.signalOn = False
        else:
            for idx in self.triggerOffIdx:
                if self.triggerOffSenAgent.getSensorState(idx):
                    self.signalOn =True

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
        self.trainDistList = [0]*len(self.pos) # distination idx for each train body.
        self.trainSpeed = trainSpeed    # train speed: pixel/periodic loop
        self.dockCount = 0      # time to stop in the station.
        self.emgStop = False    # emergency stop.

#-----------------------------------------------------------------------------
    def _getDirc(self, srcPt, destPt):
        x = destPt[0] - srcPt[0]
        y = destPt[1] - srcPt[1]
        return math.pi-math.atan2(x, y) 

#-----------------------------------------------------------------------------
    def setNextPtIdx(self, nextPtIdx):
        if nextPtIdx < len(self.railwayPts): 
            self.trainDistList = [nextPtIdx]*len(self.pos)

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
    def getTrainArea(self):
        """ Get the area train covered on the map."""
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


    def CheckSignal(self, signalList):
        for singalObj in signalList:
            x, y = singalObj.getPos()
            if self.checkNear(x, y, 20): 
                if singalObj.getState():
                    if not self.emgStop:
                        self.emgStop = True
                else:
                    if self.emgStop: self.emgStop = False
                break

#--AgentTrain------------------------------------------------------------------
    def getTrainPos(self, idx=None):
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
        if self.dockCount == 0:
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

        else:  # Train stop at the station.
            self.dockCount -= 1
