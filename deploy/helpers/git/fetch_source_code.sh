#!/bin/bash

cd /data/test-data-manager

git fetch --all

git reset --hard origin/master

git pull origin master