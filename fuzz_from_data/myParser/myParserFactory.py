from fuzz_from_data.commons.constants import *
from fuzz_from_data.commons.fuzzFromDataConfig import FUZZ_FROM_DATA_CONFIG
from fuzz_from_data.myParser.apacheLogParser import ApacheLogParser
from fuzz_from_data.myParser.HWLogParser import HWLogParser
from fuzz_from_data.myParser.proxyLogParser import ProxyLogParser
from fuzz_from_data.myParser.logParser import LogParser


class MyParserFactory:
    """
    parser factory
    """

    @staticmethod
    def product_parser(name: str) -> LogParser:
        """
        return a parser by name
        """
        src = FUZZ_FROM_DATA_CONFIG.log_path
        if name == LOG_PARSER_APACHE:
            return ApacheLogParser(src)
        elif name == LOG_PARSER_HW:
            return HWLogParser(src)
        elif name == LOG_PARSER_PROXY:
            return ProxyLogParser(src)
        else:
            print(f'error parser name! {name}')
            exit(0)
