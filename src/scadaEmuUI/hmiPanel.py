#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        uiPanel.py
#
# Purpose:     This module is used to create different function panels.
# Author:      Yuancheng Liu
#
# Created:     2020/01/10
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------
import wx

from datetime import datetime
import scadaGobal as gv

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

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
        self.connLb = wx.StaticText(self, label=' Connected ' if self.connectedFlg else ' Unconnected ')
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
        self.connLb.SetLabel(' Connected ' if self.connectedFlg else ' Unconnected ')
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

#--PanelPLC--------------------------------------------------------------------
    def updateCoils(self, coilsList):
        """ Update the coils data and UI indicator's state if there is new coils
            state chagne.
        """
        if coilsList is None or self.gpioOuList == coilsList: return  
        for idx in range(min(self.coilsNum, len(coilsList))):
            status = coilsList[idx]
            if self.gpioOuList[idx] != status:
                self.gpioOuList[idx] = status
                self.gpioOuLbList[idx].SetLabel('ON' if status else 'OFF')
                self.gpioOuLbList[idx].SetBackgroundColour(
                    wx.Colour('GREEN') if status else wx.Colour(253, 253, 253))

#--PanelPLC--------------------------------------------------------------------
    def updataPLCdata(self):
        if gv.idataMgr:
            plcdata =  gv.idataMgr.getPLCInfo(self.plcName)
            if plcdata:
                self.updateHoldingRegs(plcdata[0])
                self.updateCoils(plcdata[1])

#--PanelPLC--------------------------------------------------------------------
    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function
            will set the self update flag.
        """
        self.Refresh(False)

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
        testPanel = PanelPLC(mainFrame, 'plc1', '127.0.0.1:502')
    elif testPanelIdx == 1:
        testPanel = PanelCtrl(mainFrame)
    mainFrame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()



