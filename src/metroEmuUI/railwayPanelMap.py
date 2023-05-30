#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        railWayPanelMap.py
#
# Purpose:     This module is used to show the top view of the  main city map in
#              the railway system.
#              
# Author:      Yuancheng Liu
#
# Created:     2019/07/01
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------
import wx
import math

from datetime import datetime
import metroEmuGobal as gv
import railwayMgr as dataMgr



DEF_PNL_SIZE = (1600, 900)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelMap(wx.Panel):
    """ RailWay top view map panel to show the rail way control situation."""
    def __init__(self, parent, panelSize=DEF_PNL_SIZE):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.SetBackgroundColour(wx.Colour(30, 40, 62))
        self.panelSize = panelSize
        self.toggle = False
        # temp init the data manager here:
        gv.iMapMgr = self.mapMgr = dataMgr.MapMgr(self)

        self.Bind(wx.EVT_PAINT, self.onPaint)
        #self.Bind(wx.EVT_LEFT_DOWN, self.onLeftClick)
        
        # Set the panel double buffer.
        self.SetDoubleBuffered(True)  # Avoid the panel flash during update.

#-----------------------------------------------------------------------------
    def _drawRailWay(self, dc):
        """ Draw the background and the railway."""
        w, h = self.panelSize
        dc.SetBrush(wx.Brush(wx.Colour(30, 40, 62)))
        #dc.DrawBitmap(wx.Bitmap(gv.BGPNG_PATH), 1, 1) 
        dc.DrawRectangle(0, 0, w, h)
        # draw the tracks
        trackA = gv.iMapMgr.getTrackA()
        dc.SetPen(wx.Pen(trackA['color'], width=4, style=wx.PENSTYLE_SOLID))
        trackAPts = trackA['points']

        for i in range(len(trackAPts)-1):
            fromPt, toPt = trackAPts[i], trackAPts[i+1]
            dc.DrawLine(fromPt[0], fromPt[1], toPt[0], toPt[1])
        fromPt, toPt = trackAPts[0], trackAPts[-1]
        if trackA['type'] == gv.RAILWAY_TYPE_CYCLE: dc.DrawLine(fromPt[0], fromPt[1], toPt[0], toPt[1])

        trackB = gv.iMapMgr.getTrackB()
        dc.SetPen(wx.Pen(trackB['color'], width=4, style=wx.PENSTYLE_SOLID))
        trackBPts = trackB['points']

        for i in range(len(trackBPts)-1):
            fromPt, toPt = trackBPts[i], trackBPts[i+1]
            dc.DrawLine(fromPt[0], fromPt[1], toPt[0], toPt[1])
        fromPt, toPt = trackBPts[0], trackBPts[-1]
        dc.DrawLine(fromPt[0], fromPt[1], toPt[0], toPt[1])


        trackC = gv.iMapMgr.getTrackC()
        dc.SetPen(wx.Pen(trackC['color'], width=4, style=wx.PENSTYLE_SOLID))
        trackCPts = trackC['points']

        for i in range(len(trackCPts)-1):
            fromPt, toPt = trackCPts[i], trackCPts[i+1]
            dc.DrawLine(fromPt[0], fromPt[1], toPt[0], toPt[1])
        fromPt, toPt = trackCPts[0], trackCPts[-1]
        dc.DrawLine(fromPt[0], fromPt[1], toPt[0], toPt[1])


#--PanelMap--------------------------------------------------------------------
    def _drawTrains_old(self, dc):
        """ Draw the 2 trains on the map."""
        dc.SetPen(self.dcDefPen)
        clashPt = None
        # Draw the train1 on the map.

        #dc.SetPen(wx.Pen(wx.Colour(52, 169, 129)))

        
        # dirList = self.mapMgr.trainA.getDirs()
        # #bitmap = wx.Bitmap(gv.gTrainImgB)
        # gc = wx.GraphicsContext.Create(dc)
        # gc.SetBrush(wx.Brush(trainColor))
        # for i, point in enumerate( self.mapMgr.trainA.getPos()):
        #      gc.PushState()
        #      gc.Translate(point[0], point[1])
        #      gc.Rotate(dirList[i])
        #      gc.DrawRectangle(-5, -5, 10, 10)
        #      if i == 0 or i == 4:
        #          gc.DrawBitmap(wx.Bitmap(gv.gTrainImgB), -5, -5, 10, 10)
        # #     else:
        # #         gc.DrawBitmap(bitmap, -5, -5, 10, 10)
        #      gc.PopState()
        for point in self.mapMgr.trainA.getPos():
            dc.DrawRectangle(point[0]-5, point[1]-5, 10, 10)
        # Draw the train2 on the map.

