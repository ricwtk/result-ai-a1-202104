class Node():
    id = 1

    def __init__(self, state = None, parent = None, step = 0):
        self.id = Node.id
        self.expansion_sequence = -1
        self.state = state
        self.children = []
        self.actions = []
        self.removed = False    
        self.parent = parent
        self.step = step #step from initial to this node (for updated snake body)
        Node.id += 1
        
    def addChildren(self, action, child):
        self.actions.append(action)
        self.children.append(child)
    
    def updateRemove(self, is_removed):
        self.removed = is_removed
    
    def updateSequence(self,sequence):
        self.expansion_sequence = sequence

    def getTreeNode(self):
        return { 
            "id": self.id,
            "state": self.state,
            "expansionsequence": self.expansion_sequence,
            "children": self.children,
            "actions": self.actions,
            "removed": self.removed,
            "parent": self.parent
        }

    @classmethod
    def resetId(cls):
        Node.id = 1


class Player():

    name = "Breath-First Search"
    group = "Waiting for naptime"
    members = [
        ["Kok Shi Qi", "19049808"],
        ["Tang Wen Yi", "17102617"],
        ["Lim Pei Ni", "19066273"],
        ["Lan Yee Faye", "18123729"]
    ]
    informed = False
  
    def __init__(self, setup): 
        # setup = { # setup is changed in the tab "Game Setting" in front-end
        #   maze_size: [int, int], #[row, col]
        #   static_snake_length: bool
        # }
        self.setup = setup

    def run(self, problem):
        # problem = {
        #   snake_locations: [[int,int],[int,int],...],
        #   current_direction: str,
        #   food_locations: [[int,int],[int,int],...],
        # }
        
        solution = []
        search_tree = []
        frontier = []
        explored = []
        sequence = 1
        found_goal = False

        goal_state = problem["food_locations"]
        snake_body = problem["snake_locations"]
        initial_state = problem["snake_locations"][0] 
        Node.resetId()

        frontier.append(Node(initial_state,None))
           
        while not found_goal:
            try:
                temp = frontier[0]
                children = self.expandChildrenDirection(frontier[0], snake_body)
                frontier[0].updateSequence(sequence)
                sequence += 1
                search_tree.append(frontier[0].getTreeNode())
                explored.append(frontier[0])
                del frontier[0]
                
                for child in children:
                    if not (child.state in [e.state for e in explored]) and not (child.state in [f.state for f in frontier]) and not child.removed:
                        
                        if child.state in [g for g in goal_state]: #goal test
                            found_goal = True
                            goalie = child # the first node that explored goal
                            search_tree.append(goalie.getTreeNode())
                        else:
                            frontier.append(child) 
                    else:
                        child.updateRemove(True)
                        search_tree.append(child.getTreeNode())
            
                if not frontier and not children: # no solution when snake wraps itself
                    raise Exception

            except:
                found_goal = True
                goalie = temp # goalie = last frontier

                if goalie.parent is None: # when no solution, simply return a direction
                    solution.append(problem["current_direction"])
        
        for f in frontier:
            search_tree.append(f.getTreeNode())

        while goalie.parent is not None:
            for e in explored:
                if e.id == goalie.parent:
                    i = e.children.index(goalie.id)
                    solution.insert(0,e.actions[i])
                    goalie = e
                    break

        return solution, search_tree   

    def expandChildrenDirection(self, node, snake_body):
        children = []
        [grid_row, grid_col] = self.setup["maze_size"]
        [col, row] = node.state
        estimated_snake_body = [] if len(snake_body) - node.step < 0 else snake_body[ : len(snake_body) - node.step ] # updated body after move

        directions = {
            "n": [col, row-1],
            "s": [col, row+1],
            "e": [col+1, row],
            "w": [col-1, row]
        }  

        for d in directions.keys():

            if directions[d][0] >= grid_col or directions[d][0] < 0 or directions[d][1] >= grid_row or directions[d][1] < 0:  # check if out of grid
                continue
            
            child = Node(directions[d],node.id,node.step+1)

            if directions[d] in estimated_snake_body: #remove node if it's in body
                child.updateRemove(True)

            children.append(child)
            node.addChildren(d,child.id)

        return children
    
