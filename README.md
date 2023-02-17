

# 🌲 foREST 🌲


**foREST** is a stateful REST API fuzzy testing tool based on [OpenAPI](https://www.openapis.org/) documentation for automatically testing cloud services via REST API and finding security and reliability errors in those services. 

**foREST** analyzes OpenAPI documentation and then generates and executes test cases to test that cloud service.



## foREST Structure

**foREST** will automatically infer the producer-consumer relationship between cloud service APIs based on OpenAPI documentation, build a dependency tree, and generate test cases that satisfy the dependency relationship based on the dependency tree. This approach enables **foREST** to generate test cases intelligently, improve the efficiency of test case generation, and find more errors.

foREST code is generally divided into three parts:

* [document parsing](https://github.com/Artisan-Lab/foREST/tree/master/module/parser)

* [dependency analysis](https://github.com/Artisan-Lab/foREST/tree/master/module/parser)

* [testing execution](https://github.com/Artisan-Lab/foREST/tree/master/module/testing)

![framework—eng](https://user-images.githubusercontent.com/71680354/195775847-b46a11cd-2188-41b7-87ce-1c28b3819964.png)


## Getting started

1. Store the yaml document of the service to be tested in the openapi folder

2. Configure in the FoREST_config according to actual needs

3. Install the dependencies required to run foREST
```bash
pip3 install -r requirements.txt
```
4. run
```bash
python3 main.py
```

 ## experiment

The specific experimental procedure can be found in [experiment](https://github.com/Artisan-Lab/foREST/tree/master/experiment)


 
### BUG found

#### simple introduction of bugs
We roughly divide the bugs we find into three categories

| id | classification                    | Server    | Endpoint                                                                | Method             | issue                                                         |
|----|-----------------------------------|-----------|-------------------------------------------------------------------------|--------------------|---|
| [1](#1)  | Logical: use after delete                  | GitLab    | /users/{id}/custom_attributes /users/{id}/custom_attributes/{key}       | GET GET/PUT/DELETE | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/335276) |
| [2](#2)  | Logical: use after delete                  | GitLab    | /projects/{id}/custom_attributes /projects/{id}/custom_attributes/{key} | GET GET/PUT/DELETE | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/335276) |
| [3](#3)  | Logical: use after delete                  | GitLab    | /groups/{id}/custom_attributes /groups/{id}/custom_attributes/{key}     | GET GET/PUT/DELETE | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/335276) |
| [4](#4) | Logical: double delete | GitLab    | /projects/{id}/services/github                                          | DELETE             | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/360147) |
| [5](#5) | invalid parameter: UTF-8                | GitLab    | /hooks                                                                  | POST               | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/334606) |
| [6](#6) | invalid parameter: UTF-8                 | GitLab    | /projects/{id}/metrics/user_starred_dashboards                          | POST               | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/334606) |
| [7](#7) | invalid parameter: UTF-8                 | GitLab    | /admin/cluster/add                                                      | POST               | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/346121) |
| [8](#8) | invalid parameter: UTF-8                | GitLab    | /projects/{id}/cluster/user                                             | POST               | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/346121) |
| [9](#9) | invalid parameter: UTF-8                | GitLab    | /groups/{id}/cluster/user                                               | POST               | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/346121) |
| [10](#10) | invalid parameter: UTF-8                 | GitLab    | /projects/{id}/export                                                   | POST               | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/346121) |
| [11](#11) | invalid parameter: special characters                 | GitLab    | /projects/{project_id}/variables/{key}                                  | POST               | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/360662) |
| [12](#12) | invalid parameter: enum type with bad value              | GitLab    | /projects/{id}/environments                                             | GET                | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/360138) |
| [13](#13) | invalid parameter: long str with special char  | GitLab    | /projects/{id}/repository/commits                                       | GET                | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/356922) |
| [14](#14) | invalid parameter: special characters       | GitLab    | /projects/{id}/repository/commits                                       | POST               | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/360312) |
| [15](#15) | logical: false logic                        | GitLab    | /projects/{id}/repository/branches.                                     | POST               | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/360313) |
| [16](#16) | logical: reference loop                        | GitLab    | /projects/{id}/fork/{forked_from_id}                                    | POST               | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/346563) |
| [17](#17) | unsuported function                   | GitLab    | /projects                                                               | POST               | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/356921) |
| [18](#18) | unsuported function                  | WordPress | /categories/{id}                                                        | DELETE             | email reported                                                   |
| [19](#19) | unsuported function                  | WordPress | /tags/{id}                                                              | DELETE             | email reported                                                  |
| [20](#20) | logical: duplicated id                        | WordPress | /users                                                                  | DELETE             | email   reported                                                |


#### Steps to reproduce bugs
We show the reproduction of some of the bugs, more detailed description and reproduction of the bugs can be viewed in the issue

<span id="1">**1. GET /users/{id}/custom_attributes** </span>

**GET/DELETE/PUT /users/{id}/custom_attributes/{key}**
1. create a user
```
Sending: POST server_host/api/v4/users?user_name=a
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}      
Received: 'HTTP/1.1 201 response:{"user_id":2}
```
2. delete the user
```
Sending: DELETE server_host/api/v4/users
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}      
Received: 'HTTP/1.1 202 response:{"message":"success"}
```
3. get the user's custom attributes
```
Sending: GET server_host/api/v4/users/{id}/custom_attributes 
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
Received: 'HTTP/1.1 500 response : {"message":"500 Internal Server Error"} 
```


<span id="2">**2. GET /projects/{id}/custom_attributes**</span>

**GET/DELETE/PUT /projects/{id}/custom_attributes/{key}**
similary with **GET /users/{id}/custom_attributes**



<span id="3">**3. GET /groups/{id}/custom_attributes**</span>

**GET/DELETE/PUT /group/{id}/custom_attributes/{key}**
similary with **GET /users/{id}/custom_attributes**




<span id="4">**4.DELETE /projects/{id}/services/github**</span>
1. create a project 
```
Sending: POST server_host/api/v4/projects?name=A
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
Received: 'HTTP/1.1 201 response : {"project_id": 2}
```
2. delete the project's "github" services
```
Sending: DELETE server_host/api/v4/projects/2/services/github
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
Received: 'HTTP/1.1 500 response : {"message":"500 Internal Server Error"} 
```


<span id="5">**5. POST /hooks**</span>
create a hook with invalid "url" (UTF-8)
```
Sending: POST server_host/api/v4/hooks  
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
data: {"url": "%e5"} 
Received: 'HTTP/1.1 500 response : {"message":"500 Internal Server Error"} 
```

<span id="6">**6. POST /projects/{id}/metrics/user_starred_dashboards**</span>

1. create a project A
```
Sending: POST server_host/api/v4/projects?name=A
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
Received: 'HTTP/1.1 201 response : {"project_id": 2}
```
2. create a user starred dashboards with invalid "dashboard_path" (utf-8)
```
Sending: POST server_host/api/v4/projects/2/metrics/user_starred_dashboards
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
data:  {"dashboard_path": "%e6%99%ba%e8%83%bd%e5"}
Received: 'HTTP/1.1 500 response : {"message":"500 Internal Server Error"} 
```

<span id="7">**7. POST /admin/cluster/add**</span>

create a cluster with invalid "platform_kubernetes_attributes\[api_url\]"(UTF-8)

```
Sending: POST server_host/api/v4/admin/cluster/add
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
data:  {"platform_kubernetes_attributes": "%e5"}
Received: 'HTTP/1.1 500 response : {"message":"500 Internal Server Error"} 
```

<span id="8">**8. POST /projects/{id}/cluster/user**</span>
1. create a project
```
Sending: POST server_host/api/v4/projects?name=A
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
Received: 'HTTP/1.1 201 response : {"project_id": 2}
```
2. create a cluster for a project  with invalid "platform_kubernetes_attributes\[api_url\]"(UTF-8)
```
Sending: POST server_host/api/v4/projects/cluster/user
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
data:  {"platform_kubernetes_attributes": "%e5"}
Received: 'HTTP/1.1 500 response : {"message":"500 Internal Server Error"} 
```

<span id="9">**9. POST /groups/{id}/cluster/user**</span>
similary with  **8. POST /projects/{id}/cluster/user**

<span id="10">**10. POST /projects/{id}/export**</span>

similary with  **8. POST /projects/{id}/cluster/user**

<span id="11">**11. GET /projects/{id}/variables/{key}**</span>

1. create a project
```
Sending: POST server_host/api/v4/projects?name=A
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}    
Received: 'HTTP/1.1 201 response : {"project_id": 2}
```
2. get a project variables with a invalid "filter"(special characters)
```
Sending: GET server_host/api/v4/projects/2/variables/fuzzstring?fileter=1'
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
Received: 'HTTP/1.1 500 response : {"message":"500 Internal Server Error"} 
```

<span id="12">**12. GET /projects/{id}/environments**</span>

1. create a project
```
Sending: POST server_host/api/v4/projects?name=A
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
Received: 'HTTP/1.1 201 response : {"project_id": 2}
```
2. get a project environments with a invalid "states"(not enum)
```
Sending: GET server_host/api/v4/projects/2/environments?states=a
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
Received: 'HTTP/1.1 500 response : {"message":"500 Internal Server Error"} 
```



<span id="13">**13. GET /projects/{id}/repository/commits**</span>


1. create a project 
```
Sending: POST server_host/api/v4/projects?name=A
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
Received: 'HTTP/1.1 201 response : {"project_id": 2}
```
2. get the project commits with length of parameter 'ref_name' is too long and has special characters
```
Sending: GET server_host/api/v4/projects/2/repository/commits?ref_name=email:1@gmail.com
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
Received: 'HTTP/1.1 500 response : {"message":"500 Internal Server Error"} 
```

<span id="14">**14. POST /projects/{id}/repository/commits**  </span>

1、Create a new project  
```
Sending: POST server_host/api/v4/projects?name=a
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
Received: 'HTTP/1.1 201 response : {"project_id": 2}
```
2、Create a commit for the new project with special characters ":" in the branch parameter:
```
Sending: POST server_host/api/v4/projects/{project_id}/repository/commits
header: {'Content-Type': 'application/json',
          'Authorization': 'Bearer token'}
data:{"branch": "email:",
      "commit_message": "suaxpicd7f",
      "actions": [{"action": "create",
                   "file_path": "8apwey0w5h", 
                   "execute_filemode": "False"}]}
Received: 'HTTP/1.1 500 response : {"message":"500 Internal Server Error"} 
```


<span id="15">**15. POST /projects/{id}/repository/branches**</span>

1. create a project with an invalid "import_url"  
```
Sending: POST server_host/api/v4/projects?name=a
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
data:{"import_url": "invalid import_url"}
Received: 'HTTP/1.1 201 response : {"project_id": 2}
```
2. post "main" branch in this project
```
Sending: POST server_host/api/v4/projects/{project_id}/repository/branches?branch=main&ref=main 
data:
Received: 'HTTP/1.1 500 response : {"message":"500 Internal Server Error"} 
```

<span id="16">**16.POST /projects/{id}/fork/{forked_from_id}** </span>

1. create a project A 
```
Sending: POST server_host/api/v4/projects?name=A
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
Received: 'HTTP/1.1 201 response : {"project_id": 2}
```
2. create a project B 

```
Sending: POST server_host/api/v4/projects?name=B
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
Received: 'HTTP/1.1 201 response : {"project_id": 3}
```
3. project B fork project A
```
Sending: POST server_host/api/v4/projects/2/fork/3 
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
Received: 'HTTP/1.1 201 response : {"message":"success"} 
```
4. project A fork project B  
```
Sending: POST server_host/api/v4/projects/3/fork/2
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
Received: 'HTTP/1.1 500 response : {"message":"500 Internal Server Error"} 
```


<span id="17">**17. POST /projects**</span>
create a project with the optional parameter 'use_custom_template'

```
Sending: POST server_host/api/v4/projects?name=Administrator   
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
data: {"use_custom_template": "False"}  
Received: 'HTTP/1.1 500 response : {"message":"500 Internal Server Error"} 
```
<span id="18">**18. DELETE /categories/{id}** </span>
1. create a categories
```
Sending: POST server_host/wp-json/wp/v2/categories
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
data:  {'name': 'a'}
Received: 'HTTP/1.1 201 response : {"id": 2}
```
2. delete the categories
```
Sending: DELETE server_host/wp-json/wp/v2/tags/2
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
data:  
Received: 'HTTP/1.1 501 response : {"code":"rest_trash_not_supported"} 
```
<span id="19">**19. DELETE /tags/{id}**</span>
1. create a tag
```
Sending: POST server_host/wp-json/wp/v2/tags
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
data:  {'name': 'a'}
Received: 'HTTP/1.1 201 response : {"id": 2}
```
2. delete the tag
```
Sending: DELETE server_host/wp-json/wp/v2/tags/2
header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}  
data:  
Received: 'HTTP/1.1 501 response : {"code":"rest_trash_not_supported"} 
```

<span id="20">**20. POST /users** ------ use existed user email or user name</span>
1. create a user A
```
Sending: POST /users server_host/wp-json/wp/v2/users 
API_id: 35 header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}
data: {"username": "A", "name": "jqn6eec4uz", "email": "5@BS.yoM", "password": "string", "description": "string"}
Received: 'HTTP/1.1 201 response : {"id":"1"}
```

2. create a user A again

```
Sending: POST /users server_host/wp-json/wp/v2/users 
API_id: 35 header:{'Content-Type': 'application/json', 'Authorization': 'Bearer token'}
data: {"username": "A", "name": "jqn6eec4uz", "email": "5@BS.yoM", "password": "string", "description": "string"}
Received: 'HTTP/1.1 500 response : {"code":"existing_user_login"}
```
 

