from mutation import Mutation
from tree import *


def main():
    json_str = '''
    {
  "firstName": "John",
  "lastName": "Smith",
  "isAlive": true,
  "age": 27,
  "address": {
    "streetAddress": "21 2nd Street",
    "city": "New York",
    "state": "NY",
    "postalCode": "10021-3100"
  },
  "phoneNumbers": [
    {
      "type": "home",
      "number": "212 555-1234"
    },
    {
      "type": "office",
      "number": "646 555-4567"
    }
  ],
  "children": [
    "Kangkang",
    "Linkon",
    "Jany"
  ],
  "spouse": null
}
        '''
    tree = Tree(json_str)
    tree.export_img("original_tree.png")
    tree.print()
    Mutation.drop(tree)
    tree.export_img("dropped_tree.png")
    tree.print()
    Mutation.select(tree)
    tree.export_img("selected_tree.png")
    tree.print()
    Mutation.two_nodes_manipulated_using_random(tree)
    Mutation.duplicate(tree)
    tree.export_img("duplicated_tree.png")
    print(tree.dump())


if __name__ == "__main__":
    main()
