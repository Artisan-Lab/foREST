## A bug that can be reproduced at gitlab.com

2022-04-21 15:18:26,335 : Sending: GET /projects/{id}/environments http://192.168.112.198/api/v4/projects/12/environments?states=scheduled 
API_id: 188 header:{'Content-Type': 'application/json', 'Authorization': 'Bearer 2eJ7eBp7_3UgFU7mLpwK'}
data: 
Received: 'HTTP/1.1 500 response : {"message":"500 Internal Server Error"} 


2022-04-21 15:22:18,006 : Sending: DELETE /projects/{id}/services/github http://192.168.112.198/api/v4/projects/29/services/github 
API_id: 287 header:{'Content-Type': 'application/json', 'Authorization': 'Bearer 2eJ7eBp7_3UgFU7mLpwK'}
data: 
Received: 'HTTP/1.1 500 response : {"message":"500 Internal Server Error"} 

