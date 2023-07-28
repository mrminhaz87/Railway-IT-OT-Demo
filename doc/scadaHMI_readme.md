# Railway System SCADA HMI

**Project Design :** We want to create a railway SCADA (Supervisory Control and Data Acquisition program with a HMI (Human Machine Interface ) to provide multiple  railway junction and station state monitoring and control with below functions:

- Provide PLC (Modbus TCP) connection interface to fetch/set the PLC's register/coils state.
- Visualize the connected PLC's holding register and coils state and the digital I/O state of the PLC. 
- Visualize the tracks junction sensor-signal auto-controlling process and the sensor-signal state. 
- Visualize the tracks train-station sensor-signal auto-controlling process and the sensor-signal state. 
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

- A train sensors-signal relation map to show sensor state, signal state and the sensors-signals auto control relation ship (tracks-cross-junction and train-stations). 
- Three PLC panel to show the junction-sensor-signal control system's Digital Input/Output state, PLC holding register state and the PLC Coils state. 
- Three PLC panel to shoe the station-sensor-signal control system's Digital Input/Output state, PLC holding register state and the PLC Coils state. 

**Program version:** `v0.1.2`

Code Base: https://github.com/LiuYuancheng/Metro_emulator/tree/main/src/scadaEmuUI



------

