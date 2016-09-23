#!/bin/bash

# Auto-check for pep8 in python code
PYTHON_FILES=$(find . -type f \( -iname '*.py' \) -not -path './venv/*')

if [ -n "$PYTHON_FILES" ]; then
    flake8 $PYTHON_FILES
    if [ "$?" -ne "0" ]; then
        echo -e "$TEXT_ERROR" "Flake8 reports about the issues in the python scripts" "$TEXT_DEFAULT"
        exit 2
    fi
fi
