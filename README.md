[![Build Status](https://travis-ci.org/malirod/pylua.svg?branch=master)](https://travis-ci.org/malirod/pylua)

# pylua
Example of binding between python and lua

##Platform

Ubuntu 14.04 LTS, 16.04 LTS

##Prerequisite
- python 3.5.2

`sudo apt-get install python3-dev python3-pip python3-venv`

- PyLint

`sudo apt-get install pylint`

usage(from project root to use config): `pylint <file to check>`

- fabric

`sudo pip install fabric`

- lua 5.2

`sudo apt-get install liblua5.2 liblua5.2-dev`

##Setup

All further steps are performed in the project root

Create virtual environment

```
. venv/bin/activate
pip3 install --upgrade pip
pip install wheel
pip install -r requirements.txt


Install git hooks

`python ./tools/infrastructure/install_hooks.py`

##Usage
To run all tests run

`fab test_all`

To run specific test or test case use

`fab run_test:name=<file>:<Test_Case>.<test_method>`

##Code validation
Style check is performed with script `./tools/infrastructure/checkstyle.sh`

Usage

`./tools/infrastructure/checkstyle.sh <begin_sha>..<end_sha>`

e.g.

`./tools/infrastructure/checkstyle.sh 6c18cbb..HEAD`
