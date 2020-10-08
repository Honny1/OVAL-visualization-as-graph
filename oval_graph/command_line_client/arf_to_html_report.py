from .client import Client
from ..xml_parser import XmlParser


class ArfToHtmlReport(Client):
    def __init__(self, args):
        self.parser = None
        self.arg = self.parse_arguments(args)
        self.source_filename = self.arg.source_filename
        self.out = self.arg.output
        self.display_html = True if self.out is None else self.arg.display
        self.verbose = self.arg.verbose
        self.xml_parser = XmlParser(self.source_filename)
        self.rule_name = '.'
        self.isatty = False
        self.show_failed_rules = False
        self.show_not_selected_rules = False

    def _get_message(self):
        return {
            'description': 'Client for genretate of SCAP report from ARF file.',
            '--output': 'The directory where to save output directory with files.',
            'source_filename': 'ARF scan file',
        }

    def prepare_data(self, rules):
        src = ""
        """
        self.verbose
        self.display_html
        self.out
        self.source_filename
        """
        return src

    def prepare_parser(self):
        self.prepare_args_basic_functions()
        self.prepare_args_display()
        self.prepare_args_source_file()
