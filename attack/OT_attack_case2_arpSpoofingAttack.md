# OT Cyber Attack Demo on HMI  [Case Study 02] : ARP Spoofing Attack Case

**Project Design Purpose** : The objective of this case study is to develop a demonstration and workshop utilizing the Railway (Metro) IT/OT System Cyber Security Test Platform, the Red Team Command and Control (C2) System and the Ettercap Wrapper for APR Spoofing attack on OT system.  Our aim is to showcase how a hacker (red team member) could potentially launch an ARP Spoofing Attack on the OT system Human Machine Interface (HMI) which caused the Operation Room HQ offline.  This particular attack scenario is proposed as one of the demonstration cases for the Cross Sword 2023 Test-Run, providing a realistic and controlled environment to assess the cybersecurity resilience of the railway infrastructure.

**Attacker Vector** :  ARP Spoofing / Network Traffic Blocking / attack on specific App.

> Important : The demonstrated attack case is used for education and training for different level of IT-OT cyber security ICS course, please don't apply it on any real world system.

[TOC]

------

### Introduction

The attack study case comprises three sub-projects :

- Railway[Metro] IT/OT System Mini Cyber Range System [link of project document](https://github.com/LiuYuancheng/Railway_IT_OT_System_Cyber_Security_Platform)
- Red Team C2 Emulation system [link of project document](https://github.com/LiuYuancheng/Python_Malwares_Repo/tree/main/src/c2Emulator)
- Ettercap Wrapper program [link of project document](https://github.com/LiuYuancheng/Python_Malwares_Repo/tree/main/src/ettercapWrapper)

In this study case, we envision a scenario where a red team attacker/hacker successfully implants the Packet Dropper and Mitm Tool Ettercap via an IT-Attack, such as employing a phishing email, targeting one of the maintenance computers in the SCADA supervision network. The attack study case will illustrate how a red team attacker, external to the railway mini cyber range, executes Ettercap to broadcast the fake ARP to one Operation HMI computer and the related PLCs, then apply the packet filter to drop the specific package (ModBus-TCP packet to port 502) to changes the Operation room one HMI program offline. This will be accomplished by utilizing the Red Team C2 system from the internet and successfully bypassing the firewall's detection mechanisms.

The attack detailed road map is shown below : 

![](img/ArpSpoofing/arpspoofing.png)

