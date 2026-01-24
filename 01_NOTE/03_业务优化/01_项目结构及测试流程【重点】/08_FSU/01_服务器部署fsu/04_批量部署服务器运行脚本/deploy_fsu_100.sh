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