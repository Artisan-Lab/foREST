s = 'comment=this+is+a+comment&author=chenyang&email=990776253%40qq.com&url=fudan&submit=Post+Comment&comment_post_ID=5&comment_parent=0'
output = {x[0]: x[1] for x in [x.split("=") for x in s.split("&")]}
print(output)
