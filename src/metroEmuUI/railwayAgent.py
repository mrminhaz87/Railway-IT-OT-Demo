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
class AgentTrain(AgentTarget):
    """ Create a train object with its init railway array.
        input:  pos - The init position of the train head.
                railwayPts - list of railway points.(train will also run under 
                the list sequence.)
    """
    def __init__(self, parent, idx, pos, railwayPts, railwayType=gv.RAILWAY_TYPE_LINE):
        AgentTarget.__init__(self, parent, idx, pos, gv.TRAIN_TYPE)
        self.railwayPts = railwayPts
        self.railwayType = railwayType
        # Init the train head and tail points at the horizontal position.
        self.pos = [[pos[0] + 12*i, pos[1]] for i in range(5)]
        self.dirs = [0]*5
        self.traindir = 1   # follow the railway point with increase order.
        # self.pos = [pos[0]]*5
        # The train next distination index for each train body.
        self.trainDistList = [0]*len(self.pos) # distination idx for each train body.
        self.trainSpeed = 10    # train speed: pixel/periodic loop
        self.dockCount = 0      # time to stop in the station.
        self.emgStop = False    # emergency stop.

    def _getDirc(self, srcPt, destPt):
        x = destPt[0] - srcPt[0]
        y = destPt[1] - srcPt[1]
        return math.pi-math.atan2(x, y) 

    def setNextPtIdx(self, nextPtIdx):
        if nextPtIdx < len(self.railwayPts): 
            self.trainDistList = [nextPtIdx]*len(self.pos)


    def initDir(self, nextPtIdx):
        if nextPtIdx < len(self.railwayPts): 
            self.trainDistList = [nextPtIdx]*len(self.pos)
            nextPt = self.railwayPts[nextPtIdx]
            for i in range(len(self.pos)):
                self.dirs[i] = self._getDirc(self.pos[i], nextPt)
        print(self.dirs)

    def getDirs(self):
        return self.dirs 
    
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

    #def setTrainDir(self, dirVal):
    #    self.



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
                    self.dirs[i] = self._getDirc(trainPt, nextPt)
                else:
                    # Move one speed unit.
                    scale = float(self.trainSpeed)/float(dist)
                    trainPt[0] += int((nextPt[0]-trainPt[0])*scale)
                    trainPt[1] += int((nextPt[1]-trainPt[1])*scale)



        else:  # Train stop at the station.
            self.dockCount -= 1
