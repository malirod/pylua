# pylua
Example of binding between python and lua

##Prerequisite
- python 2.7

`sudo apt-get install python2.7-dev python-pip`

- flake8

sudo apt-get install python-flake8

- virtualenv

`sudo pip install virtualenv`

- fabric

`sudo pip install fabric`

- lua 5.2

`sudo apt-get install liblua5.2 liblua5.2-dev`

##Setup
All further steps are performed in the project root

Install git hooks

`python ./tools/infrastructure/install_hooks.py`

Create virtual environment

`virtualenv venv`

`. ./venv/bin/activate`

`pip install -r requirements.txt`

##Usage
To run all tests run

`fab test_all`

To run specific test or test case use

`fab run_test:name=<file>:<Test_Case>.<test_method>`
