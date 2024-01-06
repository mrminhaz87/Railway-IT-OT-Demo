# OT Cyber Attack on PLC [Study case 01] : False Data / Cmd Injection Attack Case

**Project Design Purpose** : We want to create some demo / study case to use the Railway[Metro] IT/OT System Cyber Security Test Platform, the Red Team C2 System and the Modbus false data injector program to demo how a hacker launch an OT(operational technology) Cyber Attack on railway train control PLC (Programmable logic controller) which may caused the trains collision accident. This attack cases is proposed as one of the attack demo cases in the Cross Sword 2023 Test-Run.

**Attacker Vector** :  Modbus False Data / Command Injection

Important : The demonstrated attack case is used for education and training for any level of IT-OT cyber security ICS course, don't apply it on any real world system.

[TOC]

------

### Introduction

The Attack Study Case include 3 sub project : 

- Railway[Metro] IT/OT System Mini Cyber Range System [link of project document](https://github.com/LiuYuancheng/Railway_IT_OT_System_Cyber_Security_Platform)
- Red Team C2 Emulation system [link of project document](https://github.com/LiuYuancheng/Python_Malwares_Repo/tree/main/src/c2Emulator)
- Modbus false command injector program [link of project document](https://github.com/LiuYuancheng/Python_Malwares_Repo/tree/main/src/falseCmdInjector) 

In this study case, we assume the hacker has implanted the false command injector program Via IT-Attack (such as using phishing email) to one of the maintenance computer in the SCADA supervision network. The attack study case will show how a red team attacker outside the railway mini cyber range launch one OT-Modbus false data injection attack and one OT-Modbus false command injection attack to the Railway train control PLC by using the Red team C2 system from internet and by pass the firewall's detection.

The attack road map is shown below : 

![](img/attackRoadmap.png)

Key Tactics, techniques, and procedures (TTP) of the attack: 

- The red team attacker will control the Malicious-Action-Programs via RTC2's web-UI from any where in the internet.
- All the communication between Malicious-Action-Programs and C2 are camouflaged as normal https POST request and response. The package size will be very small ( less than 1KB ) to avoid trigger the firewall's download/upload alert.
- The Malicious-Action-Programs will inject wrong data under high frequency to keep overwriting the train detection sensor state value read by PLC during launching the false data injection to mass up the train collision safety mechanism. 
- After false data injection attack successful, the Malicious-Action-Programs will send wrong control train throttle command to make the train collision happens. 

#### Background Knowledge 

In this section we will introduce some basic general knowledge about each such system and the attack vector TTP. 

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

The Railway[Metro] IT/OT System Security Mini Cyber range is a mini railway operation company IT/OT network emulation system for the ICS researcher or instructor to test their IT/OT-attack and defense solution or used for ICS security training and education purpose. The whole system contents 4 main part networks (as show in the below diagram) :

![](img/railwayCyberRange.jpg)

1. **Cooperate network**: A subnet simulates a normal railway company cooperate IT network with different function/ERP servers (email, DMZ, staff management) and the production management workstation (production log archiving database, internal document server, operator manuals)
2. **Supervision SCADA network**: A subnet simulate the SCADA system network with different SCADA data/historian servers, different HMI computers for system operators and maintenance computers for ICS/OT-system engineers.
3. **Production network**: A subnet contents different PLC simulators program.
4. **Physical real-world emulation network**: A subnet contents railway real-word components emulation program to show the physical effect of the real-work items.

>  Railway[Metro] IT/OT System Mini Cyber Range System Project link : [GitHub Repo](https://github.com/LiuYuancheng/Railway_IT_OT_System_Cyber_Security_Platform)



##### Red Team C2 Emulation System

The Red Team Command and Control (RTC2) server, commonly known as a C&C server, plays a pivotal role in cyber exercises and ranges. It serves as a centralized hub that red team members use to control and communicate with simulated compromised victims. This command center enables red team members or attackers to seamlessly issue instructions to the compromised machines, collect data from them, and coordinate various malicious activities within the exercise program. Our goal is to offer a comprehensive C2 server emulation solution designed for cyber exercise red team members. This solution allows them to seamlessly integrate different probing programs and malicious action programs, providing dynamic monitoring, scheduling, and control capabilities. The versatility of our solution makes it applicable across a range of fields, offering a robust platform for enhancing cyber defense readiness and testing the resilience of security measures.

![](img/c2overview.png)

> Red Team C2 Emulation System Project Link : [GitHub Repo](https://github.com/LiuYuancheng/Python_Malwares_Repo/tree/main/src/c2Emulator)



##### Modbus false command injector program

The false command injection program will provide False Data Injection (FDI) and False Command Injection (FCI) function for red team attacker to inject Modbus control data/command to either the PLC or HMI system as shown in below common False command / data injection example: 

![](img/falseDataInjection.png)

- This Modbus data injector malware is modified from the backdoor trojan program <backdoorTrojan.py> by adding the plc-Modbus communication module so the C2 Emulation system can remote control it and use it to launch the false command injection attack 

- The attack demo will show a false command injector program to attack the OT-system control chain : `Train Control HMI` -> `Train Control PLC` -> `Real-world Trains in the railway system` will illegal PLC Modbus control request. 
- The injector will issue the illegal/false Modbus command (such as inject the train front detection sensor’s holding register’s state) to make the PLC generate the incorrect electrical signal to the train then cause the trains accident happens.

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