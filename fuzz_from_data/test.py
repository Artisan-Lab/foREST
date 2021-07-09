from jsonMutation import JsonMutation
from tree import Tree

tree = Tree(
    '{"id": 244, "excerpt": "04o0zplIvuOGRBL7Eqy6K1lG9WgHdZTd", "status": "publish", "content": "restfulAPITesting"}')
tree.export_img("original.png")
tree.print()
print('muating value!')
JsonMutation.mutate_value(tree)
tree.print()
JsonMutation.drop(tree)
tree.print()
# JsonMutation.select(tree)
tree.print()
JsonMutation.duplicate(tree)
tree.print()
tree.export_img("mutated.png")
print(tree.dump())
