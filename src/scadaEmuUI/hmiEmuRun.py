#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        hmiEmuRun.py
#
# Purpose:     This module is the main wx-frame for the Human Machine Interface
#              of metro railway and signal SCADA sysetm.
#
# Author:      Yuancheng Liu
#
# Version:     v0.1
# Created:     2023/06/13
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

import os
import sys
import time
import wx
import scadaGobal as gv

import hmiPanel as pnlFunction
import hmiMgr as mapMgr
import hmiPanelMap as pnlMap
import scadaDataMgr as dataMgr

PERIODIC = 500      # update in every 500ms
FRAME_SIZE = (1800, 1000)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class UIFrame(wx.Frame):
    """ Main UI frame window."""

    def __init__(self, parent, id, title):
        """ Init the UI and parameters """
        wx.Frame.__init__(self, parent, id, title, size=FRAME_SIZE)
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        #self.SetTransparent(gv.gTranspPct*255//100)
        self.SetIcon(wx.Icon(gv.ICO_PATH))
        self._initGlobals()
        # Build UI sizer
        self.SetSizer(self._buidUISizer())
        self.updateLock = False
        if not gv.TEST_MD:
            gv.idataMgr = dataMgr.DataManager(self, gv.gPlcInfo)
        # Set the periodic call back
        self.lastPeriodicTime = time.time()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.periodic)
        self.timer.Start(PERIODIC)  # every 500 ms

    def _initGlobals(self):
        # Init the global parameters used only by this module
        gv.gTrackConfig['weline'] = {'id':'weline', 'sensorIdx': (0, 17), 'signalIdx':(0, 8), 'color': wx.Colour(52, 169, 129), 'icon': 'welabel.png'}
        gv.gTrackConfig['nsline'] = {'id':'nsline', 'sensorIdx': (17, 25), 'signalIdx':(8, 12), 'color': wx.Colour(233, 0, 97), 'icon': 'nslabel.png'}
        gv.gTrackConfig['ccline'] = {'id':'ccline', 'sensorIdx': (25, 39), 'signalIdx':(12, 19), 'color': wx.Colour(255, 136, 0), 'icon': 'cclabel.png'}
        # Init all the global instance
        gv.iMapMgr = mapMgr.MapMgr(self)

#--UIFrame---------------------------------------------------------------------
    def _buidUISizer(self):
        """ Build the main UI Sizer. """
        flagsL = wx.LEFT
        mSizer = wx.BoxSizer(wx.VERTICAL)
        mSizer.AddSpacer(5)
        font = wx.Font(12, wx.DECORATIVE, wx.BOLD, wx.BOLD)
        label = wx.StaticText(self, label="Railway HMI")
        label.SetFont(font)
        mSizer.Add(label, flag=flagsL, border=2)
        mSizer.AddSpacer(10)
        gv.iMapPanel = self.mapPanel = pnlMap.PanelMap(self)
        mSizer.Add(gv.iMapPanel, flag=flagsL, border=2)
        mSizer.AddSpacer(10)
        mSizer.Add(wx.StaticLine(self, wx.ID_ANY, size=(1790, -1),
                                style=wx.LI_HORIZONTAL), flag=flagsL, border=5)

        mSizer.AddSpacer(5)
        label2 = wx.StaticText(self, label="PLC Panels")
        label2.SetFont(font)
        mSizer.Add(label2, flag=flagsL, border=2)
        mSizer.AddSpacer(5)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.plcPnls = {}
        for key, val in gv.gPlcPnlInfo.items():
            hbox1.AddSpacer(10)
            ipaddr = val['ipaddress'] + ' : ' + str(val['port'])
            self.plcPnls[key] = pnlFunction.PanelPLC(self, val['label'], ipaddr)
            hbox1.Add(self.plcPnls[key], flag=flagsL, border=2)
        
        mSizer.Add(hbox1, flag=flagsL, border=2)
        return mSizer

#--UIFrame---------------------------------------------------------------------
    def periodic(self, event):
        """ Call back every periodic time."""
        now = time.time()
        if (not self.updateLock) and now - self.lastPeriodicTime >= gv.gUpdateRate:
            print("main frame update at %s" % str(now))
            self.lastPeriodicTime = now
            if not gv.TEST_MD:
                if gv.idataMgr: gv.idataMgr.periodic(now)
                # update the PLC display panel
                for key in self.plcPnls.keys():
                    # update the holding registers
                    tgtPlcID = gv.gPlcPnlInfo[key]['tgt']
                    rsIdx, reIdx = gv.gPlcPnlInfo[key]['hRegsInfo']
                    registList = gv.idataMgr.getPlcHRegsData(tgtPlcID, rsIdx, reIdx)
                    print(registList)
                    self.plcPnls[key].updateHoldingRegs(registList)
                    csIdx, ceIdx = gv.gPlcPnlInfo[key]['coilsInfo']
                    coilsList = gv.idataMgr.getPlcCoilsData(tgtPlcID, csIdx, ceIdx)
                    print(coilsList)
                    self.plcPnls[key].updateCoils(coilsList)
                    self.plcPnls[key].updateDisplay()
                
                for key in gv.gTrackConfig.keys():
                    tgtPlcID = 'PLC-00'
                    rsIdx, reIdx = gv.gTrackConfig[key]['sensorIdx']
                    registList = gv.idataMgr.getPlcHRegsData(tgtPlcID, rsIdx, reIdx)
                    print(key)
                    gv.iMapMgr.setSensors(key, registList)
                    csIdx, ceIdx = gv.gTrackConfig[key]['signalIdx']
                    coilsList = gv.idataMgr.getPlcCoilsData(tgtPlcID, csIdx, ceIdx)
                    gv.iMapMgr.setSingals(key, coilsList)


            self.mapPanel.periodic(now)


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class MyApp(wx.App):
    def OnInit(self):
        gv.iMainFrame = UIFrame(None, -1, gv.APP_NAME[0])
        gv.iMainFrame.Show(True)
        return True

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()
