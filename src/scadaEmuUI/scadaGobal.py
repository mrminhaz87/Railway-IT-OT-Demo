#-----------------------------------------------------------------------------
# Name:        scadaGlobal.py
#
# Purpose:     This module is used as a local config file to set constants, 
#              global parameters which will be used in the other modules.
#              
# Author:      Yuancheng Liu
#
# Created:     2010/08/26
# Copyright:   
# License:     
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

TOPDIR = 'src'
LIBDIR = 'lib'

#-----------------------------------------------------------------------------
# Init the logger:
idx = dirpath.find(TOPDIR)
gTopDir = dirpath[:idx + len(TOPDIR)] if idx != -1 else dirpath   # found it - truncate right after TOPDIR
# Config the lib folder 
gLibDir = os.path.join(gTopDir, LIBDIR)
if os.path.exists(gLibDir):
    sys.path.insert(0, gLibDir)
import Log
Log.initLogger(gTopDir, 'Logs', APP_NAME[0], APP_NAME[1], historyCnt=100, fPutLogsUnderDate=True)


#------<IMAGES PATH>-------------------------------------------------------------
IMG_FD = os.path.join(dirpath, 'img')
ICO_PATH = os.path.join(IMG_FD, "metro.ico")

TEST_MD = True
PLC_NUM = 1

# Init the agent object type
RAILWAY_TYPE_LINE   = 'RL'
RAILWAY_TYPE_CYCLE  = 'RC'
TRAIN_TYPE          = 'TR'
LABEL_TYPE          = 'LB'
SENSOR_TYPE         = 'SS'
SINGAL_TYPE         = "SG"

PERIODIC = 300      # update the main in every 300ms
MBTCP_PORT = 502

# Init the log type parameters.
DEBUG_FLG   = False
LOG_INFO    = 0
LOG_WARN    = 1
LOG_ERR     = 2
LOG_EXCEPT  = 3

# Init the UI layout flags
LAY_U = 0   # layout at up position  
LAY_D = 1   # layout at down position 
LAY_L = 2   # layout at left position
LAY_R = 3   # layout at right position
LAY_C = 4   # layout at center 
LAY_H = 5   # horizontal layout
LAY_V = 6   # vertical layout

gTrackConfig = OrderedDict()

# PLC connection info
gPlcInfo = OrderedDict()
gPlcInfo['PLC-00'] = {'id': 'PLC-00', 'ipaddress': '127.0.0.1',
                      'port': 502, 'hRegsInfo': (0, 39), 'coilsInfo': (0, 19)}

# PLC display panel information.
gPlcPnlInfo = OrderedDict()
gPlcPnlInfo['PLC-00'] = {'id': 'PLC-00', 'label': 'PLC-00[Master:slot-0]', 'ipaddress': '127.0.0.1',
                         'port': 502, 'tgt': 'PLC-00', 'hRegsInfo': (0, 15), 'coilsInfo': (0, 7)}
gPlcPnlInfo['PLC-01'] = {'id': 'PLC-01', 'label': 'PLC-01[Slave:slot-1]', 'ipaddress': '127.0.0.1',
                         'port': 502, 'tgt': 'PLC-00', 'hRegsInfo': (15, 30), 'coilsInfo': (7, 14)}
gPlcPnlInfo['PLC-02'] = {'id': 'PLC-02',  'label': 'PLC-02[Slave:slot-2]', 'ipaddress': '127.0.0.1',
                         'port': 502, 'tgt': 'PLC-00', 'hRegsInfo': (30, 39), 'coilsInfo': (14, 19)}

gTranspPct = 70     # Windows transparent percentage.
gUpdateRate = 1     # main frame update rate 1 sec.

#-------<GLOBAL VARIABLES (start with "g")>------------------------------------
# VARIABLES are the built in data type.

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

#-------<GLOBAL PARAMTERS>-----------------------------------------------------
iMainFrame = None   # UI MainFrame.
iCtrlPanel = None   # UI function control panel.
iMapPanel = None    # UI map display panel
iMapMgr = None
iPlcClient = None   # modbus client to connect to the PLC
idataMgr = None
