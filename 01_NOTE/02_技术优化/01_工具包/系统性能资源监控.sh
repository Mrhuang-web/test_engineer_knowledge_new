#!/bin/bash

# 监控系统的cpu/内存/磁盘的资源占用情况, 如果超过了, 则发出告警
# 实时监控需要配置到定时任务中去执行, 通过crontab -e编辑任务
# * * * * * /home/test_jay/test.sh >> /home/test_jay/perf.log  表示每分钟执行一次, 并记录到日志文件perf.log中
# grep -ni "过高" test.sh 来查找日志文件中的告警信息

# CPU告警上限
cpu_limit=90

# 内存告警上限
mem_limit=90

# 硬盘告警上限
disk_limit=85

# 检查CPU使用率, us用户使用+sy系统使用
cpu_usage=$(top -bn1 | grep Cpu | awk '{print $2 + $4}')

# 检查内存占用情况
mem_usage=$(free | grep Mem | awk '{print $3/$2*100}')

# 磁盘使用率
disk_usage=$(df / | grep / | awk '{print $5}' | tr -d "%")

# 告警判断
if [ $(echo "$cpu_usage > $cpu_limit" | bc) -eq 1 ]; then
	echo "cpu使用率过高!!!"$(date)
fi

if [ $(echo "$mem_usage > $mem_limit" | bc) -eq 1 ]; then
	echo "内存使用率过高!!!"$(date)
fi

if [ $(echo "$disk_usage > $disk_limit" | bc) -eq 1 ]; then
	echo "硬盘使用率过高!!!"$(date)
fi

echo "cpu使用率:"$cpu_usage"%"
echo "内存使用率:"$mem_usage"%"
echo "硬盘使用率:"$disk_usage"%"