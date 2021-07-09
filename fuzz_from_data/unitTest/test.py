# from jsonMutation import JsonMutation
# from jsonTree import Tree
#
# jsonTree = Tree(
#     '{"id": 244, "excerpt": "04o0zplIvuOGRBL7Eqy6K1lG9WgHdZTd", "status": "publish", "content": "restfulAPITesting"}')
# jsonTree.export_img("original.png")
# jsonTree.print()
# print('muating value!')
# JsonMutation.mutate_value(jsonTree)
# jsonTree.print()
# JsonMutation.drop(jsonTree)
# jsonTree.print()
# # JsonMutation.select(jsonTree)
# jsonTree.print()
# JsonMutation.duplicate(jsonTree)
# jsonTree.print()
# jsonTree.export_img("mutated.png")
# print(jsonTree.dump())


from queryStringMutation import QueryStringMutation

queryStringMutation = QueryStringMutation("a=1&b=2")
a = queryStringMutation.mutate_value()
print()
