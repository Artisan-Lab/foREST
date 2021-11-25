# 实验设置

## GitLab

GitLab运行的最低要求是4核8G，请确保机器能满足条件

GitLab覆盖率工具与GitLab集成在docker中，具体使用方法：


### 安装方法

1、安装docker

Ubuntu:
``` bash
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```
验证是否成功安装

```bash
docker -v
```

2、创建一个文件夹用来存储所有数据、日志等

```
mkdir gitlab
export GITLAB_HOME={path to dir}/gitlab
```

3、安装GitLab
```
sudo docker run --detach \
  --hostname gitlab.example.com \
  --publish 443:443 --publish 80:80 --publish 22:22 \
  --name gitlab-api \
  --restart always \
  --volume $GITLAB_HOME/config:/etc/gitlab \
  --volume $GITLAB_HOME/logs:/var/log/gitlab \
  --volume $GITLAB_HOME/data:/var/opt/gitlab \
  witcan/gitlab-ee-api
```


安装GitLab安装后需要大约一分钟的启动时间

### 使用方法

访问http://localhost进入GitLab主界面，确认GitLab运行状态，如图所示

#### 更改root用户账号密码

1、获取docker 容器id
```
ps docker
```

2、修改GitLab root用户账号密码
```
docker exec -it <容器id> bash
```

```
gitlab-rails console
user = User.where(id:1).first
user.password = ‘password’
user.password_confirmation = 'password'
user.save!
quit
```

#### 覆盖率API接口

覆盖率工具统计的是API所能触及的代码，并不是所有代码。因此在还没执行测试用例时，覆盖率很低，因为GitLab运行时触发的API很少

1、获取覆盖率：

```
GET http://localhost/api/v4/templates/get_coverage
```

2、清空覆盖率统计：

```
POST http://localhost/api/v4/templates/reset_coverage
```