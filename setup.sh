#!/bin/bash
# wifi_get 
# 

rm -f  /usr/bin/wf_get



echo "add ln to /usr/bin"
ln -s `pwd`/menu.py /usr/bin/wf_get
chmod +x /usr/bin/wf_get

echo "[+] Done. Try run 'wf_get'"

#set monitor
sudo ifconfig wlx008711014810 down
sudo iwconfig wlx008711014810 mode monitor
sudo ifconfig wlx008711014810 up

'''
安装MySql

sudo apt-get install mysql-server
sudo apt-get install mysql-client
sudo apt-get install libmysqlclient15-dev
 
安装 scapy

pip install scapy
一些扩展功能安装，可选：

pip install matplotlib pyx cryptography



安装 sqlalchemy
pip install sqlalchemy

pip 命令来安装 mysql-connector：
python3 -m pip install mysql-connector

'''