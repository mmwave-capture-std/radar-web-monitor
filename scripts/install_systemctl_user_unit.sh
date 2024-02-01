#!/bin/sh

cp mmwave-grpc-server.service \
   ~/.config/systemd/user/


PARENT_DIR=$(dirname "$PWD")
POETRY_PATH=`which poetry`
sed "s|%c|$PARENT_DIR|g; s|%p|$POETRY_PATH|g" radar-web-monitor.service > \
   ~/.config/systemd/user/radar-web-monitor.service

systemctl --user daemon-reload
