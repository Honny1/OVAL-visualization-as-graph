import uuid

from .._builder_html_report import BuilderHtmlReport
from ..xml_parser import XmlParser
from .client_arf_input import ClientArfInput
from .client_html_output import ClientHtmlOutput


class ArfToHtmlReport(ClientArfInput, ClientHtmlOutput):
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
        self.start_of_file_name = 'report-'
        self.web_browsers = []

    def _get_message(self):
        return {
            'description': 'Client for genretate of SCAP report from ARF file.',
            '--output': 'The directory where to save output directory with files.',
            'source_filename': 'ARF scan file',
        }

    def prepare_data(self, rules):
        builder = BuilderHtmlReport(
            self.display_html,
            self.xml_parser,
            self.source_filename)
        out_src = builder.save_report(
            self.get_save_src(str(uuid.uuid4())))
        self.open_results_in_web_browser(out_src)
        return out_src

    def prepare_parser(self):
        self.prepare_args_basic_functions()
        self.prepare_args_display()
        self.prepare_args_source_file()
