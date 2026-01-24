- 参考连接：
  - [Gitlab+Jenkins+K8S+Registry 建立 CI/CD 流水线 - 技术栈](https://jishuzhan.net/article/1953315897606713345)
  - [Docker命令大全：从入门到入土（不是），从懵懂到精通！一篇搞定所有骚操作 🐳 - 技术栈](https://jishuzhan.net/article/1948568411872735234)
  - [Docker 命令大全 - Docker 命令详解与使用示例 | Docker 中文文档](https://dockerdocs.xuanyuan.me/reference/commands)【可读性高】
  - [Docker 常用命令大全 - 犬小哈教程](https://www.quanxiaoha.com/docker/docker-total-cmd.html)
  - [Docker 命令大全 | 菜鸟教程](https://www.runoob.com/docker/docker-command-manual.html)



# 01_容器命令

注意：下面提到的container都是容器id的意思

## 创建容器【会启动】

- **注意：容器就是根据镜像生产的**

- docker  run    [可选参]  （镜像名字/镜像id/镜像仓库地址）

  - 可选参： 

    - --name-"name" 容器名字   
    - -d 后台方式运行 -it 使用交互形式进入容器查看内容，创建容器使用交互的方式去运行，ctrl+C退出会停止容器，返回主机 
    - -p指定端口 -p8080:8080 （本地对应端口：容器中端口，即做映射）  --network 指定网络 
    - -v 主机目录:容器目录 
    - -v 数据卷:容器目录  （公司规范使用都是通过数据全进行的持久化） 可以启动后开启连在一起（但是ctrl+c会停止）

  - ```
    docker run --name cinterface-service-yunnan \
    --net host \
    --env spring.cloud.inetutils.preferred-networks=192.168.0.55 \  # 改为你的服务器内网IP
    --env ENV_NACOS=10.1.5.109:8848 \        # 改为你的Nacos地址
    --env ENV_TYPE=yunnan \                  # 改为省份拼音（如guangdong）
    --env ENV_APP_NAME=cinterface-service-yunnan \ # 同步修改省份名
    --env ENV_NACOS_PASSWORD=r2G%zwoCj#Oz \  # 改为你的Nacos密码
    -v /tmp/logs/rbac:/opt/data/logs/ \      # 日志目录
    -d 10.1.6.34:8080/spider/yunnan/cinterface-service:spider1.0.0.0_kernelYunNan_SYT_149
    ```

  - ```
    解析
    docker run \                     # 启动新容器
      --name cinterface-service-yunnan \  # 容器名称
      --net host \                   # 网络模式				
      									容器直接使用宿主机的网络栈（非默认的 bridge 模式）
      									省去端口映射（如 -p 8080:8080），服务直接监听宿主机端口
      --env ... \                    # 环境变量（关键配置）
      									强制 Spring Cloud 应用使用指定 IP 注册到服务发现中心（避免自动选择错误的内网 IP）
      									配置 Nacos 注册中心地址（服务发现/配置管理）
      									标识服务部署环境（省份）和应用名称，用于区分多区域部署
      									Nacos 的登录密码（敏感信息应使用 docker secret 或 K8s Secret 更安全）
      -v /tmp/logs/rbac:/opt/data/logs/ \  # 卷挂载（日志持久化）
      -d \                           # 后台运行
      10.1.6.34:8080/spider/yunnan/cinterface-service:spider1.0.0.0_kernelYunNan_SYT_149  # 镜像地址
    ```

## 查看容器

```
# 列出运行中的容器
docker ps

# 列出所有容器（包括已停止的）
docker ps -a

# 只显示容器 ID
docker ps -q

# 显示容器大小
docker ps -s

- 可选参数
  - -a 列出当前正在运行和历史运行容器 
  - -q 只显示容器编号
```

## 启动/停止/重启/终止容器

```
# 启动容器
docker start CONTAINER
# 停止容器
docker stop CONTAINER
# 重启容器
docker restart CONTAINER
# 立即终止一个或多个正在运行的容器
docker kill [OPTIONS] CONTAINER [CONTAINER...]
```

## 删除容器

```
# 删除指定容器
docker rm CONTAINER
# 强制删除正在运行的容器
docker rm -f CONTAINER
# 删除所有已停止的容器
docker container prune
```

## 暂停和恢复容器进程

```
# 暂停容器
docker pause CONTAINER
# 恢复容器
docker unpause CONTAINER
```

## 创建容器【不启动】

```
docker create [OPTIONS] IMAGE [COMMAND] [ARG...]

# 创建一个 nginx 容器但不启动
docker create --name my-nginx nginx
# 创建带环境变量的容器
docker create -e MYSQL_ROOT_PASSWORD=123456 mysql
```

## 容器内部执行

```
docker exec [OPTIONS] CONTAINER COMMAND [ARG...]

# 进入容器交互式终端
docker exec -it CONTAINER bash
# 在容器中执行命令
docker exec CONTAINER ls /
# 以特定用户执行命令
docker exec -u USER CONTAINER COMMAND
```

## 获取容器或镜像信息

```
# 查看容器详细信息
docker inspect CONTAINER
# 查看镜像详细信息
docker inspect IMAGE
# 获取特定信息（使用 Go 模板）
docker inspect --format='{{.NetworkSettings.IPAddress}}' CONTAINER
```

## 获取容器的日志【重点】

```
# 查看容器日志
docker logs CONTAINER
# 实时查看日志
docker logs -f CONTAINER
# 显示时间戳
docker logs -t CONTAINER
# 显示最近的 n 行日志
docker logs --tail=n CONTAINER

docker logs  --tail=100 -f CONTAINER
```

```
进阶
	检测容器重启状态【重启日志会重置，除非持久化，看到 Restarted (x) ago就是重启了】
		docker ps -a --filter "name=你的容器名"
	
	日志驱动【默认是 json-file，但它有大小限制，默认只保留100MB，超出的会被轮转掉】
		docker inspect 容器名 | grep -A 10 LogConfig
			输出类似：/var/lib/docker/containers/容器ID/容器ID-json.log
			sudo less /var/lib/docker/containers/xxx/xxx-json.log
		
	看时间段日志
		docker logs 容器名 --since 24h --timestamps | less
			--since 24h：只看最近24小时
            --timestamps：带时间戳，方便定位
            | less：分页查看，避免终端截断
```

