#!/bin/bash

rm -rf package
mkdir package

find . -not -path "./.git*" -not -path "./__pycache__*" -not -path "./package*" -type f ! -name install.sh -type f ! -name requirements.txt -type f ! -name *.ipynb -exec cp -t package/ {} +
pip install -r requirements.txt -t ./package
