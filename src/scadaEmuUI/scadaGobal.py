#-----------------------------------------------------------------------------
# Name:        scadaGlobal.py
#
# Purpose:     This module is used as a local config file to set constants, 
#              global parameters which will be used in the other modules.
#              
# Author:      Yuancheng Liu
#
# Created:     2010/08/26
# Version:     v0.1.2
# Copyright:   Copyright (c) 2023 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------
"""
For good coding practice, follow the following naming convention:
    1) Global variables should be defined with initial character 'g'
    2) Global instances should be defined with initial character 'i'
    2) Global CONSTANTS should be defined with UPPER_CASE letters
"""

import os, sys
from collections import OrderedDict

print("Current working directory is : %s" % os.getcwd())
DIR_PATH = dirpath = os.path.dirname(__file__)
print("Current source code location : %s" % dirpath)
APP_NAME = ('SCADAEmu', 'HMI')

TOPDIRS = ['src', 'rail']
LIBDIR = 'lib'
CONFIG_FILE_NAME = 'scadaHMIConfig.txt'
CONFIG_DIR_NAME = 'configFiles'

#-----------------------------------------------------------------------------
# Init the logger:
# find the lib directory
for topdir in TOPDIRS:
    idx = dirpath.find(topdir)
    gTopDir = dirpath[:idx + len(topdir)] if idx != -1 else dirpath   # found it - truncate right after TOPDIR
    # Config the lib folder 
    gLibDir = os.path.join(gTopDir, LIBDIR)
    if os.path.exists(gLibDir):
        print("Import all the lib-module from folder : %s" %str(gLibDir))
        sys.path.insert(0, gLibDir)
        break

import Log
Log.initLogger(gTopDir, 'Logs', APP_NAME[0], APP_NAME[1], historyCnt=100, fPutLogsUnderDate=True)

# Init the log type parameters.
DEBUG_FLG   = False
LOG_INFO    = 0
LOG_WARN    = 1
LOG_ERR     = 2
LOG_EXCEPT  = 3
# init the log print module.
def gDebugPrint(msg, prt=True, logType=None):
    if prt: print(msg)
    if logType == LOG_WARN:
        Log.warning(msg)
    elif logType == LOG_ERR:
        Log.error(msg)
    elif logType == LOG_EXCEPT:
        Log.exception(msg)
    elif logType == LOG_INFO or DEBUG_FLG:
        Log.info(msg)

#-----------------------------------------------------------------------------
# Init the configure file loader.
import ConfigLoader
gGonfigPath = os.path.join(dirpath, CONFIG_FILE_NAME)
iConfigLoader = ConfigLoader.ConfigLoader(gGonfigPath, mode='r')
if iConfigLoader is None:
    print("Error: The config file %s is not exist.Program exit!" %str(gGonfigPath))
    exit()
CONFIG_DICT = iConfigLoader.getJson()

#------<IMAGES PATH>-------------------------------------------------------------
IMG_FD = os.path.join(dirpath, 'img')
ICO_PATH = os.path.join(IMG_FD, "metro.ico")
UI_TITLE = CONFIG_DICT['UI_TITLE']
TEST_MD = CONFIG_DICT['TEST_MD']      # test mode flag, True: the simulator will operate with control logic itself. 
PERIODIC = 500      # update the main in every 300ms

# Init the agent object type
RAILWAY_TYPE_LINE   = 'RL'
RAILWAY_TYPE_CYCLE  = 'RC'
TRAIN_TYPE          = 'TR'
LABEL_TYPE          = 'LB'
SENSOR_TYPE         = 'SS'
SINGAL_TYPE         = "SG"

# Init the UI layout flags
LAY_U = 0   # layout at up position  
LAY_D = 1   # layout at down position 
LAY_L = 2   # layout at left position
LAY_R = 3   # layout at right position
LAY_C = 4   # layout at center 
LAY_H = 5   # horizontal layout
LAY_V = 6   # vertical layout

