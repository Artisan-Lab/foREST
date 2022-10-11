

# foREST


foREST is a stateful REST API fuzzy testing tool based on OpenAPI documentation for automatically testing cloud services via REST API and finding security and reliability errors in those services. foREST analyzes OpenAPI documentation and then generates and executes test cases to test that cloud service.

foREST will automatically infer the producer-consumer relationship between cloud service APIs based on OpenAPI documentation, build a dependency tree, and generate test cases that satisfy the dependency relationship based on the dependency tree. This approach enables foREST to generate test cases intelligently, improve the efficiency of test case generation, and find more errors.


## foREST Structure

foREST code is generally divided into two parts:[dependency analysis](https://github.com/Artisan-Lab/Restful-api-testing/blob/FoREST_copy/dependency/dependency.md) and  [testing execution](https://github.com/Artisan-Lab/Restful-api-testing/blob/FoREST_copy/testing_render/testing.md) 。



## how to run 



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

The specific experimental procedure can be found in [experiment](https://github.com/Artisan-Lab/Restful-api-testing/blob/FoREST_copy/experiment.md)


 
## BUG

| Date | Project | Link | Finder | Status | Description |
|---------|---------|---------|---------|---------|---------|
| 2021-7-4 | GitLab | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/334606) |  | submitted | POST  /hooks |
| 2021-7-4 | GitLab | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/346121) |  | submitted | POST  /admin/clusters/add |
| 2021-7-4 | GitLab | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/334610) |  | submitted | POST  /clusters/{id}/metrics_dashboard/annotations/ |
| 2021-7-4 | GitLab | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/335276) |  | submitted | DELETE/PUT/GET  /users/{id}/custom_attributes/{key} |
| 2021-7-4 | GitLab | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/335276) |  | submitted | GET  /users/{id}/custom_attributes |
| 2021-7-4 | GitLab | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/334610) |  | submitted | POST  /projects/{id}/clusters/user |
| 2021-7-4 | GitLab | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/334606) |  | submitted | POST  /projects/{id}/metrics/user_starred_dashboards |
| 2021-7-4 | GitLab | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/335276) |  | submitted | DELETE/POST  /projects/{id}/custom_attributes/{key} |
| 2021-7-4 | GitLab | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/334610) |  | submitted | POST  /projects/{id}/export | 
| 2021-7-4 | GitLab | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/335276) |  | submitted | GET  /projects/{id}/custom_attributes |
| 2021-7-4 | GitLab | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/334610) |  | submitted | POST  /groups/{id}/clusters/user |
| 2021-7-4 | GitLab | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/335276) |  | submitted | GET /groups/{id}/custom_attributes |
| 2021-7-4 | GitLab | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/335276) |  | submitted | DELETE/PUT/GET  /groups/{id}/custom_attributes/{key} |
| 2021-7-4 | WordPress |  |  | unsubmitted | POST  /categories |
| 2021-11-4| Gitlab | [issue](https://gitlab.com/gitlab-org/gitlab/-/issues/346563) |  | submitted | POST projects/{id}/fork/forked_from_id |


 

