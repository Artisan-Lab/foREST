class save_success_case():
    def save_fuzz_success(self, success_pool, fuzz_success_json_data, method):
        if method == 'post':
            success_pool.lpush('post_success!!!!!!', fuzz_success_json_data)
        if method == 'put':
            success_pool.lpush('put_success!!!!!!', fuzz_success_json_data)
        if method == 'patch':
            success_pool.lpush('patch_success!!!!!!', fuzz_success_json_data)
        if method == 'get':
            success_pool.lpush('get_success!!!!!!', fuzz_success_json_data)
        if method == 'delete':
            success_pool.lpush('delete_success!!!!!!', fuzz_success_json_data)

    def save_fuzz_optional_success(self, success_pool, fuzz_success_json_data, method):
        if method == 'post':
            success_pool.lpush('post_optional_success!!!!!!', fuzz_success_json_data)
        if method == 'put':
            success_pool.lpush('put_optional_success!!!!!!', fuzz_success_json_data)
        if method == 'patch':
            success_pool.lpush('patch_optional_success!!!!!!', fuzz_success_json_data)
        if method == 'get':
            success_pool.lpush('get_optional_success!!!!!!', fuzz_success_json_data)
        if method == 'delete':
            success_pool.lpush('delete_optional_success!!!!!!', fuzz_success_json_data)