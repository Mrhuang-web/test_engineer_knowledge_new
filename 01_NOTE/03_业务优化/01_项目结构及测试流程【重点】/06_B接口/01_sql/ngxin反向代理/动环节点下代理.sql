user  root;
worker_processes  2;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;


events {
    worker_connections  1024;
}


http {
    map $http_origin $allow_cors {
    default 1;
    "~.*10.1.5.109.*" 1;
    # "~.*" 0;
    }
    include       mime.types;
    default_type  application/octet-stream;
    client_max_body_size    200m;
    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                     '$status $body_bytes_sent "$http_referer" '
                     '"$http_user_agent" "$upstream_addr" "$upstream_response_time" '
                     '"$upstream_cache_status" "$request_uri"';

    access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  75;

    # ie10 502 error
    proxy_buffer_size 64k;
    proxy_buffers   4 32k;
    proxy_busy_buffers_size 64k;

    server_tokens off;

    gzip on;
    gzip_min_length 2k;
    gzip_buffers 4 16k;
    #gzip_http_version 1.0;
    gzip_comp_level 2;
    gzip_types text/plain application/javascript text/css application/xml text/javascript application/x-httpd-php image/jpeg image/gif image/png;
    gzip_vary off;
    gzip_disable "MSIE [1-6]\.";
    underscores_in_headers on;

  server {
        listen       8880;
        server_name  10.1.203.120;
        client_max_body_size 100M;

        location / {
            root   /usr/local/nginx/html/test;
            index  index.html index.htm;
            try_files $uri $uri/ /index.html;
        }
                # MOA 第一层配置
        location ^~/spider/moa/ {
            proxy_pass http://compositeService/;
           }
        location ^~/spider/web/ {
            proxy_pass http://compositeService/;
           }

    }

        server {
        listen 8098;
        #server_name localhost;
        server_name 10.1.5.109;

        if ($host != '10.1.5.109') {
           return 403;
        }

        location / {
            root /usr/local/nginx/html/dist;
            index index.html index.htm;
            try_files $uri $uri/ /index.html;
        }

        location /zutai {
            root   html;
            index  index.html;
            try_files $uri $uri/ /zutai/index.html;
        }

        location ^~/spider/web/v1/ {
            proxy_pass http://gatewaycicd/v1/;
            proxy_connect_timeout 600s;
            proxy_send_timeout 600s;
            proxy_read_timeout 600s;
            proxy_set_header Host $host:$proxy_port;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            add_header Access-Control-Allow-Origin *;
            add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
            add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
        }

        location ^~/spider/web/v2/ {
            proxy_pass http://gatewaycicd/v2/;
            proxy_connect_timeout 600s;
            proxy_send_timeout 600s;
            proxy_read_timeout 600s;
            proxy_set_header Host $host:$proxy_port;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            add_header Access-Control-Allow-Origin *;
            add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
            add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
        }

                location ^~/web/ {
            proxy_pass http://gatewaycicd/web/;
            proxy_connect_timeout 600s;
            proxy_send_timeout 600s;
            proxy_read_timeout 600s;
            proxy_set_header Host $host:$proxy_port;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            add_header Access-Control-Allow-Origin *;
            add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
            add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
        }

        location ^~/spider/web/big-screen/ {
            proxy_pass http://gatewaycicd/v1/;
        }

        location ^~/spider/web/ {
            if ($http_host != '${host}:8098') {
                return 501;
            }
            proxy_pass http://10.1.5.109:8098/;
            proxy_redirect off;
            proxy_set_header Host $host:$proxy_port;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
            proxy_max_temp_file_size 0;
            proxy_connect_timeout 600s;
            proxy_send_timeout 600s;
            proxy_read_timeout 600s;
            proxy_buffer_size 4k;
            proxy_buffers 32 128k;
            proxy_busy_buffers_size 256k;
            proxy_temp_file_write_size 256k;
            proxy_set_header REMOTE_ADDR $remote_addr;
            proxy_pass_header Authorization;
            client_max_body_size 100m;
            add_header Access-Control-Allow-Origin *;
            add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
            add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
        }


        location ^~/spider/web/topo/ {
            proxy_pass http://10.1.5.109:8098/spider/web/zutai/;
            proxy_redirect off;
            proxy_set_header Host $host:$proxy_port;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
            proxy_max_temp_file_size 0;
            proxy_connect_timeout 600s;
            proxy_send_timeout 600s;
            proxy_read_timeout 600s;
            proxy_buffer_size 4k;
            proxy_buffers 32 128k;
            proxy_busy_buffers_size 256k;
            proxy_temp_file_write_size 256k;
            proxy_set_header REMOTE_ADDR $remote_addr;
            proxy_pass_header Authorization;
            client_max_body_size 100m;
            add_header Access-Control-Allow-Origin *;
            add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
            add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
        }

        location ^~/spider/web/fstatic/ {
            proxy_pass http://10.1.4.113:18080/;
        }

        location ^~/spider/web/download/ {
           proxy_pass http://10.1.4.113:18080/;
        }

        location ^~/spider/web/playVideo/ {
            proxy_pass http://10.1.4.113:18080/;
        }

        error_page 500 502 503 504 /50x.html;

        location = /50x.html {
            root html;
        }
    }

    server {
        listen 8380;
        #server_name localhost;
        server_name 10.1.5.109;

        if ($host != '10.1.5.109') {
           return 403;
        }

        location / {
            root /usr/local/nginx/html/dist;
            index index.html index.htm;
            try_files $uri $uri/ /index.html;
        }

        location /zutai {
            root   html;
            index  index.html;
            try_files $uri $uri/ /zutai/index.html;
        }

        location ^~/spider/web/v1/ {
            proxy_pass http://gatewayService/v1/;
            proxy_connect_timeout 600s;
            proxy_send_timeout 600s;
            proxy_read_timeout 600s;
            proxy_set_header Host $host:$proxy_port;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            add_header Access-Control-Allow-Origin *;
            add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
            add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
        }

        location ^~/spider/web/v2/ {
            proxy_pass http://gatewayService/v2/;
            proxy_connect_timeout 600s;
            proxy_send_timeout 600s;
            proxy_read_timeout 600s;
            proxy_set_header Host $host:$proxy_port;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            add_header Access-Control-Allow-Origin *;
            add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
            add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
        }

                location ^~/web/ {
            proxy_pass http://gatewayService/web/;
            proxy_connect_timeout 600s;
            proxy_send_timeout 600s;
            proxy_read_timeout 600s;
            proxy_set_header Host $host:$proxy_port;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            add_header Access-Control-Allow-Origin *;
            add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
            add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
        }

        location ^~/spider/web/big-screen/ {
            proxy_pass http://gatewayService/v1/;
        }

        location ^~/spider/web/ {
            if ($http_host != '${host}:8380') {
                return 501;
            }
            proxy_pass http://10.1.5.109:8380/;
            proxy_redirect off;
            proxy_set_header Host $host:$proxy_port;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
            proxy_max_temp_file_size 0;
            proxy_connect_timeout 600s;
            proxy_send_timeout 600s;
            proxy_read_timeout 600s;
            proxy_buffer_size 4k;
            proxy_buffers 32 128k;
            proxy_busy_buffers_size 256k;
            proxy_temp_file_write_size 256k;
            proxy_set_header REMOTE_ADDR $remote_addr;
            proxy_pass_header Authorization;
            client_max_body_size 100m;
            add_header Access-Control-Allow-Origin *;
            add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
            add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
        }


        location ^~/spider/web/topo/ {
            proxy_pass http://10.1.5.109:8380/spider/web/zutai/;
            proxy_redirect off;
            proxy_set_header Host $host:$proxy_port;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
            proxy_max_temp_file_size 0;
            proxy_connect_timeout 600s;
            proxy_send_timeout 600s;
            proxy_read_timeout 600s;
            proxy_buffer_size 4k;
            proxy_buffers 32 128k;
            proxy_busy_buffers_size 256k;
            proxy_temp_file_write_size 256k;
            proxy_set_header REMOTE_ADDR $remote_addr;
            proxy_pass_header Authorization;
            client_max_body_size 100m;
            add_header Access-Control-Allow-Origin *;
            add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
            add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
        }

        location ^~/spider/web/fstatic/ {
            proxy_pass http://10.1.4.113:18080/;
        }

        location ^~/spider/web/download/ {
           proxy_pass http://10.1.4.113:18080/;
        }

        location ^~/spider/web/playVideo/ {
            proxy_pass http://10.1.4.113:18080/;
        }

        error_page 500 502 503 504 /50x.html;

        location = /50x.html {
            root html;
        }
    }

    upstream gatewayService {
        server 10.1.5.110:28000;
    }
            upstream gatewaycicd {
        server 10.12.3.125:19419;
    }


        server {
                        listen       8580;
                        server_name  10.1.5.109;
                        client_max_body_size 100M;
                        underscores_in_headers on;

                        location /zutai {
                                root   html;
                                index  index.html;
                                try_files $uri $uri/ /zutai/index.html;
                        }

                        location /front {
                                root   html;
                                index  index.html;
                                try_files $uri $uri/ /front/index.html;
                        }
                        location /manage {
                                root   html;
                                index  index.html;
                                try_files $uri $uri/ /manage/index.html;
                        }
                        location / {
                                root   /usr/local/nginx/html/dist;
                                index  index.html index.htm;
                                try_files $uri $uri/ /index.html;
                        }

                        location ^~/spider/web/bpmRunTime/ {
                                proxy_set_header Host $host;
                                proxy_set_header X-Real-Ip $remote_addr;
                                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                                proxy_set_header X-Forworded-For $http_x_forwarded_for;
                                proxy_pass http://10.1.203.120:28052/;
                        }
                        location ^~/spider/web/bpmModel/ {
                                proxy_set_header Host $host;
                                proxy_set_header X-Real-Ip $remote_addr;
                                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                                proxy_set_header X-Forworded-For $http_x_forwarded_for;

                                proxy_pass http://10.1.203.120:28052/;
                        }
                        location ^~/spider/web/form/ {
                                proxy_set_header Host $host;
                                proxy_set_header X-Real-Ip $remote_addr;
                                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                                proxy_set_header X-Forworded-For $http_x_forwarded_for;

                                proxy_pass http://10.1.203.120:28052/;
                        }

                        location ^~/spider/web/uc/ {
                                proxy_set_header Host $host;
                                proxy_set_header X-Real-Ip $remote_addr;
                                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                                proxy_set_header X-Forworded-For $http_x_forwarded_for;

                                proxy_pass http://10.1.203.120:28052/;
                        }
                        location ^~/spider/web/portal/ {
                                proxy_set_header Host $host;
                                proxy_set_header X-Real-Ip $remote_addr;
                                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                                proxy_set_header X-Forworded-For $http_x_forwarded_for;

                                proxy_pass http://10.1.203.120:28052/;
                        }

                        location ^~/spider/web/download/ {
                                proxy_pass http://10.1.5.143:18080/;
                        }

                        location ^~/spider/web/v1/ {
                                proxy_pass   http://10.1.203.120:28000/v1/;
                                proxy_connect_timeout 600s;
                                proxy_send_timeout 600s;
                                proxy_read_timeout 600s;
                        }

                        location ^~/spider/web/web/ {
                                proxy_pass   http://10.1.203.120:28000/web/;
                                proxy_connect_timeout 600s;
                                proxy_send_timeout 600s;
                                proxy_read_timeout 600s;
                        }

                        location ^~/spider/web/v2/ {
                                proxy_pass   http://10.1.203.120:28000/v2/;
                                proxy_connect_timeout 600s;
                                proxy_send_timeout 600s;
                                proxy_read_timeout 600s;
                        }

                        location ^~/spider/web/ {
                                proxy_pass http://10.1.5.109:8580/;
                                proxy_redirect     off;
                                proxy_set_header   Host             $host:$proxy_port;
                                proxy_set_header   X-Real-IP        $remote_addr;
                                proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
                                proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
                                proxy_max_temp_file_size 0;
                                proxy_connect_timeout      600s;
                                proxy_send_timeout         600s;
                                proxy_read_timeout         600s;
                                proxy_buffer_size          4k;
                                proxy_buffers              32 128k;
                                proxy_busy_buffers_size    256k;
                                proxy_temp_file_write_size 256k;
                                proxy_set_header REMOTE_ADDR $remote_addr;
                                proxy_pass_header Authorization;
                                client_max_body_size 100m;
                        }

                        error_page   500 502 503 504  /50x.html;
                        location = /50x.html {
                                root   html;
                        }
        }




    upstream spider{
        server 10.1.203.120:18080 weight=1;
        server 10.1.5.144:18080 weight=1;
    }

    upstream compositeService {
    #server 10.12.3.58:13553 weight=1;
        server 10.1.5.110:28001 weight=1;
    }

   upstream bigFileUploadServiceJdk17 {
       server 10.1.203.120:28055 weight=1;
   }

    # another virtual host using mix of IP-, name-, and port-based configuration
    #
    #server {
    #    listen       8000;
    #    listen       somename:8080;
    #    server_name  somename  alias  another.alias;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}


    # HTTPS server
    #
    #server {
    #    listen       443 ssl;
    #    server_name  localhost;

    #    ssl_certificate      cert.pem;
    #    ssl_certificate_key  cert.key;

    #    ssl_session_cache    shared:SSL:1m;
    #    ssl_session_timeout  5m;

    #    ssl_ciphers  HIGH:!aNULL:!MD5;
    #    ssl_prefer_server_ciphers  on;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}
#gemc-
server {
        listen 8388;
        server_name 10.1.203.121;
        client_max_body_size 100M;
        underscores_in_headers on;  # 开启允许下划线的头
        if ( $host != '10.1.203.121' ) {
           return 403;
        }

    location ^~/auth/ {
          proxy_pass  http://10.1.5.113:8180/auth/;
    }
    location ^~/spider/inop/ {
        proxy_pass http://10.1.5.113:18680/spider/inop/;
    }

    location ^~/spider/web/composite/ {
        proxy_pass http://10.1.203.121:28001/;
        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
        proxy_set_header Host $host:$proxy_port;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Methods' 'GET,POST,DELETE';
        add_header 'Access-Control-Allow-Header' 'Content-Type,*';
        }

    location ^~/spider/web/v2/ {
        proxy_pass   http://10.1.203.121:13563/v1/;
        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
        proxy_set_header   Host             $host:$proxy_port;
        proxy_set_header   X-Real-IP        $remote_addr;
        proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
    add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
        add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
        }

    location ^~/spider/web/big-screen/ {
        proxy_pass   http://10.1.203.121:28001/v1/;
        }

    location /nginxAuth {
         internal;
         # 鉴权服务器的地址
         proxy_pass http://10.1.203.121:28001/v1/monitorapi/nginxAuth;
        proxy_http_version 1.1;
        }

    location @error403 {
        return 403 /403.html;
        }

    location ^~/spider/web/playVideo/ {
         proxy_pass  http://10.1.5.113:8389/;
        }

    location ^~/spider/web/bigFileUpload/ {
        proxy_pass   http://10.12.3.79:28090/;
        }

    location ^~/spider/web/fstatic/ {
         proxy_pass http://10.1.5.143:18080/;
         #proxy_pass   http://10.1.5.113:8080/;
         #proxy_pass  http://10.12.70.61:8080/;
        }

    location ^~/spider/web/geoserver/ {
         proxy_pass  http://10.1.5.144:7070/;
        }


    location ^~/spider/web/analyzer/api/ {
        proxy_pass http://10.252.242.92/analyzer/api/;
        proxy_redirect     off;
        proxy_set_header   Host             $host:$proxy_port;
        proxy_set_header   X-Real-IP        $remote_addr;
        proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        proxy_max_temp_file_size 0;
        proxy_connect_timeout      90;
        proxy_send_timeout         90;
        proxy_read_timeout         90;
        proxy_buffer_size          4k;
        proxy_buffers              32 128k;
        proxy_busy_buffers_size    256k;
        proxy_temp_file_write_size 256k;
        }

    location ^~/spider/web/bpmRunTime/ {
        proxy_set_header Host $host;
        proxy_set_header X-Real-Ip $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forworded-For $http_x_forwarded_for;
        proxy_pass http://10.1.203.121:28051/;
        }

    location ^~/spider/web/bpmModel/ {
        proxy_set_header Host $host;
        proxy_set_header X-Real-Ip $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forworded-For $http_x_forwarded_for;
        proxy_pass http://10.1.203.121:28050/;
        }

    location ^~/spider/web/form/ {
        proxy_set_header Host $host;
        proxy_set_header X-Real-Ip $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forworded-For $http_x_forwarded_for;
        proxy_pass http://10.1.203.121:28052/;
        }

    location ^~/spider/web/uc/ {
        proxy_set_header Host $host;
        proxy_set_header X-Real-Ip $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forworded-For $http_x_forwarded_for;
        proxy_pass http://10.1.203.121:28054/;
        }

    location ^~/spider/web/portal/ {
        proxy_set_header Host $host;
        proxy_set_header X-Real-Ip $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forworded-For $http_x_forwarded_for;
        proxy_pass http://10.1.203.121:28053/;
        }


    location ^~/spider/web/ {
        #proxy_pass http://10.1.5.113:8480/;
        proxy_pass http://10.1.5.113:8389/spider/web/;
        proxy_redirect     off;
        proxy_set_header   Host             $host:$proxy_port;
        proxy_set_header   X-Real-IP        $remote_addr;
        proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
        #proxy_set_header   X-Forworded-For  $http_x_forwarded_for;
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        proxy_max_temp_file_size 0;
        proxy_connect_timeout      600s;
        proxy_send_timeout         600s;
        proxy_read_timeout         600s;
        proxy_buffer_size          4k;
        proxy_buffers              32 128k;
        proxy_busy_buffers_size    256k;
        proxy_temp_file_write_size 256k;
        proxy_set_header REMOTE_ADDR $remote_addr;
        proxy_pass_header Authorization;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        client_max_body_size 100m;
        add_header 'Access-Control-Allow-Origin' "$http_origin";
        add_header 'Access-Control-Allow-Credentials' 'true' always ;
        # test for lixuefeng
        #chunked_transfer_encoding off;
        #add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
        }


    location ^~/spider/web/topo/ {
        proxy_pass http://10.1.5.113:8389/zutai/;
        proxy_set_header   Host             $http_host;
        proxy_set_header   X-Real-IP        $remote_addr;
        proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        proxy_connect_timeout      90;
        proxy_send_timeout         90;
        proxy_read_timeout         300;
        proxy_buffer_size          256k;
        proxy_buffers              4 256k;
        proxy_busy_buffers_size    256k;
        proxy_temp_file_write_size 256k;
        proxy_pass_header Authorization;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header REMOTE-HOST $remote_addr;
        client_max_body_size 100m;
        client_body_buffer_size 256k;
        proxy_max_temp_file_size 128m;
        }
   location ^~/spider/web/download/ {
            #auth_request /nginxAuth;
            #error_page 403 = @error403;
            #proxy_pass http://10.1.203.38:18080/;
            proxy_pass http://10.1.5.143:18080/;
            #proxy_pass http://10.1.5.113:8480/download/;
            #auth_request_set $user $upstream_http_x_forwarded_user;
            #proxy_set_header X-Forwarded-User $user;
            #auth_request http://10.1.123.53:28129/v1/monitorapi/nginxAuth;
            #add_header Cache-Control no-store;
            #add_header Cache-Control private;
            #expires 0;
            #proxy_set_header Host $host;
            #proxy_set_header X-Real-Ip $remote_addr;
            #proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            #proxy_set_header X-Forworded-For $http_x_forwarded_for;
            #add_header 'Access-Control-Allow-Origin' 'http://10.1.203.120';
            #add_header 'Access-Control-Allow-Methods' 'GET,POST,DELETE';
            #add_header 'Access-Control-Allow-Header' 'Content-Type,*';
        }
   location ^~/spider/inop/download/ {
            #auth_request /nginxAuth;
            #error_page 403 = @error403;
            proxy_pass http://10.1.5.143:18080/;
            #proxy_pass http://10.1.5.113i:8480/download/;
            #auth_request_set $user $upstream_http_x_forwarded_user;
            #proxy_set_headdder X-Forwarded-User $user;
            #auth_request http://10.1.123.53:28129/v1/monitorapi/nginxAuth;
            #add_header Cache-Control no-store;
            #add_header Cache-Control private;
            #expires 0;
            #proxy_set_header Host $host;
            #proxy_set_header X-Real-Ip $remote_addr;
            #proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            #proxy_set_header X-Forworded-For $http_x_forwarded_for;
            #add_header 'Access-Control-Allow-Origin' 'http://10.1.203.120';
            #add_header 'Access-Control-Allow-Methods' 'GET,POST,DELETE';
            #add_header 'Access-Control-Allow-Header' 'Content-Type,*';
        }

    location ^~/spider/3d/ {
        proxy_pass http://10.12.3.79:8280/;
        proxy_set_header   Host             $http_host;
        proxy_set_header   X-Real-IP        $remote_addr;
        proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        proxy_connect_timeout      90;
        proxy_send_timeout         90;
        proxy_read_timeout         300;
        proxy_buffer_size          256k;
        proxy_buffers              4 256k;
        proxy_busy_buffers_size    256k;
        proxy_temp_file_write_size 256k;
        proxy_pass_header Authorization;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header REMOTE-HOST $remote_addr;
        client_max_body_size 100m;
        client_body_buffer_size 256k;
        proxy_max_temp_file_size 128m;
        }

    }


    server {
        listen       8980;
        server_name  10.1.203.120;
        client_max_body_size 100M;

        if ( $host != '10.1.203.120' ) {
           return 403;
        }

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location ^~/web/ {
            #proxy_pass http://10.1.203.119:8085;
proxy_pass http://10.1.203.120:8085;
            proxy_redirect     off;
            proxy_set_header   Host             $host:$proxy_port;
            proxy_set_header   X-Real-IP        $remote_addr;
            proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
            proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
            proxy_max_temp_file_size 0;
            proxy_connect_timeout      600s;
            proxy_send_timeout         600s;
            proxy_read_timeout         600s;
            proxy_buffer_size          4k;
            proxy_buffers              32 128k;
            proxy_busy_buffers_size    256k;
            proxy_temp_file_write_size 256k;
            proxy_set_header REMOTE_ADDR $remote_addr;
            proxy_pass_header Authorization;
            client_max_body_size 100m;
        }
        location /webbas {
                root   html;
                index  index.html;
                try_files $uri $uri/ /webbas/index.html;

        }

        location /micro {
            root   html;
            index  index.html;
            try_files $uri $uri/ /webbas/index.html;
        }
        location /subapp/ {
            root   html;
            index  index.html;
            try_files $uri $uri/ /webbas/subapp/login/index.html;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }

    }


        upstream skywalkingServer{
                server 10.1.5.112:8082;
        }

        # B接口服务器组
    upstream binterfaceBackendgd {
      #server 10.12.70.59:18185 weight=1;
      #server 10.1.203.121:28020 weight=1;
      #server 10.1.4.49:28020 weight=1;
      server 10.1.6.80:63728 weight=1;
    }




#B接口反向代理
    server {
        listen 28080;
        server_name 10.1.5.109;
        client_max_body_size 100M;
        underscores_in_headers on;

        location / {
            proxy_pass http://binterfaceBackendgd;
            proxy_pass_request_headers on;
            proxy_set_header Host $host:$proxy_port;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            add_header 'Access-Control-Allow-0rigin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET,POST,DELETE';
            add_header 'Access-Control-Allow-Header' 'Content-Type,*';

        }

   }


   # B接口正向代理
   server {
        listen 8086;
        server_name 10.1.5.109;
        client_max_body_size 100M;
        underscores_in_headers on;
        location ~/FsuProxy {
            if ($query_string ~ ".*(?:^|\?|&)real=(.+?)(?:(?:&.*)|$)") {
               proxy_pass $1;
            }

        }

   }
}
