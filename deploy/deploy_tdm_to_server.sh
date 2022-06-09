#!/bin/bash

# Login wasadm
sh /data/test-data-manager/deploy/helpers/bash/login_wasadm.sh

# Active venv
sh /data/test-data-manager/deploy/helpers/flask/active_venv.sh

# Get down gunicorn if app is running on server
sh /data/test-data-manager/deploy/helpers/gunicorn/stop_gunicorn.sh

# Get down nginx if app is running on server
sh /data/test-data-manager/deploy/helpers/nginx/stop_nginx.sh

# Get updated source code from master branch
sh /data/test-data-manager/deploy/helpers/git/fetch_source_code.sh

# Start nginx on server
sh /data/test-data-manager/deploy/helpers/nginx/start_nginx.sh

# Start gunicorn on server
sh /data/test-data-manager/deploy/helpers/gunicorn/start_gunicorn.sh

echo "Test Data Manager is getting ready on server..."