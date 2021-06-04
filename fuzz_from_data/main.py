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
            "number": "212 555-1234",
            "test": null
        },
        {
            "type": "office",
            "number": "646 555-4567"
        }
    ],
    "children": [
        1,
        "1",
        true,
        1.2
    ],
    "spouse": null
}
    '''
    tree = Tree(json_str)
    tree.print()
    tree._dump()


if __name__ == "__main__":
    main()
