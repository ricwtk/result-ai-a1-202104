import numpy as np
import random
class Node:
  def __init__(self, state=None, parent=None):
    self.id = None
    self.state = state
    self.expansionSequence = None
    self.children = []
    self.actions = []
    self.removed = False
    self.parent = parent
    self.euDist = None
    
class Player():
  name = "Player Greedy"
  group = "Goodbye World"
  members = [
    ["Lim Han Shen", "18124693"],
    ["Brandon Wong", "17097692"],
    ["Bryan Tan", "17083445"],
    ["Yeoh Qing Tuan", "18002220"],
  ]
  informed = True

  def __init__(self, setup):
    #setup = {
    #   maze_size: [int,int],
    #   static_snake_length: bool
    #}
    self.setup = setup
    self.grid_size = self.setup["maze_size"]
    self.state_space = []


  #function for greedy breadth-first search
  def greedy_search(self, snake_location, food_location):
    self.state_space = []
    search_tree = []
    frontier = []
    explored = []
    found_goal = False
    solution = []
    goal_node = None
    flag = 0
    validNodes = []

    expansion_count = 1
    node_count = 1

    for row in range(0, self.grid_size[0]):
      self.state_space.append([])
      for col in range(0, self.grid_size[1]):
        self.state_space[row].append(Node([row, col], None))

    root = Node(state=snake_location[0], parent=None)
    root.id = 1
    root.expansionSequence = 1
    root.euDist = self.getEuclideanDist(root, food_location)
    
    frontier.append(root)    

    while not found_goal:
      if len(frontier) == 0:
        # tries to move snake step by step until the food is reachable
        solution, validNodes = self.moveStep(explored, root)
        print(solution)
        search_tree = self.buildSearchTree(validNodes)
        break
      
      frontier[0].expansionSequence = expansion_count
      expansion_count = expansion_count + 1
      
      #test for goal while expanding node
      if frontier[0].state in food_location:
        goal_node = frontier[0]
        child = goal_node
        # loop to return solution in string format
        while not child.parent == None:
          solution.insert(0, self.convertToDirection(child, child.parent))
          child = child.parent
        found_goal = True
        explored.append(goal_node)

        # since informed search does not expand all its nodes
        # this loop appends all the unexplored nodes to build search tree
        for f in frontier:
          explored.append(f)
        
        # checks to build search tree for only valid nodes or a full tree
        if flag == 1:
          search_tree = self.buildSearchTree(validNodes)
        else:
          search_tree = self.buildSearchTree(explored)
        break

      # expanding node and fetching children
      children = self.fetchChildren(self.state_space, frontier[0])

      # loop to assign details for each node
      for child in children:
        child.id = node_count + 1
        node_count = node_count + 1
        frontier[0].children.append(child.id)
        frontier[0].actions.append(self.convertToDirection(child, frontier[0]))
        child.euDist = self.getEuclideanDist(child, food_location)

      # copy the node to the explored set
      explored.append(frontier[0])
      
      # remove the expanded frontier
      del frontier[0]

      # loop to obtain sorted and updated frontier
      for child in children:
        # check if a node was expanded or generated previously
        if not (child.state in [e.state for e in explored]):
          # add and sort children into the frontier
          frontier = self.sortFrontier(child, frontier)
          
    return solution, search_tree


  # Heuristic function; to calculate Euclidean Distance of each node to goal
  def getEuclideanDist(self, currentNode, goal_state):
    node = np.array((currentNode.state[0], currentNode.state[1]))
    goal = np.array((goal_state[0][0], goal_state[0][1]))
    
    dist = np.linalg.norm(node - goal)

    return dist


  # function to arrange the frontier based on ascending Euclidean Distance
  def sortFrontier(self, currentNode, frontier):
    dupe = False

    # filters out duplicates and nodes with larger Euclidean Distance
    for i, f in enumerate(frontier):
      if f.state == currentNode.state:
        duplicated = True

    # find the index where the current node should be inserted
    if not dupe:
      index = len(frontier)
      for i, f in enumerate(frontier):
        if f.euDist > currentNode.euDist:
          index = i
          break
      frontier.insert(index, currentNode)
      
    return frontier

  
  def fetchChildren(self, state_space, node):
    children = []
    node_coord = node.state
    #print(node_coord)
    x = node_coord[0]
    y = node_coord[1]
    
    #check if north node exists; if yes, add child
    if self.isValidNode([x, y+1]):
      state_space[x][y+1].parent = node
      children.append(state_space[x][y+1])
      
    #check if south node exists; if yes, add child
    if self.isValidNode([x, y-1]):
      state_space[x][y-1].parent = node
      children.append(state_space[x][y-1])

    #check if west node exists; if yes, add child
    if self.isValidNode([x-1, y]):
      state_space[x-1][y].parent = node
      children.append(state_space[x-1][y])

    #check if east node exists; if yes, add child
    if self.isValidNode([x+1, y]):
      state_space[x+1][y].parent = node
      children.append(state_space[x+1][y])

    return children
  
      
  #function to check move validity
  def isValidNode(self, coordinates):
    x = coordinates[0]
    y = coordinates[1]
    validity = False

    # checks if node is out of bounds and if it has been assigned a parent
    if (-1 < x < self.grid_size[0]) and (-1 < y < self.grid_size[1]):
      if self.state_space[x][y].parent==None:
        validity = True
    
    # checks to avoid snake from clashing with its body
    if (coordinates in self.snake_locations):
      validity = False

    return validity


  # uses currentNode coordinates to identify direction to their parents
  def convertToDirection(self, currentNode, parent):
    move = ""
    
    if (currentNode.state[1]-parent.state[1] == -1):
      move = "n"
      
    if (currentNode.state[1]-parent.state[1] == 1):
      move = "s"

    if (currentNode.state[0]-parent.state[0] == -1):
      move = "w"

    if (currentNode.state[0]-parent.state[0] == 1):
      move = "e"

    return move


  def moveStep(self, explored, root):
    availableSteps = []
    validNodes = []
    random_step = []

    for child in root.children:
      for e in explored:
        if child == e.id:
          e.expansionSequence = None
          validNodes.append(e)
          availableSteps.append(self.convertToDirection(e, root))
        
    random_step.append(random.choice(availableSteps))
    validNodes.append(root)
    
    return random_step, validNodes


  # builds the search tree using the explored list
  def buildSearchTree(self, exploredList):
    search_tree = []
    
    for e in range(len(exploredList)-1, -1, -1):
      if exploredList[e].parent == None:
        search_tree.insert(0,
        {
          "id": exploredList[e].id,
          "state": exploredList[e].state,
          "expansionsequence": exploredList[e].expansionSequence,
          "children": exploredList[e].children,
          "actions": exploredList[e].actions,
          "removed": exploredList[e].removed,
          "parent": None
        }
      )
      else:
        search_tree.insert(0,
          {
            "id": exploredList[e].id,
            "state": exploredList[e].state,
            "expansionsequence": exploredList[e].expansionSequence,
            "children": exploredList[e].children,
            "actions": exploredList[e].actions,
            "removed": exploredList[e].removed,
            "parent": exploredList[e].parent.id
          }
        )
    return search_tree

  
  def run(self, problem):
    #problem = {
    #snake_locations: [[int,int],[int,int],...], #body of snake
    #current_direction: str,
    #food_locations: [[int,int],[int,int],...], #can have > 1 food
    #}
    self.snake_locations = problem["snake_locations"]
    solution, search_tree = self.greedy_search(problem["snake_locations"],problem["food_locations"])
    directions = "nswe"

    # this function should return the solution and the search_tree
    return solution, search_tree


#temporary main function for testing
if __name__ == "__main__":
  p1 = Player({ "maze_size": [10,10], "static_snake_length": True })
  sol, st = p1.run({'snake_locations': [[0, 5]], 'current_direction': 'e', 'food_locations': [[6, 7]]})
  print("Solution is:", sol)
  print("Search tree is:")
  for t in st:
    print(t)
