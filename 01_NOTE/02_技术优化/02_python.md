# 重点

```
所有第三方库都可以在pypi里面下载（可以直接下载出来到本地或是服务器进行安装，解决没有外网问题）
	https://pypi.org/project/charset-normalizer/3.3.2/#files
```



# linux部署

```
源码编译安装 Python 3.12.3
    # 1. 安装编译依赖
    yum groupinstall -y "Development Tools"
    yum install -y openssl-devel bzip2-devel libffi-devel readline-devel sqlite-devel wget

    # 2. 下载 Python 3.12.3 源码
    cd /usr/src
    wget https://www.python.org/ftp/python/3.12.3/Python-3.12.3.tgz
	
	# 前面几步，直接到服务里面下载（https://www.python.org/ftp/python/3.12.3/Python-3.12.3.tgz） 


    # 3. 解压并编译
    tar xzf Python-3.12.3.tgz
    cd Python-3.12.3

    # 4. 配置安装路径（关键：独立目录）
    ./configure --enable-optimizations --prefix=/usr/local/python3.12.3

    # 5. 编译（约10-20分钟）
    make -j$(nproc)

    # 6. 安装（关键：用 altinstall 不覆盖系统python）
    make altinstall
   


验证安装与命令使用
    # 验证安装成功
    /usr/local/python3.12.3/bin/python3.12 --version
    # 输出: Python 3.12.3

    # 查看当前系统所有Python版本
    ls -l /usr/bin/python*  # 系统默认2.7和3.7不变
    ls -l /usr/local/python3.12.3/bin/  # 新安装的3.12.3

    # 使用Python 3.12.3（三种方法）
    /usr/local/python3.12.3/bin/python3.12 -c "print('Hello')"
    /usr/local/python3.12.3/bin/pip3.12 install requests
    
    
    
简化命令（推荐）
为方便使用，创建软链接：
	# 创建全局可访问的命令
    ln -s /usr/local/python3.12.3/bin/python3.12 /usr/bin/python3.12
    ln -s /usr/local/python3.12.3/bin/pip3.12 /usr/bin/pip3.12

    # 现在可以直接使用
    python3.12 --version
    pip3.12 install numpy pandas



最佳实践：虚拟环境
    # 创建项目专用虚拟环境
    python3.12 -m venv /opt/myapp-env         python3.12 -m venv /root/sim/env_fsu

    # 激活环境
    source /opt/myapp-env/bin/activate		  source /root/sim/env_fsu/bin/activate

    # 此时python和pip默认使用3.12.3
    (myapp-env) python --version  # 3.12.3
    (myapp-env) pip install flask			  # 一键安装所有依赖  pip install -r requirements.txt(服务器有外网才行)
    										  # 没有的化

    # 退出环境
    deactivate

	
	重点注意：
        启动注意：（最好直接写虚拟环境的绝对路径），因为有时候进去启动识别不到的
        nohup /opt/venv/myproj/bin/python sim_fsu_hjj.py > nohup.out




如果不慎覆盖系统Python，修复方法：
    # 手动修复yum
    vi /usr/bin/yum  # 修改第一行为 #!/usr/bin/python2
```



```
# 第1步：确认Python版本
python3.12 --version
# 输出: Python 3.12.3

# 第2步：创建虚拟环境（推荐集中管理）
mkdir -p /opt/python-venvs
python3.12 -m venv /opt/python-venvs/myproject-env

# 第3步：验证创建成功
ls /opt/python-venvs/myproject-env/bin/
# 应该看到: activate  python  pip  etc.

# 第4步：激活并使用
source /opt/python-venvs/myproject-env/bin/activate

# 第5步：验证正在使用虚拟环境
which python
# 输出: /opt/python-venvs/myproject-env/bin/python

python --version
# 输出: Python 3.12.3

# 第6步：安装包测试
pip install requests

# 第7步：退出
deactivate
```



```
没有外网的情况

    步骤1：在外网机器（虚拟环境）下载所有包
   
        # 在有外网的机器上，激活相同的虚拟环境
        source /opt/myapp-env/bin/activate

        # 在requirements.txt所在目录执行
        cd /path/to/project

        # 下载所有包及其依赖到packages目录
        pip download -r requirements.txt -d ./packages

        # 结果：packages目录下会有几十个.whl或.tar.gz文件
        ls -lh packages/
        
        
    步骤2：拷贝到内网服务器
    
        # 将requirements.txt和packages目录一起压缩
        tar czf offline-packages.tar.gz requirements.txt packages/

        # 通过SCP、FTP或U盘拷贝到内网服务器
    
    
    步骤3：在内网服务器安装

        # 解压
        tar xzf offline-packages.tar.gz
        cd offline-packages

        # 激活虚拟环境
        source /opt/myapp-env/bin/activate

        # 从本地目录安装（不访问网络）
        pip install --no-index --find-links=./packages -r requirements.txt
```







