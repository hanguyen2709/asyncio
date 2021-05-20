CONTENTS OF THIS FILE
---------------------

 * Introduction
 * Requirements
 * Installation
 * Configuration
 * Troubleshooting


 INTRODUCTION
------------
This program is designed with solutions that utilize concurrency in mind, primarily asynchronous solutions using await. Performance matters!

REQUIREMENTS
------------
This module requires the following :

 * Docker
 * Docker Compose


INSTALLATION
------------
 * unzip
 With docker compose 
 Run commmand in terminal 
 * sudo docker-compose up --build
Result when run docker-compose success:
https://drive.google.com/drive/folders/1imjDqbu6g3iyYQ_KL5hIKs3Jl4EJF0XC?usp=sharing

To map any changes in local to container run:
 * sudo docker-compose up --build
To run program everytime:
* sudo docker-compose up
 
Or Manual Run the following command in terminal 
 * cd challenge
 * sudo bash
 * python3 -m venv venv
 * source venv/bin/activate
 * pip3 install -r requirements.txt
 * python3.7 challenge.py q
Result when running on local:
https://drive.google.com/drive/folders/12za_fTLZnlLnV7GxtRLIrX2tdDnVij-2?usp=sharing

 TROUBLESHOOTING
---------------

 * If don't have Python3.7 it will cause error
 * if input parameter to run this file is not "q" character, program doesn't work. 
 * Sometimes, server get error, there is a message. We need to run program again. 
