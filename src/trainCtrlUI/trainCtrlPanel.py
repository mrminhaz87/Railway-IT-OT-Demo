#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        trainCtrl.py
#
# Purpose:     This module is used to create different function panels for the 
#              train control HMI.
#
# Author:      Yuancheng Liu
#
# Created:     2023/07/12
# Version:     v0.1.2
# Copyright:   Copyright (c) 2023 LiuYuancheng
# License:     MIT License  
#-----------------------------------------------------------------------------

import os
import wx
import wx.grid

import trainCtrlGlobal as gv

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class PanelTrain(wx.Panel):
    """ Mutli-information display panel used to show all the trains' name, speed 
        current voltage and power state.
    """
    def __init__(self, parent):
        """ Init the panel."""
        wx.Panel.__init__(self, parent, size=(650, 300))
        self.SetBackgroundColour(wx.Colour(39, 40, 62))
        self.SetSizer(self._buidUISizer())

#------------------------------------------------------------------------------
    def _buidUISizer(self):
        """ Build the UI sizer with the information grid"""
        sizer = wx.BoxSizer(wx.VERTICAL)
        flagsL = wx.LEFT
        sizer.AddSpacer(5)
        # Row 0: Set the panel label
        font = wx.Font(12, wx.DECORATIVE, wx.BOLD, wx.BOLD)
        label = wx.StaticText(self, label="Trains Information")
        label.SetFont(font)
        label.SetForegroundColour(wx.Colour("WHITE"))
        sizer.Add(label, flag=flagsL, border=2)
        sizer.AddSpacer(10)
        # Row 1: set the information display grid
        self.grid = wx.grid.Grid(self, -1)
        self.grid.CreateGrid(12, 6)
        # Set the Grid size.
        self.grid.SetRowLabelSize(40)
        # Set the Grid's labels.
        self.grid.SetColLabelValue(0, 'Train-ID')
        self.grid.SetColLabelValue(1, 'Railway-ID')
        self.grid.SetColLabelValue(2, 'Speed[km/h]')
        self.grid.SetColSize(2, 100)
        self.grid.SetColLabelValue(3, 'Current[A]')
        self.grid.SetColSize(3, 100)
        self.grid.SetColLabelValue(4, 'DC-Voltage[V]')
        self.grid.SetColSize(4, 120)
        self.grid.SetColLabelValue(5, 'Power-State')
        self.grid.SetColSize(5, 120)
        sizer.Add(self.grid, flag=flagsL, border=2)
        return sizer

#------------------------------------------------------------------------------
    def updateTrainInfoGrid(self):
        """ update the trains information grid.
        """
        lineIdx = 0
        for key in gv.gTrackConfig.keys():
            trainsInfo = gv.iMapMgr.getTrainsInfo(key)
            colorVal = gv.gTrackConfig[key]['color']
            for data in trainsInfo:
                self.grid.SetCellValue(lineIdx, 0, ' '+ str(data['id']))
                self.grid.SetCellValue(lineIdx, 1, key)
                self.grid.SetCellBackgroundColour(lineIdx, 1, colorVal)
                self.grid.SetCellValue(lineIdx, 2, ' '+ str(data['speed']) + ' km/h')
                self.grid.SetCellValue(lineIdx, 3, ' '+ str(data['current']) + ' A')
                self.grid.SetCellValue(lineIdx, 4, ' '+ str(data['voltage']) + ' V')
                pwdFlg = 'ON' if data['power'] else 'OFF'
                bgColor = wx.Colour('GREEN') if data['power'] else wx.Colour('RED')
                self.grid.SetCellValue(lineIdx, 5, ' '+ str(pwdFlg))
                self.grid.SetCellBackgroundColour(lineIdx, 5, bgColor)
                lineIdx += 1
        self.grid.ForceRefresh()  # refresh all the grid's cell at one time 

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelPLC(wx.Panel):
    """ PLC panel UI to show PLC input feedback state and the relay connected 
        to the related output pin.
    """
    def __init__(self, parent, name, ipAddr):
        """ Init the panel."""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(200, 200, 200))
        # Init self paremeters
        self.plcName = name
        self.ipAddr = ipAddr
        self.regsNum = 16
        self.coilsNum = 8
        self.connectedFlg = False
        self.gpioInList = [0]*self.regsNum  # PLC GPIO input stuation list.
        self.gpioInLbList = []  # GPIO input device <id> label list.
        self.gpioOuList = [0]*self.coilsNum # PLC GPIO output situation list.
        self.gpioOuLbList = []  # GPIO output device <id> label list.
        # Init the UI.
        self.SetSizer(self.buidUISizer())
        #self.Layout() # must call the layout if the panel size is set to fix.

