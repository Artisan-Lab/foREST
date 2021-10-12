import os
from pathlib import Path


class FieldDictHelper:
    """

    """

    def __init__(self, path=None):
        if not path:
            path = os.path.join(Path(__file__).resolve().parent, "ignore_dep_fields")
        self.simple_fields = []
        self.ignore_dep_fields = []
        with open(os.path.join(os.getcwd(), path), 'r') as f:
            for line in f.readlines():
                ignore_dep_field = line.strip().lower()
                self.ignore_dep_fields.append(ignore_dep_field)

    def is_ignore_dep_field(self, field_name):
        if field_name.lower() in self.ignore_dep_fields:
            return True
        return False


field_dict_helper = FieldDictHelper