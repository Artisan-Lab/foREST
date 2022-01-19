测试时间6小时，一共51个API

### foREST

成功的API数量为45个，有返回500状态码的API有6个（能成功复现的有两个）
发送的请求数量为109533，其中2xx 43882条, 4xx 64601条, 3xx 459条, 5xx 590条, 超时1条,
POST /projects  当含有可选参数use_custom_template时会引起bug，原因是这个功能仅支持付费版本
POST /projects/{id}/fork/{forked_from_id} 当一个project自己fork自己时会引起bug
POST /projects/{id}/share 无法复现
GET /projects/{id}/repository/commits 当必选参数ref中含有特殊字符:时会引起bug
POST /projects/{id}/repository/commits 当必选参数branch中含有特殊字符:时会引起bug
POST /projects/{id}/repository/branches 无法复现
### evomaster

发送的请求数量有1035877个，最后程序存储了87个case，并没有500

### restler

成功的API数量为3个，有返回500状态码的API有2个
POST /projects  当含有可选参数use_custom_template时会引起bug，原因是这个功能仅支持付费版本
POST /projects/user/{id}
发送的请求数量为375126