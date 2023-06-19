#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        modbusTcpCom.py
#
# Purpose:     This module will provide the modbus-TCP client and server communication
#              API for testing or simulating the data flow connection between PLC and SCADA 
#              system. The module is implemented based on python pyModbus lib module: 
#              - Reference: https://github.com/sourceperl/pyModbusTCP
#
# Author:      Yuancheng Liu
#
# Created:     2023/06/11
# Version:     v_0.1
# Copyright:   
# License:     
#-----------------------------------------------------------------------------
""" Program Design:

    We want to create a normal Modbus TCP communication channel (client + server) lib
    to read the data from a real PLC or simulate the PLC Modbus data handling process (handle 
    modbusTCP request from other program which same as PLC).
    
    Four modules will be provided in this module: 

    - ladderLogic: A ladder logic obj class 

    - plcDataHandler: A pyModbusTcp.dataHandler module to keep one allow read white list and one 
        allow write white list to filter the client's coils or registers read and write request.
        As most of the PLC are using the input => register (memory) parameter config, they are 
        not allowed to change the input directly, we only provide the coil and holding register 
        write functions.
    
    - 

Returns:
    _type_: _description_
"""

import time
from collections import OrderedDict

from pyModbusTCP.client import ModbusClient
from pyModbusTCP.server import ModbusServer, DataHandler, DataBank
from pyModbusTCP.constants import EXP_ILLEGAL_FUNCTION

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class ladderLogic(object):
    """ The ladder logic object used by data handler. Only for the registers=> 
        ladder logic => coils 
    """

    def __init__(self, parent) -> None:
        self.parent = parent
        self.holdingRegsInfo = {'address': None, 'offset': None}
        self.srcCoilsInfo = {'address': None, 'offset': None}
        self.destCoilsInfo = {'address': None, 'offset': None}
        self.initLadderInfo()

    def initLadderInfo(self):
        """ Init the ladder register and coils information. please over write 
            this function.
        """
        pass

    def getHoldingRegsInfo(self):
        return self.holdingRegsInfo

    def getSrcCoilsInfo(self):
        return self.srcCoilsInfo

    def getDestCoilsInfo(self):
        return self.destCoilsInfo

    def runLadderLogic(self, regsList, coilList=None):
        """ Pass in the register state list and calculate output coils state.
        """
        return []

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class plcDataHandler(DataHandler):
    """ Module inherited from pyModbusTcp.dataHandlerto keep one allow read white list and one 
        allow write white list to filter the client's coils or registers read and write request.
        As most of the PLC are using the input => register (memory) parameter config, they are 
        not allowed to change the input directly, we only provide the coil and holding register 
        write functions.
    """
    def __init__(self, data_bank=None, allowRipList=None, allowWipList=None):
        """ Obj init example: plcDataHandler(allowRipList=['127.0.0.1', '192.168.10.112'], allowWipList=['192.168.10.113'])
        Args:
            data_bank (<pyModbusTcp.DataBank>, optional): . Defaults to None.
            allowRipList (list(str), optional): list of ip address string which are allowed to read 
                the data from PLC. Defaults to None allow any ip to read. 
            allowWipList (list(str), optional): list of ip address string which are allowed to write
                the data to PLC. Defaults to None allow any ip to write.
        """
        self.data_bank = DataBank() if data_bank is None else data_bank
        super().__init__(self.data_bank)
        self.serverInfo = None
        self.allowRipList = allowRipList
        self.allowWipList = allowWipList
        self.autoUpdate = False # auto update if the holding register state changed. 
        self.ladderDict = OrderedDict()

    def _checkAllowRead(self, ipaddress):
        """ Check whether the input IP addres is allowed to read the info."""
        if (self.allowRipList is None) or (ipaddress in self.allowRipList): return True
        return False 

    def _checkAllowWrite(self, ipaddress):
        """ Check whether the input IP addres is allowed to write the info."""
        if (self.allowWipList is None) or (ipaddress in self.allowWipList): return True
        return False

