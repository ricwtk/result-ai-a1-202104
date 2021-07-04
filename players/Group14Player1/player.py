# Node class for each position on the maze
class Node():
    
    def __init__(self, parent=None, state=None):
        self.ID = None
        self.parent = parent
        self.state = state
        self.expansionsequence = -1
        self.children = []
        self.actions = []
        self.removed = False
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.state == other.state
    
    def addChildren(self, children):
        self.children.append(children)


class Player():
    name = "Banana2"
    group = "Banana"
    members = [
        ["Sarah Low Ren Ern", "18122614"],
        ["Low Jun Jie", "19041409"],
        ["sean Suraj Nathan", "17003807"],
        ["Mukesh Rajah", "19028281"]
        ]
    informed = True
    
    def __init__(self, setup):
    # setup = {
    #   maze_size: [int, int],
    #   static_snake_length: bool
    # }
        self.setup = {
            "maze_size": setup["maze_size"],
            "static_snake_length": setup["static_snake_length"]
            }
        
    def run(self, problem):
    # problem = {
    #   snake_locations: [[int,int],[int,int],...],
    #   current_direction: str,
    #   food_locations: [[int,int],[int,int],...],
    # }    
        self.problem = {
            "snake_locations": problem["snake_locations"],
            "current_direction": problem["current_direction"],
            "food_locations": problem["food_locations"]
            }
        
        # create a virutal maze for the function depending on the settings
        nrow = self.setup["maze_size"][0]
        ncol = self.setup["maze_size"][1]
        e = []
        maze = []
        for i in range(ncol):
            e.append(0)
        for i in range(nrow):
            maze.append(e)
        
        temp_s = self.problem["snake_locations"][0]
        temp_e = self.problem["food_locations"][0]
        start = (temp_s[0], temp_s[1]) 
        end = (temp_e[0], temp_e[1])
        
        # Create initial and end node
        initial_node = Node(None, start)
        initial_node.g = initial_node.h = initial_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0
    
        # Initialize both frontier and explored
        frontier = []
        explored = []
        solution = []
    
        # Add the initial node to frontier
        frontier.append(initial_node)
    
        frontierloop = 0 # lecturer added
        # Loop until you find the end
        while len(frontier) > 0:
            if frontierloop > 1000: # lecturer added
                raise Exception("frontier loop > 1000") # lecturer added
            frontierloop += 1 # lecturer added
            print(frontierloop, end=" ") # lecturer added

            # Get the current node in the frontier with lowest f value
            first_node = frontier[0]
            first_index = 0
            for i, nodes in enumerate(frontier):
                if nodes.f < first_node.f:
                    first_node = nodes
                    first_index = i
    
            # Pop current node off frontier, add to explored
            frontier.pop(first_index)
            explored.append(first_node)
            
    
            # Return solution and search tree if reached goal
            if first_node == end_node:
                path = []
                reversed_path = []
                current = first_node
                while current is not None:
                    path.append(current.state)
                    current = current.parent
                    reversed_path = path[::-1] # Reversed path
                for i in range(len(reversed_path)):
                    if i == 0:
                        continue
                    elif reversed_path[i][0] - reversed_path[i-1][0] == 1:
                        solution.append("e")
                    elif reversed_path[i][0] - reversed_path[i-1][0] == -1:
                        solution.append("w")
                    elif reversed_path[i][1] - reversed_path[i-1][1] == 1:
                        solution.append("s")
                    elif reversed_path[i][1] - reversed_path[i-1][1] == -1:
                        solution.append("n")
                search_tree = []
                temp_tree = []
                for i in range(len(reversed_path)):
                    if i == 0:
                        first = Node(None, reversed_path[0])
                        first.ID = i + 1
                        first.expansionsequence = i + 1
                        first.addChildren(i + 2)
                        temp_tree.append(first)
                    else:
                        previous = Node(None, reversed_path[i - 1])
                        previous.ID = i
                        rest = Node(previous.ID, reversed_path[i])
                        rest.ID = i + 1
                        rest.expansionsequence = i + 1
                        if i == range(len(reversed_path))[-1]:
                            useless = i  # A holder with no purpose for if reach last node
                        else:
                            rest.addChildren(i + 2)
                        for e in range(i):
                            rest.actions.append(solution[e])
                        temp_tree.append(rest)
                        
                for e in temp_tree:
                    a = {
                        "id": e.ID,
                         "state": e.state,
                         "expansionsequence": e.expansionsequence,
                         "children": e.children,
                         "actions": e.actions,
                         "removed": e.removed,
                         "parents": e.parent
                         }
                    search_tree.append(a)
                print() # lecturer added
                return solution, search_tree

    
    
    
            # Generate children
            children = []
            for directions in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # All n, s, e, w
                # Get node position
                node_position = (first_node.state[0] + directions[0], first_node.state[1] + directions[1])
                # Make sure node position within range of the maze size
                if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                    continue
                # Prevent snake from biting itself
                if [node_position[0], node_position[1]] in self.problem["snake_locations"]:
                    continue
                new_node = Node(first_node, node_position)
                children.append(new_node)
    
            # Loop through children
            for child in children:
                # Child is on the explored list
                for explored_child in explored:
                    if child == explored_child:
                        continue
                # Create the f, g, and h values
                child.g = first_node.g + 1
                child.h = ((child.state[0] - end_node.state[0]) ** 2) + ((child.state[1] - end_node.state[1]) ** 2)
                child.f = child.g + child.h
                # Child is already in the frontier
                for open_node in frontier:
                    if child == open_node and child.g > open_node.g:
                        continue
                # Else add the child to the open list
                frontier.append(child)
        
    


if __name__ == "__main__":
  p1 = Player({ "maze_size": [10,10], "static_snake_length": True })
  sol, st = p1.run({'snake_locations': [[0, 5]], 'current_direction': 'e', 'food_locations': [[6, 7]]})
  print("Solution is:", sol)
  print("Search tree is:")
  print(st)
