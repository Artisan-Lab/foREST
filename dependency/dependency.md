## 依赖分析

foREST将API的依赖分为两部分：路径依赖与参数依赖，这也是foREST与其他测试工具相比最大的优势所在。更为细化的依赖关系划分使得foREST在生成测试用例时有着更出色的表现。

foREST的依赖分析是基于API文档的，支持swagger2.0与openAPI3.0规范，解析后会将API信息完全存储在api_lIst中，便于后续生成测试用例。

open_api_parse 将会读取api文档并生成api_list，api_list由[api_info](https://github.com/Artisan-Lab/Restful-api-testing/blob/master/entity/api_info.py)组成。其中，field_info中的depend_list字段将会记录参数依赖信息。

### 路径依赖
路径依赖利用的RESTful API以资源为核心的概念，结合RESTful API的资源从属关系，生成了依赖树。在后续测试中，将采用BFS遍历依赖树的方式，提高生成测试用例的效率。下图是gitlab中projects API的依赖树的部分展示。

![image](https://user-images.githubusercontent.com/71680354/142836790-1a47d80e-db5b-4cce-9041-31147213438e.png)


### 参数依赖

参数依赖指的是其他API的返回值中包含了该API所需的值，在获取参数依赖关系时，foREST采用贪心匹配的原则，防止遗漏依赖关系，如下图所示，id与右侧所有参数都能匹配上。

![image](https://user-images.githubusercontent.com/71680354/142836297-be8afa2e-9627-45f2-9a80-e216bdae0370.png)

此时得到的依赖关系是冗余的，将在后续测试时进行校验。


foREST对参数依赖又进行了细分，分为直接引用与格式引用。直接引用：直接将响应中的参数值作为请求中的参数值；格式引用：保留参数的格式不变，将参数值进行[mutation](https://github.com/Artisan-Lab/Restful-api-testing/blob/ba2bc86d21707e7e0eaa4288f32a5b8f164fa28e/module/basic_fuzz.py#L42)。