# 代理模式pip

```
首先尝试：
	要么就是重新获取订阅后就能回复正常
	打开代理工具、重新连接；或是关闭后再打开，再重新连接，不行再用下面的【目前可行】

1、开代理如果不能下载的话，关闭代理尝试 -- 如果可以下载就是代理问题

2、为pip加上代理即可解决
	pip install <包名> --proxy http://127.0.0.1:7890     -- 自己代理软件的本地监听地址和端口
	
	地址通常可以在你的代理软件（如Clash、Shadowsocks等）的设置中找到（通常叫HTTP/Socks5监听端口）
	V2rayN： 通常HTTP端口是 10809，Socks5端口是 10808
```



# 快速全局替换

- 使用ctrl+shift+r，快速替换全局

快速全文替换

- 使用ctrl+r，快速替换全文



# 递归文件夹文件

1. **模式匹配**：使用通配符查找文件（如 `*.txt` 匹配所有文本文件）
2. **递归搜索**：通过 `**` 递归查找子目录（需 `recursive=True`）
3. **返回列表**：直接返回匹配的完整路径列表

```
# 查找当前目录所有.py文件
print(glob.glob("*.py")) 
```

```
# 排除特定文件
all_files = glob.glob("*")
txt_files = glob.glob("*.txt")
non_txt_files = [f for f in all_files if f not in txt_files]
```

# 提取完整路径下文件名

```
os.path.basename(destination_file_path) 是 Python 中用于从完整文件路径中提取文件名（含扩展名） 的函数。
它的核心作用是剥离路径中的目录部分，仅保留最后的文件或目录名称

import os

# 基本用法
file_name = os.path.basename(destination_file_path)

print(os.path.basename("/usr/local/bin/python3"))  # 输出: "python3"

path = "/projects/src/main.py"
print(os.path.basename(path))  # 输出: "main.py"
```

# 文件路径拼接

```
# 跨平台路径拼接

# Windows 输出: "folder\\sub\\file.txt"
# Linux 输出: "folder/sub/file.txt"
path = os.path.join("folder", "sub", "file.txt")
```

```
# 绝对路径重置

# 输出: "/new_root/file.txt" (Linux/macOS)
# 输出: "C:\\new_root\\file.txt" (Windows)
path = os.path.join("/old_root", "/new_root", "file.txt")
```

# 递归创建目录

```
递归创建：自动创建路径中所有不存在的父目录【父级不存在情况】

# 安全创建 - 目录存在时不引发异常
os.makedirs("reports/2023", exist_ok=True)
```

# 正则用法

```

```

# pycharm取消右边自动化

```
解决方案：取消 pytest 作为默认测试框架
打开设置面板

Windows/Linux：File → Settings (Ctrl+Alt+S)

macOS：PyCharm → Preferences (⌘+,)

修改测试框架配置

导航到：Tools → Python Integrated Tools

在右侧面板找到 Testing 部分

修改以下两个关键设置：

Default test runner: → 从 pytest 改为 Unittests 或 <disabled>

Service: → 从 pytest 改为 Python test
```

# flask框架

```
执行方式
	1、直接文件里面运行 -- 会导致端口一直是5000【目前好像是这样】
	2、使用python .py -- 运行的话端口会跟着变化
```

# 版本库打包

```
pip freeze > requirement.txt
```

# 库解析

## **quote_plus**

```
from urllib.parse import quote_plus

说明
	空格怎么处理
		quote 把空格编码成 %20
		quote_plus 把空格编码成 +  （是 HTML 表单 application/x-www-form-urlencoded 的规则）
	默认 safe 字符集
		quote 默认 safe='/'，所以路径里的 / 不会动
		quote_plus 默认 safe=''（空串），连 / 也会被编码成 %2F
	路径用 quote，查询参数用 quote_plus
	

使用场景
	将用户输入的中文、空格、特殊符号转为合法 URL 路径或查询字符串
	生成带动态路径的 RESTful 地址，如 /item/{quote(商品名)}
	构造 OAuth、第三方 API 请求签名前的标准化 URL
	在 Django/Flask 模板外手动拼接跳转地址，防止 404 或 500
	与缓存键、重定向 URL、二维码内容等需要 ASCII--only 的场合结合使用
	
	
遇见问题处理运用：
	集团连接mysql时：
		脚本里拼的是 "mysql+pymysql://user:password@host/db" 
		这种 SQLAlchemy URI，而不是发给 HTTP 的 URL
		这类 URI 在解析时要求：用户名、密码里出现 "/、@、:、#、?、空格 …" 必须先做 百分号编码；
		如果直接把含特殊字符的明文写进去，SQLAlchemy 会把 user:pass@host 这一段拆错，
			导致 "Access denied" 或 "Invalid URI"
		原因：
			客户端 URI 解析器要求你把用户名/密码先做 URL 编码；
			quote_plus 正好顺手完成了这一步
```

