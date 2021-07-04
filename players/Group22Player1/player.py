import random
class Node: 
  def __init__(self, state=None, parent=None, direction=None, cost=0): 
    self.state= state
    self.parent = parent
    self.direction = direction
    self.children = []
    self.cost = cost
  
  def addChildren(self, children): 
    self.children.extend(children)
    
class Player():
  name = "Informed Search (GBFS)"
  group = "Caffeine"
  members = [
    ["Pan Chen Soon", "17071549"],
    ["Pan Chen Pong", "16087520"],
    ["Tan Sze Qin", "18037259"]
  ]
  informed = True

  def __init__(self, setup):
    # setup = {
    #   maze_size: [int, int],
    #   static_snake_length: bool
    # }
    self.setup = setup
    self.temp = []
    self.frontier = [] 
    self.explored = [] 
    self.search_tree = []
    self.id = 1
    self.grid_size = self.setup["maze_size"]
    self.state_space = []

  def sort (self, child): 
    duplicated = False

    for i, f in enumerate (self.frontier): 
      if f.state == child.state: 
        duplicated = True

    if not duplicated: 
      index = len(self.frontier)
      for i, f in enumerate(self.frontier): 
        if child.cost < f.cost: 
          index = i 
          break 
      self.frontier.insert(index, child)

      
  def run(self, problem):
    self.state_space = []
    self.frontier=[]
    solution = [] 
    directions = "nswe"
    explored = [] 
    children = []
    search_tree = []
    
    found_goal = False
    actions = {"n": [0, -1], "s": [0, 1], "w": [-1, 0], "e": [1, 0]}
    expansion_sequence = 0

    goal_node = problem["food_locations"][0]
    self.frontier.append(Node(problem["snake_locations"][0],None, None))

    while not found_goal: 
      current_node_children = []
      if self.frontier[0].state == problem["food_locations"][0]:
        found_goal= True
        goalie = self.frontier[0]
        break

      for x in actions: 
        new_position = [self.frontier[0].state[0] + actions[x][0], self.frontier[0].state[1] + actions[x][1]]
        cost = (abs(goal_node[0] - new_position[0]) + abs(goal_node[1] - new_position[1]))

        if not (new_position[1] < 0 or new_position[1] > self.grid_size[0]-1 or new_position[0] < 0 or new_position[0] > self.grid_size[1]-1):
          children.append(Node(new_position, self.frontier[0].state, x, cost))
          current_node_children.append(Node(new_position, self.frontier[0].state, x, cost))

      expansion_sequence += 1

      self.frontier[0].addChildren(children)
      explored.append(self.frontier[0])

      for child in children: 
        if not (child.state in [e.state for e in explored]) and not (child.state in [f.state for f in self.frontier]):
            self.sort(child)
      for f in explored:
        if f in self.frontier:
          self.frontier.remove(f)

      print('expansion sequence:', expansion_sequence)
      print("parent:", [e.state for e in explored][-1])
      print("children:", [f.state for f in current_node_children])
      print('frontier:',[f.state for f in self.frontier])
      print('cost:',[f.cost for f in self.frontier])
      print('direction:',[f.direction for f in self.frontier])
      
      print()



    path = [goalie.direction]
    while goalie.parent is not None: 
      path.insert(0, goalie.direction)
      for e in explored: 
        if e.state == goalie.parent: 
          goalie = e 
          break
    del path[-1]
    print(path)
    solution = path

    return solution, search_tree

if __name__ == "__main__":
  p1 = Player({ "maze_size": [10,10], "static_snake_length": True })
  sol, st = p1.run({'snake_locations': [[int, int]], 'current_direction': 'e', 'food_locations': [[int, int]]})
  # print("Solution is:", sol)
  # print("Search tree is:")
  # print(st)