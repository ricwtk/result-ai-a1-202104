# Player class.
class Player():
  # Class variables.
  name = "Breadth-First Search (BFS) Algorithm"
  group = "Big bois"
  members = [
    ["Tan Hanley", "18033936"],
    ["Lim Shao Yong", "19052059"],
    ["Lau Zhen Yu", "18024182"],
    ["Keanu Tan Soon Jie", "18020552"]
    # } # lecturer commented
  ]
  informed = False

  # Class constructor.
  def __init__(self, setup):
    self.setup = setup
  
  # Takes a set of coordinates, and returns a list of children, representing the potential locations the snake can move to.
  def expandAndReturnChildren(self, state):
    # A variable which converts the distance between two points into a relevant direction (i.e. [0, 1] -> [0, 0] = "n").
    addDirection = [ ['n', [0, -1]], ['s', [0, 1]], ['w', [-1, 0]], ['e', [1, 0]] ]
    # Initialize an empty list to hold all potential locations that the snake can move to.
    children = []
    # Check if the four locations adjacent to the given coordinates are considered legal moves.
    # i.e. Given the coordinates [0, 5], the four potential locations are [0, 4], [0, 6], [-1, 5],
    # and [1, 5], however [-1, 5] is illegal because it moves outside the boundary of the maze.
    for i in range(4):
      if (state[-1][0] + addDirection[i][1][0]) >= 0 and (state[-1][1] + addDirection[i][1][1]) >= 0 and (state[-1][0] + addDirection[i][1][0]) <= 9 and (state[-1][1] + addDirection[i][1][1]) <= 9:
        children.append(state + [ [state[-1][0] + addDirection[i][1][0], state[-1][1] + addDirection[i][1][1]] ])
    
    return children

  # Takes the initial and goal states of the problem, and returns a solution and a search tree.
  def bfs(self, initial_state, goal_state):
    # Define initial variables to store future data.
    state = initial_state
    frontier = []
    explored = []
    solution = []
    found_goal = False
    frontier.append([state])

    # While the goal node is not reached, the top node of the frontier is explored.
    # For the first iteration of the expandAndReturnChildren() function, the initial state is used as an argument.
    while not found_goal:
      children = self.expandAndReturnChildren(frontier[0])
      explored.append(frontier[0][-1])
      del frontier[0]
      # Once the children of a parent node are obtained, check if each child is unique (has not been explored AND does not exist in the frontier).
      for child in children:
        if not (child[-1] in explored) and not (child[-1] in [f[-1] for f in frontier]): 
          if child[-1] == goal_state:
            found_goal = True
            solution = child

          frontier.append(child)
      
      # Print a list of explored nodes, the frontier, and all respective children.
      print("Explored: ")
      print(explored)
      print("Frontier:")
      for f in frontier:
        print(f)
      print("Children: ")
      print(children)
      print("")
    
    # Returns the solution in the form of ordered sets of coordinates, representing directions.
    return solution

  # Run method for the Player() class. Runs automatically in the front-end program.
  def run(self, problem):
    # Initialize the variables for the locations of the snake and food, etc.
    initial_state = problem["snake_locations"][0]
    goal_state = problem["food_locations"][0]
    coordinates = []
    solution = []
    addDirection = [ ['n', [0, -1]], ['s', [0, 1]], ['w', [-1, 0]], ['e', [1, 0]] ]
    directions = "nswe"
    coordinates = self.bfs(initial_state, goal_state)
    
    # Convert the coordinates provided by the solution variable into actual directions to be processed by the snake object.
    # i.e. [0, 5] -> [0, 4] = "n", [0, 5] -> [1, 5] = "e", etc.
    for c in range(len(coordinates)-1):
      temp = [coordinates[c+1][0] - coordinates[c][0], coordinates[c+1][1] - coordinates[c][1]]
      for a in addDirection:
        if temp == a[-1]:
          solution.append(a[0])

    # Generate a search tree.
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

    # Return the solution and the search tree.
    return solution, search_tree