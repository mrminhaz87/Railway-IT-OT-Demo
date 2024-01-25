# OT Cyber Attack Demo on PLC [ Case Study 04 ] : Man in the middle Attack Case

**Project Design Purpose** : The objective of this case study is to develop a workshop which utilizing the Railway (Metro) IT/OT System Cyber Security Test Platform (mini cyber range), the Red Team Command and Control (C2) System and the Ettercap Wrapper for demonstrating the Man-in-the-Middle (MitM) attack on OT system.  Our aim is to showcase how a hacker (cyber range red team member) could potentially launch an MitM attack to modify the control command between HMI and PLC to caused the train accident situation. This particular attack scenario is proposed as one of the demonstration cases for the Cross Sword 2023 Test-Run, providing a realistic and controlled environment to assess the cybersecurity resilience of the railway infrastructure. It is a advanced ARP spoofing attack scenario of the [Case Study 2](OT_attack_case2_arpSpoofingAttack.md) and the Mitm is more difficulty for the operator to detect. 

**Attacker Vector** :  Man-in-the-Middle (MitM) attack / ARP Spoofing

> Important : The demonstrated attack case is used for education and training for different level of IT-OT cyber security ICS course, please don't apply it on any real world system.

[TOC]

------

### Introduction

The attack study case comprises three sub-projects :

- Railway[Metro] IT/OT System Mini Cyber Range System [> Link of project document](https://github.com/LiuYuancheng/Railway_IT_OT_System_Cyber_Security_Platform)
- Red Team C2 Emulation system [link of project document](https://github.com/LiuYuancheng/Python_Malwares_Repo/tree/main/src/c2Emulator)
- Ettercap Wrapper program [link of project document](https://github.com/LiuYuancheng/Python_Malwares_Repo/tree/main/src/ettercapWrapper)

In this study case, we envision a scenario where a red team attacker/hacker successfully implants the packet parser and data replacer (a wrapper program of MITM Tool Ettercap) via an IT-Network-Attack (such as employing a phishing email) which targeting one of the maintenance computers in the SCADA supervision network.  The attack study case will illustrate how a red team attacker ( who is external of the railway mini cyber range ) executes Ettercap wrapper to launch the ARP spoofing attack first, then use apply the Modbus packet parser to find the specific PLC control data stream, then use the replacer to modify the PLC coils' control bytes to reverse the final electrical signal control in the real world. This will be accomplished by utilizing the Red Team C2 system from the internet and successfully bypassing the firewall's detection mechanisms.

The attack detailed road map is shown below : 

![](img/mitm/attackRoadmap.png)

