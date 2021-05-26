class save_success_case():
    def save_fuzz_success(self, matr, tag, fuzz_success_json_data, method):
        if method == 'post':
            matr.lpush('post_success!!!!!!' + tag, fuzz_success_json_data)
        if method == 'put':
            matr.lpush('put_success!!!!!!' + tag, fuzz_success_json_data)
        if method == 'patch':
            matr.lpush('patch_success!!!!!!' + tag, fuzz_success_json_data)
        if method == 'get':
            matr.lpush('get_success!!!!!!' + tag, fuzz_success_json_data)
        if method == 'delete':
            matr.lpush('delete_success!!!!!!' + tag, fuzz_success_json_data)

    def save_fuzz_optional_success(self, matr, tag, fuzz_success_json_data, method):
        if method == 'post':
            matr.lpush('post_optional_success!!!!!!' + tag, fuzz_success_json_data)
        if method == 'put':
            matr.lpush('put_optional_success!!!!!!' + tag, fuzz_success_json_data)
        if method == 'patch':
            matr.lpush('patch_optional_success!!!!!!' + tag, fuzz_success_json_data)
        if method == 'get':
            matr.lpush('get_optional_success!!!!!!' + tag, fuzz_success_json_data)
        if method == 'delete':
            matr.lpush('delete_optional_success!!!!!!' + tag, fuzz_success_json_data)