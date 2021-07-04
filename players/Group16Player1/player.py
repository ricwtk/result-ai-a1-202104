class Node:
    
    def __init__(self, state = None, direction = None, parent = None, cost = 0):
        self.state = state
        self.direction = direction
        self.parent = parent
        self.children = []
        self.cost = cost
        self.info = {
            "id": 1,
            "state": self.state,
            "expansionsequence": -1,
            "children": [],
            "actions": [],
            "removed": False,
            "parent": self.parent.info["id"] if (self.parent != None) else None
        }

    def addChildren(self, children):
        self.children.extend(children)
        self.info["children"] = [c.info["id"] for c in children]
        self.info["actions"] = [c.direction for c in children]
        
def appendAndSort(frontier, node):
    duplicated = False
    removed = False
    for i, f in enumerate(frontier):
        if f.state == node.state:
            duplicated = True
            del frontier[i]
            removed = True
            break    
    if (not duplicated) or removed:
        insert_index = len(frontier)
        for i, f in enumerate(frontier):
            if f.cost > node.cost:
                insert_index = i
                break
        frontier.insert(insert_index, node)
    return frontier
        
class Player():
    
    name = "Informed Search Player"
    group = "Groupee"
    members = [
        ["Hay Su Sim", "18112342"],
        ["Gan Chu Heng", "18111773"],
        ["Moo Junn Liang", "18027623"],
        ["Loh Wil Ken", "19031301"]
    ]
    informed = True

    def __init__(self, setup):
        self.setup = setup
        
    def expandNode(self, node, node_num):
        children = []
        directions = ['n', 's', 'w', 'e']
        nswe = [-1, 1, -1, 1]
        pos = [1, 1, 0, 0]
        
        if node.direction == 'n':
            directions.pop(1)
            nswe.pop(1)
            pos.pop(1)
        elif node.direction == 's':
            directions.pop(0)
            nswe.pop(0)
            pos.pop(0)    
        elif node.direction == 'w':
            directions.pop(3)
            nswe.pop(3)
            pos.pop(3)
        elif node.direction == 'e':
            directions.pop(2)
            nswe.pop(2)
            pos.pop(2)
        
        for d in range(3):
            child_state = node.state.copy()
            child_state[pos[d]] += nswe[d]
            children.append(Node(child_state, directions[d], node))  
                
        for child in list(children):
            if (child.state[0] < 0 or child.state[0] >= self.setup["maze_size"][0] or
            child.state[1] < 0 or child.state[1] >= self.setup["maze_size"][1]):
                children.remove(child)
        
        for count in range(len(children)):
            children[count].info["id"] += count + node_num
        
        return children
    
    def run(self, problem):
        snake_locations = problem['snake_locations']
        current_direction = problem['current_direction']
        food_locations = problem['food_locations']
        
        frontier = []
        explored = []
        found_goal = False
        goalie = Node()
        search_tree = []
        solution = []
        frontier.append(Node(snake_locations[0], current_direction, None))
        no_expand = 0
        node_num = 1
        
        while not found_goal:
            if frontier[0].state == food_locations[0]:
                found_goal = True
                frontier[0].info["expansionsequence"] = 1 + no_expand
                goalie = frontier[0]
                break
            
            frontier[0].info["expansionsequence"] = 1 + no_expand     
            children = self.expandNode(frontier[0], node_num)
            frontier[0].addChildren(children)
            explored.append(frontier[0])
            
            if search_tree == []: 
                search_tree.append(frontier[0].info)
            else:
                for x in search_tree:
                    if x["id"] == frontier[0].info["id"]:
                        x = frontier[0].info
                  
            del frontier[0]
            
            for child in children:
                if not (child.state in [e.state for e in explored]) and not (child.state in [f.state for f in frontier]):
                    cost = abs(child.state[0] - food_locations[0][0]) + abs(child.state[1] - food_locations[0][1])
                    child.cost = cost
                    frontier = appendAndSort(frontier, child)  
                else:
                    child.info["removed"] = True
                    
                search_tree.append(child.info)
                node_num = child.info["id"]
                    
            no_expand += 1
        
        solution = [goalie.direction]
    
        while goalie.parent != explored[0]:
            solution.insert(0, goalie.parent.direction)
            goalie = goalie.parent
        
        return solution, search_tree