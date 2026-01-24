# 01_配置管理

配置列表

```
里面的yml文件【并非docker compose】
	这里的yml是应用程序的配置【 Spring Boot 应用的配置文件】
	
	是一个微服务（或单体应用）的 YAML 配置文件，用于定义：
        服务器端口（server.port）
        Spring Boot 相关配置（如 MVC、资源处理、文件上传大小等）
        Nacos 服务发现配置（spring.cloud.nacos.discovery）
        日志配置（logging）
        FTP 服务器连接信息
        单点登录（SSO）相关配置
        安全过滤规则（如 SQL 注入、XSS 防护）
        以及其他业务相关配置（如导出路径、定时任务等）
```

