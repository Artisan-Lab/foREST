
## foREST
```
2021-12-29 02:39:21,270 : {'api number': 23, 'test rounds nember': 0, 'already send requests number': 89865, '2xx requests number': 52276, '4xx requests number': 37584, '3xx requests number': 0, '5xx requests number': 1, 'timeout requests number': 4, 'test rounds number': 500, 'already send rounds': 499}
1
API coverage(success/total): 20/23
runtime 3:55:20.238993
```
找到两个bug
POST /groups/{id}/hooks
DELETE /groups/{id}
## restler
```
Request coverage (successful / total): 1 / 23
No bugs were found.
Task Fuzz succeeded.
Collecting logs...
```

## evomaster
```
* Evaluated tests: 16301
* Evaluated actions: 89212
* Needed budget: 92%
* Passed time (seconds): 14401
* Execution time per test (ms): Avg=883.00 , min=22.00 , max=1741.00
* Computation overhead between tests (ms): Avg=0.41 , min=0.00 , max=36.00
```
GET /api/v4/groups/{id}/subgroups 同时出现这两个参数all_available、statistics
