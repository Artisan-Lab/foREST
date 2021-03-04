import os

from module.dep_analysis import get_dep_info
from module.display import dep_info_display
from module.parse import parse

if __name__ == '__main__':
    #规范解析
    api_info_list = parse("openapi/project.yaml", 1.0)
    #生成依赖矩阵
    matrix, weight_info_list = get_dep_info(api_info_list)
    # #展示依赖关系
    # dep_matrix = res['dep_matrix']
    # weight_info_list = res['weight_info_list']
    # dep_matrix = matrix = [
    #     [-1, -1, -1, 4, 5,-1, -1, -1, 4, 5],
    #     [-1, 2, -1, 4, 5,-1, -1, -1, 4, 5],
    #     [-1, 2, 3, 4, 5,-1, -1, -1, 4, 5],
    #     [1, 2, 3, 4, 5,-1, -1, -1, 4, 5],
    #     [1, 2, 3, 4, 5,-1, -1, -1, 4, 5],
    #     [-1, -1, -1, 4, 5,-1, -1, -1, 4, 5],
    #     [-1, 2, -1, 4, 5,-1, -1, -1, 4, 5],
    #     [-1, 2, 3, 4, 5,-1, -1, -1, 4, 5],
    #     [1, 2, 3, 4, 5,-1, -1, -1, 4, 5],
    #     [1, 2, 3, 4, 5,-1, -1, -1, 4, 5]
    #
    # ]
    dep_info_display(api_info_list,matrix,weight_info_list)