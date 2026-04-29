#!/bin/sh
# Start detatched so remains running in background
# Give it a name to manage it more easily
# Make sure coverage builds persist between containers
# Keep a shared folder to transfer files more easily
sudo docker run -i -d \
	--name my_fuzz4all \
	-v ./coverage:/home/coverage \
	-v ./outputs:/home/Fuzz4All/outputs \
	-v ./tools:/home/Fuzz4All/tools \
	stevenxia/fuzz4all:latest
