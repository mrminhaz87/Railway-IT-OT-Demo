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

The false command injection program will provide False Data Injection (FDI) and False Command Injection (FCI) function for red team attacker to inject Modbus control data/command to either the PLC or HMI system as shown in below example: 

![](img/falseDataInjection.png)

- This Modbus data injector malware is modified from the backdoor trojan program <backdoorTrojan.py> by adding the plc-Modbus communication module so the C2 Emulation system can remote control it and use it to launch the false command injection attack 

- The attack demo will show a false command injector program to attack the OT-system control chain : `Train Control HMI` -> `Train Control PLC` -> `Real-world Trains in the railway system` will illegal PLC Modbus control request. 
- The injector will issue the illegal/false Modbus command (such as inject the train front detection sensor’s holding register’s state) to make the PLC generate the incorrect electrical signal to the train then cause the trains accident happens.

> Modbus false command injector program program link: [GitHub Repo](https://github.com/LiuYuancheng/Python_Malwares_Repo/tree/main/src/falseCmdInjector)