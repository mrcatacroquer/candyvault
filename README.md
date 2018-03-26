# candyvault
The ultimate devops machine.

## Getting Started

This project supports the creation of a vault box that will store candies for developers.
As soon as a development task gets solved the developer will be able to open the vault using his or her personal RFID vault card. On the other hand the vault will remain closed if the developer is not having candies available.

## Hardware

Parts needed:
* [Raspberry Pi 1 Model B+](https://www.raspberrypi.org/products/raspberry-pi-1-model-b-plus/) - A tiny board able to handle both the needed hardware and software parts.
* [RFID RC522](https://www.amazon.com/Gowoops-RFID-Kit-Arduino-Raspberry/dp/B01KFM0XNG/ref=sr_1_3?ie=UTF8&qid=1522078820&sr=8-3&keywords=RFID+RC522) - A hardware module to read RFID cards
* [Servo motor SG90](https://www.amazon.com/ElectroBot-Micro-Helicopter-Airplane-Controls/dp/B071KJV7DD/ref=sr_1_2_sspa?s=electronics&ie=UTF8&qid=1522078852&sr=1-2-spons&keywords=servo+motor&psc=1) - Tiny servo motor to be used as the door lock.

 Learn how to get started with Raspberry PI [here](https://projects.raspberrypi.org/en/projects/raspberry-pi-getting-started). You will need to conntect the RFID module as it's explained [here](http://www.instructables.com/id/RFID-RC522-Raspberry-Pi/).
 
## Software

The code is having two main applications:

* [CaldyVault API](candyvault.py) - The API
The WEB API that will accept web requests in order to grant candies to the develpers. It uses the Python [Flask Microframework](http://flask.pocoo.org/) and the [pymysql](https://pymysql.readthedocs.io/en/latest/) Pyhton library.

* [CandyVault Keeper](candyvaultkeeper.py) - The Keeper
The tool in charge of opening the vault door. It will check if the card used is having a candy available.

## Want to replicate the project? You will need to...

* Create the MySQL database, schema is used at the [MySQL helper script](mysqlhelper.py).
* Update the MySQL database name, user name and password at the [MySQL helper script](mysqlhelper.py) file.
* The [addusers.py](addusers.py) will help you to read RFID cards and store them as users at the MySQL DB.
* Create a new "secret_key" for the Flask API application. Check the [Flask documentation](http://flask.pocoo.org/docs/0.12/quickstart/) for more help.