## **elasticsearch**

```
from elasticsearch import Elasticsearch   --> 用于连接，单操作
from elasticsearch.helpers import bulk    --> 用于批量


连接
	es = Elasticsearch(
        "https://localhost:9200",			# 仅传这个即可【测试环境】
        basic_auth=("elastic","pwd"),		# 可以不要
        verify_certs=False,          		# 生产环境请换合法证书
        request_timeout=30)
   es.info()
   


索引检测
	es.indices.exists(index=self.index_name)



索引新建
	需要创建索引结构【mapping部分，具体构建不太清楚】
	es.indices.create(index="news", body=mapping，ignore=400)	#index 可以根据自己的需求改



索引写入
	doc = {"title": "ES 8 发布", "content": "...", "@timestamp": "2025-09-29T12:00:00Z"}
	es.index(index="news", id=1, document=doc)		



索引批量写入
    写入的索引json，存到一个列表，一次性写入，chunk_size即写入长度
	from elasticsearch.helpers import bulk
    actions = [
        {"_index": "news", "_id": i,
         "_source": {"title": f"title {i}", "content": f"text {i}"}}
        for i in range(1000)
    ]
    bulk(es, actions, chunk_size=500, request_timeout=60)



索引查询
	{"query": {"bool": {"must": []}}}
	
    resp = es.search(index="news",
                     query={"match": {"title": "发布"}},
                     size=10)
    for hit in resp['hits']['hits']:
        print(hit['_source'])



索引增
	


索引删
	urldelmapping = self.url + "/" + self.index_name + \
                        "/" + indetype + "/_delete_by_query"
    
	requests.post(urldelmapping, pload)
	result_dict = {"query": {"bool": {"must": [...]}}}    # 查询的索引内容
	json.dumps(result_dict)								  # 转json格式
	requests.post(urldelmapping, pload)					  # 提交请求即可

索引改
```

![image-20250929170851624](assets/image-20250929170851624.png)

![image-20250929171452696](assets/image-20250929171452696.png)

## sqlalchemy

### text方式

```
作用是：
	把一个原始 SQL 字符串包装成一个可执行的 SQL 表达式对象，让 SQLAlchemy 能识别并安全地执行它


SQLAlchemy 的参数化查询语法
	:device_id 和 :mete_code 是 占位符
	
	sql = text("SELECT * FROM t WHERE id = :device_id")
	result = conn.execute(sql, device_id=self.device_id)   # 相当于device_id传给:device_id

优点：
	防止注入：
		如果是：
			sql = f"SELECT * FROM t WHERE id = {self.device_id}"
			这种f-string 或格式化字符串容易被注入
		
```



## 配置读取

### configparser

```
Python 标准库中用于读取和写入配置文件的模块
	仅支持ini
	Windows INI 文件格式的配置[应用程序的参数设置、数据库连接信息]


简单配置【ini类】
	读取配置文件
		import configparser

        config = configparser.ConfigParser()
        config.read('config.ini')

        # 读取字段
        debug = config['DEFAULT'].getboolean('debug')
        db_host = config['database']['host']
        db_port = config.getint('database', 'port')

        print(f"Debug: {debug}")
        print(f"DB Host: {db_host}, Port: {db_port}")

	简单版汇总
        import configparser
        # 初始化
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        # 读取 【初始化后，就直接可以用对象进行调用方法了】
        debug = config.getboolean('DEFAULT', 'debug')
        db_port = config.getint('database', 'port')
        log_dir = config.get('paths', 'log_dir')
        # 修改
        config.set('database', 'host', '192.168.1.100')
        # 写入
        with open('config_updated.ini', 'w') as f:
            config.write(f)
```

![image-20250929173738948](assets/image-20250929173738948.png)

### config

