class node:
    def __init__(self,id,name,label,weight):
        self.name =name
        self.label =label
        self.id = id
        self.weight = weight#consume越多，权重越大，圆越大

    def __repr__(self):
        return repr((self.name, self.label,self.id,self.weight))