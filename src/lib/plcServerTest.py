import modbusTcpCom

ALLOW_R_L = ['127.0.0.1', '192.168.0.10']
ALLOW_W_L = ['127.0.0.1']


hostIp = 'localhost'
hostPort = 502
dataMgr = modbusTcpCom.plcDataHandler(allowRipList=ALLOW_R_L, allowWipList=ALLOW_W_L)

server = modbusTcpCom.modbusTcpServer(hostIp=hostIp, hostPort=hostPort, dataHandler=dataMgr)
serverInfo = server.getServerInfo()
dataMgr.initServerInfo(serverInfo)


dataMgr.updateOutPutCoils(0, [1, 1, 0, 0])

dataMgr.updateHoldingRegs(0, [0, 0, 1, 1])
print('Start server ...')
server.startServer()