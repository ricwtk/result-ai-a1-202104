class GreedyNode:
    def __init__(self, id=None, expansion_sequence=None, state=None, parent=None, h=None, removed=False):
        self.id = id
        self.expansion_sequence = expansion_sequence
        self.state = state
        self.parent = parent
        self.h = h
        self.removed = removed
        self.children = []
        self.actions = []

    def addChildren(self, children):
        self.children.extend(children)

    def addAction(self, action):
        self.actions.append(action)
