#!/usr/bin/env bash

# Change to the script directory
# -- は dirname: invalid option -- 'b' を回避するために使用
cd `dirname $0`
pipenv run pip freeze > requirements.txt
pipenv run pip install -r requirements.txt -t package/ --upgrade