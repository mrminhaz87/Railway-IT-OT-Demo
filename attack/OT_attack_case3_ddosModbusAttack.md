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