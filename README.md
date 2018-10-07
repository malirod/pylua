# pylua

[![Build Status](https://travis-ci.org/malirod/pylua.svg?branch=master)](https://travis-ci.org/malirod/pylua)

Example of binding between python and lua

## Platform

Ubuntu 18.04 LTS

## Prerequisite

- python 3 (3.6.6)

`sudo apt install python3-dev python3-pip python3-venv`

- fabric

`sudo pip install fabric`

- lua 5.3

`sudo apt install liblua5.3 liblua5.3-dev`

## Setup

All further steps are performed in the project root

Create virtual environment

```bash
python3.6 -m venv venv
source venv/bin/activate
pip3 install --upgrade pip
pip install wheel
pip install -r requirements.txt
```

Install git hooks

`python ./tools/install_hooks.py`

## Usage

To run all tests run

`fab test_all`

To run specific test or test case use

`fab run_test:name=<file>:<Test_Case>.<test_method>`

## Code validation

Style check is performed with script `./tools/checkstyle.sh`