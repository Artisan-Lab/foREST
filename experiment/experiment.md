# experiment setup

## GitLab

The minimum requirement for GitLab to run is 4 cores and 8G, so make sure your machine can meet the conditions

The GitLab coverage tool is integrated with GitLab in docker, and is used in the following way.


### setup

1、install docker

Ubuntu:
``` bash
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```
check

```bash
docker -v
```

2、Create a folder to store all data, logs, etc.

```
mkdir gitlab
export GITLAB_HOME={path to dir}/gitlab
cd {path to dir}/gitlab
```

3、install GitLab
```
sudo docker run --detach \
  --hostname gitlab.example.com \
  --publish 443:443 --publish 80:80 --publish 23:23 \
  --name gitlab-api \
  --restart always \
  --volume $GITLAB_HOME/config:/etc/gitlab \
  --volume $GITLAB_HOME/logs:/var/log/gitlab \
  --volume $GITLAB_HOME/data:/var/opt/gitlab \
  witcan/gitlab-ee-api
```


Installing GitLab takes about a minute to start after installation

### usage

Visit http://localhost to access the main GitLab interface and confirm the GitLab running status, as shown in the figure

![image](https://user-images.githubusercontent.com/71680354/143377420-13759ad8-9440-4d9e-842c-7cb9b3d2c845.png)


#### Change the password of the root user account

1、Get the docker container id
```
docker ps
```
![image](https://user-images.githubusercontent.com/71680354/143377461-387c9583-f668-4552-b793-c724cf0a536a.png)

2、Change the GitLab root user account password
```
docker exec -it <docker id> bash
```

```
gitlab-rails console
user = User.where(id:1).first
user.password = 'password'
user.password_confirmation = 'password'
user.save!
quit
```

#### Coverage API Interface

The coverage tool counts the code that the API can touch, not all of it. So coverage is low when test cases have not been executed yet, because the GitLab runtime triggers very few APIs

1、get coverage：

```
GET http://localhost/api/v4/templates/get_coverage
```
![image](https://user-images.githubusercontent.com/71680354/143377559-10a32939-cfe9-45a5-83d4-b33eb9376e9b.png)


2、reset coverage：

```
POST http://localhost/api/v4/templates/reset_coverage
```

### experiment parameter

#### [EvoMaster](https://github.com/EMResearch/EvoMaster) blackbox model

```
java -jar evomaster.jar --blackBox true --bbSwaggerUrl file:///C:/Users/42511/OneDrive/coding/Restful-api-testing/openapi/projects-api.yaml --outputFormat JAVA_JUNIT_4 --maxTime 600s --ratePerMinute 300 --bbTargetUrl http://192.168.112.162 --header0 'Authorization:Bearer qt36fUTL6m_1Y8r4iiob' --header1 'a:a' --header2 'b:b'
```

#### [RESTler](https://github.com/microsoft/restler-fuzzer)

```
./Restler.exe compile --api_spec 
```

```
./Restler.exe fuzz --grammar_file ./Compile/grammar.py --dictionary_file ./Compile//dict.json --token_refresh_interval 360000 --token_refresh_command 'python3 ../main.py' --no_ssl --time_budget 16 --settings ..\setting.json
```