#-------<GLOBAL VARIABLES (start with "g")>------------------------------------
# VARIABLES are the built in data type.
gTrackConfig = OrderedDict()
# PLC connection info
gPlcInfo = OrderedDict()
# Init the PLC connection global information.
gSensorPlcID = CONFIG_DICT['SEN_PLC_ID']
gSensorPlcIP = CONFIG_DICT['SEN_PLC_IP']
gSensorPlcPort = int(CONFIG_DICT['SEN_PLC_PORT'])
gPlcInfo['PLC-00'] = {'id': gSensorPlcID, 'ipaddress': gSensorPlcIP, 'port': gSensorPlcPort, 
                      'hRegsInfo': (0, 39), 'coilsInfo': (0, 19)}

gStationPlcID = CONFIG_DICT['STN_PLC_ID']
gStationPlcIP = CONFIG_DICT['STN_PLC_IP']
gStationPlcPort = int(CONFIG_DICT['STN_PLC_PORT'])
gPlcInfo['PLC-03'] = {'id': gStationPlcID, 'ipaddress': gStationPlcIP,'port': gStationPlcPort, 
                      'hRegsInfo': (0, 22), 'coilsInfo': (0, 22)}

# PLC display panel information.
gPlcPnlInfo = OrderedDict()

# init junction Plcs
gPlcPnlInfo['PLC-00'] = {'id': 'PLC-00', 'label': 'PLC-00[Master:slot-0]',
                         'ipaddress': gSensorPlcIP, 'port': gSensorPlcPort,
                         'tgt': 'PLC-00', 'hRegsInfo': (0, 15), 'coilsInfo': (0, 7)}
gPlcPnlInfo['PLC-01'] = {'id': 'PLC-01', 'label': 'PLC-01[Slave:slot-1]',
                         'ipaddress': gSensorPlcIP, 'port': gSensorPlcPort,
                         'tgt': 'PLC-00', 'hRegsInfo': (15, 30), 'coilsInfo': (7, 14)}
gPlcPnlInfo['PLC-02'] = {'id': 'PLC-02',  'label': 'PLC-02[Slave:slot-2]',
                         'ipaddress': gSensorPlcIP, 'port': gSensorPlcPort,
                         'tgt': 'PLC-00', 'hRegsInfo': (30, 39), 'coilsInfo': (14, 19)}
# init station Plcs
gPlcPnlInfo['PLC-03'] = {'id': 'PLC-03', 'label': 'PLC-03[Master:slot-0]',
                         'ipaddress': gStationPlcIP, 'port': gStationPlcPort,
                         'tgt': 'PLC-03', 'hRegsInfo': (0, 8), 'coilsInfo': (0, 8)}
gPlcPnlInfo['PLC-04'] = {'id': 'PLC-04', 'label': 'PLC-04[Slave:slot-1]',
                         'ipaddress': gStationPlcIP, 'port': gStationPlcPort,
                         'tgt': 'PLC-03', 'hRegsInfo': (8, 16), 'coilsInfo': (8, 16)}
gPlcPnlInfo['PLC-05'] = {'id': 'PLC-05', 'label': 'PLC-05[Slave:slot-2]',
                         'ipaddress': gStationPlcIP, 'port': gStationPlcPort,
                         'tgt': 'PLC-03', 'hRegsInfo': (16, 22), 'coilsInfo': (16, 22)}

gUpdateRate = float(CONFIG_DICT['CLK_INT'])    # main frame update rate 1 sec.


gStataionNameDict = {}
gWeStationFile = os.path.join(DIR_PATH, CONFIG_DIR_NAME, CONFIG_DICT['WE_STATION_CFG'])
gNsStationFile = os.path.join(DIR_PATH, CONFIG_DIR_NAME, CONFIG_DICT['NC_STATION_CFG'])
gCcStationFile = os.path.join(DIR_PATH, CONFIG_DIR_NAME, CONFIG_DICT['CC_STATION_CFG'])


#-------<GLOBAL PARAMTERS>-----------------------------------------------------
iMainFrame = None   # UI MainFrame.
iCtrlPanel = None   # UI function control panel.
iMapPanel = None    # UI map display panel
iMapMgr = None
idataMgr = None
