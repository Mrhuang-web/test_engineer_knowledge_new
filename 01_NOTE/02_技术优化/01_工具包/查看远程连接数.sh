#!/bin/bash

# 查看远程连接数包含web/ssh/tcp连接

netstat -atn  |  awk  '{print $5}' | sort -nr  |  uniq -c