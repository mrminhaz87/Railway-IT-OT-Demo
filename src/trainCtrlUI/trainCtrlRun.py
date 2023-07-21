#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        uiRun.py
#
# Purpose:     This module is used as a sample to create the main wx frame.
#
# Author:      Yuancheng Liu
#
# Created:     2019/01/10
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------

import os
import sys
import time
import wx
import trainCtrlGlobal as gv
import trainCtrlPanel as pnlFunction
import trainDataMgr as dataMgr

PERIODIC = 500      # update in every 500ms
FRAME_SIZE = (1200, 650)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class UIFrame(wx.Frame):
    """ Main UI frame window."""
    def __init__(self, parent, id, title):
        """ Init the UI and parameters """
        wx.Frame.__init__(self, parent, id, title, size=FRAME_SIZE)
        # No boader frame:
        self.SetBackgroundColour(wx.Colour(39, 40, 62))
        self.SetIcon(wx.Icon(gv.ICO_PATH))
        #self.SetTransparent(gv.gTranspPct*255//100)
        self._initGlobals()
        
        # Build UI sizer
        self._buildMenuBar()
        self.SetSizer(self._buidUISizer())
        self.updateLock = False
        if not gv.TEST_MD:
            gv.idataMgr = dataMgr.DataManager(self, gv.gPlcInfo)

        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusText('Test mode: %s' %str(gv.TEST_MD))
        # Set the periodic call back
        self.lastPeriodicTime = time.time()
        self.timer = wx.Timer(self)
        self.updateLock = False
        self.Bind(wx.EVT_TIMER, self.periodic)
        self.timer.Start(PERIODIC)  # every 500 ms

#--UIFrame---------------------------------------------------------------------
    def _initGlobals(self):
        # Init the global parameters used only by this module
        gv.gTrackConfig['weline'] = {'id':'weline', 'num': 4, 'color': wx.Colour(52, 169, 129), 'icon': 'welabel.png'}
        gv.gTrackConfig['nsline'] = {'id':'nsline', 'num': 3, 'color': wx.Colour(233, 0, 97), 'icon': 'nslabel.png'}
        gv.gTrackConfig['ccline'] = {'id':'ccline', 'num': 3, 'color': wx.Colour(255, 136, 0), 'icon': 'cclabel.png'}
        # Init all the global instance
        # if gv.gCollsionTestFlg: gv.gTestMD = False # disable the test mode flag to fetch the signal from PLC
        # Init all the train list

#--UIFrame---------------------------------------------------------------------
    def _buildMenuBar(self):
        menubar = wx.MenuBar()  # Creat the function menu bar.
        # Add the config menu
        
        # Add the about menu.
        helpMenu = wx.Menu()
        aboutItem = wx.MenuItem(helpMenu, 200,text = "Help",kind = wx.ITEM_NORMAL)
        helpMenu.Append(aboutItem)
        self.Bind(wx.EVT_MENU, self.onHelp, aboutItem)
        menubar.Append(helpMenu, '&About')

        self.SetMenuBar(menubar)


#--UIFrame---------------------------------------------------------------------
    def _buidUISizer(self):
        """ Build the main UI Sizer. """
        flagsL = wx.LEFT
        mSizer = wx.BoxSizer(wx.HORIZONTAL)
        mSizer.AddSpacer(5)
        vbox0 = wx.BoxSizer(wx.VERTICAL)
        vbox0.AddSpacer(5)
        gv.iInfoPanel = pnlFunction.PanelTrain(self)
        vbox0.Add(gv.iInfoPanel, flag=flagsL, border=2)
        tPwrSZ = self._buildTrainCtrlSizer()
        vbox0.Add(tPwrSZ, flag=flagsL, border=2)
        mSizer.Add(vbox0, flag=flagsL, border=2)
        mSizer.AddSpacer(15)
        mSizer.Add(wx.StaticLine(self, wx.ID_ANY, size=(-1, 560),
                            style=wx.LI_VERTICAL), flag=flagsL, border=2)
        
        self.plcPnls = {}
        plcSZ = self._buildPlcPnlsSizer("PLC Monitor Panels [Train]", 
                                ('PLC-06', 'PLC-07'))
        mSizer.Add(plcSZ, flag=flagsL, border=2)
        return mSizer


    def _buildTrainCtrlSizer(self):
        flagsL = wx.LEFT
        vbox0 = wx.BoxSizer(wx.VERTICAL)
        vbox0.AddSpacer(5)
        font = wx.Font(12, wx.DECORATIVE, wx.BOLD, wx.BOLD)
        label = wx.StaticText(self, label="Trains Power Control")
        label.SetFont(font)
        label.SetForegroundColour(wx.Colour("WHITE"))
        vbox0.Add(label, flag=flagsL, border=2)
        vbox0.AddSpacer(5)
        for key, panelCfg in gv.gTrackConfig.items():
            img, color = panelCfg['icon'], panelCfg['color']
            if img is None: continue
            img = os.path.join(gv.IMG_FD, img)
            png = wx.Image(img, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            sublabel = wx.StaticBitmap(self, -1, png, (10, 5), (png.GetWidth(), png.GetHeight()))
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox.Add(sublabel, flag=flagsL, border=2)
            
            for i in range(panelCfg['num']):
                trainPanel = pnlFunction.PanelTainCtrl(self, panelCfg['id'], i, bgColor=color)
                hbox.Add(trainPanel, flag=flagsL, border=2)
                hbox.AddSpacer(5)
            vbox0.Add(hbox, flag=flagsL, border=2)
            vbox0.AddSpacer(5)
        return vbox0


#--UIFrame---------------------------------------------------------------------
    def _buildPlcPnlsSizer(self, PanelTitle, panelKeySeq):
        flagsL = wx.LEFT
        font = wx.Font(12, wx.DECORATIVE, wx.BOLD, wx.BOLD)
        vSizer = wx.BoxSizer(wx.VERTICAL)
        vSizer.AddSpacer(5)
        label = wx.StaticText(self, label=PanelTitle)
        label.SetFont(font)
        label.SetForegroundColour(wx.Colour("WHITE"))
        vSizer.Add(label, flag=flagsL, border=2)
        vSizer.AddSpacer(5)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        #panelSeq = ('PLC-00', 'PLC-01', 'PLC-02')
        for key in panelKeySeq:
            hbox1.AddSpacer(10)
            panelInfo = gv.gPlcPnlInfo[key]
            ipaddr = panelInfo['ipaddress'] + ' : ' + str(panelInfo['port'])
            self.plcPnls[key] = pnlFunction.PanelPLC(self, panelInfo['label'], ipaddr)
            hbox1.Add(self.plcPnls[key], flag=flagsL, border=2)
        
        vSizer.Add(hbox1, flag=flagsL, border=2)
        return vSizer


#--UIFrame---------------------------------------------------------------------
    def periodic(self, event):
        """ Call back every periodic time."""
        now = time.time()
        if (not self.updateLock) and now - self.lastPeriodicTime >= gv.gUpdateRate:
            print("main frame update at %s" % str(now))
            self.lastPeriodicTime = now
            if not gv.TEST_MD:
                if gv.idataMgr: gv.idataMgr.periodic(now)
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

#-----------------------------------------------------------------------------
    def onHelp(self, event):
        """ Pop-up the Help information window. """
        wx.MessageBox(' If there is any bug, please contect: \n\n \
                        Author:      Yuancheng Liu \n \
                        Email:       liu_yuan_cheng@hotmail.com \n \
                        Created:     2023/07/20 \n \
                        GitHub Link: https://github.com/LiuYuancheng/Metro_emulator \n', 
                    'Help', wx.OK)

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
