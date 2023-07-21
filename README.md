# Metro_Railway_System_Emulator

**Project Design :** We want to create a digital twin type Metro  emulation system to simulate multiple trains running on different tracks with the control signals. The system contents 3 parts: 

- Metro railway signal system real word emulator (2D).

- HMI and SCADA system for railway and train control. 
- PLC and latching relay emulators.



2D metro emulator UI: 

![](doc/interface.png)



SCADA-HMI UI

![](doc/hmiUI.png)



Train Power Controller UI

![](doc/traincontroller.png)



------



### System Design 

The 3 parts will follow below work flow: 

#### System network design

![](doc/img/networkDesign.png)

#### System data communication network design

![](doc/img/networkCommDesign.png)



Signal system PLC ladder diagrams set

![](doc/img/signalPlc.png)



Station system PLC ladder diagram set: 

![](doc/img/stationPlc.png)

Train control PLC config: 

![](doc/img/trainPlc.png)

For each sensors-Signal set, the circuit logic is below:

![](doc/circuit_logic2.png)



Verify circuit logic: https://www.circuit-diagram.org/editor/









------

> last edit by LiuYuancheng (liu_yuan_cheng@hotmail.com) by 30/05/2023 if you have any problem, please send me a message. 