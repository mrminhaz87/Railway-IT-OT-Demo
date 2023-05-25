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
# License:     YC
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
        self.trackA = {
            'name' : 'WE Line',
            'color': wx.Colour(52, 169, 129),
            'points': [(50, 400), (1550, 400), (1550, 500), (50, 500)]
        }
        headPosA = (50, 400)
        self.trainA = agent.AgentTrain(self, 0, headPosA, self.trackA['points'])

        self.trackB = {
            'name' : 'NS Line',
            'color': wx.Colour(233, 0, 97),
            'points': [(750, 50), (850, 50), (850, 850), (750, 850)]
        }

        self.trackC = {
            'name' : 'Cycler Line',
            'color': wx.Colour(255, 136, 0),
            'points': [(200, 200), (1400, 200), (1400, 700), (200, 700)]
        }

    def getTrackA(self):
        return self.trackA
        
    def getTrackB(self):
        return self.trackB
    
    def getTrackC(self):
        return self.trackC
    
    def periodic(self , now):
        """ Periodicly call back function."""
        # update the trains position.
        self.trainA.updateTrainPos()