import numpy as np

class Node:
  def __init__(self, state=None, parent=None):
    self.id = None
    self.state = state
    self.expansionSequence = None
    self.children = []
    self.parent = parent
    self.actions = []
    self.removed = False
    
class Player():
  name = "Informed Search"
  group = "Salla Kutta"
  members = [
    ["Isaac Lim Nyit Wang", "17045378"],
    ["Keven Tai Yuan Tian", "17035023"],
    ["Shankarnivash Rao", "18007930"],
  ]
  informed = True

  def __init__(self, setup):
    #setup = {
    #   maze_size: [int,int],
    #   static_snake_length: bool
    #}
    self.setup = setup
    self.grid = self.setup["maze_size"]
    self.state_space = []


  #function for greedy best first search
  def greedy_bfs(self, snake_location, food_location):
    self.state_space = []
    frontier = []
    explored = []
    found_goal = False
    solution = []
    goal_node = None

    snake_length = 1
    node_count = 1

    for row in range(0, self.grid[0]):
      self.state_space.append([])
      for col in range(0, self.grid[1]):
        self.state_space[row].append(Node([row, col], None))

    root = Node(state=snake_location[0], parent=None)
    root.id = 1
    root.expansionSequence = 1
    
    frontier.append(root)    

    while not found_goal:
      frontier[0].expansionSequence = snake_length
      snake_length = snake_length + 1
      
      #goal testing during node expansion
      if frontier[0].state == food_location[0]:
        goal_node = frontier[0]
        child = goal_node
        while not child.parent == None:
          solution.insert(0, self.convertToDirection(child, child.parent))
          child = child.parent
        found_goal = True
        explored.append(goal_node)

        # informed search not expanding all of its nodes
        for f in frontier:
          explored.append(f)
        
        search_tree_method = self.buildSearchTree(explored)
        break
      
      # loop to append details for each node
      for child in children:
        child.id = node_count + 1
        node_count = node_count + 1
        frontier[0].children.append(child.id)
        frontier[0].actions.append(self.convertToDirection(child, frontier[0]))

      explored.append(frontier[0])
      
      # delete the expanded frontier
      del frontier[0]

      # obtain sorted frontier
      for child in children:
        if not (child.state in [e.state for e in explored]):
          # add children into the frontier
          frontier = self.sortFrontier(child, frontier)
          
    return solution, 

  
  def ChildrenNode(self, state_space, node):
    children = []
    node_coordinate = node.state
    
    #check if north node exists; if yes, add child
    if self.isValidNode([node_coordinate[0], node_coordinate[1]+1]):
      state_space[node_coordinate[0]][node_coordinate[1]+1].parent = node
      children.append(state_space[node_coordinate[0]][node_coordinate[1]+1])
      
    #check if south node exists; if yes, add child
    elif self.isValidNode([node_coordinate[0], node_coordinate[1]-1]):
      state_space[node_coordinate[0]][node_coordinate[1]-1].parent = node
      children.append(state_space[node_coordinate[0]][node_coordinate[1]-1])

    #check if west node exists; if yes, add child
    elif self.isValidNode([node_coordinate[0]-1, node_coordinate[1]]):
      state_space[node_coordinate[0]-1][node_coordinate[1]].parent = node
      children.append(state_space[node_coordinate[0]-1][node_coordinate[1]])

    #check if east node exists; if yes, add child
    elif self.isValidNode([node_coordinate[0]+1, node_coordinate[1]]):
      state_space[node_coordinate[0]+1][node_coordinate[1]].parent = node
      children.append(state_space[node_coordinate[0]+1][node_coordinate[1]])

    return children
  
      
  #function to check move validity
  def isValidNode(self, coordinates):
    x = coordinates[0]
    y = coordinates[1]
    validity = False

    # checks if node is out of bounds and if it has been assigned a parent
    if (-1 < x < self.grid[0]) and (-1 < y < self.grid[1]):
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

  def run(self, problem):
    #problem = {
    #snake_locations: [[int,int],[int,int],...], #body of snake
    #current_direction: str,
    #food_locations: [[int,int],[int,int],...], #can have > 1 food
    #}
    self.snake_locations = problem["snake_locations"]
    solution = self.greedy_bfs(problem["snake_locations"],problem["food_locations"])
    directions = "nswe"
    search_tree = [
      {
        "id": 1,
        "state": "0,0",
        "expansionsequence": 1,
        "children": [2,3,4],
        "actions": ["n","w","e"],
        "removed": False,
        "parent": None
      },
      {
        "id": 2,
        "state": "5,0",
        "expansionsequence": 2,
        "children": [5,6,7],
        "actions": ["n","s","w"],
        "removed": False,
        "parent": 1
      },
      {
        "id": 3,
        "state": "0,3",
        "expansionsequence": -1,
        "children": [],
        "actions": [],
        "removed": False,
        "parent": 1
      },
      {
        "id": 4,
        "state": "0,4",
        "expansionsequence": -1,
        "children": [],
        "actions": [],
        "removed": False,
        "parent": 1
      },
      {
        "id": 5,
        "state": "5,0",
        "expansionsequence": -1,
        "children": [],
        "actions": [],
        "removed": True,
        "parent": 2
      },
      {
        "id": 6,
        "state": "5,3",
        "expansionsequence": -1,
        "children": [],
        "actions": [],
        "removed": False,
        "parent": 2
      },
      {
        "id": 7,
        "state": "1,0",
        "expansionsequence": -1,
        "children": [],
        "actions": [],
        "removed": False,
        "parent": 2
      }
    ]
    
    # return solution,search tree # lecturer commented
    return solution,search_tree # lecturer added
    


#temporary main function for testing
if __name__ == "__main__":
  p1 = Player({ "maze_size": [10,10], "static_snake_length": True })
  sol, bfs = p1.run({'snake_locations': [[0, 5]], 'current_direction': 'e', 'food_locations': [[6, 7]]})
  print("Solution is:", sol)
  print("Search tree is:")
  for b in bfs:
    print(b)