```
说明：
	支持json，yaml，ini


语法：
	# 加载配置文件
	from config import Config

    cfg = Config()
    cfg.load('config.json')  # 或 .yaml, .ini
    
    # 读取配置项
    db_host = cfg.get('database.host', default='localhost')
	db_port = cfg.get('database.port', default=3306)
		
	#  支持层级访问（点语法  -- json）
	user = cfg.get('database.credentials.user')
	
	# 多文件加载（后加载覆盖前加载）
	cfg.load('default.json')
	cfg.load('local.json')  # 覆盖 default 中的值
	
	# 环境变量覆盖（自动）
	cfg = Config()
    cfg.load('config.json')
    # 自动读取 DATABASE_HOST 覆盖 config.json 中的 database.host
    
    # 类型转换
    port = cfg.get('database.port', type=int)  # 自动转换
    
    # 默认值与必填项
    port = cfg.get('database.port', default=5432, required=True)
```



```
案例
	from config import Config

    cfg = Config()
    cfg.load('config.json')  # 或 .yaml, .ini
    
    db_host = cfg.get('database.host', default='localhost')
	db_port = cfg.get('database.port', default=3306)
	
	// config.json
    {
      "database": {
        "host": "127.0.0.1",
        "port": 5432,
        "credentials": {
          "user": "admin",
          "pass": "secret"
        }
      }
    }
    
    user = cfg.get('database.credentials.user')
    
    cfg.load('default.json')
	cfg.load('local.json')  # 覆盖 default 中的值
	
	
	cfg = Config()
    cfg.load('config.json')
    # 自动读取 DATABASE_HOST 覆盖 config.json 中的 database.host
    
    
    port = cfg.get('database.port', type=int)  # 自动转换
    port = cfg.get('database.port', default=5432, required=True)
```

```
flask
    project/
    ├── config/
    │   ├── default.json
    │   ├── dev.json
    │   └── prod.json
    ├── app.py
    └── .env
    
	# default.json
    {
      "app": {
        "name": "MyApp",
        "debug": false
      },
      "database": {
        "host": "localhost",
        "port": 5432,
        "name": "mydb"
      }
    }
    
    
    # dev.json
    {
      "app": {
        "debug": true
      },
      "database": {
        "host": "dev.db.local"
      }
    }
    
    
    from config import Config
    import os

    env = os.getenv('ENV', 'dev')
    cfg = Config()
    cfg.load(f'config/default.json')
    cfg.load(f'config/{env}.json')

    print("App name:", cfg.get('app.name'))
    print("Debug:", cfg.get('app.debug'))
    print("DB host:", cfg.get('database.host'))
```

![image-20250930110854764](assets/image-20250930110854764.png)

![image-20250930111205930](assets/image-20250930111205930.png)



![image-20250930111221605](assets/image-20250930111221605.png)

### toml

```
目录结构
	project
    ├── config.toml
    ├── config.dev.toml
    ├── config.prod.toml
    └── run.py
    
    
代码
    import tomllib, os, pathlib

    ENV = os.getenv("APP_ENV", "dev")          # 环境变量决定环境
    base_path = pathlib.Path(__file__).with_name("config.toml")
    env_path  = base_path.with_suffix(f".{ENV}.toml")

    cfg = tomllib.loads(base_path.read_text())
    if env_path.exists():
        cfg |= tomllib.loads(env_path.read_text())  # 3.9+ 字典合并

    # 使用
    print(cfg["db"]["host"])
```

![image-20250929175220662](assets/image-20250929175220662.png)

![image-20250929175231628](assets/image-20250929175231628.png)

![image-20250929175243762](assets/image-20250929175243762.png)

### yaml

```



代码
    import yaml, os, pathlib

    ENV = os.getenv("APP_ENV", "dev")
    base = yaml.safe_load(open("config.base.yml"))
    env  = yaml.safe_load(open(f"config.{ENV}.yml"))
    config = {**base, **env}          # 简单合并
```

![image-20250930104636258](assets/image-20250930104636258.png)

![image-20250930104645468](assets/image-20250930104645468.png)

### json

```



代码
	import json, os
    ENV = os.getenv("APP_ENV", "dev")
    base = json.load(open("config.base.json"))
    env  = json.load(open(f"config.{ENV}.json"))
    config = {**base, **env}
```

![image-20250930104812484](assets/image-20250930104812484.png)

### py

```



代码
	import os, importlib
    ENV = os.getenv("APP_ENV", "dev")
    base = importlib.import_module("settings")
    env  = importlib.import_module(f"settings_{ENV}")
    cfg  = {k: getattr(env, k, getattr(base, k)) for k in dir(base) if k.isupper()}
```

