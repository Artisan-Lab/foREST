from module.basic_fuzz import BasicFuzz
from module.genetic_algorithm import GeneticAlgorithm
from module.jsonhandle import JsonHandle


class GetValue:

    @staticmethod
    def get_value_from_resource(resource, parameter_name, parameter_type):
        value = JsonHandle.find_field_in_dic(resource.resource_data, parameter_name, parameter_type)
        return value

    @staticmethod
    def get_value(field_info):
        # 获取参数值
        value = None
        if field_info.field_type == 'bool':
            value = BasicFuzz.fuzz_value_from_field(field_info)
            return value
        # if redis_external_key.exists(field_info.field_name):
        #     # 先判断该参数有没有由外部指定
        #     value = redis_external_key.get(field_info.field_name)
        #     log = Log(log_name='hit_external_field')
        #     log.info('Key: ' + str(field_info.field_name) + 'Value: ' + str(value))
        #     return value
        if field_info.depend_list[0]:
            # 判断该参数可否从其他请求的响应中获取
            genetic_algorithm = GeneticAlgorithm(field_info.depend_list[1])
            for i in range(len(field_info.depend_list[1])):
                winner_depend_field_index = genetic_algorithm.get_winner_index()
                value = redis_response_handle.get_specific_value_from_response_pool(
                    field_info.depend_list[0][int(winner_depend_field_index / 2)])
                if value:
                    self.request.add_genetic_algorithm(genetic_algorithm)
                    if winner_depend_field_index % 2 == 0 and (isinstance(value, str)):
                        return BasicFuzz.fuzz_mutation_parameter(value)
                    else:
                        return value
                genetic_algorithm.winner_failed()
            field_info.depend_list[1] = genetic_algorithm.get_survival_points_list
        if field_info.field_type == 'dict':
            # 如果没有得到并且该参数是dict类型的话，将递归生成该参数
            value = {}
            if field_info.object:
                for sub_field_info in field_info.object:
                    if sub_field_info.require:
                        sub_field_value = ComposeRequest.GetValue(sub_field_info)
                        if sub_field_value:
                            value[sub_field_info.field_name] = sub_field_value
                return value
        elif field_info.field_type == 'list':
            # 同上
            if isinstance(field_info.array, list):
                value = []
                sub_value = {}
                for array_field in field_info.array:
                    if array_field.require:
                        sub_value[array_field.field_name] = ComposeRequest.GetValue(array_field)
                value.append(sub_value)
                return value
            elif isinstance(field_info.array, str):
                value = []
                for i in range(0, 5):
                    value.append(BasicFuzz.fuzz_value_from_type(field_info.array))
                return value
        if value is None:
            # 如果不能获得该参数的话，用fuzz
            value = BasicFuzz.fuzz_value_from_field(field_info)
        return value