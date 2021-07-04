class Player:
    name = 'Player 1 - Breadth First Search'
    group = 'McFries'
    members = [
		["Liew Hsien Loong", "18030221"],
		["Steven Soo Yon Zhang", "16039166"],
		["Ng Wei Xiang", "18033167"],
		["Teh Jiing Ren", "18027565"]
	]
    informed = False

    def __init__(self, setup):
        self.setup = setup

    def run(self, problem):
        search = BreadthFirstSearch(problem['snake_locations'],
                                 problem['food_locations'],
                                 maze_size=self.setup['maze_size'])
        (solution, search_tree) = search.algorithm()
        return (solution, search_tree)

class Node:
    def __init__(
        self,
        id = None,
        sequence = None,
        state = None,
        parent = None,
        removed = False,
        ):
        self.id = id
        self.sequence = sequence
        self.state = state
        self.parent = parent
        self.removed = removed
        self.children = []
        self.actions = []

    def addChildren(self, children):
        self.children.extend(children)

    def addAction(self, action):
        self.actions.append(action)

class BreadthFirstSearch:
    def __init__(
        self,
        initial_state,
        goal_state,
        state_space = None,
        maze_size = None,
        ):
        self.initial_state = initial_state[0]
        self.snake = initial_state
        self.goal_state = goal_state
        self.state_space = self.initStateSpace(state_space, maze_size)
        self.nodes = 0
        self.expansions = 0
        self.actions = 'nswe'

    def initStateSpace(self, state_space, maze_size):
        result = []
        if maze_size is not None:
            for i in range(0, maze_size[0]):
                for j in range(0, maze_size[1]):
                    result.append([i, j])
            return result
        return state_space

    # expand and return children
    def getChildren(self, node):
        self.expansions += 1
        node.sequence = self.expansions
        children = []
        # check for any connection linked to the node
        for (idx, location) in enumerate(self.getLocation(node.state)):
            if location in self.state_space and location \
                not in self.snake:
                self.nodes += 1
                children.append(Node(self.nodes, -1, location,
                                node.state, False))
                node.addAction(self.actions[idx])
        return children

    def getLocation(self, location):
        n = [location[0], location[1] - 1]
        s = [location[0], location[1] + 1]
        w = [location[0] - 1, location[1]]
        e = [location[0] + 1, location[1]]
        return (n, s, w, e)

    def getSolution(self, solution):
        action = []
        for (idx, location) in enumerate(solution):
            if idx != len(solution) - 1:
                result = [solution[idx + 1][0] - location[0],
                          solution[idx + 1][1] - location[1]]
                if result == [0, 1]:
                    action.append('s')
                elif result == [0, -1]:
                    action.append('n')
                elif result == [-1, 0]:
                    action.append('w')
                elif result == [1, 0]:
                    action.append('e')
        return action

    def getSearchTree(self, explored):
        search_tree = []
        for e in explored:
            tree_node = {
                'id': e.id,
                'state': ','.join(str(v) for v in e.state),
                'expansionsequence': e.sequence,
                'children': [child.id for child in e.children],
                'actions': e.actions,
                'removed': e.removed,
                'parent': self.getParentId(e.parent, explored),
                }
            search_tree.append(tree_node)
        return search_tree

    def getParentId(self, parent_state, explored):
        for e in explored:
            if e.state == parent_state:
                return e.id
        return None

    def algorithm(self):
        frontier = []
        explored = []
        removed = []
        found_goal = False
        goalie = Node()
        self.nodes += 1
        # add initial state to frontier
        frontier.append(Node(self.nodes, self.expansions,
                        self.initial_state, None, False))

        while not found_goal:
            # expand the first in the frontier
            children = self.getChildren(frontier[0])
            # add children list to the expanded node
            frontier[0].addChildren(children)
            # add to the explored list
            explored.append(frontier[0])
            # remove the expanded frontier
            del frontier[0]
            # add children to the frontier
            for child in children:
                # check if a node was expanded or generated previously
                if not child.state in [e.state for e in explored] \
                    and not child.state in [f.state for f in frontier]:
                    # goal test
                    if child.state in self.goal_state:
                        found_goal = True
                        goalie = child
                    frontier.append(child)
                else:
                    child.removed = True
                    removed.append(child)

            # print("Explored: ", [e.state for e in explored]) # lecturer removed
            # print("Frontier: ", [f.state for f in frontier]) # lecturer removed
            # print("Children: ", [c.state for c in children]) # lecturer removed
            # print("") # lecturer removed

        solution = [goalie.state]
        while goalie.parent is not None:
            solution.insert(0, goalie.parent)
            for e in explored:
                if e.state == goalie.parent:
                    goalie = e
                    break
        return (self.getSolution(solution), self.getSearchTree(explored
                + frontier + removed))
        
if __name__ == "__main__":
    p1 = Player({ "maze_size": [10,10], "static_snake_length": True })
    sol, st = p1.run({'snake_locations': [[0, 5]], 'current_direction': 'e', 'food_locations': [[6, 7]]})
    print("Solution is:", sol)
    print("Search tree is:")
    print(st)
        