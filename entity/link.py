class link:
    def __init__(self,source,target,type):
        self.source = source
        self.target = target
        self.type = type

    def __repr__(self):
        return repr((self.source, self.target, self.type))