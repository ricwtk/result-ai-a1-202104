class Player():
    name = "Bryan Tang"
    group = "bt smeli"
    members = [
        ["Bryan Tang", "18041772"],
        ["Chun Hou", "18043547"],
        ["Wei Jun", "18034223"],
        ["Weng Xi", "18043521"]
      ]

    informed = False
    #uninformed search using Breadth-First Search

    def __init__(self,setup):
        self.setup = setup
        #accesing value in items in setup dictionary 
        for key, value in setup.items():
            if key == "maze_size":
                #set the value of maze size acquired in the UI to variable maze_size
                self.maze_size = value
        
    def run(self, problem):   
        solution = []
        #accesing value in items in problem dictionary 
        for key, value in problem.items(): 
            if key =="snake_locations":
                #set the value of snake current location acquired in the UI to variable snake_locations                       
                snake_locations=value
            if key =="food_locations":
                #set the value of food current location acquired in the UI to variable food_locations                                       
                food_locations=value           
        
        #calling search algorithm function
        [solution,tree] = bfs(snake_locations, food_locations, self.maze_size)   
                
        return solution, tree


class Node():
    def __init__(self, state=None, parent=None, directionFromParent=None, identity = None):
        self.state = state
        self.parent = parent
        self.directionFromParent = directionFromParent
        self.identity = identity

def removeRedundantCoordinate(children,current):
    for i,child in enumerate(children):
        if (child.state == current):
            del children[i]
    return children

def checkRemoved(node,children):
    for child in children:
        if node.state == child.state:
            return True
        return False
    
def getParentId(node,explored):
    for e in explored:
        if node.parent == e.state:
            return e.identity
    return None
        
             
def createTree(node,children,expansionsequence,explored): 
    Dict = {}
    
    Dict["id"] = node.identity
    Dict["state"] = node.state
    Dict["expansionsequence"] = expansionsequence
    Dict["children"] = [child.identity for child in children]
    Dict["actions"] =  [child.directionFromParent for child in children]
    Dict["removed"] = checkRemoved(node,children)
    Dict["parent"] = getParentId(node,explored)

    return Dict
    

def expandAndReturnChild(current, size,node_id): 
    children = []
    #setting the axis value with the value acquired in current parameter
    #current[1] is y-axis, current[0] is x-axis    
    up = current[1]-1 #node moving up e.g: [0,1] to [0,0], hence subtracting y-axis = moving node up
    down = current[1]+1 #node moving down e.g: [0,1] to [0,2], hence adding y-axis = moving node down
    left = current[0]-1 #node moving left e.g: [1,1] to [0,1], hence subtracting x-axis = moving node left  
    right = current[0]+1 #node moving right e.g: [1,1] to [2,1], hence adding y-axis = moving node right        
    
    #checking if node's next action is within the maze size
    #if next action is over the maze size, then return same position    
    if current[1]==size[1]-1: #e.g: maze size =10x10, current= [0,9], next action is moving down, hence, return to same position
        down = size[1]-1 
    if current[1] == 0:
        up = 0
    if current[0]==0:
        left = 0
    if current[0] == size[0]-1:
        right = size[0]-1

    #create new children node 
    moveUp = Node([current[0],up], current, 'n',node_id+1)
    moveDown = Node([current[0],down], current, 's',node_id+2)
    moveLeft = Node([left, current[1]], current, 'w',node_id+3)
    moveRight = Node([right,current[1]], current, 'e',node_id+4)
    
    #parsing in children node to children list
    children.append(moveUp)
    children.append(moveDown)
    children.append(moveLeft)
    children.append(moveRight)
    
    number_of_nodes_added = len(children)
    
    removeRedundantCoordinate(children,current)
    
    return(children) ,number_of_nodes_added

def bfs(initial, goal, size):
    frontier =[] #frontier to determine the next move
    explored = [] #node that have been explored
    solution=[] #storing direction to food location
    Tree = [] #storing tree

    found_goal = False
    goalNode=Node()
    
    node_id = 1
    expansionsequence = 0
    frontier.append(Node(initial[0], None, None,node_id))

    while not found_goal:
        expansionsequence +=1
        [children, number_counter] = expandAndReturnChild(frontier[0].state, size,node_id)
        node_id += number_counter
        Tree.append(createTree(frontier[0],children,expansionsequence,explored))
        explored.append(frontier[0])

        del frontier[0]
        
        #check if children is redundant, removing loopy path
        for child in children:
          if not (child.state in [e.state for e in explored]) and not (child.state in [f.state for f in frontier]):
            if child.state == goal[0]: #checking if the next move(children) is the goal state (food)
                found_goal = True #if child == food state, then found goal = true, hence, while loop will be break
                goalNode = child
            
            frontier.append(child)
        
        print("Explored:", [e.state for e in explored])
        print("Frontier:", [f.state for f in frontier])
        print("Children:", [c.state for c in children])
        print("")
    
    
    solution = [goalNode.directionFromParent]
    while goalNode.directionFromParent is not None:
        for e in explored:
            if e.state == goalNode.parent:
                solution.insert(0, e.directionFromParent)
                goalNode = e
    del solution[0]      
      
    return solution, Tree

if __name__ == "__main__":
    p1 = Player({"maze_size":[10,10], "static_snake_length": True})
    [sol,tree] = p1.run({'snake_locations': [[9, 3]], 'current_direction': 'e', 'food_locations': [[0, 3]]})
    print("Solution is: ", sol)
    print("Tree is : ", tree)

