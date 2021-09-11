#!/usr/bin/env bash

cd `dirname $0`
pipenv run pip freeze > requirements.txt
pipenv run pip install -r requirements.txt -t package/ --upgrade