## 依赖分析

foREST将API的依赖分为两部分：路径依赖与参数依赖，这也是foREST与其他测试工具相比最大的优势所在。更为细化的依赖关系划分使得foREST在生成测试用例时有着更出色的表现。

foREST的依赖分析是基于API文档的，支持swagger2.0与openAPI3.0规范，解析后会将API信息完全存储在api_lIst中，便于后续生成测试用例。

open_api_parse 将会读取api文档并生成api_list，api_list由[api_info](https://github.com/Artisan-Lab/Restful-api-testing/blob/master/entity/api_info.py)组成

