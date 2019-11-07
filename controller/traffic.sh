#!/bin/bash

ssh pi@172.26.17.125 "
iperf -s -D -p 5001
"&

ssh pi@172.26.17.128 "
iperf -s -D -p 5001
"&

ssh pi@172.26.17.131 "
iperf -s -D -p 5001
"&

ssh pi@172.26.17.127 "
iperf -s -D -p 5001
"&

ssh pi@172.26.17.130 "
iperf -s -D -p 5001
"&

ssh pi@172.26.17.124 "
iperf -s -D -p 5001
"&

ssh pi@172.26.17.126 "
iperf -s -D -p 5001
"&

sudo ssh wits_ids@172.26.17.83 -o "StrictHostKeyChecking no" "
iperf -c 10.0.0.5 -u -b50M -i 1 -t 30 -p 5001
iperf -c 10.0.0.11 -u -b50M -i 1 -t 30 -p 5001
"&

sudo ssh root@172.26.17.157 -o "StrictHostKeyChecking no" -p 10022 "
sudo hping3 -c 15000 -d 120 -S 10.0.0.5 -w 64 -p 80 --flood
sudo hping3 -c 15000 -d 120 -S 10.0.0.11 -w 64 -p 80 --flood
"&


