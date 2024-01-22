# Railway[Metro] IT/OT System Cyber Security Test Platform

**Project Design :** We want to create a digital twin type Railway system emulation platform to simulate multiple trains running on different tracks with different sensor-signal control for cyber security researchers to demo/test different kind of IT attack's affect on OT system. The system contents 6 main components (programs): 

- 2D Railway[Metro] System Real-world Emulator
- Railway System SCADA HMI
- Railway System Trains Controller HMI
- Railway Junctions Sensor-Signal System Control PLC Simulator
- Railway Stations Sensor-Signal System Control PLC Simulator
- Railway Trains Sensor-Power System Control PLC Simulator

##### Project Use Case: 

We are glad to share that the Railway [Metro] IT/OT Emulation System Cyber Security Test Platform we developed this year was used for building one part of the cyber-attack target training system in the NATO CCDCOE Cross Sword 2023 offensive cyber exercise. LinkedIn post 2: [link](https://www.linkedin.com/posts/natoccdcoe_crossedswords-activity-7140986334961217536-7dM5/?utm_source=share&utm_medium=member_desktop)

![](doc/img/linkedinpost2.png)

[TOC]

------

### Introduction 

The Railway[Metro] IT/OT System Security Test Platform is mini railway IT/OT network emulation system for the ICS researcher or instructor to test their IT/OT-attack and defense solution or used for ICS security training and education purpose. The whole system contents 4 main part networks (as show in the below diagram): 

![](doc/img/Components.png)

1. **Cooperate network**: A subnet simulates a normal railway company cooperate IT network with different function/ERP servers (email, DMZ, staff management) and the production management workstation (production log archiving database, internal document server, operator manuals)
2. **Supervision SCADA network**:  A subnet simulate the SCADA system network with different SCADA data/historian servers, different HMI computers for system operators and maintenance computers for ICS/OT-system engineers. 
3. **Production network**:  A subnet contents different PLC simulators program. 
4. **Physical real-world emulation network**: A subnet contents different real-word components emulator to show the physical effect of the real-work items.



Railway[Metro] IT/OT System security test platform is build by 6 main components (introduced in the program design) under below structure: 

![](doc/img/networkCommDesign.png)

The detail introduction of each component is shown below: 



#### 1. 2D Railway[Metro] System Real-world Emulator

2D Railway[Metro] System real-world emulator UI: 

![](doc/video/connectionHub5.gif)

2D Railway[Metro] System real-world emulator UI detailed software design document: [link](doc/metroEmuUI_readme.md)



#### 2. Railway System SCADA HMI

Railway System SCADA HMI UI :

![](doc/video/scadaHmi.gif)

Railway System SCADA HMI detailed software design document: [link](doc/scadaHMI_readme.md)



#### 3. Railway System Trains Controller HMI

Railway System Trains Controller HMI UI

![](doc/video/trainHMIhalf.gif)

Railway System Trains Controller HMI detailed software design document: [link](doc/trainsCtrlHMI.md)



#### 4. Railway Junctions Sensor-Signal System Control PLC Simulator

PLCs set Digital I/O connection and the Ladder logic:

![](doc/img/signalPlc.png)

Railway Junctions Sensor-Signal System Control PLC Simulator detailed software design document: [link](doc/sensorsPLCSimu_readme.md)



#### 5. Railway Stations Sensor-Signal System Control PLC Simulator

PLCs set Digital I/O connection and the Ladder logic:

![](doc/img/stationPlc.png)

Railway Stations Sensor-Signal System Control PLC Simulator detailed software design document: [link](doc/stationPLCSimu_readme.md)



#### 6. Railway Trains Sensor-Power System Control PLC Simulator

PLCs set Digital I/O connection and the Ladder logic:

![](doc/img/trainPlc.png)

Railway Trains Sensor-Power System Control PLC Simulator detailed software design document: [link](doc/trainsPlcSimu_readme.md)



**Program version:** `v0.1.2`

Code base: https://github.com/LiuYuancheng/Metro_emulator/tree/main/src

------

### System Design 

The 3 parts will follow below work flow: 

#### System network design

![](doc/img/networkDesign.png)

Verify circuit logic: https://www.circuit-diagram.org/editor/



------

> last edit by LiuYuancheng (liu_yuan_cheng@hotmail.com) by 30/05/2023 if you have any problem, please send me a message. 