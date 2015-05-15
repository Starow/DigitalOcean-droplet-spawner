#!/bin/bash

set -x
set -e

apt-get install python-virtualenv libffi-dev libssl-dev

virtualenv virtenv

. ./virtenv/bin/activate

pip install requests[security]

pip install -r requirements.txt
