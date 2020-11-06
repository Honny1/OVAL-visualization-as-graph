from ..xml_parser import XmlParser
from .client import Client


class ClientArfInput(Client):
    def __init__(self, args):
        super().__init__(args)
        self.show_failed_rules = self.arg.show_failed_rules
        self.show_not_selected_rules = self.arg.show_not_selected_rules
        self.xml_parser = self.xml_parser = XmlParser(self.source_filename)

    def _get_lines_of_wanted_not_selected_rules(self):
        out = []
        out.append('== The not selected rule IDs ==')
        for rule in self._get_wanted_rules_from_array_of_ids(
                self.xml_parser.notselected_rules):
            out.append(rule + '(Not selected)')
        return out

    def get_only_fail_rule(self, rules):
        return list(
            filter(
                lambda rule: self.xml_parser.used_rules[rule]['result'] == 'fail',
                rules))

    def search_rules_id(self):
        return self._check_rules_id(
            self._get_wanted_rules_from_array_of_ids(
                self.xml_parser.used_rules.keys()),
            self._get_wanted_rules_from_array_of_ids(
                self.xml_parser.notselected_rules))