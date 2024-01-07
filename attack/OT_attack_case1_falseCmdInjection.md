# OT Cyber Attack Demo on PLC [Case Study 01] : False Data / Cmd Injection Attack Case

**Project Design Purpose** : The objective of this case study is to develop a demonstration and workshop utilizing the Railway (Metro) IT/OT System Cyber Security Test Platform, the Red Team Command and Control (C2) System, and the Modbus false data injector program. Our aim is to showcase how a hacker (red team member) could potentially launch an Operational Technology (OT) Cyber Attack on the programmable logic controllers (PLCs) governing railway train control, with the potential consequence of causing a collision accident between two trains. This particular attack scenario is proposed as one of the demonstration cases for the Cross Sword 2023 Test-Run, providing a realistic and controlled environment to assess the cybersecurity resilience of the railway infrastructure.

**Attacker Vector** :  Modbus False Data / Command Injection

> Important : The demonstrated attack case is used for education and training for different level of IT-OT cyber security ICS course, please don't apply it on any real world system.

[TOC]

------

### Introduction

The attack study case comprises three sub-projects :

- Railway[Metro] IT/OT System Mini Cyber Range System [link of project document](https://github.com/LiuYuancheng/Railway_IT_OT_System_Cyber_Security_Platform)
- Red Team C2 Emulation system [link of project document](https://github.com/LiuYuancheng/Python_Malwares_Repo/tree/main/src/c2Emulator)
- Modbus false command injector program [link of project document](https://github.com/LiuYuancheng/Python_Malwares_Repo/tree/main/src/falseCmdInjector) 

In this study case, we envision a scenario where a red team attacker/hacker successfully implants the false command injector program via an IT-Attack, such as employing a phishing email, targeting one of the maintenance computers in the SCADA supervision network. The attack study case will illustrate how a red team attacker, external to the railway mini cyber range, executes an OT Modbus false data injection attack and an OT Modbus false command injection attack on the Railway train control programmable logic controller (PLC). This will be accomplished by utilizing the Red Team C2 system from the internet and successfully bypassing the firewall's detection mechanisms.

The attack detailed road map is shown below : 

![](img/attackRoadmap.png)

Key Tactics, techniques, and procedures (TTP) of the attack: 

- The red team attacker will remotely control the Malicious-Action-Programs through RTC2's web-UI, enabling access from any location on the internet.
- To camouflage the communication, all interactions between the Malicious-Action-Programs and the Command and Control (C2) system will be disguised as standard HTTPS POST requests and responses. Notably, the package size will be kept minimal (less than 1KB) to prevent triggering the firewall's alert mechanisms related to download/upload activities.
- The Malicious-Action-Programs will execute a high-frequency injection of inaccurate data, deliberately overwriting the state values of train detection sensors read by the PLC. This continuous false data injection aims to disrupt the train collision safety mechanism.
- Following the successful execution of the false data injection attack, the Malicious-Action-Programs will transmit incorrect commands to control the train throttle, intentionally inducing a collision between trains. This multi-step approach is designed to exploit vulnerabilities in the system's detection and control mechanisms, posing a significant threat to the overall safety of the railway infrastructure.

#### Background Knowledge 

Within this section, we aim to provide fundamental, general knowledge about each respective system and elucidate the Tactics, Techniques, and Procedures (TTP) associated with the attack vectors. This foundational information will serve as a primer for understanding the intricate details of the systems involved and the methodologies employed in the attack scenarios.

##### False Data Injection (FDI) and False Command Injection (FCI)

False Data Injection (FDI) and False Command Injection (FCI) are both types of cyber attacks that can target Operational Technology (OT) systems, which are used in industrial control and critical infrastructure environments. However, they differ in their objectives and methods.

1. **False Data Injection (FDI):**

   - **Objective:** The main goal of FDI is to manipulate the data within the OT system, leading to incorrect or misleading information being processed by the control systems.
   - **Method:** Attackers inject false or manipulated data into the sensors or communication channels within the OT system. This can lead to the control systems making incorrect decisions based on the compromised data.

   **Example:** In a power grid, an FDI attack might involve injecting false sensor readings that indicate lower electricity demand than actual. This could lead to incorrect decisions in adjusting power generation levels, potentially causing disruptions or even damage to the system.

2. **False Command Injection (FCI):**

   - **Objective:** FCI aims to manipulate the commands sent to the control systems, causing them to execute unauthorized or malicious actions.
   - **Method:** Attackers inject false or unauthorized commands into the communication channels or control signals of the OT system. This can lead to the control systems taking actions that are not intended or authorized.

   **Example:** In an industrial manufacturing plant, an FCI attack might involve injecting false commands that instruct a robotic arm to perform unsafe movements or alter production parameters. This could lead to physical damage to equipment or compromise the quality of manufactured products.

In summary, while both FDI and FCI attacks target OT systems, FDI focuses on manipulating the data flowing through the system to deceive decision-making processes, while FCI involves injecting false commands to manipulate the actions of the control systems. Both types of attacks can have serious consequences, potentially leading to operational disruptions, safety hazards, or damage to critical infrastructure. Security measures, such as network segmentation, encryption, and intrusion detection systems, are crucial for protecting OT systems from these types of attacks.



##### Railway[Metro] IT/OT System Mini Cyber Range System

The Railway[Metro] IT/OT System Security Mini Cyber Range serves as a compact emulation system for a railway operation company's IT/OT network. It caters to ICS researchers and instructors, providing a platform to assess and refine their IT/OT attack and defense solutions, as well as facilitating ICS security training and education. The comprehensive system is organized into four main network components, as illustrated in the diagram below:

![](img/railwayCyberRange.jpg)

- **Cooperate network**: This subnet replicates a typical railway company's corporate IT network, encompassing various functional servers (email, DMZ, staff management) and a production management workstation. This workstation hosts essential components such as the production log archiving database, internal document server, and operator manuals.
- **Supervision SCADA network**: Simulating the SCADA system network, this subnet features distinct SCADA data/historian servers, multiple HMI computers for system operators, and maintenance computers dedicated to ICS/OT-system engineers.
- **Production network**: This subnet houses diverse PLC simulator programs, contributing to a realistic representation of the production environment within the railway system.
- **Physical real-world emulation network**: In this subnet, railway real-world components are emulated to demonstrate the tangible effects of actual items in the real working environment.

>  Railway[Metro] IT/OT System Mini Cyber Range System Project link : [GitHub Repo](https://github.com/LiuYuancheng/Railway_IT_OT_System_Cyber_Security_Platform)



##### Red Team C2 Emulation System

The Red Team Command and Control (RTC2) server, commonly known as a C&C server, plays a pivotal role in cyber exercises and ranges. It serves as a centralized hub that red team members use to control and communicate with simulated compromised victims. This command center enables red team members or attackers to seamlessly issue instructions to the compromised machines, collect data from them, and coordinate various malicious activities within the exercise program. Our goal is to offer a comprehensive C2 server emulation solution designed for cyber exercise red team members. This solution allows them to seamlessly integrate different probing programs and malicious action programs, providing dynamic monitoring, scheduling, and control capabilities. The versatility of our solution makes it applicable across a range of fields, offering a robust platform for enhancing cyber defense readiness and testing the resilience of security measures.

![](img/c2overview.png)

> Red Team C2 Emulation System Project link : [GitHub Repo](https://github.com/LiuYuancheng/Python_Malwares_Repo/tree/main/src/c2Emulator)



##### Modbus False Command Injector Program

This program serves a dual purpose by offering both False Data Injection (FDI) and False Command Injection (FCI) capabilities, enabling red team attackers to inject Modbus control data/commands into either the Programmable Logic Controller (PLC) or Human Machine Interface (HMI) system. Illustrated below is a common example of false command/data injection:

![](img/falseDataInjection.png)

- he Modbus data injector malware is an adaptation of the backdoor trojan program `<backdoorTrojan.py>`, where a plc-Modbus communication module is integrated. This modification enables the C2 Emulation system to remotely control and utilize the injector for launching false command injection attacks.

- The attack demonstration will spotlight the false command injector program targeting the OT-system control chain: `Train Control HMI` -> `Train Control PLC` -> `Real-world Trains in the railway system` through illicit PLC Modbus control requests. The injector will execute an illegal/false Modbus command, such as injecting the state of the train front detection sensor's holding register, prompting the PLC to generate an incorrect electrical signal to the train, resulting in a simulated train accident. This showcase underscores the potential impact of false command injection on the safety and integrity of the railway system.

> Modbus false command injector program program link: [GitHub Repo](https://github.com/LiuYuancheng/Python_Malwares_Repo/tree/main/src/falseCmdInjector)



------

### Train Operation Workshop and Attack Procedures 

#### Train Operation Basic Background Knowledge Introduction 

There will be a short work shop to introduce the train basic train control part in the railway system before the red team members can implement the attack. The train cyber range network topology is shown below : 

![](img/topology.png)

The false data injection program will be implanted in one of the computer in the Operational room network, we named it as rail_op_victim. This computer is in the PLC's white list. 

**Real world Emulator Train Operation Introduction**

The trains on the real-world emulator will be under one of the below three states : 

![](img/TrainState.png)

The train operator can monitor the train state (speed, throttle state, break state and power state) from the Train control HMI panel. 

**Train’s Senor-Power physical wire connection to PLC and auto control logic** 

The train content 2 safety control to avoid collision happens: 

- Auto collision avoidance : each train will have a front collision detection sensor, when the sensor detected front got a train in a distance, it will auto trigger the break to slow down the train speed. 
- Manual collision avoidance : when the train operator find the train speed got exception or he think if there is a possible collision, he can press the train emergency stop button to stop the train. 

The train control PLC logic is shown below: 

![](img/TrainSafeCtrl.png)

- For each PLC there will be one coil to control the train's power, when the coils is turn off, the train throttle will be set to 0 and the break will on. 
- The train sensor will be linked to PLC's input, the sensor state will be record in a PLC holding register (HR0), then the holding register will trigger the ladder logic to change the break control coil. 
- The train speed sensor will be record in another holding register(HR1) and the HMI will read the speed data from the register. 

In normal state, the front collision detection sensor is not allowed to be changed by any Modbus control cmd from HMI. It can only be set by the train’s electrical sensor (such as a radar).

Attack malware will use illegal cmd to overwrite the front collision sensor’s state to mess up the train’s auto control logic to cause the trains accident

#### OT-Attack Procedures 

As Introduced in the previous section, we need to implement 2 kind of attack False Data Injection (FDI) and False Command Injection (FCI) to bypass the auto and manual train collision avoidance  safety mechanism to make the train accident happens. 

False Data Injection (FDI) :  we need to inject the incorrect front sensor detection data in the PLC's sensor data record holding register to bypass the auto collision avoidance mechanism. 

False Command Injection : we need to inject the incorrect train power control command to the train power coil to override the train operator's emergency stop action. 

##### Attack Pre-condition Introduction

In this demo, the false data injector has been installed in the previous IT-network attack. The victim machine (ip) which will the run the injector is in trains control PLC ‘s allow read and allow write list. The effected VMs in the OT network is shown below: 

![](img/AttackDiagram.png)

The attack demo will show a false command injector program to attack the OT-system control chain: Train Control HMI -> Train Control PLC -> Real-world Trains in the railway system will illegal PLC Modbus control request. 

The injector will issue the illegal/false Modbus command (such as inject the train front detection sensor’s holding register’s state) to make the PLC generate the incorrect electrical signal to the train then cause the trains accident happens.

##### Attack Procedure Introduction 

To make the train collision accident happens below: 

![](img/collsision.png)

The attack malware (injector) need to repeat inject at less 3 commands in two trains PLC under the frequency which higher than trains operator.

1. Keep sending power cut off command to the front train (ccline-0) to make it stop.
2. Keep send full throttle command to behind train (ccline-1) to make it rush to the front train (ccline-0) .
3. To avoid the behind train (ccline-1) collision detection sensor trigger train break, keep injecting the detection sensor clear cmd (holding register val=0, front safe) to ccline-1 PLC.

Then the accident will happen, the attack is possible to be detected by train operator if he found the train ccline-1’s throttle and speed is unusual.

**How the malware to prevent the train operator do emergency stop to save train if he detected the attack/exception state:**

As shown below PLC clock cycle : 

![](img/plcClock.png)

1. PLC will accept the command from t0 to t1 and update its memory.
2. Plc will execute its ladder logic based on the latest memory state at t1. the execute take a very short period t1 - t2.
3. The attacker will send multiple false cmd  in high sequency try to overwrite the train operator’s correct control command. Unless the operator can press the train emergency stop button supper fast (which is impossible faster than the malware program), then he will not be able to stop the train accident.



------

### Red Team Attack Detail Steps

As the red team attackers are our side the railway cyber range network. So to launch the attack then need to use the attack control C2 system. As introduced in the Attack Pre-condition Introduction section. The false data injection program is already executed in on of the maintenance computer in the cyber range, so when the red team attacker login the C2, then will see the false data/cmd injection program has been registered in the C2 as shown below : ![](img/C2Img/Register.png)

Before start to inject the data / command, the red team attacker needs to read the PLC data first. To assign a PLC task to the injector select link to task detail => Assign a special task via Json (in the malware tasks control page)

##### Read Holding Register State

Select the false Modbus data injector page, then select the **Assign a special task via Json**, then fill in the task detail : 

- TaskType: `modbus`
- Repeat: `int <number of the injection repeat times>`
- Tasks data: `read;reg;<start Holding register index>;<offset>`

Read Holding Register State

![](img/C2Img/readReg.png)

Press the `submit` button, when the false data injector report the task finished, check the result by click the `Show task result` button (As shown below the red team attacker can read the holding register data from HR0 to HR3) : 

![](img/c2Img/readRegRst.png)

After several try, the attacker can identify which holding registers are used in the PLC.

##### Read Output Coils State

Same as the previous steps, the red team attacker can fill in the task detail below to red the coil state to identify all the coils used by the PLC : 

- TaskType: `modbus`
- Repeat: `int <number of the injection repeat times>`
- Tasks data: `read;coil;<start coil index>;<offset>`

![](img/C2Img/readCoilRst.png)



##### Launch False Data Injection Attack

The red team need to override the train detection sensor's record in the holding register : send not detected val 0 to keep override the train detection sensor feedback data 1.  

- TaskType: `modbus`
- Repeat: `100000`
- Tasks data: `write;reg;3;0`

![](img/C2Img/writeReg.png)

After injected the sensor data the attacker can override the auto collision avoidance mechanism.



##### Launch False Command Injection Attack

The red team need to override the train emergency control coil's value : keep sending the emergency stop OFF value to the related PLC.  

- TaskType: `modbus`
- Repeat: `10000`
- Tasks data: `write;coil;3;1`

![](img/C2Img/writeCoil.png)

Press the `submit` button, when the false data injector report the task finished, check the result by click the `Show task result` button : 

![](img/C2Img/writeCoilRst.png)



##### Attack Demo Video

https://www.youtube.com/watch?v=J0qpOhigNL8&t=16s



------

> Last edit by LiuYuancheng(liu_yuan_cheng@hotmail.com) at 06/01/2024, if you have any problem, please send me a message.  Copyright (c) 2023 LiuYuancheng