#-----------------------------------------------------------------------------
    def initServerInfo(self, serverInfo):
        """ Init the server Information.
            Args: serverInfo (<ModbusServer.ServerInfo>): after passed the datahandler to the 
            modbus server, call this function and pass in the ModbusServer.ServerInfo obj so in 
            PLC logic you can all the set/update function to change the value in databank.
        """
        self.serverInfo = serverInfo

    def addLadderLogic(self, ladderKey, logicObj):
        self.ladderDict[ladderKey] = logicObj

#-----------------------------------------------------------------------------
# Init all the iterator read() functions.(Internal callback by <modbusTcpServer>)
# All the input args will follow below below formate:
#   address (int): output coils address idx [Q0.x] 
#   count (int): address offset, return list length will be x + offsert.
#   srv_info (ModbusServer.ServerInfo>): passed in by server.

    def read_coils(self, address, addrOffset, srv_info):
        """ Read the output coils state"""
        try:
            if self._checkAllowRead(srv_info.client.address):
                return super().read_coils(address, addrOffset, srv_info)
        except Exception as err:
            print("read_coils() Error: %s" %str(err))
        return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)

    def read_d_inputs(self, address, addrOffset, srv_info):
        """ Read the discrete input idx[I0.x]"""
        try:
            if self._checkAllowRead(srv_info.client.address):
                return super().read_d_inputs(address, addrOffset, srv_info)
        except Exception as err:
            print("read_d_inputs() Error: %s" %str(err))
        return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)

    def read_h_regs(self, address, addrOffset, srv_info):
        """ Read the holding registers [idx]. """
        try:
            if self._checkAllowRead(srv_info.client.address):
                return super().read_h_regs(address, addrOffset, srv_info)
        except Exception as err:
            print("read_h_regs() Error: %s" %str(err))
        return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)

    def read_i_regs(self, address, addrOffset, srv_info):
        """ Read the input registers"""
        try:
            if self._checkAllowRead(srv_info.client.address):
                return super().read_i_regs(address, addrOffset, srv_info)
        except Exception as err:
            print("read_i_regs() Error: %s" %str(err))
        return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)

#-----------------------------------------------------------------------------
# Init all the iterator write() functions.(Internal callback by <modbusTcpServer>)
# All the input args will follow below below formate:
#   address (int): output coils address idx [Q0.x] 
#   count (int): address offset, return list length will be x + offsert.
#   srv_info (ModbusServer.ServerInfo>): passed in by server.


    def write_coils(self, address, bits_l, srv_info):
        """ Write the PLC out coils."""
        try:
            if self._checkAllowWrite(srv_info.client.address):
                return super().write_coils(address, bits_l, srv_info)
        except Exception as err:
            print("write_coils() Error: %s" %str(err))
        return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)

    def write_h_regs(self, address, words_l, srv_info):
        """ write the holding registers."""
        try:
            if self._checkAllowWrite(srv_info.client.address):
                result = super().write_h_regs(address, words_l, srv_info)
                if self.autoUpdate: self.updateState()
                return result
        except Exception as err:
            print("write_h_regs() Error: %s" %str(err))
        return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)

