from module.data_analysis.logpool import *

result = {}


def api_dependency(max_sequence_length: int):
    global result
    for user in log_pool.user_dict:
        identifier_list = [log.identifier for log in log_pool.user_dict[user]]
        for i in range(len(identifier_list)):
            dfs(identifier_list, i, result, [], max_sequence_length)
    return result


def dfs(nums, index, res, path, max_sequence_length):
    if len(path) > 1:
        for i in range(max_sequence_length):
            if i == len(path):
                if i not in result:
                    result[i] = {}
                save_path = " ".join(path)
                if save_path in res[i]:
                    res[i][save_path] += 1
                else:
                    res[i][save_path] = 1
    if index >= len(nums) or nums[index] in path or len(path) >= max_sequence_length:
        return
    dfs(nums, index + 1, res, path + [nums[index]], max_sequence_length)


