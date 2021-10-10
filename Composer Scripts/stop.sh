#!/usr/bin/sh
ssh -t -p 2222 'jp@172.24.122.108' sudo systemctl stop  rabbitmq-server.service

ssh -t minnie@172.24.151.237 sudo service apache2 stop