#--PanelPLC--------------------------------------------------------------------
    def buidUISizer(self):
        """ Build the UI and the return the wx.sizer. """
        mSizer = wx.BoxSizer(wx.VERTICAL) # main sizer
        flagsR = wx.LEFT
        mSizer.AddSpacer(5)
        # Row idx = 0 : set the basic PLC informaiton.
        self.nameLb = wx.StaticText(self, label=" PLC Name: ".ljust(15)+self.plcName)
        mSizer.Add(self.nameLb, flag=flagsR, border=5)
        self.ipaddrLb = wx.StaticText( self, label=" PLC IPaddr: ".ljust(15)+self.ipAddr)
        mSizer.Add(self.ipaddrLb, flag=flagsR, border=5)
        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        hbox0.Add(wx.StaticText(self, label="Connection:".ljust(15)), flag=flagsR, border=5)
        self.connLb = wx.StaticText(self, label='Connected' if self.connectedFlg else 'Unconnected')
        self.connLb.SetBackgroundColour( wx.Colour('GREEN') if self.connectedFlg else wx.Colour(120, 120, 120))
        hbox0.Add(self.connLb, flag=flagsR, border=5)
        mSizer.Add(hbox0, flag=flagsR, border=5)
        mSizer.AddSpacer(10)
        # Row idx = 1: set the GPIO and feed back of the PLC. 
        mSizer.Add(wx.StaticLine(self, wx.ID_ANY, size=(220, -1),
                                 style=wx.LI_HORIZONTAL), flag=flagsR, border=5)
        mSizer.AddSpacer(10)
        # - row line structure: Input indicator | output label | output button with current status.
        for i in range(self.regsNum):
            hsizer = wx.BoxSizer(wx.HORIZONTAL)
            # Col idx = 0: PLC input indicators.
            lbtext = " R_%H 0."+str(i)
            inputLb = wx.StaticText(self, label=lbtext.ljust(12))
            inputLb.SetBackgroundColour(wx.Colour(120, 120, 120))
            hsizer.Add(inputLb, flag=flagsR, border=5)
            self.gpioInLbList.append(inputLb)
            # Col idx =1: PLC output labels.
            hsizer.AddSpacer(15)
            if i < self.coilsNum:
                hsizer.Add(wx.StaticText(self, label=str(
                    " %Q 0."+str(i)+':').ljust(12)), flag=flagsR, border=5)
                # Col idx =2: PLC output ON/OFF contorl buttons.
                hsizer.AddSpacer(5)
                outputBt = wx.Button(self, label='OFF', size=(50, 17), name=self.plcName+':'+str(i))
                self.gpioOuLbList.append(outputBt)
                hsizer.Add(outputBt, flag=flagsR, border=5)
            mSizer.Add(hsizer, flag=flagsR, border=5)
            mSizer.AddSpacer(3)
        return mSizer

#--PanelPLC--------------------------------------------------------------------
    def setConnection(self, state):
        """ Update the connection state on the UI."""
        self.connectedFlg = state
        self.connLb.SetLabel('Connected' if self.connectedFlg else 'Unconnected')
        self.connLb.SetBackgroundColour(
            wx.Colour('GREEN') if self.connectedFlg else wx.Colour(120, 120, 120))
        self.Refresh(False)

