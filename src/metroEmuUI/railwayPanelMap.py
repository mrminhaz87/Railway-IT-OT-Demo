#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        railWayPanelMap.py
#
# Purpose:     This module is used to display the top view of the main railway 
#              system current state.
# 
# Author:      Yuancheng Liu
#
# Version:     v0.1
# Created:     2023/06/01
# Copyright:   
# License:     
#-----------------------------------------------------------------------------
import wx
import math

import metroEmuGobal as gv

DEF_PNL_SIZE = (1600, 900)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelMap(wx.Panel):
    """ RailWay top view map"""
    def __init__(self, parent, panelSize=DEF_PNL_SIZE):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.bgColor = wx.Colour(30, 40, 62)
        self.SetBackgroundColour(self.bgColor)
        self.panelSize = panelSize
        self.toggle = False
        # Paint the map
        self.Bind(wx.EVT_PAINT, self.onPaint)
        # self.Bind(wx.EVT_LEFT_DOWN, self.onLeftClick)
        self.SetDoubleBuffered(True)  # Set the panel double buffer to void the panel flash during update.

#-----------------------------------------------------------------------------
    def _drawEnvItems(self, dc):
        """ Draw the environment items."""
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
        dc.SetBrush(wx.Brush(self.bgColor))
        dc.DrawRectangle(0, 0, w, h)
        for key, trackInfo in gv.iMapMgr.getTracks().items():
            dc.SetPen(wx.Pen(trackInfo['color'], width=4, style=wx.PENSTYLE_SOLID))
            trackPts = trackInfo['points']
            for i in range(len(trackPts)-1):
                fromPt, toPt = trackPts[i], trackPts[i+1]
                dc.DrawLine(fromPt[0], fromPt[1], toPt[0], toPt[1])
            # Connect the head and tail if the track is a circle:
            if trackInfo['type'] == gv.RAILWAY_TYPE_CYCLE: 
                fromPt, toPt = trackPts[0], trackPts[-1]
                dc.DrawLine(fromPt[0], fromPt[1], toPt[0], toPt[1])

#--PanelMap--------------------------------------------------------------------
    def _drawTrains_old(self, dc):
        """ Draw the trains on the map."""
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
        trainDict = gv.iMapMgr.getTrains()
        for key, val in trainDict.items():
            for i, train in enumerate(val):
                trainColor = '#CE8349' if train.emgStop else 'GREEN'
                dc.SetBrush(wx.Brush(trainColor))
                for point in train.getPos():
                    dc.DrawRectangle(point[0]-5, point[1]-5, 10, 10)
                # draw the train ID:
                dc.SetTextForeground(wx.Colour(trainColor))
                pos = train.getTrainPos(idx=0)
                dc.DrawText( key+'-'+str(i), pos[0]+5, pos[1]+5)

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
                dc.DrawText("S-"+str(id), x-10, y-25)
                dc.SetBrush(wx.Brush(color))
                dc.DrawRectangle(x-5, y-5, 10, 10)

#-----------------------------------------------------------------------------
    def _drawStation(self, dc):
        dc.SetPen(self.dcDefPen)
        dc.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        for key, stations in gv.iMapMgr.selfStations().items():
            colorCode = gv.iMapMgr.getTracks(trackID=key)['color']
            dc.SetTextForeground(colorCode)
            for station in stations:
                id = station.getID()
                pos = station.getPos()
                x, y = pos[0], pos[1]
                dc.SetPen(self.dcDefPen)
                dc.SetBrush(wx.Brush(colorCode))
                dc.DrawText(str(id), x-10, y-30)
                if station.getDockState():
                    dc.SetBrush(wx.Brush('BLUE'))
                    dc.DrawCircle(x, y, 8)
                    dc.SetPen(wx.Pen('BLUE', width=1, style=wx.PENSTYLE_SOLID))
                    dc.SetBrush(wx.Brush('BLUE', wx.TRANSPARENT))
                    dc.DrawRectangle(x-35, y-7, 70, 14)
                else:
                    dc.DrawCircle(x, y, 8)
                    dc.SetPen(wx.Pen(colorCode, width=1, style=wx.PENSTYLE_LONG_DASH))
                    dc.SetBrush(wx.Brush(colorCode, wx.TRANSPARENT))
                    dc.DrawRectangle(x-35, y-7, 70, 14)


    #--PanelMap--------------------------------------------------------------------
    def onPaint(self, event):
        """ Draw the whole panel by using the wx device context."""
        dc = wx.PaintDC(self)
        self.dcDefPen = dc.GetPen()
        # Draw all the components
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
        # Call the onPaint to update the map display.
        self.updateDisplay()
