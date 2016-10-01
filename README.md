[![Build Status](https://travis-ci.org/malirod/pylua.svg?branch=master)](https://travis-ci.org/malirod/pylua)

# pylua
Example of binding between python and lua

##Platform

Ubuntu 14.04 LTS, 16.04 LTS

##Prerequisite
- python 2.7

`sudo apt-get install python2.7-dev python-pip`

- PyLint

`sudo apt-get install pylint`

usage(from project root to use config): `pylint <file to check>`


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

##Python & Lua binding
Binding is implemented with help of [lupa library](https://pypi.python.org/pypi/lupa)

Read it's manual to know how it works.