#-----------------------------------------------------------------------------
# define all the public functions wich can be called from other module.
    
    def setAutoUpdate(self, updateFlag):
        self.autoUpdate = updateFlag

    def setAllowReadIpaddresses(self, ipList):
        if isinstance(ipList, list) or isinstance(ipList, tuple) or ipList is None:
            self.allowRipList = list(ipList)
            return True
        print("setAllowReadIpaddresses(): the input IP list is not valid.")
        return False

    def setAllowWriteIpaddresses(self, ipList):
        if isinstance(ipList, list) or isinstance(ipList, tuple) or ipList is None:
            self.allowWipList = list(ipList)
            return True
        print("setAllowWriteIpaddresses(): the input IP list is not valid.")
        return False

    def updateOutPutCoils(self, address, bitList):
        if self.serverInfo:
            return super().write_coils(address, bitList, self.serverInfo)
        print("updateOutPutCoils() Error: Parent modBus server not config, call initServerInfo() first.")
        return False

    def updateHoldingRegs(self, address, bitList):
        if self.serverInfo:
            result = super().write_h_regs(address, bitList, self.serverInfo)
            if self.autoUpdate: self.updateState()
            return result
        print("updateHoldingRegs() Error: Parent modBus server not config, call initServerInfo() first.")
        return False

    def updateState(self):
        """ Update the PLC state base on the input ladder logic one by one."""
        for key, item in self.ladderDict.items():
            print("update laddre logic: %s" %str(key))
            holdRegsInfo = item.getHoldingRegsInfo()
            if holdRegsInfo['address'] is None or holdRegsInfo['offset'] is None: continue
            print('1')
            regState = self.data_bank.get_holding_registers(holdRegsInfo['address'], number=holdRegsInfo['offset'], srv_info=self.serverInfo)
            srcCoilState = None
            srcCoilInfo = item.getSrcCoilsInfo()
            if srcCoilInfo['address'] is None or srcCoilInfo['offset'] is None:
                pass
            else:
                srcCoilState = self.data_bank.get_coils(srcCoilInfo['address'], number=srcCoilInfo['offset'], srv_info=self.serverInfo)
            destCoilState = item.runLadderLogic(regState, coilList=srcCoilState)
            print('2')
            if destCoilState is None or len(destCoilState) == 0: continue
            destCoidInfo = item.getDestCoilsInfo()
            self.updateOutPutCoils(destCoidInfo['address'], destCoilState)
            print('3')
            

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class modbusTcpClient(object):
    """ Modbus-TCP client module to read/write data from/to PLC."""
    def __init__(self, tgtIp, tgtPort=502, defaultTO=30) -> None:
        self.tgtIp = tgtIp
        self.tgtPort = tgtPort
        self.client = ModbusClient(
            host=self.tgtIp, port=self.tgtPort, auto_open=True)
        self.client.timeout = defaultTO  # set time out.
        # Try to connect to the PLC in 1 sec
        for _ in range(5):
            print('Try to login to the PLC unit.')
            if self.client.open(): break
            time.sleep(0.2)
        if self.client.is_open:
            print('Success connect to the target PLC: %s' % str(self.tgtIp))
        else:
            print('Failed to connect to the target PLC: %s' % str(self.tgtIp))

    def checkConn(self):
        return self.client.is_open

    def getCoilsBits(self, addressIdx, offset):
        if self.client.is_open:
            data = self.client.read_coils(addressIdx, offset)
            if data: return list(data)
        return None
    
    def getHoldingRegs(self, addressIdx, offset):
        if self.client.is_open:
            data = self.client.read_holding_registers(addressIdx, offset)
            if data: return list(data)
        return None

    def setCoilsBit(self, addressIdx, bitVal):
        if self.client.is_open:
            data = self.client.write_single_coil(addressIdx, bitVal)
            return data
        return None

    def setHoldingRegs(self, addressIdx, bitVal):
        if self.client.is_open:
            data = self.client.write_single_register(addressIdx, bitVal)
            return data
        return None

    def close(self):
        self.client.close()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class modbusTcpServer(object):
    """ Modbus-TCP server module simulate a PLC"""
    def __init__(self, hostIp='localhost', hostPort=502, dataHandler=None) -> None:
        self.hostIp = hostIp
        self.hostPort = hostPort
        if dataHandler is None:
            print("PLC logic data handler is not define, init failed, exiting...")
            exit()
        self.server = ModbusServer(host=hostIp, port=hostPort, data_hdl=dataHandler)

    def isRunning(self):
        return self.server.is_run
    
    def getServerInfo(self):
        return self.server.ServerInfo

    def startServer(self):
        print("Start to run the Modbus TCP server: (%s, %s)" %(self.hostIp, str(self.hostPort)))
        self.server.start()

    def stopServer(self):
        if self.isRunning():self.server.stop()
