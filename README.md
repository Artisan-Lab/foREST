 

#  

#  

# Restful-api-testing



Restful-api-testing 是一款基于OpenAPI文档的有状态的REST API模糊测试工具，用于通过REST API自动测试云服务并查找这些服务中的安全性和可靠性错误。Restf-api-testing会分析OpenAPI文档，然后生成并执行测试用例，从而对该云服务进行测试。

Restful-api-testing会依据OpenAPI文档，自动地推断出云服务API之间的生产者-消费者关系，构建依赖矩阵，并依据依赖矩阵生成满足依赖关系的测试用例，这种方式使得Restful-api-testing能够智能地生成测试用例，提高测试用例的生成效率，并发现更多的错误。

在模糊模块，Restful-api-testing引入了metamorphic testing，metamorphic testing将自动的分析云服务API之间的metamorphic relationship（MR），并依据MR生成更多的、高效的测试用例。更重要的是，该方法拓展了更多的bug类型，能够更全面地检测云服务地安全性和可靠性！

 

# 一、代码结构


├── common　　　　　　　　　　　　　　#公共类

|　　└── common_utils.py 　　　　　　　#工具类

├── core　　　　　　　　　　　　　　　　#核心代码

|　　└── case_execution　　　　　　　　#执行测试用例

|　　　　　├── runalways.py　　　　　　#整体测试流程

|　　　　　└── test.py　　　　　　　　　#测试能不能一直跑

|　└── case_generation　　　　　　　　　 #生成测试用例

|　　　　├── delete_test.py　　　　　　　#生成delete测试用例

|　　　　├── get_test.py　　　　　　　　　#生成get测试用例

|　　　　├── patch_test.py　　　　　　　#生成patch测试用例

|　　　　├── post_test.py　　　　　　　　#生成post测试用例

|　　　　└── put_test.py　　　　　　　　#生成put测试用例

├── dependec_matrix　　　　　　　　　　#依赖矩阵模块

|　　├── dep_analysis.py　　　　　　　　#依赖分析

|　　└── graph2.py　　　　　　　　　　　#绘制依赖矩阵

├── display　　　　　　　　　　　　　　　#展示模块

|　　└── display.py　　　　　　　　　　　#展示API间依赖关系

├── entity　　　　　　　　　　　　　　　　#定义特定的数据结构

|　　├── api_info.py　　　　　　　　　　　#定义API信息存储的数据结构

|　　├── field_info.py　　　　　　　　　　#定义API参数的数据结构

|　　├── graph.py　　　　　　　　　　　#定义图结构

|　　├── link.py　　　　　　　　　　　　　#定义节点之间的线段和方向

|　　├── node.py　　　　　　　　　　　　#定义节点

|　　└── object_info.py　　　　　　　　　#定义结构体数据结构

├── metamorphic　　　　　　　　　　　　#metamorphic testing 模块

|　　├── fuzz_and_judge.py　　　　　　　#生成有效的参数

|　　├── fuzz_MR_parameter.py　　　　　#生成满足MR关系的参数

|　　├── metamorphic_compare.py　　　　#比较响应是否满足MR关系

|　　├── metamorphic_testing.py　　　　　#metamorphic testing 

|　　└── MR_testing.yml　　　　　　　　　#判断响应应该满足哪些MR关系

├── module　　　　　　　　　　　　　　　#模块

|　　├── Combination.py　　　　　　　　#组合所有optional参数

|　　├── Coverage_get_tool.py　　　　　　#获取覆盖率

|　　├── Fuzz_monitor.py　　　　　　　　#检测代码覆盖率

|　　└── kill_thread.py　　　　　　　　　#结束长期未响应进程

├── openapi　　　　　　　　　　　　　　 #openapi文档

|　　├── openapi.yaml　　　　　　　　　#gitlab-openapi

|　　├── projects-api.yaml　　　　　　　#gitlab-projects-openapi

|　　└── wordpress.yaml　　　　　　　　 #wordpress-openapi

├── parse　　　　　　　　　　　　　　　#openapi文档解析模块

|　　└── parse.py

├── tools 　　　　　　　　　　　　　　　#工具

|　　├── common.js

|　　├── display.html

|　　└── graph.js

└── README.md



# 使用说明



1.将待测服务的yaml文档存放在openapi文件夹下

2.在配置文件[test_config]中配置test_yaml文件

3.依据配置文件内容，选择测试模式

启动命令
```bash
python3 main.py
```
4.可以使用log_parse模块进行日志分析
 
# Bug
| Date | Project | Link | Finder | Status | Description |
|---------|---------|---------|---------|---------|---------|
| 2021-7-4 | GitLab |  |  | submitted | POST /hooks |
| 2021-7-4 | GitLab |  |  | submitted | POST /admin/clusters/add |
| 2021-7-4 | GitLab |  |  | submitted | POST /clusters/{id}/metrics_dashboard/annotations/ |
| 2021-7-4 | GitLab |  |  | submitted | DELETE/PUT/GET /users/{id}/custom_attributes/{key} |
| 2021-7-4 | GitLab |  |  | submitted | POST /hooks |
| 2021-7-4 | GitLab |  |  | submitted | POST /hooks |
| 2021-7-4 | GitLab |  |  | submitted | POST /hooks |
| 2021-7-4 | GitLab |  |  | submitted | POST /hooks |
| 2021-7-4 | GitLab |  |  | submitted | POST /hooks | 
| 2021-7-4 | GitLab |  |  | submitted | POST /hooks |
| 2021-7-4 | GitLab |  |  | submitted | POST /hooks |
| 2021-7-4 | GitLab |  |  | submitted | POST /hooks |
| 2021-7-4 | GitLab |  |  | submitted | POST /hooks |
