#!/usr/bin/sh
ssh -t -p 2222 'jp@172.24.122.108' sudo ./rabbitstart2.sh

ssh -t minnie@172.24.151.237 sudo ./apache2start.sh
