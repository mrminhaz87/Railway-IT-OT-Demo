# Railway System SCADA HMI

**Project Design :** We want to create a railway SCADA (Supervisory Control and Data Acquisition) program with a HMI (Human Machine Interface ) to provide below multiple railway junctions and stations state monitor and control functions:

- Provide PLC (Modbus TCP) connection interface to fetch/set the PLCs' register/coils state.
- Visualize the connected PLC's holding register state, coils state and the digital I/O state. 
- Visualize the tracks junction the sensor & signal state and sensor-signal auto-controlling process. 
- Visualize the tracks train-station sensor & signal state and sensor-signal auto-controlling process  . 
- Provide the sensors and signals' state overload control (admin engineer debug permission).

[TOC]

------

### Introduction 

The Railway System SCADA HMI is part of the Railway IT/OT System security test platform. It is used to monitor the whole railway tracks sensors-signal auto control system.  You can refer the system topology diagram to check its function in the system by below link:

-  [Railway IT/OT System security test platform system structure diagram](img/networkCommDesign.png)
-  [Railway IT/OT System security test platform network topology diagram](img/networkDesign.png)



**Railway System SCADA HMI User Interface**

![](video/scadaHmi.gif)

The HMI contents below components and function:

- A train sensors-signal relation map to show sensors state, signals state and the sensors-signals auto control relation ship (tracks-cross-junction and train-stations). 
- Three PLC panel to show the junction-sensor-signal control system's Digital Input/Output state, PLC holding register state and the PLC Coils state. 
- Three PLC panel to shoe the station-sensor-signal control system's Digital Input/Output state, PLC holding register state and the PLC Coils state. 

**Program version:** `v0.1.2`

Code Base: https://github.com/LiuYuancheng/Metro_emulator/tree/main/src/scadaEmuUI



------

### Program design

The program contents 2 main threads: 

- Main user interface thread : HMI map to show the junctions and stations' sensor-signal state, junction control PLC set [PLC-00, PLC-01 and PLC-02] state with the digital I/O information, station control PLC set [PLC-03, PLC-04 and PLC-05] state with the digital I/O information.
- PLC Communication thread : communicate with the Railway Junctions Sensor-Signal System Control PLC Simulator and Railway Stations Sensor-Signal System Control PLC Simulator through Modbus TCP to get the OT data.

This is the program modules workflow diagram: 

![](img/scadaHMI/workflow.png)



##### User interface design

The program user interface design detail is shown below:

![](img/scadaHMI/uidetail.png)



##### Program module files list

| Idx  | Program File       | Execution Env | Description                                                  |
| ---- | ------------------ | ------------- | ------------------------------------------------------------ |
| 1    | trainHMIConfig.txt |               | system config file.                                          |
| 2    | trainCtrlGlobal.py | python 3      | System global file, the system config file's contents will be saved in the global parameters. |
| 3    | trainCtrlPanel.py  | python 3      | All the UI function panels module.                           |
| 4    | trainDataMgr.py    | python 3      | This module provides map manger to generate the display panel ,  data manger to process the PLC data, PLC connector to communicate with PLC. |
| 5    | trainCtrlRun.py    | python        | Main HMI user interface.                                     |
|      |                    |               |                                                              |