#--PanelPLC--------------------------------------------------------------------
    def updateHoldingRegs(self, regList):
        """ Update the holding register's data and UI indicator's state if there 
            is new register chagne.
        """
        if regList is None or self.gpioInList == regList: return # no new update
        for idx in range(min(self.regsNum, len(regList))):
            status = regList[idx]
            if self.gpioInList[idx] != status:
                self.gpioInList[idx] = status
                self.gpioInLbList[idx].SetBackgroundColour(
                    wx.Colour('GREEN') if status else wx.Colour(120, 120, 120))

    def updateCoils(self, coilsList):
        if coilsList is None or self.gpioOuList == coilsList: return  
        for idx in range(min(self.coilsNum, len(coilsList))):
            status = coilsList[idx]
            if self.gpioOuList[idx] != status:
                self.gpioOuList[idx] = status
                self.gpioOuLbList[idx].SetLabel('ON' if status else 'OFF')
                self.gpioOuLbList[idx].SetBackgroundColour(
                    wx.Colour('GREEN') if status else wx.Colour(253, 253, 253))

    def updataPLCdata(self):
        if gv.idataMgr:
            plcdata =  gv.idataMgr.getPLCInfo(self.plcName)
            if plcdata:
                self.updateHoldingRegs(plcdata[0])
                self.updateCoils(plcdata[1])

    
    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function
            will set the self update flag.
        """
        self.Refresh(False)

#--PanelPLC--------------------------------------------------------------------
    def updateInput(self, idx, status): 
        """ Update the input state for each PLC input indicator."""
        if idx >= 8 or not status in [0,1]: 
            print("PLC panel:   the input parameter is not valid") 
            return
        elif self.gpioInList[idx] != status:
            self.gpioInList[idx] = status
            # Change the indicator status.
            self.gpioInLbList[idx].SetBackgroundColour(
                wx.Colour('GREEN') if status else wx.Colour(120, 120, 120))
            self.Refresh(False) # needed after the status update.

#--PanelPLC--------------------------------------------------------------------
    def updateOutput(self, idx, status):
        """ Update the output state for each PLC output button."""
        if idx >= 8 or not status in [0,1]: 
            print("PLC panel:   the output parameter is not valid") 
            return
        elif self.gpioOuList[idx] != status:
            self.gpioOuList[idx] = status
            [lbtext, color] = ['ON', wx.Colour('Green')] if status else [
            'OFF', wx.Colour(200, 200, 200)]
            self.gpioOuLbList[idx].SetLabel(lbtext)
            self.gpioOuLbList[idx].SetBackgroundColour(color)
            self.Refresh(False) # needed after the status update.

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
        label = wx.StaticText(self, label=" %s - %s" %(self.trackID, str(self.trainID)))
        label.SetFont(font)
        label.SetForegroundColour(wx.WHITE)
        vbox.Add(label, flag=flagsL, border=2)

        vbox.Add(wx.StaticLine(self, wx.ID_ANY, size=(90, -1),
                                 style=wx.LI_HORIZONTAL), flag=flagsL, border=2)
        vbox.AddSpacer(2)
        hbox0 =  wx.BoxSizer(wx.HORIZONTAL)
        # Add the start button.
        self.recbtn1 = wx.BitmapButton(self, bitmap=startBmp,
                                       size=(startBmp.GetWidth()+10, startBmp.GetHeight()+10))
        self.recbtn1.Bind(wx.EVT_BUTTON, self.turnOnTrainPwr)
        hbox0.Add(self.recbtn1, flag=flagsL, border=2)
        # Add the emergency stop button.
        self.recbtn2 = wx.BitmapButton(self, bitmap=stoptBmp,
                                       size=(stoptBmp.GetWidth()+10, stoptBmp.GetHeight()+10))
        self.recbtn2.Bind(wx.EVT_BUTTON, self.turnOffTrain)
        hbox0.Add(self.recbtn2, flag=flagsL, border=2)
        hbox0.AddSpacer(5)
        vbox.Add(hbox0, flag=flagsL, border=2)
        return vbox
    
    #-----------------------------------------------------------------------------
    def turnOnTrainPwr(self, event):
        gv.gDebugPrint(' Turn on train power: %s on track: %s' %(str(self.trainID), self.trackID))
        if gv.idataMgr:
            TrainTgtPlcID = 'PLC-06'
            startIdx = gv.gTrackConfig[self.trackID]['trainCoilIdx'][0]
            idx = startIdx + int(self.trainID)
            gv.idataMgr.setPlcCoilsData(TrainTgtPlcID, idx, True)

    #-----------------------------------------------------------------------------
    def turnOffTrain(self, event):
        gv.gDebugPrint(' Turn off train power: %s on track: %s' %(str(self.trainID), self.trackID))
        if gv.idataMgr:
            TrainTgtPlcID = 'PLC-06'
            startIdx = gv.gTrackConfig[self.trackID]['trainCoilIdx'][0]
            idx = startIdx + int(self.trainID)
            gv.idataMgr.setPlcCoilsData(TrainTgtPlcID, idx, False)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelCtrl(wx.Panel):
    """ Function control panel."""

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        self.gpsPos = None
        self.SetSizer(self._buidUISizer())

#--PanelCtrl-------------------------------------------------------------------
    def _buidUISizer(self):
        """ build the control panel sizer. """
        flagsR = wx.CENTER
        ctSizer = wx.BoxSizer(wx.VERTICAL)
        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        ctSizer.AddSpacer(5)
        # Row idx 0: show the search key and map zoom in level.
        hbox0.Add(wx.StaticText(self, label="Control panel".ljust(15)),
                  flag=flagsR, border=2)
        ctSizer.Add(hbox0, flag=flagsR, border=2)
        return ctSizer

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    """ Main function used for local test debug panel. """

    print('Test Case start: type in the panel you want to check:')
    print('0 - PanelImge')
    print('1 - PanelCtrl')
    #pyin = str(input()).rstrip('\n')
    #testPanelIdx = int(pyin)
    testPanelIdx = 1    # change this parameter for you to test.
    print("[%s]" %str(testPanelIdx))
    app = wx.App()
    mainFrame = wx.Frame(gv.iMainFrame, -1, 'Debug Panel',
                         pos=(300, 300), size=(640, 480), style=wx.DEFAULT_FRAME_STYLE)
    if testPanelIdx == 0:
        testPanel = PanelImge(mainFrame)
    elif testPanelIdx == 1:
        testPanel = PanelTrain(mainFrame)
    mainFrame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()



