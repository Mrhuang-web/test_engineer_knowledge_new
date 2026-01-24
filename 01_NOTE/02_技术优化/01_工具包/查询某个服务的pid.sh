#!/bin/bash

# 查询 xx 进程的pid, 执行方式为 ./test.sh xx

ps -ef | grep $1 | grep -v grep | grep -v $$ | awk '{print $2}'