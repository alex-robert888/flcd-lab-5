class ParseTreeNode(object):
    def __init__(self, info, parent, right_sibling):
        self.info = info
        self.parent = parent
        self.right_sibling = right_sibling
