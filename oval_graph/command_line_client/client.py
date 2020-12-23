import argparse
import re
import sys
from datetime import datetime

from .. import __version__


class Client():
    def __init__(self, args):
        self.parser = None
        self.arg = self.parse_arguments(args)
        self.hide_passing_tests = self.arg.hide_passing_tests
        self.source_filename = self.arg.source_filename
        self.rule_name = self.arg.rule_id
        self.out = self.arg.output
        self.verbose = self.arg.verbose

        self.date = str(datetime.now().strftime("-%d_%m_%Y-%H_%M_%S"))
        self.isatty = sys.stdout.isatty()

        self.all_rules = self.arg.all
        self.show_failed_rules = False
        self.show_not_selected_rules = False

    @staticmethod
    def _get_message():
        return {
            'description': '',
            'source_filename': '',
        }

    #    Non-implemented functions can handle different types of the input file.
    #    Functions for input file processing and corresponding rule ID.

    def prepare_data(self, rules):
        """
        Function processes HTML graphs or JSON and
        return array of where is saved output file if exitsts.
        """
        raise NotImplementedError

    # Functions for selection of rules

    def search_rules_id(self):
        """
        Function retunes array of all matched IDs of rules in selected file.
        """
        raise NotImplementedError

    def get_only_fail_rule(self, rules):
        """
        Function processes array of matched IDs of rules in selected file.
        Function retunes array of failed matched IDs of rules in selected file.
        """
        raise NotImplementedError

    def _get_rows_of_unselected_rules(self):
        """
        Function retunes array of rows where is not selected IDs of rules in selected file.
        """
        raise NotImplementedError

    def run_gui_and_return_answers(self):
        if self.isatty:
            if self.all_rules:
                return self._get_rules()

            try:
                import inquirer
                return inquirer.prompt(self.get_questions())
            except ImportError:
                print(self.get_selection_rules())
            return None
        return self._get_rules()

    def _get_rules(self):
        if self.show_failed_rules:
            return {'rules': self.get_only_fail_rule(self.search_rules_id())}
        return {'rules': self.search_rules_id()}

    def _get_list_of_matched_rules(self):
        if self.show_failed_rules:
            return self.get_only_fail_rule(self.search_rules_id())
        return self.search_rules_id()

    def _get_list_of_lines(self):
        lines = ['== The Rule ID regular expressions ==']
        for rule in self._get_list_of_matched_rules():
            lines.append("^" + rule + "$")
        if self.show_not_selected_rules:
            for line in self._get_rows_of_unselected_rules():
                lines.append(line)
        lines.append(
            "Interactive rule selection is not available,"
            " because inquirer is not installed."
            " Copy id of the rule you want to visualize and"
            " paste it into a command with regular"
            " expression characters(^$).\n"
            "Alternatively, use the --all or --all-in-one arguments.")
        return lines

    def get_selection_rules(self):
        return "\n".join(self._get_list_of_lines())

    def _get_choices(self):
        if self.show_not_selected_rules:
            print("\n".join(self._get_rows_of_unselected_rules()))
        return self._get_list_of_matched_rules()

    def get_questions(self):
        from inquirer.questions import Checkbox as checkbox
        choices = self._get_choices()
        questions = [
            checkbox(
                'rules',
                message=(
                    "= The Rules IDs = (move - UP and DOWN arrows,"
                    " select - SPACE or LEFT and RIGHT arrows, submit - ENTER)"),
                choices=choices,
            ),
        ]
        return questions

    def _get_wanted_rules(self, rules):
        return [
            x for x in rules if re.search(
                self.rule_name, x)]

    def _check_rules_id(self, rules, notselected_rules):
        if notselected_rules and not rules:
            raise ValueError(
                ('Rule(s) "{}" was not selected, '
                 "so there are no results. The rule is"
                 ' "notselected" because it'
                 " wasn't a part of the executed profile"
                 " and therefore it wasn't evaluated "
                 "during the scan.")
                .format(notselected_rules))
        if not notselected_rules and not rules:
            raise ValueError('404 rule "{}" not found!'.format(self.rule_name))
        return rules

    # Function for setting arguments

    def parse_arguments(self, args):
        self.prepare_parser()
        return self.parser.parse_args(args)

    def prepare_args_when_user_can_list_in_rules(self):
        self.parser.add_argument(
            '--show-failed-rules',
            action="store_true",
            default=False,
            help="Show only FAILED rules")
        self.parser.add_argument(
            '--show-not-selected-rules',
            action="store_true",
            default=False,
            help="Show notselected rules. These rules will not be visualized.")

    def prepare_parser(self):
        self.parser = argparse.ArgumentParser(
            prog='oval-graph',
            description=self._get_message().get('description'))
        self.parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s ' + __version__)
        self.parser.add_argument(
            '-a',
            '--all',
            action="store_true",
            default=False,
            help="Process all matched rules.")
        self.parser.add_argument(
            '--hide-passing-tests',
            action="store_true",
            default=False,
            help=(
                "Do not display passing tests for better orientation in"
                " graphs that contain a large amount of nodes."))
        self.parser.add_argument(
            '-v',
            '--verbose',
            action="store_true",
            default=False,
            help="Displays details about the results of the running command.")
        self.parser.add_argument(
            '-o',
            '--output',
            action="store",
            default=None,
            help='The file where to save output.')
        self.parser.add_argument(
            "source_filename",
            help=self._get_message().get('source_filename'))
        self.parser.add_argument(
            "rule_id", help=(
                "Rule ID to be visualized. A part from the full rule ID"
                " a part of the ID or a regular expression can be used."
                " If brackets are used in the regular expression "
                "the regular expression must be quoted."))
