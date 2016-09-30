#!/bin/bash

COMMITS_RANGE=$1
echo "Processing commits range: $COMMITS_RANGE"

TEXT_DEFAULT="\\033[0;39m"
TEXT_INFO="\\033[1;32m"
TEXT_ERROR="\\033[1;31m"
TEXT_UNDERLINE="\\0033[4m"
TEXT_BOLD="\\0033[1m"

##################################################################
### Check for odd whitespace
##################################################################

echo -e "$TEXT_INFO" "Checking odd whitespaces" "$TEXT_DEFAULT"
git diff --check $COMMITS_RANGE --color
if [ "$?" -ne "0" ]; then
    echo -e "$TEXT_ERROR" "Your changes introduce whitespace errors" "$TEXT_DEFAULT"
    exit 1
fi
echo -e "$TEXT_INFO" "PASSED" "$TEXT_DEFAULT"

##################################################################
### Auto-check for pep8 in python code
##################################################################

echo -e "$TEXT_INFO" "Checking python style with flake8" "$TEXT_DEFAULT"

PYTHON_FILES=$(git diff $COMMITS_RANGE --name-only --diff-filter=ACM | grep -e "\.py$")

if [ -n "$PYTHON_FILES" ]; then
    flake8 $PYTHON_FILES
    if [ "$?" -ne "0" ]; then
        echo -e "$TEXT_ERROR" "Flake8 reports about the issues in the python scripts" "$TEXT_DEFAULT"
        exit 3
    fi
fi

echo -e "$TEXT_INFO" "PASSED" "$TEXT_DEFAULT"

exit 0
