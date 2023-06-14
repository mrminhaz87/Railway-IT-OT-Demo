#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        hmiPanelMap.py
#
# Purpose:     This module is used to display the top view of the main railway 
#              system current state.
# 
# Author:      Yuancheng Liu
#
# Version:     v0.1
# Created:     2023/06/13
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

import os
import wx
import math

import scadaGobal as gv

DEF_PNL_SIZE = (1750, 480)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelMap(wx.Panel):
    """ RailWay top view map"""
    def __init__(self, parent, panelSize=DEF_PNL_SIZE):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.bgColor = wx.Colour(30, 40, 62)
        self.SetBackgroundColour(self.bgColor)
        self.panelSize = panelSize
        #self.bitMaps = self._loadBitMaps()
        self.toggle = False
        # Paint the map
        self.Bind(wx.EVT_PAINT, self.onPaint)
        # self.Bind(wx.EVT_LEFT_DOWN, self.onLeftClick)
        self.SetDoubleBuffered(True)  # Set the panel double buffer to void the panel flash during update.

#-----------------------------------------------------------------------------
    def _drawRailWay(self, dc):
        """ Draw the background and the railway."""
        w, h = self.panelSize
        dc.SetBrush(wx.Brush(self.bgColor))
        dc.DrawRectangle(0, 0, w, h)
        trackSeq = ('weline', 'ccline', 'nsline')

        for i, trackName in enumerate(trackSeq):
            color = gv.gTrackConfig[trackName]['color']
            dc.SetPen(wx.Pen(color, width=4, style=wx.PENSTYLE_SOLID))
            dc.DrawLine(50, 100+160*i, 1700, 100+160*i,)

    def _drawSensors(self, dc):
        dc.SetPen(self.dcDefPen)
        dc.SetFont(wx.Font(7, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        dc.SetBrush(wx.Brush('GRAY'))
        for key, sensorAgent in gv.iMapMgr.getSensors().items():
            sensorId = sensorAgent.getID()
            sensorInfoList = sensorAgent.getSensorsInfo()
            dc.SetTextForeground(wx.Colour('White'))
            for i, sensorInfo in enumerate(sensorInfoList):
                pos = sensorInfo['pos']
                dc.DrawText(sensorId+"-s"+str(i), pos[0]+3, pos[1]+3)
                state = sensorInfo['state']
                if state:
                    color = 'YELLOW' if self.toggle else 'BLUE'
                    dc.SetBrush(wx.Brush(color))
                    dc.DrawRectangle(pos[0]-4, pos[1]-4, 8, 8)
                    dc.SetBrush(wx.Brush('GRAY'))
                else:
                    dc.DrawRectangle(pos[0]-4, pos[1]-4, 8, 8)


    #--PanelMap--------------------------------------------------------------------
    def onPaint(self, event):
        """ Draw the whole panel by using the wx device context."""
        dc = wx.PaintDC(self)
        self.dcDefPen = dc.GetPen()
        # Draw all the components
        self._drawRailWay(dc)
        self._drawSensors(dc)

    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function
            will set the self update flag.
        """
        self.Refresh(False)
        self.Update()
        self.toggle = not self.toggle

#--PanelMap--------------------------------------------------------------------
    def periodic(self , now):
        """ periodicly call back to do needed calcualtion/panel update"""
        # Call the onPaint to update the map display.
        
        self.updateDisplay()
