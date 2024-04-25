Mini Railway Cyber Range 

### Railway [Metro] IT-OT System Cyber Security Test Platform

![](doc/img/logo/logo_mini_size.png)



**Project Design Purpose :** Our objective is to develop a miniature cyber range capable of simulating the IT-OT environment of a railway company/system. This platform serves multiple purposes including cyber exercises, professional training, IT-OT security project research, development and testing. It will provide a simplified and straightforward digital-twin style Operational Technology (OT) environments emulation platform for the railway signaling systems. This platform will simulate the operations of multiple trains on various tracks, each equipped with distinct sensor-signal controls. Additionally, it will emulate a normal corporate network with various user activities to simulate the Information Technology (IT) environment. The program will offer several different modules to simulate Level 0 (Physical Process Field I/O device) to Level 5 (Internet DMZ Zone) of an IT-OT environment, as illustrated below:

![](doc/img/RmImg/rm_01_syslvl.png)

This platform serves as a cyber range for conducting cyber security exercises to demonstrate and assess the impact of various IT attacks on OT systems. The system comprises four primary components: 

1. 2D Railway [Metro] System Physical-world Emulator. 
2.  Railway OT-Field-Controller Simulation (PLC & RTU) Programs.
3. Railway SCADA System Simulator. 
4. Railway Company's Corporate Environment Simulation. 

```
# version:     v0.1.4
# Created:     2023/05/21
# Copyright:   Copyright (c) 2023 LiuYuancheng
# License:     MIT License
```

**Table of Contents**

[TOC]

------

### Introduction

The Mini Railway Cyber Range ( Railway [Metro] IT-OT System Cyber Security Test Platform ) serves as a miniature railway IT/OT network emulation system designed to empower ICS researchers in testing their IT/OT attack and defense solutions on our cyber range. Additionally, it also provides different IT and OT cyber attack cases for the ICS security training and education purposes. The entire system is composed of below contents: 

- **Two sub cyber ranges**: Railway Company IT-System Cyber Range and Railway System OT-System Cyber Range
- **Four main network components**:  Corporate network, Supervision SCADA network, Production network and Physical real-world emulation network. 
- **Nine program modules**: 2D Railway [Metro] System Real-world Emulator, Railway System SCADA HMI, Railway System Trains Controller HMI, Railway junction and station Sensor-Signal System Control PLC Simulators, Train control PLC simulators, Train monitoring RTU simulators, Railway company staff activities auto generator and cyber attack scenario simulation program.

![](doc/img/RmImg/rm_03_overview.png)

`version v0.1.4 (2024)`

#### Introduction of railway company IT-system cyber range

