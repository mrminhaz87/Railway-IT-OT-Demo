import time
import modbusTcpCom

hostIp = '127.0.0.1'
hostPort = 502

client = modbusTcpCom.modbusTcpClient(hostIp)

print('Test connection')

while not client.checkConn():
    print('try connect to the PLC')
    print(client.getCoilsBits(0, 4))
    time.sleep(0.5)

print('read the coils')
print(client.getCoilsBits(0, 4))
time.sleep(0.5)

print('read the holding registers')
print(client.getHoldingRegs(0, 4))
time.sleep(0.5)

print('Set the coils')
client.setCoilsBit(2, 1)
time.sleep(0.5)
print(client.getCoilsBits(0, 4))
time.sleep(0.5)

print('Set the holding registers')
client.setHoldingRegs(1, 1)
time.sleep(0.5)
print(client.getHoldingRegs(0, 4))
time.sleep(0.5)

client.close()