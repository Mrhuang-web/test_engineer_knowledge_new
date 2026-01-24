注意：[进程和作业管理-Linux命令大全（手册）](https://ipcmen.com/category/system-management/process-and-job-management)百科大全

# 命令下载

```
sudo yum install telnet
	telnet，用于测试是否能联通对方ip即端口

```



# 进程查看

```
ps aux
    a：显示所有用户的进程（包括其他用户的）
    u：以用户为主的格式显示
    x：显示没有控制终端的进程（比如后台进程）
    
    
    
top
```

# 端口查看

```
查看所有端口监听情况（包括进程名）
sudo ss -tulnp
	-t：TCP
    -u：UDP
    -l：监听状态
    -n：不解析服务名（显示端口号）
    -p：显示进程 PID 和名称
    
指定端口：端口，想查是哪个进程
sudo lsof -i :8080
sudo ss -tulnp | grep :8080


看“端口+进程”一起
sudo ss -tulnp


netstat -ntlp
netstat -pln |grep  1080
```



# 端口命令

- | 命令                                    | 作用                       | 常用参数                                             |
  | :-------------------------------------- | :------------------------- | :--------------------------------------------------- |
  | `ss -tuln`<br />netstat -tuln【旧版本】 | 查看监听端口               | `-t` (TCP), `-u` (UDP), `-l` (监听), `-n` (数字格式) |
  | `ss -tunp`                              | 查看端口及进程信息         | 加 `-p` 显示进程                                     |
  | `lsof -i :端口`                         | 精确查看端口占用进程       | 需 `sudo` 权限                                       |
  | `nc -zv IP 端口`                        | 测试远程端口是否开放       | `-z` (扫描), `-v` (详细)                             |
  | telnet 目标IP 端口号                    | **检查远程主机端口连通性** |                                                      |

- ```
  案例
  
  检查 80 端口是否被占用
  sudo ss -tulnp | grep ':80'
  
  
  查找占用 3306 端口的进程
  sudo lsof -i :3306
  
  
  测试远程主机的 443 端口
  nc -zv example.com 443
  ```


# iptables服务修改

```
情况1：
	正常修改
		vim /etc/sysconfig/iptables
		systemctl restart iptables
		
情况2：
	错误位置定位、行数或查找内容
		/内容+回车		定位到对应位置
		:行数+回车		定位到指定位置
		错误位置定位		
					   sudo systemctl status iptables.service  【用这个】 
					   sudo journalctl -xe -u iptables.service
```

# 时间命令

```
date

timedatectl

date +"格式字符串"
date +"%Y-%m-%d"           # 2025-08-11（年月日）
date +"%T"                 # 15:30:45（24小时制时间）
date +"%H:%M:%S"           # 同上（时分秒）
date +"%A, %B %d %Y"       # Monday, August 11 2025（星期+全日期）
date +"%s"                 # 1754904645（Unix时间戳）


echo "当前时间: $(date +'%Y-%m-%d %H:%M:%S')"
```

# 文件复制/转移

```
cp -r 源项目目录路径 目标文件夹路径

cp -a 源目录 目标目录  # 等同于 cp -pdr
```

# 重命名文件

```
修改文件名
mv old_filename new_filename

移动文件
mv filename /path/to/destination/

同时修改文件名并移动
mv old_filename /path/to/destination/new_filename
```

# 持续运行

```
正常情况执行flask，如果关闭远程连接，flask也会关闭

正常情况 -->flask run --host=0.0.0.0 --port=5000 (确保监听所有接口)。 关闭ssh就会关闭

方式1（用这种）
	nohup python3  .py文件  &

    nohup: 忽略后续收到的 SIGHUP 信号。
    > flask.log: 将标准输出重定向到文件 flask.log。
    2>&1: 将标准错误也重定向到标准输出（即同样写入 flask.log）。
    &: 让命令在后台运行。
    可以用 ps aux | grep flask 查看进程，用 kill 停止进程
    
方式2
	使用 screen 或 tmux (终端复用器)
	流程:
		1. 连接服务器，安装 screen (通常已安装) 或 tmux (sudo apt/yum install tmux)。
		2. 启动一个新会话：screen -S flask_session 或 tmux new -s flask_session。
		3. 在打开的新会话窗口中启动 Flask：flask run --host=0.0.0.0 --port=5000。
		4. 按下 Ctrl + A 然后 D (screen) 或 Ctrl + B 然后 D (tmux) 分离当前会话（detach）。此时会话在后台运行，Flask 也在其中运行。
		5. 安全地关闭你的 SSH 连接。
		
	恢复查看/管理:
		* 重新 SSH 连接到服务器。
		* 使用 screen -r flask_session 或 tmux attach -t flask_session 重新附加到之前的会话，可以看到 Flask 的输出和控制台。
		
	特点： 非常强大灵活，不仅可以防 SIGHUP，还能随时恢复交互式会话查看日志或操作，适合需要交互或监控的场景。Ctrl + C 即可停止 Flask。
```

# 内存查看

```
free -h

查看每个进程占用内存情况

方法1：
ps aux --sort=-%mem | head -n 11     【推荐】
aux: 显示所有用户的进程详细信息。
--sort=-%mem: 按内存使用率降序排序 (-rss 则可按 RES 大小降序排序)。
head -n 11: 显示前11行（第一行是标题行，后面10行是进程信息）。


方法2：
top


方法3【推荐、写成sh脚本直接用】：
ps -eo pid,user,rss,pmem,comm --sort=-rss | head -n 11 | awk 'BEGIN { printf "%-8s %-10s %-10s %-8s %s\n", "PID", "USER", "RSS", "PMEM%", "COMMAND" } NR>1 { rss_mb = $3 / 1024; if (rss_mb > 1024) { rss_size = sprintf("%.1fG", rss_mb / 1024) } else { rss_size = sprintf("%.0fM", rss_mb) } printf "%-8s %-10s %-10s %-8s %s\n", $1, $2, rss_size, $4"%", $5 }'
```



# 硬盘查看

```
df -h
```

# 文件查看

```
less > more：能上下翻、能向上搜、能行号、能“tail -f”。
more：只能向下走，功能阉割版。
cat：一次性全倒出，想交互就用 less
```

| 键 / 操作                  | less                                | more                | cat（其实无交互，但给点bonus） |
| -------------------------- | ----------------------------------- | ------------------- | ------------------------------ |
| **向下翻屏**               | Space 或 f                          | Space               | 无（直接输出完）               |
| **向上翻屏**               | b                                   | b（仅部分系统支持） | 无                             |
| **向下 1 行**              | ↓ 或 j                              | ↓                   | 无                             |
| **向上 1 行**              | ↑ 或 k                              | 无                  | 无                             |
| **跳到文件尾**             | G                                   | G                   | 无                             |
| **跳到文件头**             | g 或 1G                             | 1g（部分）          | 无                             |
| **搜索向下**               | `/关键字` 回车 → n 下一个，N 上一个 | `/关键字` 回车 → n  | 无                             |
| **搜索向上**               | `?关键字` 回车 → n/N                | 无                  | 无                             |
| **退出**                   | q                                   | q                   | Ctrl-C（强行中断）             |
| **帮助**                   | h                                   | h                   | 无                             |
| **显示行号**               | `-N` 启动或 `:n` 临时切换           | 无                  | `cat -n` 启动时带行号          |
| **打开即带行号**           | `less -N file`                      | 无                  | `cat -n file`                  |
| **监控实时追加**           | F（类似 tail -f，Ctrl-C 退出等待）  | 无                  | 无                             |
| **打开第 N 行**            | `less +N file`                      | 无                  | 无                             |
| **保存当前屏幕内容到文件** | s（部分编译版支持）                 | 无                  | 无                             |

# 多程序执行

```
方法一：使用 nohup 或 & 后台运行（适合简单场景）
    nohup python3 script1.py > log1.out &
    nohup python3 script2.py > log2.out &
    缺点：不好管理，重启后失效，日志分散
    

使用 tmux 或 screen（适合手动管理）
	tmux new -s script1
	python3 script1.py
	然后 Ctrl+B 再按 D 退出会话，脚本继续在后台运行（优点：可以回来看输出，适合调试，缺点：不适合长期自动化部署）


方法三：使用 systemd 创建服务（适合长期运行）
	每个脚本写一个 .service 文件，比如 /etc/systemd/system/myscript1.service
	
	ini文件
	[Unit]
    Description=My Python Script 1
    After=network.target

    [Service]
    ExecStart=/usr/bin/python3 /path/to/script1.py
    Restart=always
    User=youruser

    [Install]
    WantedBy=multi-user.target
    
    sudo systemctl enable myscript1.service
	sudo systemctl start myscript1.service
	

方法四：使用进程管理工具（推荐）
	sudo apt install supervisor
	
	配置 /etc/supervisor/conf.d/myscripts.conf：
	
	ini文件
	[program:script1]
    command=python3 /path/to/script1.py
    autostart=true
    autorestart=true
    stderr_logfile=/var/log/script1.err.log
    stdout_logfile=/var/log/script1.out.log

    [program:script2]
    command=python3 /path/to/script2.py
    autostart=true
    autorestart=true
    stderr_logfile=/var/log/script2.err.log
    stdout_logfile=/var/log/script2.out.log
    
    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl status
    
    npm install -g pm2
    pm2 start script1.py --interpreter python3
    pm2 start script2.py --interpreter python3
    pm2 save
    pm2 startup
    
    
方法五：使用容器（Docker）
	每个脚本一个容器，或一个容器运行多个脚本，适合大规模部署
	FROM python:3.11
    COPY script1.py /app/
    CMD ["python3", "/app/script1.py"]
    
    docker build -t myscript1 .
	docker run -d --name script1_container myscript1
```

# sftp查看[重点]

```
首先需要连接通：
		即sftp服务开通端口给要连接的那个
		使用完整格式
		:"GX_Aigcc@2O@5_7","sftpIp":"10.243.184.151","sftpPort":10022,"s
		
			sftp -oPort=10022 GX_Aigcc@2O@5_7@10.243.184.151
			连接时会提示输入密码：52131sda
		连接成功后，在SFTP提示符sftp>下执行：
			# 假设今天是2023年12月11日，则路径为 /GX/20231210 （timeOffset=-1表示前一天）
				cd /GX/20231210
			# 2. 列出文件（检查文件是否存在）
				ls -lh
			# 3. 查找特定前缀的文件
				ls -lh MeterPowerDaily_GX_*
		
		下载并查看文件内容
			# 方法1：直接下载到本地/GX目录
				sftp> lcd /GX/              # 设置本地目录
				sftp> get MeterPowerDaily_GX_20231210.csv
			# 方法2：下载后查看（退出sftp后）
				exit
				cat /GX/MeterPowerDaily_GX_20231210.csv
			# 方法3：流式查看（不下载）
			sftp> get - | head -n 20    # 查看前20行
		
			# 压缩包情况（不下载）
				# 查看压缩文件内部内容（不落地解压）
				zcat /GX/MeterPowerDaily_GX_20231210.csv.gz | awk -F'|' '{print $1,$2}'  # 按|分隔符查看字段
				# 统计行数（不解压）
				zcat /GX/MeterPowerDaily_GX_20231210.csv.gz | wc -l
				# 查找特定内容
				zcat /GX/MeterPowerDaily_GX_20231210.csv.gz | grep "002330"
			
			# 压缩包（下载）
				# 1. 下载文件（本地目录/GX/）
				sftp> lcd /GX/
				sftp> get MeterPowerDaily_GX_20231210.csv.gz

				# 2. 退出sftp后解包查看
				sftp> exit

				# 3. 解压并查看（多种方式）
				gunzip -c /GX/MeterPowerDaily_GX_20231210.csv.gz | head -n 20  # 解压到屏幕
				# 或
				zcat /GX/MeterPowerDaily_GX_20231210.csv.gz | head -n 20       # 直接查看
				# 或
				gzip -dc /GX/MeterPowerDaily_GX_20231210.csv.gz > /GX/MeterPowerDaily_GX_20231210.csv  # 解压到文件
			# 方式3：
				直接在 SFTP 中下载并查看
				# 在 SFTP 会话里
					sftp> get Building_GX_202511.csv.gz /tmp/
					sftp> exit

					# 然后查看
					zcat /tmp/Building_GX_202511.csv.gz | head
		
		# 3. 检查下载的文件
			head -n 5 /GX/MeterPowerDaily_GX_20231210.csv  # 查看前5行
			wc -l /GX/MeterPowerDaily_GX_20231210.csv      # 统计总行数
```