The IT-network sub cyber range project will simulate the normal corporate network of the railway company ( lvl4~lvl5 in an IT-OT environment) , we will use the [Custer User Emulation System](https://github.com/LiuYuancheng/Windows_User_Simulator)  to automate simulate different kinds staff (blue team)'s daily work such as IT-Support-Engineer, Officer Staff, Railway HQ operator, Train driver / Train safety checker. It also provide the malicious activities (red teaming) generation program for simulate the attack scenario. The project consists of three primary components as shown below:

| Components Name                         | Components Description                                       | Reference links                                              |
| --------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Corporate network environment           | A network with physical hardware / virtual machine (such as computer,  node, firewall, router, switches ... ) to simulate the railway company's IT-network. | [> Detail Example Link](https://github.com/LiuYuancheng/Cross-Sword-2023-Nato-Event/tree/main/ansibleVM) |
| Company staff activities auto generator | A cluster user (blue team) activities generation system to simulate virtual staff (such as IT-Support-Engineer, Officer Staff, Railway HQ operator, Train driver / safety checker...) daily work activities and network traffic. | [> Detail Example Link ](https://github.com/LiuYuancheng/Lockshield_202X_NCL/tree/main/LS2024/deployment) |
| Attack simulation system                | An attacker (red team) malicious activates generation system which can simulate hacker's attacking action such as phishing email, FDI, FCI, MITM, DDoS... | [> Detail Example Link](https://github.com/LiuYuancheng/Lockshield_202X_NCL/tree/main/LS2024/src/Hackers) |

#### Introduction of railway system OT-system cyber range

The OT-environment cyber range will simulate the railway track signaling system and the train control system (lvl0 ~ lvl3 in an IT-OT environment) includes the the real-world physical device action, the OT-production network with the OT field device and the  railway system's supervision SCADA network. 

| Components Name                             | Level   | Components Description                                       | Document link                                      |
| ------------------------------------------- | ------- | ------------------------------------------------------------ | -------------------------------------------------- |
| 2D Physical Real-world Simulator            | Lvl-0   | A physical world components/device (track, train, signal sensor, city) simulation program with a 2D UI for user to view the real-world situation. | [> Detailed Program Doc](src/metroEmuUI/readme.md) |
| Track Junctions Sensor-Signal PLC Simulator | Lvl-1   | A emulation program to simulate the function of multiple PLC devices in the track junction sensor-signal control part in the railway signaling system. |                                                    |
| Stations Sensor-Signal PLC Simulator        | Lvl-1   | A emulation program to simulate the function of multiple PLC devices in the station train dock guiding sensor-signal control part in the station signaling system. |                                                    |
| Train Sensor-Power PLC Simulator            | Lvl-1   | A emulation program to simulate the function of PLC device on Train to control the train's power and the motion. |                                                    |
| Train Sensor RTU Simulator                  | Lvl-1   | A emulation program to simulate the function of RTU device on Train to read trains' sensor data and send back to the SCADA-HMI system |                                                    |
| Trains Controller HMI                       | Lvl-2   | HMI to connect to the train control PLC and RTU to monitor train state and control the trains operation. | [> Detailed Program Doc](src/scadaEmuUI/readme.md) |
| Railway Controller HMI                      | Lvl-2/3 | SCADA HMI in railway track management HQ to monitor and control the railway track operation. |                                                    |

#### Introduction of the cyber range networks

The cyber range provide four different network to simulate the IT-OT environment from level0 to level5, the overview of the network is shown below:

![](doc/img/RmImg/rm_02_network.png)

`version v0.1.4 (2024)`

1. **Corporate network**: This subnet replicates a typical railway company's corporate IT system network, encompassing various functional servers (wen, email, DMZ, staff management...) and a production management workstation. This workstation hosts essential components such as the production log archiving database, internal document server, and operator manuals. It will simulate the `Level 5 Internet DMZ Zone` and `Level 4 Enterprise Zone`  of the IT-OT environment.
2. **Supervision SCADA network**: A subnet simulating the OT environment SCADA system network, this subnet features distinct SCADA data/historian servers, multiple HMI computers for system operators, and maintenance computers dedicated to ICS/OT-system engineers. It will simulate the `Level 3 Operations Management Zone`  and  `Level 2 Control Center (HQ) Processing LAN` of the OT environment.
3. **Production network**: This subnet host all ICS field device PLC & RTU simulator programs, contributing to a realistic representation of the production environment within the railway system. It will simulate the `Level 1 Controller LAN` of the OT environment.  
4. **Physical real-world emulation network**: In this subnet, railway real-world components are emulated to demonstrate the tangible effects of actual physical items / device (sensors, moto, switch ...) in the real working environment, all the device simulation program will running in this subnet to generate the "virtual" electrical signal and feed the signal in the PLC and RTU in the production network. This network will simulate the `Level 0 Physical Process Field I/O devices` of the OT environment. 



------

### Project Use Case

**Cross Sword 2023**

We are glad to share that the Railway [Metro] IT/OT Emulation System Cyber Security Test Platform we developed this year was used for building one part of the cyber-attack target training system in the NATO CCDCOE Cross Sword 2023 offensive cyber exercise. CCDCOE LinkedIn POST: [ > link](https://www.linkedin.com/posts/natoccdcoe_crossedswords-activity-7140986334961217536-7dM5/?utm_source=share&utm_medium=member_desktop)

![](doc/img/RmImg/rm_04_usecase01.png)

**OT Cyber exercise workshop case studies**

Currently we use our the cyber range provide different demo and hands-on training  case study  for IT-OT cyber attack workshop.



------

### System Design 





**Railway Company OT-System Cyber Range Introduction**

The OT-System Cyber Range is designed to replicate the tangible, physical hardware aspects of a railway system. It will emulate the railway control center featuring a supervisory SCADA network, the Sensor Signal PLC network governing railway and train control in the production environment and emulate the physical wire connections that constitute the real-world infrastructure

![](doc/img/networkCommDesign.png)

Included components: 

- One real world emulator
- One HQ HMI (master mode) 
- N train dispatcher HMI (slave mode )
- 2 train control PLC
- 3 Junction signal control PLC
- 3 Station control PLC
- One train operator HMI (master mode)
- N train driver HMI
- N train safety checker HMI



**Railway Company IT-System Cyber Range** **Introduction**

Railway[Metro] **IT** System security mini cyber range is constructed by 5 main sub-network (introduced in the program design) under below structure. Within the IT System Cyber Range, our goal is to meticulously simulate not only the hardware infrastructure of the Company's network but also replicate the daily human activities of Railway Company staff. This approach aims to create an immersive and realistic environment closely resembling the operations of a genuine railway company.

![](attack/img/topology.png)

Six kinds of different railway company staff human activity emulator: 

- IT-Support-Engineer
- Railway Officer, 
- Railway HQ operator, 
- Train driver / Operator 
- Railway safety checker
- Railway maintenance engineer

`Version v0.3.1`

------

### Detailed Sub-System Design

The detail introduction of each component is shown below: 

#### 1. 2D Railway[Metro] System Real-world Emulator

Our objective is to develop a Railway system emulator that accurately simulates real-world scenarios, including trains navigating tracks, responding to signal systems, docking at stations, and being controlled by train drivers. The system encompasses four tracks, ten trains, a track junction signal control system, a station control system, and a train driver controller. Additionally, the emulator facilitates connectivity to three sets of PLC modules through a dedicated PLC interface. This comprehensive design aims to provide a realistic and dynamic railway simulation environment. 2D Railway[Metro] System real-world emulator UI: 

![](doc/video/connectionHub5.gif)

2D Railway[Metro] System real-world emulator UI detailed software design document: [ > link](doc/metroEmuUI_readme.md)



#### 2. Railway System SCADA HMI

Our aim is to develop a Railway SCADA (Supervisory Control and Data Acquisition) program integrated with a Human Machine Interface (HMI) to facilitate the comprehensive monitoring and control of multiple railway junctions and stations. The envisioned functionalities include:

- Offering a PLC (Modbus TCP) connection interface for fetching and setting the PLCs' register and coil states.
- Visualizing the current state of connected PLCs, including holding register states, coil states, and digital I/O states.
- Providing a visual representation of the state of tracks, including sensor and signal states, along with an overview of the sensor-signal auto-controlling process.
- Displaying the state of tracks and train-station sensors and signals, along with insights into the auto-controlling processes.
- Implementing an overload control mechanism for sensor and signal states, accessible with appropriate administrative engineer debug permissions.

Railway System SCADA HMI UI :

![](doc/video/scadaHmi.gif)

Railway System SCADA HMI detailed software design document: [> link](doc/scadaHMI_readme.md)



#### 3. Railway System Trains Controller HMI

Our goal is to develop a Trains Controller Human Machine Interface (HMI) that offers comprehensive information visualization and control capabilities for multiple trains. The key functions include:

- Implementing a PLC (Modbus TCP) connection interface to facilitate the fetching and setting of PLC register and coil states.
- Visualizing the current states of connected PLCs, including holding registers and coils.
- Extracting data from trains control PLC sets to simulate a 750V-DC power trains system. This system will then display pertinent trains information such as speed, current, and voltage to the user.
- Incorporating a Trains Power Control Panel, allowing users to effortlessly toggle the power states of individual trains.

This design ensures an efficient and user-friendly interface for monitoring and controlling multiple trains, offering real-time insights into their vital parameters and enabling seamless power management. 

Railway System Trains Controller HMI UI:

![](doc/video/trainHMIhalf.gif)

Railway System Trains Controller HMI detailed software design document: [> link](doc/trainsCtrlHMI.md)



#### 4. Railway Junctions Sensor-Signal System Control PLC Simulator

**Project Design :** we want to create a Programmable Logic Controllers(PLC) set with 3 PLCs to below tasks:

1. Read the 39 train sensors (connect to PLCs' input) state from the real-word emulator to PLCs' holding register state.
2. Run the pre-set ladder logic (flip-flop latching relay) to change the 19 real-world signals (connect to PLCs' output coils) state. 
3. Create a Modbus server to handle the HMI's Modbus TCP request to update/change register/coils value. 

This simulator will simulate 3 standard Siemens S71200 PLCs (16 input + 8 output / total 48 input + 24 output) PLCs connected under master and salve mode.  The PLCs set Electrical I/O connection and the Ladder logic is shown below. 

![](doc/img/signalPlc.png)

Railway Junctions Sensor-Signal System Control PLC Simulator detailed software design document: [ > link](doc/sensorsPLCSimu_readme.md)



#### 5. Railway Stations Sensor-Signal System Control PLC Simulator

**Project Design :** we want to create a Programmable Logic Controllers(PLC) set with 3 PLCs to below tasks:

1. Read the 22 train stations' train dock sensors  (connect to PLCs' input) from the real-word emulator to PLCs' holding register state.
2. Run the pre-set ladder logic (direct trigger latching relay) to change the 44 real-world station enter/exit signals (connect to PLCs' output coils) state. 
3. Create a Modbus server to handle the HMI's Modbus TCP request to update/change register/coils value. 

This simulator will simulate 3 standard Siemens S71200 PLCs (16 input + 8 output / total 48 input + 24 output) PLCs connected under master and salve mode. The PLCs set Electrical  I/O connection and the Ladder logic:

![](doc/img/stationPlc.png)

Railway Stations Sensor-Signal System Control PLC Simulator detailed software design document: [> link](doc/stationPLCSimu_readme.md)



#### 6. Railway Trains Sensor-Power System Control PLC Simulator

**Project Design :** we want to create a Programmable Logic Controllers(PLC) set with 2 PLCs to below tasks:

1. Read the 10 trains speed sensors  (connect to PLCs' input) from the real-word emulator to PLCs' holding register state.

2. Use 10 PLC output coils to control the trains power.
3. Create a Modbus server to handle the HMI's Modbus TCP request to update/change register/coils value. 

This simulator will simulate 2 standard Siemens S71200 PLCs (16 input + 8 output / total 32 input + 16 output) PLCs connected under master and salve mode. The PLCs set Electrical I/O connection and the Ladder logic:

![](doc/img/trainPlc.png)

Railway Trains Sensor-Power System Control PLC Simulator detailed software design document: [link](doc/trainsPlcSimu_readme.md)



**Program version:** `v0.3.2`

Code base: https://github.com/LiuYuancheng/Metro_emulator/tree/main/src

------

### System Network Design 

#### Main cyber range network design

![](doc/img/network_mapping.png)

#### OT cyber range network design

![](doc/img/networkDesign.png)



------

### Cyber Attack Demonstration Case Study

Currently we use our mini cyber range provide one IT cyber attack case study and four different OT cyber attack case study. 

#### IT system cyber attack case study

##### IT system cyber attack case 1: Phishing and backdoor trojan 

![](doc/img/attackRoadMap.png)

Detailed case study document [> link](https://github.com/LiuYuancheng/Cross-Sword-2023-Nato-Event/blob/main/attackDemos/falseDataInjection/instructorManual_FDJ.md)

#### OT system cyber attack case study

##### OT Cyber Attack Demo on PLC [Case Study 01] : False Data / Cmd Injection Attack Case

![](attack/img/falseCmdInjection.png)

Detailed case study document [> link](attack/OT_attack_case1_falseCmdInjection.md)

##### OT Cyber Attack Demo on HMI  [Case Study 02] : ARP Spoofing Attack Case

![](attack/img/ArpSpoofing/arpspoofing.png)

Detailed case study document [> link](attack/OT_attack_case2_arpSpoofingAttack.md)

##### OT Cyber Attack Demo on PLC [ Case Study 03 ] : DDoS Attack Case

![](attack/img/ddos/ddosAtkRoadmap.png)

Detailed case study document [> link](attack/OT_attack_case3_ddosModbusAttack.md)

##### OT Cyber Attack Demo on HMI-PLC control Chain [ Case Study 04 ] : Man in the middle Attack Case

![](attack/img/mitm/attackRoadmap.png)

Detailed case study document [> link](attack/OT_attack_case4_MitmAttack.md)



------

#### Problem and Solution

Refer to `doc/ProblemAndSolution.md`



------

> last edit by LiuYuancheng (liu_yuan_cheng@hotmail.com) by 30/05/2023 if you have any problem, please send me a message. 