#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        modbusTcpCom.py
#
# Purpose:     This module will provide modbus-TCP client and server communication
#              API for testing or simulating the communication between PLC and SCADA 
#              system. The module is implemented based on python pyModbus module: 
#              https://github.com/sourceperl/pyModbusTCP
#
# Author:      Yuancheng Liu
#
# Created:     2023/06/11
# Version:     v_0.1
# Copyright:   
# License:     
#-----------------------------------------------------------------------------
""" Program Design:

    We want to create a normal Modbus TCP communication channel (client + server)
    to read the data from a real PLC or simulate the PLC Modbus data handling process.
    Three module will be provided in this module: 

    - plcDataHandler: A pyModbusTcp.dataHandler module to keep one allow read white list and one 
        allow write list to filter the Client's coil or register read and write request.
        As most of the PLC are using the input => register (memory) parameter config, they are 
        not allowed to change the input directly, we only provide the coil and holding 
        register write function.

Returns:
    _type_: _description_
"""

import time

from pyModbusTCP.client import ModbusClient
from pyModbusTCP.server import ModbusServer, DataHandler
from pyModbusTCP.constants import EXP_ILLEGAL_FUNCTION

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class plcDataHandler(DataHandler):

    def __init__(self, data_bank=None, allowRipList=None, allowWipList=None):
        super().__init__(data_bank)
        self.serverInfo = None
        self.allowRipList = allowRipList
        self.allowWipList = allowWipList

#-----------------------------------------------------------------------------
    def initServerInfo(self, serverInfo):
        """ Init the server Information.
            Args:
                serverInfo (<ModbusServer.ServerInfo>): _description_
        """
        self.serverInfo = serverInfo

    def _checkAllowRead(self, ipaddress):
        """ Check whether the IP addres is allowed to read the info."""
        if (self.allowRipList is None) or (ipaddress in self.allowRipList): return True
        return False 

    def _checkAllowWrite(self, ipaddress):
        """ Check whether the IP addres is allowed to write the info."""
        if (self.allowWipList is None) or (ipaddress in self.allowWipList): return True
        return False

#-----------------------------------------------------------------------------
# Init all the iterator read() functions.(Internal callback by <modbusTcpServer>)

    def read_coils(self, address, addrOffset, srv_info):
        """ Read the output coils state
            Args:
                address (int): output coils address idx[Q0.x] 
                count (_type_): address offset 
                srv_info (_type_): _description_
        """
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
        """ Read the holding register [idx]. """
        try:
            if self._checkAllowRead(srv_info.client.address):
                return super().read_h_regs(address, addrOffset, srv_info)
        except Exception as err:
            print("read_h_regs() Error: %s" %str(err))
        return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)

    def read_i_regs(self, address, addrOffset, srv_info):
        """ Read the input register"""
        try:
            if self._checkAllowRead(srv_info.client.address):
                return super().read_i_regs(address, addrOffset, srv_info)
        except Exception as err:
            print("read_i_regs() Error: %s" %str(err))
        return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)

#-----------------------------------------------------------------------------
# Init all the iterator write() functions.(Internal callback by <modbusTcpServer>)
    def write_coils(self, address, bits_l, srv_info):
        """ Write the PLC out coils.
            Args:
                address (int): output coils address idx[Q0.x] 
                count (_type_): address offset 
                srv_info (_type_): _description_
        """
        try:
            if self._checkAllowWrite(srv_info.client.address):
                return super().write_coils(address, bits_l, srv_info)
        except Exception as err:
            print("write_coils() Error: %s" %str(err))
        return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)

    def write_h_regs(self, address, words_l, srv_info):
        """ write the holding register"""
        try:
            if self._checkAllowWrite(srv_info.client.address):
                return super().write_h_regs(address, words_l, srv_info)
        except Exception as err:
            print("write_coils() Error: %s" %str(err))
        return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)

#-----------------------------------------------------------------------------
# define all the public functions wich can be called from other module.
    
    def setAllowReadIpaddresses(self, ipList):
        self.allowRipList = ipList

    def setAllowWriteIpaddresses(self, ipList):
        self.allowWipList = ipList

    def updateOutPutCoils(self, address, bitList):
        if self.serverInfo:
            return super().write_coils(address, bitList, self.serverInfo)
        print("updateOutPutCoils() Error: Parent modBus server not config, call initServerInfo() first.")
        return False

    def updateHoldingRegs(self, address, bitList):
        if self.serverInfo:
            return super().write_h_regs(address, bitList, self.serverInfo)
        print("updateHoldingRegs() Error: Parent modBus server not config, call initServerInfo() first.")
        return False

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
