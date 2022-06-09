#!/bin/bash

cd /data/test-data-manager

supervisord -c runfile.ini

echo "Application is getting up..."