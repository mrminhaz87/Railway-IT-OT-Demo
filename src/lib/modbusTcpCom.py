#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        modbusTcpCom.py
#
# Purpose:     This module will provide modbus-TCP client and server communication
#              API for simulating PLC and SCADA system communication. The module is
#              implemented based on python pyModbus module: 
#              https://github.com/sourceperl/pyModbusTCP
#
# Author:      Yuancheng Liu
#
# Created:     2023/06/11
# Version:     v_0.1
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

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

#-----------------------------------------------------------------------------
# Init all the read() functions.

    def read_coils(self, address, addrOffset, srv_info):
        """ Read the output coils state
            Args:
                address (int): output coils address idx[Q0.x] 
                count (_type_): address offset 
                srv_info (_type_): _description_
        """
        if self.allowRipList:
            if srv_info.client.address in self.allowRipList:
                return super().read_coils(address, addrOffset, srv_info)
            else:
                return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)
        return super().read_coils(address, addrOffset, srv_info)

    def read_d_inputs(self, address, addrOffset, srv_info):
        """ Read the discrete input idx[I0.x]"""
        if self.allowRipList:
            if srv_info.client.address in self.allowRipList:
                return super().read_d_inputs(address, addrOffset, srv_info)
            else:
                return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)
        return super().read_d_inputs(address, addrOffset, srv_info)

    def read_h_regs(self, address, addrOffset, srv_info):
        """ Read the holding register [idx]. """
        if self.allowRipList:
            if srv_info.client.address in self.allowRipList:
                return super().read_h_regs(address, addrOffset, srv_info)
            else:
                return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)
        return super().read_d_inputs(address, addrOffset, srv_info)
    
    def read_i_regs(self, address, addrOffset, srv_info):
        if self.allowRipList:
            if srv_info.client.address in self.allowRipList:
                return super().read_i_regs(address, addrOffset, srv_info)
            else:
                return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)
        return super().read_i_regs(address, addrOffset, srv_info)

#-----------------------------------------------------------------------------
# Init all the write() functions.
    def write_coils(self, address, bits_l, srv_info):
        """ Write the PLC out coils.
            Args:
                address (int): output coils address idx[Q0.x] 
                count (_type_): address offset 
                srv_info (_type_): _description_
        """
        if self.allowWipList:
            if srv_info.client.address in self.allowWipList:
                return super().write_coils(address, bits_l, srv_info)
            else:
                return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)
        return super().write_coils(address, bits_l, srv_info)

    def write_h_regs(self, address, words_l, srv_info):
        """ write the holding register"""
        if self.allowWipList:
            if srv_info.client.address in self.allowWipList:
                return super().write_h_regs(address, words_l, srv_info)
            else:
                return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)
        return super().write_h_regs(address, words_l, srv_info)

#-----------------------------------------------------------------------------
    def setAllowReadIpaddresses(self, ipList):
        self.allowRipList = ipList

#-----------------------------------------------------------------------------
    def setAllowWriteIpaddresses(self, ipList):
        self.allowWipList = ipList

#-----------------------------------------------------------------------------
    def updateOutPutCoils(self, address, bitList):
        if self.serverInfo:
            return self.write_coils(address, bitList, self.serverInfo)
        print("updateOutPutCoils() Error: Parent modBus server not config, call initServerInfo() first.")
        return False

    def updateHoldingRegs(self, address, bitList):
        if self.serverInfo:
            return self.read_h_regs(address, bitList, self.serverInfo)
        print("updateHoldingRegs() Error: Parent modBus server not config, call initServerInfo() first.")
        return False

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class modbusTcpClient(object):

    def __init__(self, tgtIp, tgtPort=502, defaultTO=30) -> None:
        self.tgtIp = tgtIp
        self.tgtPort = tgtPort
        self.client = ModbusClient(host=self.tgtIp, port=self.tgtPort, auto_open=True)
        self.client.timeout = defaultTO # set time out.
        if self.client.is_open:
            print('Success connect to the target PLC: %s' %str(self.tgtIp))
        else:
            print('Failed to connect to the target PLC: %s' %str(self.tgtIp))

    def checkConn(self):
        return self.client.is_open

    def getCoilsBits(self, addressIdx, offset):
        if self.client.is_open:
            data = self.client.read_coils(addressIdx, offset)
            return list(data)
        return None

    def setCoilsBit(self, addressIdx, bitVal):
        if self.client.is_open:
            data = self.client.write_single_coil(addressIdx, bitVal)
            return data
        return None

    def getHoldingRegs(self, addressIdx, offset):
        if self.client.is_open:
            data = self.client.read_holding_registers(addressIdx, offset)
            return list(data)
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

    def __init__(self, hostIp='localhost', hostPort=502, dataHandler=None, allowRipList = None, allowWipList = None ) -> None:
        self.hostIp = hostIp
        self.hostPort = hostPort
        if dataHandler is None:
            print("PLC logic data handler is not define, init failed, exiting...")
            exit()
        self.server = ModbusServer(host=hostIp, port=hostPort, data_hdl=dataHandler)

    def isRunning(self):
        return self.server.is_run
    
    def startServer(self):
        print("Start to run the Modbus TCP server: (%s, %s)" %(self.hostIp, str(self.hostPort)))
        if self.isRunning: 
            print("The server is running, stop and restart it.")
            self.server.stop()
        self.server.start()

    def stopServer(self):
        if self.isRunning():self.server.stop()