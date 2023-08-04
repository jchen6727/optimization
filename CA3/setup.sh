#!/bin/bash

# create a backup of the batch directory
mv ../batchdir ../batchdir_$(date +"%m_%d")

mkdir ../batchdir

cp runner.py gridsrch.py ca3.py utils.py sge.sh optunasrch.py ../batchdir