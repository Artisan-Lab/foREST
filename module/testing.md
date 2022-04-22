## foREST 测试执行

foREST在生成测试序列时，将以[BFS](https://github.com/Artisan-Lab/Restful-api-testing/blob/87a1dde3e0435057a5fce6e5bd64b5104b8d98a1/testing_render/testing.py#L64) 的方式遍历依赖树,从而尽可能地满足API之间的依赖关系。

在遍历过程中，对于同一个节点，我们将优先通过POST API来创建资源，以便进行其他操作。用GET 请求来确认服务器数据库中存储地数据信息，并与foREST资源池进行比对。

foREST在生成测试用例时，会依据 [依赖分析](https://github.com/Artisan-Lab/Restful-api-testing/blob/FoREST_copy/dependency/dependency.md) 中得到的depend_list，从资源池中获取数据。

### 遗传算法

由于依赖分析采用了贪心的原则，foREST通过 [遗传算法](https://github.com/Artisan-Lab/Restful-api-testing/blob/FoREST_copy/module/genetic_algorithm.py) 筛选参数，并且将每次测试结果都进行反馈，从而筛选掉冗余的依赖关系。该算法保证了最终得到的依赖关系是收敛的

### 资源池

foREST 在测试过程中，动态地构建了一个模拟[资源池](https://github.com/Artisan-Lab/Restful-api-testing/blob/FoREST_copy/module/redishandle.py) ，该资源池模拟服务器数据库行为，对资源进行增、删、改、查操作，从而使生成的测试用例更加接近测试人员的正常行为