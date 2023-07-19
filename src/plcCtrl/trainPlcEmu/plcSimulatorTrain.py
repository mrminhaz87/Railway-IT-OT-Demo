#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        plcSimulatorTrain.py
#
# Purpose:     A simple plc simulation module to connect and control the real-world 
#              emulator via UDP (to simulate the eletrical signals change) and handle
#              SCADA system Modbus TCP request.
#              - This module will simulate 3 PLCs connected under master-slave mode
#               
# Author:      Yuancheng Liu
#
# Version:     v0.2
# Created:     2023/05/29
# Copyright:   
# License:     
#-----------------------------------------------------------------------------
""" 
    Program design:
        We want to create a PLC simulator which can simulate a PLC set (Master[slot-0], 
        Slave[slot-1], Slave[slot-2]) with thress 16-in 8-out PLCs. The PLC sets will
        take 22 input signal and provide 22 output signal to implement the railway station
        control system.
"""

from collections import OrderedDict

import plcSimGlobalTrain as gv
import modbusTcpCom
import plcSimulator

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class onlyCoilLadderLogic(modbusTcpCom.ladderLogic):
    """ A Direct connection ladder logic diagram set
    """
    def __init__(self, parent, ladderName) -> None:
        super().__init__(parent, ladderName=ladderName)

    def initLadderInfo(self):
        self.holdingRegsInfo['address'] = 0
        self.holdingRegsInfo['offset'] = 10
        self.srcCoilsInfo['address'] = None
        self.srcCoilsInfo['offset'] = None
        self.destCoilsInfo['address'] = 0
        self.destCoilsInfo['offset'] = 10

#-----------------------------------------------------------------------------
    def runLadderLogic(self, regsList, coilList=None):
        print(regsList)
        return []
        
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class trainPowerPlcSet(plcSimulator.plcSimuInterface):
    """ A PlC simulator to provide below functions: 
        - Create a modbus service running in subthread to handle the SCADA system's 
            modbus requirment.
        - Connect to the real world emulator to fetch the sensor state and calculate 
            the output coils state based on the ladder logic. 
        - Send the signal setup request to the real world emulator to change the signal.
    """
    def __init__(self, parent, plcID, addressInfoDict, ladderObj):
        super().__init__(parent, plcID, addressInfoDict, ladderObj)
        self.powerChangeFlg = False

    def initInputState(self):
        self.regsAddrs = (0, 10)
        self.regSRWfetchKey = 'trains'
        self.regs2RWmap = OrderedDict()
        self.regs2RWmap['weline'] = (0, 4)
        self.regs2RWmap['nsline'] = (4, 7)
        self.regs2RWmap['ccline'] = (7, 10)
        self.regsStateRW = OrderedDict()
        self.regsStateRW['weline'] = [0]*4
        self.regsStateRW['nsline'] = [0]*3
        self.regsStateRW['ccline'] = [0]*3

    def initCoilState(self):
        self.coilsAddrs = (0, 10)
        self.coilsRWSetKey = 'trains'
        self.coils2RWMap = OrderedDict()
        self.coils2RWMap['weline'] = (0, 4)
        self.coils2RWMap['nsline'] = (4, 7)
        self.coils2RWMap['ccline'] = (7, 10)
        self.coilStateRW = OrderedDict()
        self.coilStateRW['weline']  = [False]*4
        self.coilStateRW['nsline']  = [False]*3 
        self.coilStateRW['ccline']  = [False]*3 

    def changeRWSignalCoil(self):
        if self.powerChangeFlg:
            super.changeRWSignalCoil()




#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    gv.gDebugPrint("Start Init the PLC: %s" %str(gv.PCL_NAME), logType=gv.LOG_INFO)
    gv.iLadderLogic = onlyCoilLadderLogic(None, ladderName='only_coil_control')
    addressInfoDict = {
        'hostaddress': ('localhost', 504),
        'realworld':gv.gRealWordIP, 
        'allowread':gv.ALLOW_R_L,
        'allowwrite': gv.ALLOW_W_L
    }
    plc = trainPowerPlcSet(None, gv.PCL_NAME, addressInfoDict,  gv.iLadderLogic)
    plc.run()

if __name__ == "__main__":
    main()
