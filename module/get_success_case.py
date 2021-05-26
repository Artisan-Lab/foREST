class get_success_case():
    def get_fuzz_success(self, matr, tag, method):
        if method == 'post':
            fuzz_success_json_data = matr.lindex('post_success!!!!!!' + tag, 0)
            return fuzz_success_json_data
        if method == 'put':
            fuzz_success_json_data = matr.lindex('put_success!!!!!!' + tag, 0)
            return fuzz_success_json_data
        if method == 'patch':
            fuzz_success_json_data = matr.lindex('patch_success!!!!!!' + tag, 0)
            return fuzz_success_json_data
        if method == 'get':
            fuzz_success_json_data = matr.lindex('get_success!!!!!!' + tag, 0)
            return fuzz_success_json_data
        if method == 'delete':
            fuzz_success_json_data = matr.lindex('delete!!!!!!' + tag, 0)
            return fuzz_success_json_data