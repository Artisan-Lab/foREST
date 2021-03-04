class g:
    def __init__(self,nodes,links):
        self.nodes = nodes
        self.links = links
    def __repr__(self):
        return repr((self.nodes, self.links))