FSU模拟器批量创建

    [执行步骤]
        1、在本地生成100fsu模拟器
        2、到生成100fsu的父级目录，输入powershell，打开powershell窗口
            执行tar -czf fsu_100.tar.gz -C D:\06_test\tmp\fsu_100 .
            这里的D:\fsu_100 需要换成生成100fsu的父级目录
        
        3、在服务器FSU模拟器父级目录下，构建一个sh脚本（deploy_100_fsu.sh）  -- 对文件进行初步解压
            #!/bin/bash
            # 用法：sudo bash deploy_100_fsu.sh
            set -e
            
            PKG=/home/sudoroot/fsu_100.tar.gz
            DEST=/root/spider_fsu_GX
            LOG=$DEST/deploy.log
            
            mkdir -p $DEST
            echo ">>> 1. 解压"
            tar -xzf $PKG -C $DEST
            chown -R root:root $DEST        # 如果只想 root 能管
            chmod -R 755 $DEST
            
            启动
                sudo bash deploy_100_fsu.sh

        4、执行脚本（已执行解压）
            方式1（批量跑） -- 构建在sh脚本中直接运行：
                cd /root
                find . -name start.sh -type f -print0 | xargs -0 -n1 -P0 bash
            方式2（逐个跑） -- 构建在sh脚本中直接运行：
                cd /root
                find . -name start.sh -type f -print0 | xargs -0 -n1 bash
            方式3（到各个路径下执行 -- 目前用这个-需要等一会才能起来） -- sh  deploy_100_fsu_bak.sh
                cd /root
                find . -name start.sh -type f -print0 | xargs -0 -I{} bash -c 'cd "$(dirname "{}")" && bash start.sh'
                启动
                    sh  deploy_100_fsu_bak.sh



FSU_data_xlxs_批量生成
    [执行步骤]
        1、选择对应站点即可
        2、后续可以根据需求补充测点和设备[目前仅传输部分测点]
    
    本脚本用于批量生成FSU（Field Supervision Unit）设备数据，包含三张核心数据表：
        FSU表 - FSU设备基础信息
        Device表 - 设备类型和参数信息
        Signal表 - 信号测点及通道配置
    CONFIG 字典中配置参数：
        CONFIG = {
            'fsu_ver': 'V1.0',           # FSU版本号
            'interval': 60,              # 采集间隔（秒）
            'm': '通用',                  # 设备厂商
            'brand': '通用',              # 设备品牌
            'version': '1.0',            # 设备版本
            'devicesubtype': 1,          # 设备子类型
            'ratedcapacity': 0.000000,   # 额定容量
            'signal_channels': 5,        # 每个测点生成的通道号数量（关键配置！）
        }
    站点/机房ID递增规则
        FSU#1 → siteid: 4401002000001, roomid: 440100200000100
        FSU#2 → siteid: 4401002000002, roomid: 440100200000200
        FSU#3 → siteid: 4401002000003, roomid: 440100200000300
        ...
    通道号生成规则
        每个测点（如"相电流Ia"）生成N个通道号（000, 001, 002...）：
            设备类型: 高压配电柜
            测点: 001307 - 相电流Ia
            通道号: 000, 001, 002, 003, 004 (共5个)
    设备ID生成规则
        设备ID为15位数字，全局递增：
        100100000000001
        100100000000002
        100100000000003
        ...