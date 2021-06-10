class get_success_case():
    def get_fuzz_success(self, success_pool, method):
        if method == 'post':
            fuzz_success_json_data = success_pool.lindex('post_success!!!!!!', 0)
            return fuzz_success_json_data
        if method == 'put':
            fuzz_success_json_data = success_pool.lindex('put_success!!!!!!', 0)
            return fuzz_success_json_data
        if method == 'patch':
            fuzz_success_json_data = success_pool.lindex('patch_success!!!!!!', 0)
            return fuzz_success_json_data
        if method == 'get':
            fuzz_success_json_data = success_pool.lindex('get_success!!!!!!', 0)
            return fuzz_success_json_data
        if method == 'delete':
            fuzz_success_json_data = success_pool.lindex('delete!!!!!!', 0)
            return fuzz_success_json_data