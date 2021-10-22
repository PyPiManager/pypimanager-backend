# pypimanager-backend

## 部署方式

###　方式一：构建应用镜像

#### 优点

直接编写到docker-compose里即可，无需再进入容器操作设置程序守护

#### 缺点

不好更新维护代码

#### 方式

```
docker build . -t pypimanager_backend:2.0.0
```

### 方式二：使用基础镜像，外挂代码

#### 优点

代码通过数据卷映射到容器内部，便于维护更新代码

#### 缺点

需要使用容器内部的systemd系统服务队程序进行守护

#### 方式

1. 下载镜像
```
docker pull python:3.7.9-buster
```
2. 启动容器
```
docker run --name py3.7.9env --rm -it python:3.7.9-buster /bin/bash

root@026d2ce545bd:/# python -V
Python 3.7.9
root@026d2ce545bd:/# pip -V
pip 21.2.4 from /usr/local/lib/python3.7/site-packages/pip (python 3.7)
```
3. 配置apt源并更新
拷贝容器内部的apt源到宿主机
```
docker cp py3.7.9env:/etc/apt/sources.list .
```
编辑`sources.list`，更换为163的源
```
# deb http://snapshot.debian.org/archive/debian/20211011T000000Z buster main
deb http://mirrors.163.com/debian buster main
# deb http://snapshot.debian.org/archive/debian-security/20211011T000000Z buster/updates main
deb http://mirrors.163.com/debian-security buster/updates main
# deb http://snapshot.debian.org/archive/debian/20211011T000000Z buster-updates main
deb http://mirrors.163.com/debian buster-updates main
```
编辑完成后拷贝回容器内部
```
docker cp sources.list py3.7.9env:/etc/apt/sources.list
```
更新源
```
apt update
```

4. 安装常用服务
   1. 安装vim
   ```
   apt intall vim
   ```
   2. 安装sshd并配置
   安装
   ```
   apt install openssh-server
   ```
   配置`/etc/ssh/sshd_config`
   ```
   PasswordAuthentication yes
   PermitRootLogin yes
   ```
   启动
   ```
   root@026d2ce545bd:/etc/apt# service ssh start
   [ ok ] Starting OpenBSD Secure Shell server: sshd.
   root@026d2ce545bd:/etc/apt# service ssh status
   [ ok ] sshd is running.
   ```
5. 修改密码为123456
```
root@026d2ce545bd:/etc/apt# passwd 
New password: 
Retype new password: 
passwd: password updated successfully
```
6. 保存定制好的镜像，在docker-compose使用
```
docker commit 026d2ce545bd toddlerya/py_env:3.7.9-buster
```