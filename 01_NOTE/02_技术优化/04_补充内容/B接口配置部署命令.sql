  2  kubectl  get pods -n cmchain
    3  kubectl apply -f cmchain_nginx_services.yaml
    4  kubectl get pods -n cmchain
    5  vi gateway_configmap.yaml
    6  vi gateway_configmap_gm.yaml
    7  vi gateway_nginx_configmap_nginx.yaml
    8  kubectl apply -f gateway_configmap.yaml
    9  kubectl apply -f gateway-service.yaml
   10  kubectl apply -f gateway_configmap_gm.yaml
   11  kubectl apply -f gateway-service-gm.yaml
   12  docker ps
   13  kubectl  get pods -n cmchain
   14  kubectl logs -n cmchain cmchain-baascore-7f69c65697-mwgdt
   15  pwd
   16  kubectl config view --minify --output 'jsonpath={.clusters[0].name}'
   17  kubectl logs -n cmchain cmchain-baascore-7f69c65697-mwgdt
   18  kubectl config view --minify --output 'jsonpath={.clusters[0].name}'
   19  kubectl config view --minify
   20  cd
   21  ls
   22  vi hub-secret.yaml
   23  ls
   24  ll
   25  history
   26  pwd
   27  cd /mnt
   28  ls
   29  cd nfs
   30  ls
   31  cd install
   32  ls
   33  cd deploy_scripts/
   34  ls
   35  cd k8s
   36  ls
   37  cd multiset/
   38  ls
   39  vi gateway_configmap.yaml
   40  ls
   41  vi gateway_configmap_gm.yaml
   42  vi gateway_nginx_configmap_nginx.yaml
   43  vi cmchain_configmap_bootstrap_single.yaml
   44  vi kubectl apply -f cmchain_configmap_logback.yaml
   45  ls -atl|more
   46  pwd
   47  ls
   48  ll
   49  history
   50  kubectl  get pods -n cmchain
   51  kubectl logs -n cmchain cmchain-baascore-7f69c65697-mwgdt
   52  history
   53  kubectl config view --minify
   54  docekr
   55  kubectl logs -n cmchain cmchain-baascore-7f69c65697-mwgdt
   56  kubectl logs -n cmchain cmchain-baascore-7f69c65697-mwgdt --tail=500
   57  kubectl logs -n cmchain cmchain-baascore-7f69c65697-mwgdt --tail=500|more
   58  kubectl logs -n cmchain cmchain-baascore-7f69c65697-mwgdt
   59  cd /mnt/nfs
   60  ls
   61  cd cmchain/
   62  ls
   63  cd cmri
   64  ls
   65  cd ../
   66  kubectl get pods -n cmchain
   67  kubectl -n cmchain logs cmchain-baascore-7f69c65697-mwgdt
   68  pwd
   69  cd ..
   70  cd de
   71  cd install
   72  cd deploy_scripts/
   73  ls
   74  cd k8s
   75  ls
   76  cd multiset/
   77  ls
   78  ../sh/restart_service.sh baascore
   79  kubectl  get pods -n cmchain
   80  kubectl -n cmchain logs cmchain-baascore-7f69c65697-2rdxk
   81  kubectl  get pods -n cmchain
   82  kubectl -n cmchain logs cmchain-cmchain-baascore-7f69c65697-2rdxk
   83  kubectl -n cmchain logs cmchain-cmchain-baascore-7f69c65697-2rdx
   84  kubectl -n cmchain logs cmchain-baascore-7f69c65697-2rdxk
   85  ls
   86  vi cmchain_baascore_services.yaml
   87  pwd
   88  cd /mnt/nfs
   89  ls
   90  cd baas
   91  ls
   92  cd temp_cmchain/
   93  ls
   94  cd ../chainconf
   95  ls
   96  cd ../
   97  kubectl get pods -n cmchain
   98  kubectl exec -it cmchain-baascore-7f69c65697-2rdxk -n cmchain -- bash
   99  kubectl get ns
  100  cd /mnt/nfs/install/deploy_scripts/k8s/multiset
  101  ../sh/restart_service.sh baascore
  102  kubectl  get pods -n cmchain
  103  kubectl exec -it cmchain-baascore-7f69c65697-wmwbn -n cmchain -- bash
  104  kubectl get ns
  105  pwd
  106  cd /root
  107  ls
  108  cd .kube/
  109  ls
  110  vi config
  111  cd /mnt/nfs/install/deploy_scripts/k8s/multiset
  112  kubectl get ns
  113  kubectl exec -it cmchain-baascore-7f69c65697-wmwbn -n cmchain -- bash
  114  pwd
  115  cd /mnt
  116  cd nfs
  117  ls
  118  cd baas
  119  ls
  120  cd command
  121  ls
  122  ll
  123  cd fabric1.4.6/
  124  ls
  125  cd ecdsa/
  126  ls
  127  ll
  128  cd ../
  129  ls
  130  cd command
  131  ls
  132  cd fabric2.2.1/
  133  ls
  134  cd ecdsa/
  135  ls
  136  ll
  137  kubectl exec -it cmchain-baascore-7f69c65697-wmwbn -n cmchain -- bash
  138  cd ../../
  139  ls
  140  cd install/
  141  ls
  142  cd deploy_scripts/
  143  ls
  144  cd k8s
  145  ls
  146  cd multiset/
  147  ls
  148  vi cmchain_baassupport_services.yaml
  149  kubectl get pods -n cmchain
  150  kubectl -n cmchain exec -it cmchain-baassupport-66c9d9c4bc-nml5g -- bash
  151  kubectl -n cmchain exec -it cmchain-baascore-7f69c65697-wmwbn -- bash
  152  kubectl delete deployment -n cmchain cmchain-baascore
  153  ls
  154  kubectl apply -f cmchain_baascore_services.yaml
  155  kubectl get pods -n cmchain
  156  kubectl -n cmchain exec -it cmchain-baascore-7f69c65697-8fx9q -- bash
  157  kubectl get ns
  158  kubectl get pods -n erqqialhzq0durjd
  159  kubectl logs -n erqqialhzq0durjd peer0-51d81789-org1-070016ee-56df69b9d6-jt5b4
  160  kubectl get pods -n erqqialhzq0durjd -owide
  161  kubectl get ns
  162  kubectl get pods -n 47jovjyzszsrutwn -owide
  163  kubectl -n  47jovjyzszsrutwn logs go-fabric-proxy-8b7f8bb54-pcnrm
  164  kubectl get pods -n 47jovjyzszsrutwn -owide
  165  kubectl get pods -n cmchain -owide
  166  kubectl exec -it cmchain-baascore-7f69c65697-8fx9q -n 47jovjyzszsrutwn /bin/bash
  167  kubectl exec -it cmchain-baascore-7f69c65697-8fx9q -n cmchain /bin/bash
  168  kubectl get pods -n 47jovjyzszsrutwn -owide
  169  kubectl get cm -n 47jovjyzszsrutwn -owide
  170  kubectl edit cm go-fabric-proxy-configmap -n 47jovjyzszsrutwn
  171  kubectl get nodes
  172  kubectl taint 10.1.4.196
  173  kubectl taint 10.1.4.196 key=test:NoSchedule
  174  kubectl taint node 10.1.4.196 key=test:NoSchedule
  175  kubectl get pods -n 47jovjyzszsrutwn -owide
  176  kubectl delete pod -n 47jovjyzszsrutwn go-fabric-proxy-8b7f8bb54-pcnrm
  177  kubectl get pods -n 47jovjyzszsrutwn -owide
  178  kubectl delete pod -n 47jovjyzszsrutwn prometheus-47jovjyzszsrutwn-677457775f-q4dl8
  179  kubectl get pods -n 47jovjyzszsrutwn -owide
  180  kubectl describe pod -n 47jovjyzszsrutwn prometheus-47jovjyzszsrutwn-677457775f-f567m
  181  kubectl edit deployment  -n 47jovjyzszsrutwn prometheus
  182  kubectl get deploy  -n 47jovjyzszsrutwn
  183  kubectl edit deployment  -n 47jovjyzszsrutwn prometheus-47jovjyzszsrutwn
  184  kubectl get pods -n 47jovjyzszsrutwn -owide
  185  kubectl get pods -n gateway
  186  ls
  187  vi gateway-service.yaml
  188  kubectl get ns
  189  kubectl get pods -n erqqialhzq0durjd
  190  kubectl delete ns erqqialhzq0durjd
  191  vi gateway-service.yaml
  192   kubectl get pods -n gateway
  193  ../sh/gatewayTest.sh 6e16bbc1da3f45a8b318a26687f09e4b 10.1.4.193
  194  ../sh/gatewayTest.sh 6e16bbc1da3f45a8b318a26687f09e4b 10.1.4.193:31008
  195  ../sh/gatewayTest.sh 6e16bbc1da3f45a8b318a26687f09e4b 10.1.4.194:31008
  196  ../sh/gatewayTest.sh 6e16bbc1da3f45a8b318a26687f09e4b 10.1.4.195:31008
  197  ls
  198  kubectl get pods -n gatway
  199  kubectl get pods -n gateway
  200  kubectl exec -it -n gateway gateway-6fc669d45d-5gfbf -- bash
  201  kubectl get pods -n gateway -owide
  202  ../sh/restart_service_gateway.sh gateway
  203  kubectl -n gateway delete pod gateway-6fc669d45d-5gfbf
  204  kubectl -n gateway delete pod gateway-gm-f66f4644c-x424m
  205  kubectl get pods -n gateway -owide
  206  kubectl -n cmchain describe pod gateway-6fc669d45d-hnzs8
  207  kubectl -n gateway  describe pod gateway-6fc669d45d-hnzs8
  208  ls
  209  vi    gateway-service.yaml
  210  vi    gateway-service-gm.yaml
  211  vi    gateway-service.yaml
  212  vi    gateway-service-gm.yaml
  213  kubectl apply -f gateway-service.yaml
  214  kubectl apply -f gateway-service-gm.yaml
  215  kubectl get pods -n gateway -owide
  216  ../sh/gatewayTest.sh 6e16bbc1da3f45a8b318a26687f09e4b 10.1.4.195:31008
  217  kubectl exec -it -n gateway gateway-668c4fd87-j6cgw -- bash
  218  ls
  219  vi  gateway-service.yaml
  220  vi gateway_configmap.yaml
  221  vi gateway-service.yaml
  222  vi gateway-service-gm.yaml
  223  kubectl apply -f gateway-service.yaml
  224  kubectl apply -f gateway-service-gm.yaml
  225  kubectl get pods -n gateway
  226  kubectl delete pod -n gateway gateway-85cbbdb6b9-qp8jw
  227  kubectl delete pod -n gateway gateway-gm-675b5cf954-q7dbj
  228  ../sh/gatewayTest.sh 6e16bbc1da3f45a8b318a26687f09e4b 10.1.4.195:31008
  229  kubectl exec -it -n gateway gateway-85cbbdb6b9-qp8jw -- bash
  230  kubectl get pods -n gateway
  231  kubectl exec -it -n gateway gateway-85cbbdb6b9-44g59 -- bash
  232  ls
  233  vi gateway-service.yaml
  234  kubectl get deploy -n gateway
  235  kubectl delete deploy -n gateway
  236  kubectl delete deploy gateway -n gateway
  237  kubectl delete deploy gateway-gm -n gateway
  238  kbuectl apply -f gateway-service.yaml
  239  kubectl apply -f gateway-service.yaml
  240  kubectl get pods -n gateway
  241  kubectl -n gateway exec -it gateway-85cbbdb6b9-lntsf -- bash
  242  kubectl get pods -n gateway -owide
  243  kubectl -n gateway exec -it gateway-85cbbdb6b9-lntsf -- bash
  244  ls
  245  vi gateway_configmap.yaml
  246  kubectl get cm -n gateway
  247  kubectl edit cm gateway-configmap -n gateway
  248  kubectldelete deply -n gateway gateway
  249  kubectl delete deply -n gateway gateway
  250  kubectl delete deply gateway -n gateway
  251  kubectl get deploy -n gateway
  252  kubectl delete deploy -n gateway
  253  kubectl delete deploy gateway -n gateway
  254  vi gateway-service.yaml
  255  vi gateway_configmap.yaml
  256  kubectl apply -f gateway_configmap.yaml
  257  kubectl apply -f gateway-service.yaml
  258  ../sh/gatewayTest.sh 6e16bbc1da3f45a8b318a26687f09e4b 10.1.4.195:31008
  259  ls
  260  vi gateway_configmap_gm.yaml
  261  vi gateway-service-gm.yaml
  262  history
  263  ../sh/gatewayTest.sh 6e16bbc1da3f45a8b318a26687f09e4b 10.1.4.195:31008
  264  pwd
  265  top
  266  df
  267  top
  268  df
  269  vi /etc/sysconfig/iptables
  270  pwd
  271  ls
  272  cd /etc/sysconfig/iptables
  273  cd /etc/sysconfig
  274  cp iptables iptables.org
  275  vi iptables
  276  systemctl restart iptables
  277  cd /opt
  278  ls
  279  cd nfs
  280  ls
  281  cd /mnt
  282  ls
  283  cd nfs
  284  ls
  285  ll
  286  ls
  287  docker ps
  288  history
  289  cd /mnt/nfs
  290  ls
  291  pwd
  292  ls
  293  pwd
  294  ls
  295  cd ..
  296  ls
  297  cd ..
  298  ls
  299  history|grep mount
  300  mount -t nfs -o nolock 10.1.4.196:/opt/nfs /mnt/nfs
  301  cd /mnt/nfs
  302  ls
  303  cd baas
  304  ls
  305  cd command
  306  ls
  307  cd ..
  308  ls
  309  cd app
  310  ls
  311  cd ..
  312  ls
  313  pwd
  314  ls
  315  docker ps|grep gateway
  316  docker logs -f c1ae --tail=10
  317  kubectl get pods
  318  kubectl get pods -n default
  319  kubectl get pods
  320  kubectl get nodes
  321  docker ps
  322  kubectl get pods -n cmchain
  323  history|grep kubectl
  324  kubectl get pods -n cmchain
  325  kubectl logs -n cmchain cmchain-baascore-7f69c65697-8fx9q
  326  ll /mnt/nfs/baas/chainconf/BC4EAC8FB7CB51D5B193E1ACD8F7EC8B
  327  more /mnt/nfs/baas/chainconf/BC4EAC8FB7CB51D5B193E1ACD8F7EC8B
  328  kubectl logs -n cmchain cmchain-baascore-7f69c65697-8fx9q
  329  pwd
  330  ls
  331  cd  ..
  332  ls
  333  cd install
  334  ls
  335  cd deploy_scripts/
  336  ls
  337  cd k8s
  338  ls
  339  cd sh
  340  ls
  341  more restart_service.sh
  342  sudo kubectl  get pods -n cmchain |grep $serviceName | awk '{print $1}'
  343   kubectl  get pods -n cmchain |grep baas | awk '{print $1}'
  344   kubectl  get pods -n cmchain |grep baascore | awk '{print $1}'
  345  ls
  346  vi restart_service.sh
  347  history
  348  history|grep kubectl|grep delete
  349  pwd
  350  ls
  351  pwd
  352  ls
  353  kubectl get pods -n cmchain
  354  pwd
  355  ls
  356  ./restart_service.sh cmchain-baascore
  357  kubectl  get pods -n cmchain
  358  docker images
  359  curl 10.1.4.196:5000/cmri-baas/fabric-peer
  360  pwd
  361  ls
  362  ./restart_service.sh cmchain-baascore
  363  kubectl  get pods -n cmchain
  364  kubectl logs -n cmchain  cmchain-baascore-7f69c65697-c294j
  365  kubectl get pods -n cmchain
  366  pwd
  367  kubectl get pods -n cmchain
  368  kubectl logs -n cmchain cmchain-baascore-7f69c65697-c294j
  369  kubectl logs -n cmchain cmchain-baascore-7f69c65697-c294j --tail=10
  370  ./restart_service.sh cmchain-baascore
  371   kubectl  get pods -n cmchain
  372  kubectl logs -n cmchain cmchain-baascore-7f69c65697-fc7f7
  373   kubectl  get pods -n cmchain
  374  kubectl logs -n cmchain cmchain-admin-bc65cf444-2dg9n
  375   kubectl  get pods -n cmchain
  376  kubectl logs -n cmchain cmchain-auth-787569967c-mq7bt
  377   kubectl  get pods -n cmchain
  378  kubectl logs -n cmchain cmchain-gateway-f78d599f9-dfxqc
  379   kubectl  get pods -n cmchain
  380  kubectl logs -n cmchain cmchain-baascore-7f69c65697-fc7f7
  381   kubectl  get pods -n cmchain
  382  kubectl logs -n cmchain cmchain-baascore-7f69c65697-fc7f7
  383  kubectl logs -n cmchain cmchain-baascore-7f69c65697-fc7f7  --tail20
  384  kubectl logs -n cmchain cmchain-baascore-7f69c65697-fc7f7  --tail=20
  385  kubectl logs -n cmchain cmchain-baascore-7f69c65697-fc7f7  --tail=500
  386   kubectl  get pods -n cmchain
  387  kubectl logs -n cmchain cmchain-baassupport-66c9d9c4bc-nml5g --tail=500
  388   kubectl  get pods -n cmchain
  389  kubectl logs -n cmchain cmchain-baascore-7f69c65697-fc7f7 --tail=500
  390  curl http://36.139.0.78:7650/wizdata/ui
  391  curl ifconfig.me
  392  kubectl logs -n cmchain cmchain-baascore-7f69c65697-fc7f7 --tail=500
  393  ls
  394  kubectl get pods -n cmchain
  395  df -h |grep nfs
  396  kubectl get nodes
  397   kubectl get pods -n cmchain -owide
  398  kubectl get ns
  399  kubeclt -n 47jovjyzszsrutwn get pods
  400  kubectl -n 47jovjyzszsrutwn get pods
  401  kubectl -n 47jovjyzszsrutwn logs go-fabric-proxy-8b7f8bb54-9gv2t
  402  pwd
  403  cd /mnt/nfs/install/deploy_scripts/k8s/sh
  404  ls
  405  kubectl get ns
  406  kubectl -n 47jovjyzszsrutwn get pods
  407  kubectl -n 47jovjyzszsrutwn get pods |grep -v NAME|awk '{"kubectl -n 47jovjyzszsrutwn  delete pod " $1}'
  408  kubectl -n 47jovjyzszsrutwn get pods |grep -v NAME
  409  kubectl -n 47jovjyzszsrutwn get pods |grep -v NAME|awk '{print "kubectl -n 47jovjyzszsrutwn  delete pod " $1}'
  410  kubectl -n 47jovjyzszsrutwn get pods |grep -v NAME|awk '{print "kubectl -n 47jovjyzszsrutwn  delete pod " $1}'  |sh
  411  kubectl -n 47jovjyzszsrutwn get pods
  412  kubectl -n gateway get pods
  413  kubectl -n gateway delete pod gateway-668c4fd87-mjnm2
  414  kubectl -n gateway get pods
  415  kubectl exec -it -n gateway gateway-668c4fd87-mjnm2 -- bash
  416  ls
  417  kubectl exec -it -n gateway gateway-668c4fd87-mjnm2 -- sh
  418  kubectl exec -it -n gateway gateway-668c4fd87-r7x7j -- sh
  419  kubectl get pods -n cmchain
  420  kubectl logs -n cmchain cmchain-baascore-7f69c65697-fc7f7 --tail=500
  421  docker ps
  422  vi /etc/fstab
  423  mount -a
  424  mount
  425  vi /etc/fstab
  426  ls
  427  df
  428  pwd
  429  top
  430  pwd
  431  kubectl get nodes
  432  df
  433  cd /opt
  434  ls
  435  cd nfs
  436  ls
  437  cd nfs
  438  ls
  439  cd install
  440  ls
  441  cd scripts/
  442  ls
  443  cd ..
  444  ls
  445  cd ..
  446  df
  447  ls
  448  du -sk 碳核宝部署
  449  pwd
  450  ls
  451  crontab -l
  452  cd /etc/sysconfig
  453  ls
  454  vi iptables
  455  systemctl restart iptables
  456  docker ps -a
  457  ll
  458  cd /mnt/nfs
  459  ls
  460  cd cmchain
  461  ls
  462  cd cmri
  463  ls
  464  cd A4FA9C1394BD7905A0A9AC3DE93280DC/
  465  ls
  466  pwd
  467  ls
  468  vi *.yaml
  469  pwd
  470  ls
  471  cd ..
  472  ls
  473  vi
  474  vi /etc/ssh/sshd_config
  475  vi /etc/ssh/sshd_config
  476  service sshd restart
  477  /bin/systemctl restart sshd.service
  478  lscpu
  479  cat /proc/cpuinfo
  480  cat /proc/cpuinfo |grep physical
  481  cat /proc/meminfo
  482  df -h
  483  vi /etc/ssh/sshd_config
  484  service sshd restart
  485  ps -ef |grep Jetty
  486  find / -name "jetty.xml" 2>/dev/null
  487  cd /opt/aspmon/agent_host_root/spectre/standalone/3.0
  488  netstat -pln |grep 2022
  489  /opt/aspmon/agent_host_root/spectre/standalone/3.0
  490  cd /opt/aspmon/agent_host_root/spectre/standalone/3.0
  491  ll
  492  netstat  -pln|grep 2022
  493  kill -9 8309
  494  rm  -rf /opt/aspmon/agent_host_root/spectre/standalone/3.0
  495  netstat -pln |grep 10250
  496  ps -ef |grep 986
  497  netstat -pln |grep  1080
  498  ps -ef |grep 5390
  499  ps -ef |grep  8086
  500  netstat -pln |grep  1080
  501  cd /etc/
  502  ll
  503  cd sysconfig/
  504  ll
  505  vi  iptables
  506  systemctl restart iptables
  507  sudo shutdown -h now
  508  cd /etc/docker
  509  ll
  510  vi daemon.json
  511  ps -ef
  512  ps -ef | grep java
  513  top
  514  docker ps
  515  docker ps -a
  516  docker ps -a | grep bin
  517  docker ps -a | grep nginx
  518  telnet 10.1.203.120 8848
  519  sudo yum install telnet
  520  telnet 10.1.203.120 8848
  521  docker ps
  522  netstat -ntlp
  523  docker run --name ftpproxy-service-p1 --net host --log-driver=json-file --log-opt max-size=30m --log-opt max-file=3 --env ENV_NACOS=10.1.203.120:8848 --env ENV_TYPE=gdems-dev --env ENV_APP_NAME=ftpproxy --env ENV_NACOS_PASSWORD='D&V2HR43TutFjf%aKqk' -v /tmp/logs/ftpproxy-service:/opt/data/logs/ -d  10.1.6.34:8080/cicd-public-60/ftpproxy-service:1.0.3.2_5_20250710070932
  524  docker ps
  525  netstat -ntlp
  526  docker run --name switchmanage-service-p1 --net host --log-driver=json-file --log-opt max-size=30m --log-opt max-file=3 --env ENV_NACOS=10.1.203.120:8848 --env ENV_TYPE=gdems-dev --env ENV_APP_NAME=switchmanage --env ENV_NACOS_PASSWORD='D&V2HR43TutFjf%aKqk' -v /tmp/logs/switchmanage-service:/opt/data/logs/ -d  10.1.6.34:8080/cicd-public-72/switchmanage-service:1.0.3.2_4_20250710070446
  527  ps -ef | grep kafka
  528  cd /opt/docker
  529  ll
  530  cd common/
  531  cd kafka/
  532  ll
  533  cd zookeeper-3.4.10/
  534  ps -ef | grep zookeeper
  535  ll
  536  cd data/
  537  cd ..
  538  rm -rf data/
  539  ll
  540  cd  conf/
  541  cd ..
  542  ll
  543  mkdir data
  544  ll
  545  cd conf/
  546  vim zoo.cfg
  547  cd ../bin/
  548  sh zkServer.sh start
  549  ps -ef | grep zookeeper.out
  550  ps -ef | grep zookeeper
  551  cd ../data/
  552  jps -ml
  553  ps -ef | grep zookeeper
  554  cd ../..
  555  cd kafka_2.11-0.11.0.0/
  556  cd logs/
  557  cd ..
  558  rm -rf logs/
  559  ll
  560  mkdir logs
  561  cd config/
  562  ll
  563  vim server.properties
  564  cd ..
  565  rm -rf kafka-logs/
  566  ll
  567  cat start.sh
  568  cd bin/
  569  ll
  570  ./kafka-server-start.sh ../config/server.properties &
  571  java --version
  572  java -version
  573  cd /usr/local/
  574  mkdir jdk
  575  ll
  576  cd jdk/
  577  mv /home/sudoroot/jdk-8u181-linux-x64.tar.gz  .
  578  ll
  579  tar -zxvf jdk-8u181-linux-x64.tar.gz
  580  ll
  581  rm -rf jdk-8u181-linux-x64.tar.gz
  582  ll
  583  vim /etc/profile
  584  source /etc/profile
  585  java -version
  586  cd /home/sudoroot/
  587  ll
  588  rm -rf kafka_2.11-0.11.0.0.tar.gz
  589  ll
  590  cd /opt/docker/common/
  591  cd kafka/
  592  ps -ef | grep kafka
  593  cd kafka_2.11-0.11.0.0/bin/
  594  ./kafka-server-start.sh ../config/server.properties &
  595  cd ../
  596  cd ..
  597  cd zookeeper-3.4.10/
  598  ll
  599  cd bin/
  600  sh zkServer.sh start
  601  ps -ef | grep zookeeper
  602  cd ../../kafka_2.11-0.11.0.0/bin/
  603  ./kafka-server-start.sh ../config/server.properties &
  604  ps -ef | grep kafka
  605  docker ps
  606  docker logs bcfff
  607  docker logs -f --tail 200 bcfff
  608  pwd
  609  cd ../..
  610  ll
  611  rm -rf zookeeper-3.4.10.tar.gz
  612  ll
  613  docker ps
  614  docker exec -it bcfff /bin/bash
  615  docker ps
  616  docker logs -f --tail 200 3c6d1
  617  docker logs -f --tail 200 switchmanage-service-p1
  618  docker logs -f --tail 200 ftpproxy-service-p1
  619  docker ps
  620  docker restart binterface-service-server-p1
  621  docker logs -f --tail 200 binterface-service-server-p1
  622  docker logs -f --tail 200 binterface-service-client-p1
  623  docker restart binterface-service-client-p1
  624  docker logs -f --tail 200 binterface-service-client-p1
  625  docker logs -f --tail 200 binterface-service-server-p1
  626  docker logs -f --tail 200 binterface-service-client-p1
  627  docker logs -f --tail 200 binterface-service-data-p1
  628  docker restart binterface-service-data-p1
  629  docker logs -f --tail 200 binterface-service-data-p1
  630  docker logs -f --tail 200 ftpproxy-service-p1
  631  docker restart ftpproxy-service-p1
  632  docker logs -f --tail 200 ftpproxy-service-p1
  633  docker logs -f --tail 200 switchmanage-service-p1
  634  docker stop switchmanage-service-p1
  635  docker ps
  636  docker logs -f --tail 200 bcfff
  637  docker ps
  638  docker logs -f --tail 200 4fa9c
  639  docker ps
  640  docker logs -f --tail 200 3c6d
  641  docker logs -f --tail 200 bcfff
  642  vim /etc/profile
  643  docker logs -f --tail 200 bcfff
  644  docker ps
  645  docker logs -f -tail 200 3c6d1
  646  docker logs -f --tail 200 3c6d1
  647  docker ps
  648  docker logs -f --tail 200 4fa9c
  649  docker ps
  650  ps -ef|grep swich
  651  docker logs -f --tail 200 binterface-service-server-p1
  652  docker ps
  653  docker inspect bcfff82185a4
  654  docker ps
  655  ps -ef | grep kafka
  656  docker ps
  657  docker logs -f --tail 200 bcff
  658  docker ps
  659  yum
  660  yum -y install gcc pcre-devel zlib-devel openssl openssl-devel
  661  mv /home/sudoroot/nginx-1.21.6.tar.gz /usr/local/
  662  cd /usr/local/
  663  tar -zxvf nginx-1.21.6.tar.gz -C /usr/local/nginx
  664  mkdir nginx
  665  ll
  666  tar -zxvf nginx-1.21.6.tar.gz -C /usr/local/nginx
  667  cd /usr/local/nginx/nginx-1.21.6
  668  ./configure --prefix=/usr/local/nginx
  669  make && make install
  670  cd /usr/local/nginx/sbin
  671  ./nginx -v
  672  ps -ef | grep nginx
  673  ./nginx
  674  vim ../conf/nginx.conf
  675  cd ../conf/
  676  ll
  677  cp nginx.conf /home/sudoroot/
  678  rm -rf /home/sudoroot/nginx.conf
  679  ll
  680  mv /home/sudoroot/nginx.conf .
  681  ll
  682  cd ../sbin/
  683  ./nginx -s reload
  684  docker ps
  685  docker logs -f --tail 200 bcff
  686  docker ps
  687  docker logs -f --tail 200 3c6d
  688  docker ps
  689  docker logs -f --tail 200 4fa9
  690  ls
  691  docker ps
  692  history
  693  docker ps -a
  694  docker ps
  695  history
  696  ps -ef |grep kafka
  697  pwdx 58512
  698  pwdx 60071
  699  cd /opt/docker/common/kafka/zookeeper-3.4.10/bin
  700  ls
  701  ps -ef | grep nginx
  702  netstat -ntlp | grep 24642
  703  netstat -ntlp | 2
  704  netstat -ntlp | grep 20614
  705  docker ps
  706  docker logs -f --tail 200 bcff
  707  docker ps
  708  docker stop ba29599bbf76
  709  docker stop 3c6d152306bb
  710  docker start ba29599bbf76
  711  docker rm 3c6d152306bb
  712  docker stop bcfff82185a4
  713  docker rm bcfff82185a4
  714  docker stop 4fa9c203e352
  715  docker rm 4fa9c203e352
  716  docker ps
  717  docker run --name binterface-service-server-p1 --net host --log-driver=json-file --log-opt max-size=30m --log-opt max-file=3 --env ENV_NACOS=10.1.203.120:8848 --env ENV_TYPE=gdems-dev  --env ENV_APP_NAME=sc-binterface-p1 --env ENV_NACOS_PASSWORD='D&V2HR43TutFjf%aKqk'  --env RUN_MODE=server --env SERVER_PORT=18083 --env APPLICATION_NAME=binterface-service-server-p1 -v /tmp/logs/binterface-service-server:/opt/data/logs/ -d 10.1.6.34:8080/cicd-public-49/binterface-service:1.0.3.2_48_20250910075431
  718  docker run --name binterface-service-client-p1 --net host --log-driver=json-file --log-opt max-size=30m --log-opt max-file=3 --env ENV_NACOS=10.1.203.120:8848 --env ENV_TYPE=gdems-dev  --env ENV_APP_NAME=sc-binterface-p1  --env ENV_NACOS_PASSWORD='D&V2HR43TutFjf%aKqk'  --env RUN_MODE=client  --env SERVER_PORT=18081 --env APPLICATION_NAME=binterface-service-client-p1 -v /tmp/logs/binterface-service-client:/opt/data/logs/ -d 10.1.6.34:8080/cicd-public-49/binterface-service:1.0.3.2_48_20250910075431
  719  docker run --name binterface-service-data-p1 --net host --log-driver=json-file --log-opt max-size=30m --log-opt max-file=3 --env ENV_NACOS=10.1.203.120:8848 --env ENV_TYPE=gdems-dev  --env ENV_APP_NAME=sc-binterface-p1  --env ENV_NACOS_PASSWORD='D&V2HR43TutFjf%aKqk'  --env RUN_MODE=dataHandle --env SERVER_PORT=18085 --env APPLICATION_NAME=binterface-service-data-p1 -v /tmp/logs/binterface-service-data:/opt/data/logs/ -d 10.1.6.34:8080/cicd-public-49/binterface-service:1.0.3.2_48_20250910075431
  720  docker ps
  721  docker logs -f --tail 200 4f7d
  722  ll
  723  docker ps
  724  docker logs -f --tail 400 binterface-service-client-p1
  725  docker logs -f --tail 400 binterface-service-client-p1 | grep 20250912100455
  726  docker ps
  727  docker logs -f --tail 400 ftpproxy-service-p1
  728  docker ps
  729  docker logs -f --tail 400 binterface-service-server-p1
  730  docker ps
  731  docker logs -f --tail 400 binterface-service-client-p1
  732  ll
  733  lsof -i:8011
  734  docker ps
  735  docker logs -f --tail 200 3823
  736  docker logs -f --tail 200 3823 | grep 10.1.4.194
  737  docker logs  3823 | grep 10.1.4.194
  738  docker logs -f --tail 200 3823
  739  docker logs  3823 | grep 10.1.4.194
  740  docker ps
  741  docker logs  74ae | grep 10.1.4.194
  742  docker logs -f --tail 200 74ae
  743  docker logs 74ae | grep 20250912162755
  744  docker logs 74ae | grep 20250912175656
  745  docker ps
  746  docker logs -f --tail 200 4f7d
  747  docker ps
  748  docker rm -f 35fa
  749  docker rm -f 3823
  750  docker rm -f 4f7d
  751  docker ps
  752  docker run --name binterface-service-server --net host --log-driver=json-file --log-opt max-size=30m --log-opt max-file=3 --env ENV_NACOS=10.1.203.120:8848 --env ENV_TYPE=gdems-dev  --env ENV_APP_NAME=gdems-binterface --env ENV_NACOS_PASSWORD='D&V2HR43TutFjf%aKqk'  --env RUN_MODE=server --env SERVER_PORT=18083 --env APPLICATION_NAME=binterface-service-server -v /tmp/logs/binterface-service-server:/opt/data/logs/ -d 10.1.6.34:8080/cicd-public-49/binterface-service:1.0.3.2_48_20250910075431
  753  docker run --name binterface-service --net host --log-driver=json-file --log-opt max-size=30m --log-opt max-file=3 --env ENV_NACOS=10.1.203.120:8848 --env ENV_TYPE=gdems-dev  --env ENV_APP_NAME=gdems-binterface  --env ENV_NACOS_PASSWORD='D&V2HR43TutFjf%aKqk'  --env RUN_MODE=client  --env SERVER_PORT=18081 --env APPLICATION_NAME=binterface-service -v /tmp/logs/binterface-service-client:/opt/data/logs/ -d 10.1.6.34:8080/cicd-public-49/binterface-service:1.0.3.2_48_20250910075431
  754  docker run --name binterface-service-data --net host --log-driver=json-file --log-opt max-size=30m --log-opt max-file=3 --env ENV_NACOS=10.1.203.120:8848 --env ENV_TYPE=gdems-dev  --env ENV_APP_NAME=gdems-binterface  --env ENV_NACOS_PASSWORD='D&V2HR43TutFjf%aKqk'  --env RUN_MODE=dataHandle --env SERVER_PORT=18085 --env APPLICATION_NAME=binterface-service-data -v /tmp/logs/binterface-service-data:/opt/data/logs/ -d 10.1.6.34:8080/cicd-public-49/binterface-service:1.0.3.2_48_20250910075431
  755  docker ps
  756  docker logs -f --tail 200 5dcd
  757  ps -ef | grep kafka
  758  docker logs -f --tail 200 5dcd
  759  docker ps
  760  docker restart ba29
  761  docker restart 5dcd
  762  docker restart 74ae
  763  docker restart 241d
  764  docker ps
  765  docker logs -f --tail 200 5dcd
  766  telnet 10.1.5.109 9092
  767  ping 10.1.5.109 9092
  768  ping 10.1.5.109
  769  vim /etc/sysconfig/iptables
  770  telnet 10.1.5.109 9092
  771  docker logs -f --tail 200 5dcd
  772  docker ps
  773  docker logs -f --tail 200 ba29
  774  docker logs ba29 | grep 00001006000000167191
  775  docker logs -f --tail 200 ba29
  776  docker logs ba29 | grep 10.1.4.194
  777  docker ps
  778  docker inspect bcfff82185a4
  779  docker logs -f --tail 2000 ba29599bbf7
  780  clear
  781  ls
  782  docker ps
  783  docker ps -a
  784  docker ps -a|grep bin
  785  clear
  786  dokcer ps |grep bin
  787  docker ps |grep bin
  788  docker logs -f --tail 300 4f7d79419fb1
  789  docker ps
  790  docker logs -f --tail 200 binterface-service-client-p1
  791  docker logs -f --tail 200 binterface-service
  792  docker ps
  793  docker logs -f --tail 200 35fa08a765f3
  794  docker ps
  795  docker inspect 35fa08a765f3
  796  docker ps
  797  docker logs 5dcd | grep "<Name>LOGIN</Name>"
  798  docker logs 5dcd | grep "<Name>SEND_DEV_CONF_DATA</Name>"
  799  docker logs 5dcd | grep "<Name>SEND_ALARM</Name>"
  800  docker logs -f --tail 200 5dcd
  801  docker logs 5dcd | grep "<Name>SEND_DEV_CONF_DATA</Name>"
  802  docker logs -f --tail 200 5dcd
  803  ps -ef
  804  ps -ef | grep kafka
  805  kill -9 60071
  806  kill -9 58512
  807  ps -ef | grep kafka
  808  docker ps
  809  top | grep nginx
  810  ps -ef | grep nginx
  811  free -m
  812  top
  813  ps -ef | grep kube
  814  cat /etc/docker/daemon.json
  815  tar -zcvf /home/sudoroot/kafka.tar.gz /opt/docker/common/
  816  scp /home/sudoroot/kafka.tar.gz sudoroot@10.1.4.194:/opt/docker
  817  scp /home/sudoroot/kafka.tar.gz sudoroot@10.1.4.194:/home/sudoroot
  818  telnet 10.1.4.194 9092
  819  docker ps
  820  docker restart binterface-service-server
  821  docker restart binterface-service
  822  docker restart binterface-service-data
  823  docker restart ftpproxy-service-p1
  824  docker logs -f --tail 200 binterface-service-server
  825  docker ps
  826  docker restart binterface-service-server
  827  docker restart binterface-service
  828  docker restart binterface-service-data
  829  docker restart ftpproxy-service-p1
  830  docker logs -f --tail 200 binterface-service-server
  831  docker logs binterface-service-server | grep SEND_ALARM
  832  docker logs -f --tail 200 binterface-service-server
  833  docker logs binterface-service-server | grep SEND_ALARM
  834  docker logs binterface-service-server | grep ALARM
  835  docker logs -f --tail 200 binterface-service-server
  836  docker logs binterface-service-server | grep "SEND_DEV_CONF_DATA"
  837  docker logs binterface-service-server | grep "<Name>SEND_DEV_CONF_DATA</Name>"
  838    </PK_Type>
  839    <Info>
  840  docker logs binterface-service-server | grep "<Name>SEND_DEV_CONF_DATA</Name></PK_Type><Info><FSUID>20250912175656</FSUID>"
  841  clear
  842  docker logs binterface-service-server | grep "<Name>SEND_DEV_CONF_DATA</Name></PK_Type><Info><FSUID>20250912175656</FSUID>"
  843  docker logs -f --tail 200 binterface-service-server
  844  cd /home/sudoroot/
  845  ll
  846  rm -rf kafka.tar.gz
  847  date
  848  mv influxdb-1.6.3.x86_64.rpm /usr/local/
  849  mv grafana-10.3.10-1.x86_64.rpm /usr/local/
  850  cd /usr/local/
  851  ll
  852  sudo yum localinstall influxdb-1.6.3.x86_64.rpm
  853  vim /etc/influxdb/influxdb.conf
  854  systemctl start influxdb.service
  855  systemctl status influxdb.service
  856  netstat -ntl[
  857  netstat -ntlp
  858  vim /etc/influxdb/influxdb.conf
  859  netstat -ntlp | grep 2003
  860  netstat -ntlp | grep 8083
  861  netstat -ntlp | grep 8088
  862  systemctl start influxdb.service
  863  systemctl status influxdb.service
  864  netstat -ntlp | grep 8088
  865  vim /etc/influxdb/influxdb.conf
  866  cat /var/log/influxdb/influxdb.log
  867  systemctl status influxdb.service
  868  vim /etc/influxdb/influxdb.conf
  869  ps -ef | grep influxdb
  870  cd /var/lib/
  871  ll
  872  systemctl status influxdb.service
  873  journalctl -u influxdb.service
  874  systemctl start influxdb.service
  875  journalctl -u influxdb.service
  876  systemctl status influxdb.service
  877  chmod 777 -R /etc/influxdb/
  878  chmod 777 -R /var/lib/influxdb/
  879  systemctl start influxdb.service
  880  systemctl status influxdb.service
  881  vim /etc/influxdb/influxdb.conf
  882  cat /var/log/messages
  883  tail -200f /var/log/messages
  884  cat /var/log/messages | grep influxdb
  885  cat /var/log/messages | grep "Sep 17 15:55:47"
  886  cat /var/log/messages | grep "Sep 17 15:36:50"
  887  cd /usr/local/
  888  ll
  889  sudo yum localinstall grafana-10.3.10-1.x86_64.rpm
  890  systemctl start grafana-server.service
  891  systemctl staus grafana-server.service
  892  systemctl status grafana-server.service
  893  netstat -ntlp | grep 3000
  894  systemctl status firewalld
  895  vim /etc/sysconfig/iptables
  896  netstat -ntlp | grep 21726
  897  cat /etc/grafana/grafana.ini
  898  vim /etc/grafana/grafana.ini
  899  journalctl -u grafana-server
  900  systemctl status grafana-server.service
  901  sudo firewall-cmd --list-all
  902  cat /etc/grafana/grafana.ini
  903  vim /etc/grafana/grafana.ini
  904  systemctl restart grafana-server.service
  905  systemctl status grafana-server.service
  906  ps -ef | grep grafana
  907  netstat -ntlp | grep 1604
  908  netstat -ntlp | grep 16804
  909  vim /etc/grafana/grafana.ini
  910  systemctl restart grafana-server.service
  911  ps -ef | grep grafana
  912  vim /etc/grafana/grafana.ini
  913  systemctl restart grafana-server.service
  914  ll
  915  cd /home/sudoroot/
  916  ll
  917  mv prometheus-2.44.0.linux-amd64.tar.gz /usr/local/
  918  mv node_exporter-1.1.2.linux-amd64.tar.gz /usr/local/
  919  cd /usr/local/
  920  ll
  921  tar -zxvf prometheus-2.44.0.linux-amd64.tar.gz
  922  ll
  923  mv prometheus-2.44.0.linux-amd64 prometheus
  924  ll
  925  cd /usr/lib/systemd/system
  926  ll
  927  vi prometheus.service
  928  systemctl daemon-reload
  929  systemctl start prometheus
  930  cd /usr/local/
  931  ll
  932  rm -rf nginx-1.21.6.tar.gz
  933  rm -rf grafana-10.3.10-1.x86_64.rpm
  934  rm -rf prometheus-2.44.0.linux-amd64.tar.gz
  935  tar -zxvf node_exporter-1.1.2.linux-amd64.tar.gz
  936  ll
  937  mv node_exporter-1.1.2.linux-amd64 node_exporter
  938  ll
  939  rm -rf node_exporter-1.1.2.linux-amd64.tar.gz
  940  vi /usr/lib/systemd/system/node_exporter.service
  941  systemctl daemon-reload
  942  systemctl start node_exporter
  943  cd prometheus/
  944  ll
  945  vim prometheus.yml
  946  systemctl restart prometheus.service
  947  ls
  948  cd /
  949  ls
  950  ls usr
  951  ls etc
  952  ls /etc/nginx
  953  ls
  954  ls /etc/nginx/mine_mailcap.types
  955  cd ..
  956  ls
  957  ls sys
  958  ls /sys/kernel
  959  ps -ef|grep nginx
  960  pwdx 24642
  961  cd /usr/local/nginx/sbin
  962  ls
  963  cd nginx
  964  cat nginx
  965  ls
  966  cd ..
  967  ls
  968  cd conf
  969  ls
  970  cat ngxin.conf
  971  cat nginx.conf
  972  ls
  973  cd ..
  974  ls
  975  ps -ef
  976  docker ps
  977  ps -ef | grep kafka
  978  ps -ef | grep zookee
  979  free -m
  980  top
  981  ps -ef | grep kube
  982  top
  983  ps -ef | grep kube
  984  kill -9 982
  985  kill -9 1049
  986  kill -9 4000
  987  kill -9 7167
  988  ps -ef | grep kube
  989  top
  990  dockr logs -f --tail 200 binterface-service-server
  991  docker logs -f --tail 200 binterface-service-server
  992  docker logs binterface-service-server | grep "不存在的FSU"
  993  docker logs binterface-service-server | grep "20250901000"
  994  docker logs binterface-service-server | grep "20250900000"
  995  docker logs binterface-service-server | grep "20250912175656"
  996  docker ps
  997  docker logs binterface-service-server | grep "20250912175656"
  998  docker logs binterface-service-server | grep "20250905000"
  999  docker logs binterface-service-server | grep "响应"
 1000  docker logs -f --tail 200 binterface-service-server
