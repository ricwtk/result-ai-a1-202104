from .node_class import BFSNode

class BFS:
    def __init__(self, initial_state, goal_state, maze_size):
        self.initial_state = initial_state[0]
        self.snake_body = initial_state
        self.goal_state = goal_state # Can have multiple goal states
        self.maze_size = maze_size
        self.number_of_nodes = 0
        self.number_of_expansions = 0
        self.ACTIONS_DICT = {
            "coordinates": [[0, -1], [0, 1], [1, 0], [-1, 0]],
            "actions": "nsew"
        }


    def getNeighbours(self, state):
        neighbours = []

        for coord in self.ACTIONS_DICT["coordinates"]:
            neighbours.append([state[0] + coord[0], state[1] + coord[1]])

        return neighbours


    def getAction(self, coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        resultant_coord = [x1 - x2, y1 - y2]
        coord_idx = self.ACTIONS_DICT["coordinates"].index(resultant_coord)
        return self.ACTIONS_DICT["actions"][coord_idx]


    def getParentId(self, parent_state, nodes):
        for node in nodes:
            if node.state == parent_state:
                return node.id
        return None


    def generateSearchTree(self, nodes):
        search_tree = []

        # Recreate search tree
        for node in nodes:
            tree_node = {
                "id": node.id,
                "state": ','.join(str(v) for v in node.state),
                "expansionsequence": node.expansion_sequence,
                "children": [child.id for child in node.children],
                "actions": node.actions,
                "removed": node.removed,
                "parent": self.getParentId(node.parent, nodes) # search for parent ID
            }

            search_tree.append(tree_node)

        return search_tree


    def expandAndReturnChildren(self, node):
        # Add expansion sequence
        self.number_of_expansions += 1
        node.expansion_sequence = self.number_of_expansions

        # Will return neighbouring nodes
        children = []

        for idx, neighbour in enumerate(self.getNeighbours(node.state)):
            if neighbour[0] in range(0, self.maze_size[0]) and neighbour[1] in range(0, self.maze_size[1]) and neighbour not in self.snake_body:
                self.number_of_nodes += 1
                children.append(BFSNode(self.number_of_nodes, -1, neighbour, node.state, False))
                node.addAction(self.ACTIONS_DICT["actions"][idx])

        return children


    def bfs(self):
        frontier = []
        explored = []
        removed = []
        found_goal = False
        goalie = BFSNode()

        self.number_of_nodes += 1

        # `frontier` variable needs to append BFSNode class
        # This is because the frontier will be storing an array of yet to visit Node states
        frontier.append(BFSNode(self.number_of_nodes, self.number_of_expansions, self.initial_state, None, False))

        # Where BFS begins
        while not found_goal:
            # Get the children paths of the first frontier element
            children = self.expandAndReturnChildren(frontier[0])
            frontier[0].addChildren(children)
            # Put the first element of the frontier to the explored array
            explored.append(frontier[0])
            # Delete first frontier as it is already explored
            del frontier[0]

            for child in children:
                # If the state in child is not in explored and
                # is not in any of the states in the BFSNodes of the frontier array
                # Meaning that it has not been explored at all
                if not (child.state in [e.state for e in explored]) and not (child.state in [f.state for f in frontier]):
                    # Goal test
                    if child.state in self.goal_state:
                        found_goal = True
                        # Goalie is the goal node
                        goalie = child
                    # Append the child path to frontier for exploration
                    frontier.append(child)
                else:
                    child.removed = True
                    removed.append(child)

        solution = [goalie.state]
        solution_actions = []
        # Loop through to find the entire solution path
        while goalie.parent is not None:
            # Insert the parent before the child in the array
            solution.insert(0, goalie.parent)
            solution_actions.insert(0, self.getAction(goalie.state, goalie.parent))
            for e in explored:
                # To get the parent's parent
                if e.state == goalie.parent:
                    # Next goal node will be the e node to get the parent of the goal node's parent
                    goalie = e
                    break

        return solution_actions, self.generateSearchTree(explored + frontier + removed)