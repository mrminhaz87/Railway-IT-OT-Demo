#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        railWayPanel.py
#
# Purpose:     This module is used to provide different function panels for the 
#              rail way hub function.
#              
# Author:      Yuancheng Liu
#
# Version:     v0.1
# Created:     2023/06/01
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

import os 
import wx
import metroEmuGobal as gv

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

class PanelTainCtrl(wx.Panel):
    """ Train control Panel control panel."""

    def __init__(self, parent, trackID, trainID, bgColor=wx.Colour(200, 210, 200)):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(bgColor)
        self.trackID = trackID
        self.trainID = trainID
        self.SetSizer(self._buidUISizer())

#-----------------------------------------------------------------------------
    def _buidUISizer(self):
        """ build the control panel sizer. """
        flagsL = wx.LEFT
        startBmp = wx.Bitmap(os.path.join(gv.IMG_FD, 'reset32.png'), wx.BITMAP_TYPE_ANY)
        stoptBmp = wx.Bitmap(os.path.join(gv.IMG_FD, 'emgStop32.png'), wx.BITMAP_TYPE_ANY)
        font = wx.Font(11, wx.DECORATIVE, wx.BOLD, wx.BOLD)
        vbox = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, label="Train: %s - %s" %(self.trackID, str(self.trainID)))
        label.SetFont(font)
        label.SetForegroundColour(wx.WHITE)
        vbox.Add(label, flag=flagsL, border=2)

        vbox.Add(wx.StaticLine(self, wx.ID_ANY, size=(136, -1),
                                 style=wx.LI_HORIZONTAL), flag=flagsL, border=2)
        vbox.AddSpacer(5)
        hbox0 =  wx.BoxSizer(wx.HORIZONTAL)
        # Add the start button.
        self.recbtn1 = wx.BitmapButton(self, bitmap=startBmp,
                                       size=(startBmp.GetWidth()+10, startBmp.GetHeight()+10))
        self.recbtn1.Bind(wx.EVT_BUTTON, self.startTrain)

        hbox0.Add(self.recbtn1, flag=flagsL, border=2)
        hbox0.AddSpacer(5)
        # Add the start button.
        self.recbtn2 = wx.BitmapButton(self, bitmap=stoptBmp,
                                       size=(stoptBmp.GetWidth()+10, stoptBmp.GetHeight()+10))
        self.recbtn2.Bind(wx.EVT_BUTTON, self.stopTrain)
        hbox0.Add(self.recbtn2, flag=flagsL, border=2)
        hbox0.AddSpacer(5)
        vbox.Add(hbox0, flag=flagsL, border=2)
        return vbox
    
    #-----------------------------------------------------------------------------
    def startTrain(self, event):
        event.GetEventObject().GetId() 
        if gv.iMapMgr:
            gv.gDebugPrint('Start train: %s on track: %s' %(str(self.trainID), self.trackID))
            trains = gv.iMapMgr.getTrains(trackID=self.trackID)
            trainAgent = trains[self.trainID]
            trainAgent.setTrainSpeed(10)
            trainAgent.setEmgStop(False)

    #-----------------------------------------------------------------------------
    def stopTrain(self, event):
        if gv.iMapMgr:
            gv.gDebugPrint('Stop train: %s on track: %s' %(str(self.trainID), self.trackID))
            trains = gv.iMapMgr.getTrains(trackID=self.trackID)
            trainAgent = trains[self.trainID]
            trainAgent.setTrainSpeed(0)
            trainAgent.setEmgStop(True)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    """ Main function used for local test debug panel. """

    print('Test Case start: type in the panel you want to check:')
    print('0 - PanelImge')
    print('1 - PanelCtrl')
    #pyin = str(input()).rstrip('\n')
    #testPanelIdx = int(pyin)
    testPanelIdx = 0    # change this parameter for you to test.
    print("[%s]" %str(testPanelIdx))
    app = wx.App()
    mainFrame = wx.Frame(gv.iMainFrame, -1, 'Debug Panel',
                         pos=(300, 300), size=(640, 480), style=wx.DEFAULT_FRAME_STYLE)
    if testPanelIdx == 0:
        testPanel = PanelTainCtrl(mainFrame, 'weline', 1, bgColor=wx.Colour(52, 169, 129))
    elif testPanelIdx == 1:
        testPanel = PanelCtrl(mainFrame)
    mainFrame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()

