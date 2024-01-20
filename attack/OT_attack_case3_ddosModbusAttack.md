# OT Cyber Attack Demo on PLC [ Case Study 03 ] : DDoS Attack Case

**Project Design Purpose** : The objective of this case study is to develop a workshop which utilizing the Railway (Metro) IT/OT System Cyber Security Test Platform (mini cyber range) , DDoS Attack Management System and DDoS PLC(Modbus-TCP) Attacker for demonstrating the distributed denial-of-service attack on one in the OT system. Our aim is to showcase how a hacker (cyber range red team member) could potentially launch a DDoS attack on the OT Programable Logic Controller which caused interruption on the PLC control chain. This particular attack scenario is proposed as one of the demonstration cases for the Cross Sword 2023 Test/Partners-Run, providing a realistic and controlled environment to assess the cybersecurity resilience of the railway infrastructure.

**Attacker Vector** :  Distributed denial-of-service attack

>  Important : The demonstrated attack case is used for education and training for different level of IT-OT cyber security ICS course, please don't apply it on any real world system.

[TOC]

------

### Introduction

The attack study case comprises three sub-projects :

- Railway[Metro] IT/OT System Mini Cyber Range System [> Link of project document](https://github.com/LiuYuancheng/Railway_IT_OT_System_Cyber_Security_Platform)
- DDoS Attack Management System [> Link of the project document](https://github.com/LiuYuancheng/Python_Malwares_Repo/blob/main/src/ddosAttacker/readme.md)
- DDoS PLC(Modbus-TCP) Attacker  [> Link of the project document](https://github.com/LiuYuancheng/Python_Malwares_Repo/blob/main/src/ddosPlcAttacker/readme.md)

In this study case, we envision a scenario where a red team attacker/hacker successfully implants the DDoS-Attack-Program on several computers in the railway system  cooperate network, the supervision network and even the production network an IT-Network-Attack (such as employing a phishing email). The target is one of the PLC in the production network which will control the trains power.  The attack study case will illustrate how a red team attacker, external to the railway mini cyber range, control multiple DDoS attacker to launch the DDoS Modbus-TCP requests attack at the same time to Interrupt the normally OT HMI-PLC control chain.  This will be accomplished by utilizing the Red Team C2 DDoS Attack Management System from the internet and successfully bypassing the firewall's detection mechanisms.

The attack detailed road map is shown below : 

![](img/ddos/ddosAtkRoadmap.png)

##### Key Tactics, techniques, and procedures (TTP) of the attack

Based on the attack detailed road map there will 4 kinds TTP are included in the ARP spoofing attack scenario : 

**Botnets:**

- **Tactic:** Enlist a large number of compromised devices to form a botnet.
- **Technique:** Malicious actors infect and control a network of computers, servers, or IoT devices (botnet) to generate and send a massive volume of traffic to the target.
- **Procedures**: To simulate the botnets DDoS attack, we configured 3 nodes in different network to send the high frequency Modbus-TCP request. 

**Amplification Attacks:**

- **Tactic:** Increase the volume of attack traffic.
- **Technique:** Exploit protocols that allow a small request to trigger a much larger response. Examples include DNS amplification, NTP amplification, and SNMP reflection attacks.
- **Procedures** : Each  DDoS attacker will parallel start as much thread (100+) as possible to fully use the nodes' network bandwidth to sending the request simultaneously. 

**Layer 7 Attacks (Application Layer):**

- **Tactic:** Exploit vulnerabilities in the application layer.
- **Technique:** Target specific applications or services to exhaust server resources. Examples include HTTP floods, Slowloris attacks, and application-specific exploits.
- **Procedures**: The attack is targeting the PCL's firmware via ModBus-TCP protocol, Modbus-TCP is an Ethernet-based variant of the Modbus protocol, which is commonly used in industrial automation systems for communication between programmable logic controllers (PLCs), computers, and other devices. Modbus-TCP is designed to operate over TCP/IP networks and is used for reading and writing data between devices in real-time industrial applications.

**Bot Spoofing and Obfuscation:**

- **Tactic:** Evade detection and analysis.
- **Technique:** Employ techniques to make the malicious traffic appear more legitimate, such as using diverse user agents, randomizing payloads, or mimicking legitimate user behavior.
- **Procedures :**To camouflage the communication, all interactions between the Malicious-Action-Programs and the Command and Control (C2) system will be disguised as standard HTTPS POST requests and responses, the key control message will be encrypted via pre-set session key. Notably, the package size will be kept minimal (less than 1KB) to prevent triggering the firewall's alert mechanisms related to download/upload activities.



------

### Background Knowledge 

Within this section, we aim to provide fundamental, general knowledge about each respective system and elucidate the Tactics, Techniques, and Procedures (TTP) associated with the attack vectors. This foundational information will serve as a primer for understanding the intricate details of the systems involved and the methodologies employed in the attack scenarios.

##### Distributed denial-of-service attack

A distributed denial-of-service (DDoS) attack is a malicious attempt to disrupt the normal traffic of a targeted server, service or network by overwhelming the target or its surrounding infrastructure with a flood of Internet traffic.

DDoS attacks achieve effectiveness by utilizing multiple compromised computer systems as sources of attack traffic. Exploited machines can include computers and other networked resources such as [IoT devices](https://www.cloudflare.com/learning/ddos/glossary/internet-of-things-iot/).

From a high level, a DDoS attack is like an unexpected traffic jam clogging up the highway, preventing regular traffic from arriving at its destination. A basic application later DDoS attack diagram is shown below: 

![](img/ddos/ddosApplayer.png)

Reference: https://www.cloudflare.com/learning/ddos/what-is-a-ddos-attack/

##### Railway[Metro] IT/OT Mini Cyber Range System

For the Railway IT/OT System general introduction please refer refer to the [study case 1](OT_attack_case1_falseCmdInjection.md), the cyber range system diagram is shown below:

![](img/railwayCyberRange.jpg)

**Human-Machine Interface**: In the context of industrial automation and control systems, OT HMI refers to the Human-Machine Interface used in Operational Technology (OT) environments. OT encompasses the technologies and systems used to monitor and control physical devices, processes, and infrastructure in sectors like manufacturing, energy, utilities, and transportation.

**Targeted Host/App/Service** : In this attack case study, as shown in the the `Attack detailed road map`  the target is on of the trains control PLC in the production network of Railway IT/OT Mini Cyber Range and the Train control HMI which is running on one work station in the system's supervision network ( operation room ).  It provides a graphical representation of the operational status, real-time data, and control options, allowing operators to monitor and manage industrial processes efficiently  monitor for the HQ operator to monitor the Trains speed, power, brake, voltage and current information and the Train Operator/Driver can also control the train via the HMI. The Main UI is shown below :

