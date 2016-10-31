#!/bin/bash

TEXT_DEFAULT="\\033[0;39m"
TEXT_INFO="\\033[1;32m"
TEXT_ERROR="\\033[1;31m"
TEXT_UNDERLINE="\\0033[4m"
TEXT_BOLD="\\0033[1m"

COMMITS_RANGE=$1

if [ -n "$COMMITS_RANGE" ]; then
  echo "Processing commits range: $COMMITS_RANGE"
else
  echo ${TEXT_ERROR}"No commits provided"${TEXT_DEFAULT}
  exit 1
fi

##################################################################
### Check for python version and script encoding
##################################################################

echo -e "$TEXT_INFO" "Checking python version and script encoding" "$TEXT_DEFAULT"

PYTHON_FILES_NUMBER=$(git diff $COMMITS_RANGE --name-only | grep -e '\.py$' | wc -l)
if [ "$PYTHON_FILES_NUMBER" -ne "0" ]; then
    PYTHON_VERSION="python2$"
    PYTHON_VERSION_MATCHES=$(head -n1 $(git diff $COMMITS_RANGE --name-only | grep -e '\.py$') | grep -i $PYTHON_VERSION | wc -l)

    if [ "$PYTHON_VERSION_MATCHES" -ne "$PYTHON_FILES_NUMBER" ]; then
        echo -e "${TEXT_ERROR}Some python file(s) have wrong shebang. Expected is:${TEXT_DEFAULT} ${TEXT_BOLD} $PYTHON_VERSION ${TEXT_DEFAULT}"
        exit 2
    fi

    PYTHON_ENCODING_HEADER="utf-8"
    PYTHON_CODE_PAGE_MATCHES=$(head -n2 $(git diff $COMMITS_RANGE --name-only | grep -e '\.py$') | grep -i $PYTHON_ENCODING_HEADER | wc -l)

    if [ "$PYTHON_CODE_PAGE_MATCHES" -ne "$PYTHON_FILES_NUMBER" ]; then
        echo -e "${TEXT_ERROR}Some python file(s) have wrong encoding. Expected is:${TEXT_DEFAULT} ${TEXT_BOLD} $PYTHON_ENCODING_HEADER ${TEXT_DEFAULT}"
        exit 2
    fi
else
    echo "No python files to check"
fi

echo -e "$TEXT_INFO" "PASSED" "$TEXT_DEFAULT"

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
### Auto-check python code with pylint
##################################################################

echo -e "$TEXT_INFO" "Checking python style with pylint" "$TEXT_DEFAULT"

PYTHON_FILES=$(git diff $COMMITS_RANGE --name-only --diff-filter=ACM | grep -e "\.py$")

if [ -n "$PYTHON_FILES" ]; then
    pylint --rcfile=.pylintrc $PYTHON_FILES
    if [ "$?" -ne "0" ]; then
        echo -e "$TEXT_ERROR" "Pylint reports about the issues in the python scripts" "$TEXT_DEFAULT"
        exit 3
    fi
fi

echo -e "$TEXT_INFO" "PASSED" "$TEXT_DEFAULT"

exit 0
