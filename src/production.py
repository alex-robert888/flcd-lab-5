class Production(object):
    # left_side: (program)
    # right_side: (enter, action_list, exit)
    def __init__(self, left_side=None, right_side=None):
        self.left_side = left_side
        self.right_side = right_side

    def __str__(self):
        return f"{self.left_side[:]} -> {self.right_side[:]}"
