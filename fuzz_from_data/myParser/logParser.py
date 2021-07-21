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
        logs = self.log_path.split(',')
        for log in logs:
            self.content += open(log, 'r').readlines()

    def export(self):
        """
        return the converted json data
        """
        pass