![image-20250930105014178](assets/image-20250930105014178.png)

![image-20250930105021103](assets/image-20250930105021103.png)

### 统一化

```
把“加载逻辑”做成单例，业务代码只认 config.xxx


# config.py
import os, pathlib, tomllib, yaml, json, importlib

_FMT = os.getenv("CONFIG_FMT", "toml")   # 可切换 toml / yaml / json / py
_ENV = os.getenv("APP_ENV", "dev")

def _load_toml():
    base = tomllib.loads(pathlib.Path("config.toml").read_text())
    env_path = pathlib.Path(f"config.{_ENV}.toml")
    if env_path.exists():
        base |= tomllib.loads(env_path.read_text())
    return base

def _load_yaml():
    base = yaml.safe_load(open("config.base.yml"))
    env  = yaml.safe_load(open(f"config.{_ENV}.yml"))
    return {**base, **env}

def _load_json():
    base = json.load(open("config.base.json"))
    env  = json.load(open(f"config.{_ENV}.json"))
    return {**base, **env}

def _load_py():
    base = importlib.import_module("settings")
    env  = importlib.import_module(f"settings_{_ENV}")
    return {k: getattr(env, k, getattr(base, k)) for k in dir(base) if k.isupper()}

loader = {"toml": _load_toml, "yaml": _load_yaml, "json": _load_json, "py": _load_py}
config = loader[_FMT]()      # 全局单例


业务代码：
from config import config
print(config["db"]["host"])
```

### 总结

```
新项目 → 直接 TOML（官方推荐，注释+嵌套+日期）
DevOps/容器 → YAML（k8s 同生态）
老系统/运维 → INI（最直观）
开发者自己 → Python 文件（最灵活）
把“加载逻辑”封装成单例，业务代码只认 config.xxx，就能同时满足：
    一行切换 dev/test/prod
    用户改配置不动代码
    仓库永远干净
```

### 套用模板

```
目录结构（一共 6 个文件）
    myapp/
    ├── app.py
    ├── config.py
    ├── config.toml
    ├── config.example.toml
    ├── config.dev.toml          # 用户自己复制生成
    ├── config.prod.toml
    └── requirements.txt
```

```
库规整
	tomli>=2.0.0; python_version<"3.11"   # 3.11 内置 tomllib




    """
    全局单例 config，用法：
        from config import config
        print(config.db.host)
    """
    import os
    import pathlib
    import sys

    if sys.version_info >= (3, 11):
        import tomllib
    else:
        import tomli as tomllib

    # -------------- 可覆盖的默认 --------------
    ENV = os.getenv("APP_ENV", "dev")          # dev / test / prod
    CONFIG_DIR = pathlib.Path(__file__).parent
    # -----------------------------------------

    def _merge(base: dict, override: dict) -> dict:
        """递归合并字典"""
        for k, v in override.items():
            if k in base and isinstance(base[k], dict) and isinstance(v, dict):
                _merge(base[k], v)
            else:
                base[k] = v
        return base

    def load_toml(path: pathlib.Path) -> dict:
        return tomllib.loads(path.read_text())

    # 加载顺序：base <- env
    base_path = CONFIG_DIR / "config.toml"
    env_path  = CONFIG_DIR / f"config.{ENV}.toml"

    if not base_path.exists():
        raise FileNotFoundError(base_path)

    config_dict = load_toml(base_path)
    if env_path.exists():
        config_dict = _merge(config_dict, load_toml(env_path))
    else:
        # 用户还没复制，给友好提示
        print(f"⚠️  {env_path} 不存在，已回退到公共配置")

    # 转成对象属性访问（可选）
    class AttrDict:
        def __init__(self, d):
            for k, v in (d or {}).items():
                setattr(self, k, AttrDict(v) if isinstance(v, dict) else v)

    config = AttrDict(config_dict)





    from config import config

    def main():
        print(f"--- 当前环境：{config.app.name} {config.app.version} ---")
        print(f"DB 连接：{config.db.user}@{config.db.host}:{config.db.port}")
        print(f"日志级别：{config.app.log_level}")

    if __name__ == "__main__":
        main()
```

![image-20250930105734446](assets/image-20250930105734446.png)

![image-20250930105747360](assets/image-20250930105747360.png)

![image-20250930105758524](assets/image-20250930105758524.png)

![image-20250930105809449](assets/image-20250930105809449.png)
