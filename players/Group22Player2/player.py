import random
class Node: 
  def __init__(self, state = None, parent=None, direction=None):
    self.state = state
    self.parent = parent 
    self.direction = direction 
    self.children = []

  def addChildren(self, children): 
    self.children.extend(children)

class Player():
  name = "Uninformed Search (BFS)"
  group = "Caffeine"
  members = [
    ["Pan Chen Soon", "17071549"],
    ["Pan Chen Pong", "16087520"],
    ["Tan Sze Qin", "18037259"]
  ]
  informed = False  
  
  def __init__(self, setup):
    # setup = {
    #   maze_size: [int, int],
    #   static_snake_length: bool
    # }
    self.setup = setup
    self.maze_size = self.setup["maze_size"]



  def run(self, problem):
    # problem = {
    #   snake_locations: [[int,int],[int,int],...],
    #   current_direction: str,
    #   food_locations: [[int,int],[int,int],...],
    # }
    solution = []
    # children = []
    directions = "nswe"
    explored = []
    frontier = []
    expansionSequence = 1
    search_tree = []
    search_tree.append({
        'id': 1, 
        'expansion_sequence': 1, 
        'state': problem["snake_locations"][0], 
        'children': [],
        'actions': [], 
        'removed': False, 
        'parent': None
      })
  
    #append the snake location into the frontier
    frontier.append(Node(problem["snake_locations"][0], None))
    found_goal = False
    # actions dict to be loop later when expanding the node
    actions = {"n": [0, -1], "s": [0, 1], "w": [-1, 0], "e": [1, 0]}

    while not found_goal:
      children = []
      print("Expansion Sequence", expansionSequence) 
      expansionSequence = expansionSequence + 1
      print("Current Node: ", frontier[0].state)

      # loop all the actions in the actions dict to expand the node. 
      for x in actions: 
        new_position = [frontier[0].state[0] + actions[x][0], frontier[0].state[1] + actions[x][1]]
        if not (new_position[0] < 0 or new_position[0] > self.maze_size[1]-1 or new_position[1]<0  or new_position[1] > self.maze_size[0]-1):
          children.append(Node(new_position, frontier[0].state, x))
      
      frontier[0].addChildren(children)
      explored.append(frontier[0])
      print("Children of Current Node: ", [f.state for f in children])

      for child in children: 
        if not (child.state in [e.state for e in explored]) and not (child.state in [f.state for f in frontier]): 
            if child.state == problem["food_locations"][0]:
              found_goal = True 
              goalie = child
            frontier.append(child)
      
      del frontier[0]
      print("Direction: ", [f.direction for f in frontier])
      print("States in Frontier: ", [f.state for f in frontier])
      print()

    path = [goalie.direction]
    while goalie.parent is not None: 
      path.insert(0, goalie.direction)
      for e in explored: 
        if e.state == goalie.parent: 
          goalie = e 
          break
    del path[-1]
    solution = path
    
    return solution, search_tree


if __name__ == "__main__":
  p1 = Player({ "maze_size": [10,10], "static_snake_length": True })
  sol, st = p1.run({'snake_locations': [[1, 6]], 'current_direction': 'e', 'food_locations': [[6, 7]]})
  print("Solution is:", sol)
  print("Search tree is:")
  print(st)
