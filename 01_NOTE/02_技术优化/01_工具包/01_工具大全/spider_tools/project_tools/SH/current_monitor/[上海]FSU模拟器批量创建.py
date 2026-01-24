# -*- coding: utf-8 -*-
import os, shutil, re, subprocess

LOCAL_PROJECT = r"E:\tmp\sim_fsu_sh_hjj"  # 1. 改成已有项目-实际路径
TMP_DIR = r"E:\tmp\spider_fsu_GX"  # 2. 临时生成目录[即存在复制项目的父级目录]
REMOTE_BASE = "/root/spider_fsu_GX"
os.makedirs(TMP_DIR, exist_ok=True)

num = 0
for i in range(1, 11):
    port = 8200 + i - 1
    fsu_name = f"fsu_{i:03d}"
    tgt = os.path.join(TMP_DIR, fsu_name)

    # 1. 复制整个项目
    if os.path.exists(tgt):
        shutil.rmtree(tgt)
    shutil.copytree(LOCAL_PROJECT, tgt)

    # 2. 改 config.py
    cfg = os.path.join(tgt, "config.py")
    with open(cfg, "r", encoding="utf-8") as f:
        txt = f.read()
    txt = re.sub(r"^PORT\s*=\s*\d+", f"PORT = {port}", txt, flags=re.M)
    with open(cfg, "w", encoding="utf-8") as f:
        f.write(txt)

    # 3. 改 start.sh（Windows→Linux 换行 & 路径）
    start = os.path.join(tgt, "start.sh")
    remote_dir = f"{REMOTE_BASE}/{fsu_name}"
    new_content = f"nohup /root/spider_hjj_fsu_sh/env_fsu/bin/python {remote_dir}/sim_fsu_hjj.py > {remote_dir}/nohup.out 2>&1 &\n"
    with open(start, "w", encoding="utf-8", newline="\n") as f:  # 强制 Unix 换行
        f.write(new_content)
    num += 1

print(f"{num}个FSU已部署并启动！")
