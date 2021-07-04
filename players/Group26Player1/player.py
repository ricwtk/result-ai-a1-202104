import itertools

class Player():
  name = "A* Search player"
  group = "Fancy"
  members = [
    ["Tan Wyyee", "17013673"],
    ["Kok Ming Ho", "19024272"],
    ["Sin Jun", "18087619"],
    ["Leong Yen Loong", "18076083"]
  ]
  informed = True

  def __init__(self, setup):
    # setup = {
    #   maze_size: [int, int],
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
    directions = "nswe"
    # the following algorithm is NOT a valid algorithm
    # it randomly generates solution that is invalid
    # its purpose is to show you how this class will work
    # not a guide to how to write your algorithm
    solution, search_tree = astar(problem, self.setup)
    # solution = [random.choice(directions) for step in range(random.randint(1,10))]
    # the following search tree is a static search tree 
    # to show you the format of the variable 
    # to generate a search tree that can be displayed in the frontend.
    # you are required to generate the search tree based on your search algorithm
    # this function should return the solution and the search_tree
    return solution, search_tree
class searchTree:
    def __init__(self, node=None, expansionsequence=-1, removed = True):
        self.node = node
        self.removed = removed
        self.expansionsequence = expansionsequence
        self.children = []
        self.childrenaction = []
        
    def returnTreeNode(self):
        for child in self.node.children:
            self.children.append(child.id)
            self.childrenaction.append(child.action)
        if self.node.parent is not None:
            objectDictionary = {
                "id" : self.node.id,
                "state" : self.node.state,
                "expansionsequence": self.expansionsequence,
                "children" : self.children,
                "actions" : self.childrenaction,
                "removed" : self.removed,
                "parent" : self.node.parent.id
                }
        elif self.node.parent is None:
              objectDictionary = {
                "id" : self.node.id,
                "state" : self.node.state,
                "expansionsequence": self.expansionsequence,
                "children" : self.children,
                "actions" : self.childrenaction,
                "removed" : self.removed,
                "parent" : None
                }
            
        
        return objectDictionary

class Node:
    def __init__(self, state=None, parent=None, action=None, id=-1, gCost =-1, hCost = -1):
        self.id = id
        self.state = state
        self.parent = parent
        self.children = []
        self.action = action
        self.gCost = gCost
        self.hCost = hCost
        self.fCost = self.gCost + self.hCost
    def addChildren(self, children):
        self.children.extend(children)
    
def astar(problem, setup):
     print("this is A* search.")
     idIterator = itertools.count(1)
     expansionSequenceIterator = itertools.count(1)
     trees = []
     frontier = []
     explored = []
     found_goal = False
     goalie = Node()
     solution = []
     frontier.append(Node(problem["snake_locations"][0], None, None, next(idIterator), 0, 
                          returnManhanttanDistance(problem["snake_locations"][0], problem["food_locations"][0])))
     trees.append(searchTree(frontier[0],-1, False))
     for x in problem["snake_locations"]:     
         explored.append(Node(x, None))
     while not found_goal:
        # expand the first in the frontier
        children = expandAndReturnChildren(setup["maze_size"], frontier[0], idIterator,problem)
        # add children list to the expanded node
        frontier[0].addChildren(children)     
        for tree in trees:
            if tree.node.id is frontier[0].id:
                tree.expansionsequence = next(expansionSequenceIterator)
                break
        # add to the explored list
        explored.append(frontier[0])        
        # remove the expanded frontier
        del frontier[0]
        # add children to the frontier
        for child in children:
            trees.append(searchTree(child))
            # check if a node was expanded or generated previously
            if not (child.state in [e.state for e in explored]) and not (child.state in [f.state for f in frontier]):
                # goal test
                if child.state == problem["food_locations"][0]:
                    found_goal = True
                    goalie = child
                frontier = appendAndSort(frontier, child)
                for tree in trees:
                    if tree.node.id is child.id:
                        tree.removed = False
                        break
                #frontier.append(child)
        print("Explored:", [e.state for e in explored])
        print("Frontier:", [f.state for f in frontier])
        print("Children:", [c.state for c in children])
        print("Trees:", [t.node.id for t in trees])
        print("")
        solution = [goalie.action]
        path = [goalie.state]
        while goalie.parent is not None:
            solution.insert(0, goalie.parent.action)
            path.insert(0,goalie.parent.state)
            for e in explored:
                if e.state == goalie.parent.state:
                    goalie = e
                    break
     print("path: ",path)
     del solution[0]
     search_tree = []
     for node in trees:
         search_tree.append(node.returnTreeNode())
     return solution, search_tree
        
def expandAndReturnChildren(maze, node, idIterator,problem):
    children = []
    expand = [-1,1]
    for x in expand:
        if node.state[0]+x <= maze[0] and node.state[0]+x >= 0 and node.state[1] <= maze[1] and node.state[1] >= 0:
            if x == -1:
                direction = "w"
            elif x == 1:
                direction = "e"
            children.append(Node([node.state[0]+x,node.state[1]],node, direction, next(idIterator),
                                 returnManhanttanDistance(problem["snake_locations"][0], [node.state[0]+x,node.state[1]]), 
                                 returnManhanttanDistance([node.state[0]+x,node.state[1]], problem["food_locations"][0])))
    for y in expand:
        if node.state[0] <= maze[0] and node.state[0] >= 0 and node.state[1]+y <= maze[1] and node.state[1]+y >= 0:
            if y == -1:
                direction = "n"
            elif y == 1:
                direction = "s"
            children.append(Node([node.state[0],node.state[1]+y],node, direction, next(idIterator),
                                  returnManhanttanDistance(problem["snake_locations"][0], [node.state[0],node.state[1]+y]), 
                                  returnManhanttanDistance([node.state[0],node.state[1]+y], problem["food_locations"][0])))
    print("return child")
    return children
def returnManhanttanDistance(fromNode, toNode):
    distance = abs(toNode[0] - fromNode[0]) + abs(toNode[1] - fromNode[1])
    return distance

def appendAndSort(frontier, node):
  print("Fcost: ", node.fCost)
  duplicated = False
  removed = False
  for i, f in enumerate(frontier):
    if f.state == node.state:
      duplicated = True
      if f.fCost > node.fCost:
        del frontier[i]
        removed = True
        break    
  if (not duplicated) or removed:
    insert_index = len(frontier)
    for i, f in enumerate(frontier):
      if f.fCost > node.fCost:
        insert_index = i
        break
    frontier.insert(insert_index, node)
  return frontier

if __name__ == "__main__":
  p1 = Player({ "maze_size": [10,10], "static_snake_length": True })
  sol, st = p1.run({'snake_locations': [[2,5],[3,5],[4,5],[5,5],[6,5],[7,5],[8,5],[8,6],[8,7],[8,8],[7,8],[6,8],[5,8],[4,8],[3,8],[2,8],[1,8]], 'current_direction': 'e', 'food_locations': [[9, 9]]})
  print("Solution is:", sol)
  print("Search tree is:")
  print(st)