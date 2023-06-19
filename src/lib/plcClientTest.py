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

print('Test: read the coils')
result = client.getCoilsBits(0, 4)
if result == [True, True, False, False]: 
    print(" - test pass")
else:
    print(" - test Fail, result: %s" %str(result))
time.sleep(0.5)

print('read the holding registers')
result = client.getHoldingRegs(0, 4)
if result == [0, 0, 1, 1]: 
    print(" - test pass")
else:
    print(" - test Fail, result: %s" %str(result))
time.sleep(0.5)

print('Set the holding registers')
client.setHoldingRegs(1, 1)
time.sleep(0.5)
result = client.getHoldingRegs(0, 4)
if result == [0, 1, 1, 1]: 
    print(" - test pass")
else:
    print(" - test Fail, result: %s" %str(result))
time.sleep(0.5)

print('Test: check auto update coils')
result = client.getCoilsBits(0, 4)
if result == [True, False, False, False]: 
    print(" - test pass")
else:
    print(" - test Fail, result: %s" %str(result))
time.sleep(0.5)

print('Set the coils')
client.setCoilsBit(1, 1)
time.sleep(0.5)
result = client.getCoilsBits(0, 4)
if result == [True, True, False, False]: 
    print(" - test pass")
else:
    print(" - test Fail, result: %s" %str(result))
time.sleep(0.5)



client.close()