#-----------------------------------------------------------------------------
    def _drawTrains(self, dc):
        """ Draw the 2 trains on the map."""
        dc.SetPen(self.dcDefPen)
        clashPt = None
        # Draw the train1 on the map.

        #dc.SetPen(wx.Pen(wx.Colour(52, 169, 129)))
        #trainColor = 'RED' if self.mapMgr.trainA.emgStop else '#CE8349'
        #dc.SetBrush(wx.Brush(trainColor))
        trainDict = gv.iMapMgr.getTrains()
        for key, val in trainDict.items(): 
            for train in val:
                trainColor = 'RED' if train.emgStop else 'GREEN'
                dc.SetBrush(wx.Brush(trainColor))
                for point in  train.getPos():
                    dc.DrawRectangle(point[0]-5, point[1]-5, 10, 10)

#-----------------------------------------------------------------------------
    def _drawSensors(self, dc):
        dc.SetPen(self.dcDefPen)
        dc.SetFont(wx.Font(7, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        dc.SetBrush(wx.Brush('GRAY'))
        for key, sensorAgent in gv.iMapMgr.getSensors().items():
            sensorId = sensorAgent.getID()
            sensorPos = sensorAgent.getPos()
            sensorState = sensorAgent.getSensorsState()
            dc.SetTextForeground(wx.Colour('White'))
            for i in range(sensorAgent.getSensorCount()):
                pos = sensorPos[i]
                dc.DrawText(sensorId+"-s"+str(i), pos[0]+3, pos[1]+3)
                state = sensorState[i]
                if state:
                    color = 'YELLOW' if self.toggle else 'BLUE'
                    dc.SetBrush(wx.Brush(color))
                    dc.DrawRectangle(pos[0]-4, pos[1]-4, 8, 8)
                    dc.SetBrush(wx.Brush('GRAY'))
                else:
                    dc.DrawRectangle(pos[0]-4, pos[1]-4, 8, 8)

#-----------------------------------------------------------------------------
    def _drawSignals(self, dc):
        dc.SetPen(self.dcDefPen)
        dc.SetFont(wx.Font(7, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        dc.SetBrush(wx.Brush('Green'))
        for key, signals in gv.iMapMgr.getSignals().items():
            for signalAgent in signals:
                id = signalAgent.getID()
                pos = signalAgent.getPos()
                state = signalAgent.getState()
                dir = signalAgent.dir
                color = 'RED' if state else 'GREEN'
                dc.SetPen(wx.Pen(color, width=2, style=wx.PENSTYLE_SOLID))
                x, y = pos[0], pos[1]
                if dir == 0:
                    y -= 15 
                elif dir ==1:
                    y += 15
                elif dir == 2:
                    x -= 15
                elif dir == 3:
                    x += 15
                dc.DrawLine(pos[0], pos[1], x, y)
                dc.DrawText("S"+str(id), x-10, y-25)
                dc.SetBrush(wx.Brush(color))
                dc.DrawRectangle(x-5, y-5, 11, 11)

    #--PanelMap--------------------------------------------------------------------
    def onPaint(self, event):
        """ Draw the whole panel by using the wx device context."""
        dc = wx.PaintDC(self)

        self.dcDefPen = dc.GetPen()
        # Draw the railway as background.
        self._drawRailWay(dc)
        self._drawTrains(dc)
        self._drawSensors(dc)
        self._drawSignals(dc)

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
        # Update the mapManger's periodic function.
        self.mapMgr.periodic(now)

        # Call the onPaint to update the map display.
        self.updateDisplay()