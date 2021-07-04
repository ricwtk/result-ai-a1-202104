import itertools

class Player:
    name = "Informed Agent: A* Search"
    group = "1M"
    members = [
        ["Phyllis Chong Yee Teng", "18011551"],
        ["Khirrtini Muraleetharan", "18032052"],
        ["Khairul Akmal bin Khairulanwar", "18045872"]
        ]
    informed = True

    def __init__(self, setup):
        self.setup = setup

    def run(self, problem):
        searchTree = []
        solution, searchTree = astar(problem, self.setup)
        return solution, searchTree


class Node:
    def __init__(self, state = None, parent = None, action = None, id = -1, gn = -1, hn = -1):
        self.state = state
        self.parent = parent
        self.children = []
        self.action = action
        self.id = id
        self.gn = gn
        self.hn = hn
        self.fn = self.gn + self.hn

    def addChildren(self, children):
        '''
        function that adds the children of the node into its list
        '''
        self.children.extend(children)

class searchTreeNode:
    def __init__(self, node = None,  removed = True, expansionSequence=-1,):
        self.node = node
        self.removed = removed
        self.expansionSequence = expansionSequence
        self.children = []
        self.action = []
        
    def updateTree(self):
        '''
        function that updates children nodes in search tree
        '''
        for child in self.node.children:
            self.children.append(child.id)
            self.action.append(child.action)

        dict = {
                "id" : self.node.id,
                "state" : self.node.state,
                "expansionsequence": self.expansionSequence,
                "children" : self.children,
                "actions" : self.action,
                "removed" : self.removed
                }

        #link to parent if their respective parent node exists
        if self.node.parent is not None:
            dict["parent"] = self.node.parent.id

        else:
            dict["parent"] = None
            
        return dict


def manhDistance(fromN, toN):
    #a formula function to calculate the g(n) and h(n)
    d = abs(toN[0] - fromN[0]) + abs(toN[1] - fromN[1])
    return d


def sorter(frontier, node):
    '''
    function that sorts the frontier list to obtain the lowest
    value of f(n) at index[0] in the list
    '''
    duplicates = False
    removed = False

    #check and remove duplicates
    for i, j in enumerate(frontier):
        if j.state == node.state:
            duplicates = True
            if j.fn > node.fn:
                del frontier[j]
                removed = True
                break

    #sorts the list
    if removed or (not duplicates):
        index = len(frontier)
        for i, j in enumerate(frontier):
            if j.fn > node.fn:
                index = i
                break
        frontier.insert(index, node)

    return frontier

def expandAndReturnChildren(maze_size, node, idCount, problem):
    ''' 
    a function that uses the temp list to indicate the direction of the snake:
    north or south; east or west depending on the corresponding coordinates
    '''
    temp = [-1,1]
    children = []

    for i in temp:
        if 0 <= node.state[0] + i <= maze_size[0] and 0 <= node.state[1] <= maze_size[1]:
            if i == -1:
                action = 'w'
            else:
                action = 'e'
            children.append(Node([node.state[0] + i, node.state[1]], node, action, next(idCount),
                                 manhDistance(problem["snake_locations"][0], [node.state[0] + i, node.state[1]]), manhDistance([node.state[0] + i, node.state[1]], problem["food_locations"][0])))
            
        if 0 <= node.state[0] <= maze_size[0] and 0 <= node.state[1] + i <= maze_size[1]:
            if i == -1:
                action = 'n'
            else:
                action = 's'
            children.append(Node([node.state[0] , node.state[1] + i], node, action, next(idCount),
                                  manhDistance(problem["snake_locations"][0], [node.state[0], node.state[1] + i]), manhDistance([node.state[0] , node.state[1] + i], problem["food_locations"][0])))
    return children

def astar(problem, setup):
    #initialising variables
    idCount = itertools.count(1)
    expCount = itertools.count(1)

    frontier = [Node(problem["snake_locations"][0], None, None, next(idCount), 0, manhDistance(problem["snake_locations"][0], problem["food_locations"][0]))]
    explored = []
    solution = []
    tempSearchTree = []
    searchTree = []

    isFound = False
    foodLocation = Node()

    #update snake body locations to avoid the snake from running to itself
    for i in problem["snake_locations"]:     
        explored.append(Node(i, None))

    tempSearchTree.append(searchTreeNode(frontier[0], False, next(expCount)))
        
    while not isFound:
        #get children of the current node and update
        children = expandAndReturnChildren(setup["maze_size"], frontier[0], idCount, problem)
        frontier[0].addChildren(children) 

        #adds the current node to the explored list
        explored.append(frontier[0])     
        
        #remove from frontier as it is no longer needed
        del frontier[0]

        #run loop to check if child nodes are the food location
        for child in children:
            tempSearchTree.append(searchTreeNode(child))

            if not (child.state in [e.state for e in explored]) and not (child.state in [f.state for f in frontier]):
                
                #goal check
                if child.state == problem["food_locations"][0]:
                    isFound = True
                    foodLocation = child

                #calls function to sort the frontier
                frontier = sorter(frontier, child)

                #check if the node is unnecessary and to be removed OR to be expanded next
                for i in tempSearchTree:
                    if i.node.id is child.id:
                        i.removed = False
                        break

                for i in tempSearchTree:
                    if i.node.id is frontier[0].id and i.expansionSequence is -1:
                        i.expansionSequence = next(expCount)
                        break
        
        #solution: direction based (nswe)
        solution = [foodLocation.action]
        
        #solution: coordinates based (e.g. 0,1)
        path = [foodLocation.state] 

        #updates solution and path list based on food location
        while foodLocation.parent is not None:
            solution.insert(0, foodLocation.parent.action)
            path.insert(0,foodLocation.parent.state)
            for e in explored:
                if e.state == foodLocation.parent.state:
                    foodLocation = e
                    break

    del solution[0]
    
    #update search tree
    for node in tempSearchTree:
        searchTree.append(node.updateTree())
        
    return solution, searchTree


