class ParseTreeNode(object):
    def __init__(self, index, info, parent, right_sibling):
        self.index = index
        self.info = info
        self.parent = parent
        self.right_sibling = right_sibling

    def __str__(self):
        return f"{self.index} | {self.info} | {self.parent} | {self.right_sibling}"
