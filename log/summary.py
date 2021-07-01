
def pre_summary(flag):
    if not flag.scard('over'):
        flag.sadd('over', 0)
    if not flag.scard('total_requests'):
        flag.sadd('total_requests', 0)
    if not flag.scard('success_requests'):
        flag.sadd('success_resquest', 0)
    if not flag.scard('bug_number'):
        flag.sadd('bug_number', 0)
    if not flag.scard('visited_list'):
        flag.sadd('visited_list', str([]))
