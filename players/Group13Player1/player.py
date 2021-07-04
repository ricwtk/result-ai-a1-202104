import random #used for testing only

class Node:
  def __init__(self, state=None, parent=None):
    self.id = None
    self.state = state
    self.expansionSequence = None
    self.children = []
    self.actions = []
    self.removed = False
    self.parent = parent
    
class Player():
  name = "Player BFS"
  group = "Goodbye World"
  members = [
    ["Lim Han Shen", "18124693"],
    ["Brandon Wong", "17097692"],
    ["Bryan Tan", "17083445"],
    ["Yeoh Qing Tuan", "18002220"],
  ]
  informed = False

  def __init__(self, setup):
    #setup = {
    #   maze_size: [int,int],
    #   static_snake_length: bool
    #}
    self.setup = setup
    self.grid_size = self.setup["maze_size"]
    self.state_space = []


  #function for breadth-first search
  def bfs(self, snake_location, food_location):
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
    
    frontier.append(root)
    
    while not found_goal:
      # fetch the nodes identified as children
      try:
        children = self.fetchChildren(self.state_space, frontier[0])
      except:
        # tries to move snake step by step until the food is reachable        
        solution, validNodes = self.moveStep(explored, root)
        flag = 1
        break
      
      for n in range(0, len(children), 1):
        children[n].id = node_count + 1
        frontier[0].children.append(children[n].id)
        frontier[0].actions.append(self.convertToDirection(children[n], frontier[0]))

        node_count = node_count + 1
      
      # copy the node to the explored set
      explored.append(frontier[0])

      # adds the expansion sequence number only when node is expanded
      frontier[0].expansionSequence = expansion_count
      
      # remove the expanded frontier
      del frontier[0]
      
      expansion_count = expansion_count + 1
      
      # loop through the children
      for child in children:
        # check if a node was expanded or generated previously
        if not (child in explored) and not (child in frontier):
          explored.append(child)
          # goal test
          if child.state in food_location:
            goal_node = child
            # loop to return solution in string form
            while not child.parent == None:
              solution.insert(0, self.convertToDirection(child, child.parent))
              child = child.parent
            found_goal = True
            explored.append(goal_node)

          # add children to the frontier
          frontier.append(child)
    
    # checks to build search tree for only valid nodes or a full tree
    if flag == 1:
      search_tree = self.buildSearchTree(validNodes)
    else:
      search_tree = self.buildSearchTree(explored)
    
    return solution, search_tree


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
  
      
  #function to check coordinate validity
  def isValidNode(self, coordinates):
    #print(node.state[0])
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


  # used to randomly return one valid step at a time if solution not found
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
    solution, search_tree = self.bfs(problem["snake_locations"],problem["food_locations"])
    directions = "nswe"

    # this function should return the solution and the search_tree
    return solution, search_tree


#temporary main function for testing
if __name__ == "__main__":
  p1 = Player({ "maze_size": [10,10], "static_snake_length": True })
  snake_location = [0,5]

  sol, st = p1.run({'snake_locations': [snake_location], 'current_direction': 'e', 'food_locations': [[6,7]]})

  print("Solution is:", sol)
  print("Search tree is:")
  for t in st:
    print(t)
    
##  for i in range(5):
##    x = random.randint(0,4)
##    y = random.randint(0,4)
##    sol, st = p1.run({'snake_locations': [snake_location], 'current_direction': 'e', 'food_locations': [[x, y]]})
##    print("Snake: ", snake_location, "Food: [", x,y, "]")
##    print("Solution is:", sol)
##    print("Search tree is:")
##    for t in st:
##      print(t)
##    print()
##    snake_location = [x,y]
