class LogParser:
    """
    parse logs and return json-structured HTTP request data.
    """

    def __init__(self, log_path):
        self.log_path = log_path
        self.content = []

    def parse(self):
        """
        begin to parse
        """
        pass

    def read_logs(self):
        """
        read a single file or many files
        """
        if isinstance(self.log_path, str):
            self.content = open(self.log_path, 'r').readlines()
        elif isinstance(self.log_path, list):
            for item in self.log_path:
                self.content += open(item, 'r').readlines()

    def export(self):
        """
        return the converted json data
        """
        pass
