import webbrowser
import json
import os
import shutil
import pprint
from datetime import datetime
import sys
import uuid

from .converter import Converter
from .client import Client


class ArfToJson(Client):
    def create_dict_of_rule(self, rule_id):
        return self.xml_parser.get_oval_tree(rule_id).save_tree_to_dict()

    def file_is_empty(self, path):
        return os.stat(path).st_size == 0

    def save_dict_as_json(self, dict_, src):
        if os.path.isfile(src) and not self.file_is_empty(src):
            with open(src, "r") as f:
                data = json.load(f)
                for key in data:
                    dict_[key] = data[key]
        with open(src, "w+") as f:
            json.dump(dict_, f)

    def prepare_data(self, rules):
        try:
            out = []
            rule = None
            out_oval_tree_dict = dict()
            for rule in rules['rules']:
                date = str(datetime.now().strftime("-%d_%m_%Y-%H_%M_%S"))
                out_oval_tree_dict['graph-of-' + rule +
                                   date] = self.create_dict_of_rule(rule)
            if self.out is not None:
                self.save_dict_as_json(out_oval_tree_dict, self.out)
                out.append(self.out)
            else:
                print(
                    str(json.dumps(out_oval_tree_dict, sort_keys=False, indent=4)))
            return out
        except Exception as error:
            raise ValueError('Rule: "{}" Error: "{}"'.format(rule, error))
