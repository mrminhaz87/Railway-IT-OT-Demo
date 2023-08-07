# Cyber-Attack Scenario

**Project Design :** To full filled some demo and education purpose of the Railway[Metro] IT/OT System Security Test Platform, we will preset some cyber attack Scenario with the attack scripts to demo applying different attack on the platform. Currently below attack scenario are included: 

- False command injection attack via phishing email and Backdoor Trojan

[TOC]

------

### Attack Scenario 1: False command injection attack via phishing email and backdoor trojan

#### Introduction 

In this attack scenario, we will show how a hacker makes a breakthrough of a internal laptop in the cooperate network via phishing email, collects the critical documents from management workstation, gains the remote control of a security-careless configured maintenance laptop in the SCADA network then launch the harmful/false commands to attack the trains controller PLCs to cause the train collision accident in the real-world. The attack road map is shown below:

![](img/falseCmdInjection.png)

#### Detailed Attack Storyline

As shown the introduction and the attack road map, the hacker will do the attack via below 7 steps: 

##### Attack Step1

The attacker use one user/staff (Alice)'s laptop to send a phishing email (contents a fake IT support application form with a file download link)  to the IT management team. 

##### Attack Step2

A remiss support engineer Bob opened the phishing email, clicked the link and downloaded the backdoor trojan program. When the trojan is active, it change Bob's laptops remote login configuration, so the attacker is able to remotely check Bob's browser history,  cookies,  commands history and access some company's credentials document and internal system operating manuals. After analysis Bob's commands history, and all the accessable documents, the attacker figured out: 

- There is a computer in supervision network behind the firewall which Bob did use his laptop to SSH login before, he can use this to pass though the firewall. 
- There are 2 SCADA servers in the supervision network. 
- The maintenance laptop's login credential may be in one of the password record file in the management workstation. 

##### Attack Step3

After tried every username/password in the record file, the attacker ssh login the maintenance laptop successfully. He scanned the network to try to figure out the supervision network structure and the server's IP addresses, then he roughly understand the network topology of the SCADA network and found 2 servers may be the SCADA servers introduced in one of the user manual he found in step2. 

##### Attack Step4

The attack tried to capture the p-cap of the 2 servers which he though are SCADA servers, he find the Modbus communication traffic packages. Based on the incoming Modbus message package  length he figure out the trains controller SCADA server (server A) IP address. Based on the  outgoing Modbus package, he figured out the trains controller PLCs' IP address and some registers information (address and idx offset).

##### Attack Step5

The attacker created his own Modbus communication client program (malware) on the maintenance laptop, then he try to connect to the PLC and fetch some data. Based on the Fetched PLC data and the observation of the real-world emulator's trains state, the attack create his mapping file of: 

- PLC holding registers -> PLC electrical signal in -> Real-world trains' speed sensors. 
- PLC coils -> PLC electrical signal out -> Real-world trains' power control. 

So he know how to monitor the trains state and roughly understand the control sequence of the trains.

##### Attack Step6

Based on the internal critical operator manuals the attacker found in step2, he also knows there is a PLC coil enable/disable to trains' collision auto-avoidance setting. He analyzed the Modbus traffic, his trains PLC controller map and use his malware to insert the harmful PLC coils turn off command to  overwrite the coils which he though may be used to disable the train collision auto-avoidance. 

##### Attack Step7

The attack observed the real-world emulator, choose the train he want to attack. Then he used his malware to insert train power off command to overwrite the PLC coils to active the targeted train's emergency stop .state As the collision auto-avoidance is disabled in step 6, then the train behind the attacked trains arrived the attacked train location, the train accident happens. 





------

> last edit by LiuYuancheng (liu_yuan_cheng@hotmail.com) by 07/08/2023 if you have any problem, please send me a message. 

