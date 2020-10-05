from ..converter import Converter
from ..oval_node import restore_dict_to_tree
from .client_html_output import ClientHtmlOutput
from .client_json_input import ClientJsonInput


class JsonToHtml(ClientHtmlOutput, ClientJsonInput):
    def __init__(self, args):
        super().__init__(args)
        self.oval_tree = None

    def _get_message(self):
        return {
            'description': 'Client for visualization of JSON created by command arf-to-json',
            'source_filename': 'JSON file',
        }

    def load_json_to_oval_tree(self, rule):
        dict_of_tree = self.json_data_file[rule]
        try:
            return restore_dict_to_tree(dict_of_tree)
        except Exception:
            raise ValueError('Data is not valid for OVAL tree.')

    def create_dict_of_oval_node(self, oval_node):
        converter = Converter(oval_node)
        return converter.to_JsTree_dict(self.hide_passing_tests)

    def create_dict_of_rule(self, rule):
        self.oval_tree = self.load_json_to_oval_tree(rule)
        return self.create_dict_of_oval_node(self.oval_tree)

    def _put_to_dict_oval_trees(self, dict_oval_trees, rule):
        dict_oval_trees[rule.replace(
            self.start_of_file_name, '')] = self.create_dict_of_rule(rule)

    def _get_src_for_one_graph(self, rule):
        return self.get_save_src(rule.replace(self.start_of_file_name, ''))

    def prepare_parser(self):
        super().prepare_parser()
        self.prepare_args_all_in_one()
        self.prepare_args_display()
