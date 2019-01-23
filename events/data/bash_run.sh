#!/bin/bash
source ../root/env/bin/activate
python ../root/platinum/events/data/download_data.py
python ../root/platinum/manage.py migrate
