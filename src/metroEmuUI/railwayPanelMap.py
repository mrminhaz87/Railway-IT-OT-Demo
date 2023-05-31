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
        # self.Bind(wx.EVT_LEFT_DOWN, self.onLeftClick)
        
        # Set the panel double buffer.
        self.SetDoubleBuffered(True)  # Avoid the panel flash during update.

#-----------------------------------------------------------------------------
    def _drawEnvItems(self, dc):
        dc.SetPen(self.dcDefPen)
        dc.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        dc.SetTextForeground(wx.Colour('White'))
        for item in gv.iMapMgr.getEnvItems():
            id = item.getID()
            pos = item.getPos()
            bitmap = item.getWxBitmap()
            size = item.getSize()
            dc.DrawBitmap(bitmap, pos[0]-size[0]//2, pos[1]-size[1]//2)
            dc.DrawText(str(id), pos[0]-size[0]//2, pos[1]-size[1]//2-15)

#-----------------------------------------------------------------------------
    def _drawRailWay(self, dc):
        """ Draw the background and the railway."""
        w, h = self.panelSize
        dc.SetBrush(wx.Brush(wx.Colour(30, 40, 62)))
        #dc.DrawBitmap(wx.Bitmap(gv.BGPNG_PATH), 1, 1) 
        dc.DrawRectangle(0, 0, w, h)
        for key, trackInfo in gv.iMapMgr.getTracks().items():
            dc.SetPen(wx.Pen(trackInfo['color'], width=4, style=wx.PENSTYLE_SOLID))
            trackPts = trackInfo['points']
            for i in range(len(trackPts)-1):
                fromPt, toPt = trackPts[i], trackPts[i+1]
                dc.DrawLine(fromPt[0], fromPt[1], toPt[0], toPt[1])
            fromPt, toPt = trackPts[0], trackPts[-1]
            if trackInfo['type'] == gv.RAILWAY_TYPE_CYCLE: dc.DrawLine(fromPt[0], fromPt[1], toPt[0], toPt[1])

#--PanelMap--------------------------------------------------------------------
    def _drawTrains_old(self, dc):
        """ Draw the 2 trains on the map."""
        dc.SetPen(self.dcDefPen)
        clashPt = None
        # Draw the train1 on the map.

        # dc.SetPen(wx.Pen(wx.Colour(52, 169, 129)))
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
        """ Draw the trains on the map."""
        dc.SetPen(self.dcDefPen)
        clashPt = None
        # Draw the trains on the map.
        trainDict = gv.iMapMgr.getTrains()
        for key, val in trainDict.items():
            for train in val:
                trainColor = '#CE8349' if train.emgStop else 'GREEN'
                dc.SetBrush(wx.Brush(trainColor))
                for point in train.getPos():
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
                if dir == gv.LAY_U:
                    y -= 15 
                elif dir == gv.LAY_D:
                    y += 15
                elif dir == gv.LAY_L:
                    x -= 15
                elif dir == gv.LAY_R:
                    x += 15
                dc.DrawLine(pos[0], pos[1], x, y)
                dc.DrawText("S"+str(id), x-10, y-25)
                dc.SetBrush(wx.Brush(color))
                dc.DrawRectangle(x-5, y-5, 10, 10)

#-----------------------------------------------------------------------------
    def _drawStation(self, dc):
        dc.SetPen(self.dcDefPen)
        dc.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        dc.SetBrush(wx.Brush('Blue'))
        for key, stations in gv.iMapMgr.selfStations().items():
            colorCode = gv.iMapMgr.getTracks(trackID=key)['color']
            dc.SetBrush(wx.Brush(colorCode))
            dc.SetTextForeground(colorCode)
            for station in stations:
                id = station.getID()
                pos = station.getPos()
                x, y = pos[0], pos[1]
                dc.DrawCircle(x, y, 8)
                dc.DrawText(str(id), x-10, y-25)

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
        self._drawStation(dc)
        self._drawEnvItems(dc)

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
