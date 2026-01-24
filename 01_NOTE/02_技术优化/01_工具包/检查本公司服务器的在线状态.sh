#!/bin/bash

# 检查服务器在线状态
# 如服务器的ip分别是192.168.11.182或199或100或126或88等
# 根据需要进行变更

for i in 182 199 100 126 88
do
        ping -c 2 192.168.11.$i >/dev/null
        if [ $? -eq 0 ]; then
                echo "$i up"
        else
                echo "$i down"
        fi
done