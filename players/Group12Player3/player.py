import random
class Node:
  def __init__(self, state=None, parentstate=None, parentdirection = None, direction = None, numberparent = None, cost = None):
    self.state = state
    self.parentstate = parentstate
    self.parentdirection = parentdirection
    self.direction = direction
    self.numberparent = numberparent
    self.cost = cost
    self.children = []

  def addChildren(self, children):
    self.children.extend(children)

def expandAndReturnChildren(node):
    children = []
    if node.direction == "n":
      children.append(Node([node.state[0]+1,node.state[1]], node.state, node.direction, "e", node.numberparent + 1, None))
      children.append(Node([node.state[0]-1,node.state[1]], node.state, node.direction, "w", node.numberparent + 1, None))
      children.append(Node([node.state[0],node.state[1]-1], node.state, node.direction, "n", node.numberparent + 1, None))
    if node.direction == "s":
      children.append(Node([node.state[0]+1,node.state[1]], node.state, node.direction, "e", node.numberparent + 1, None))
      children.append(Node([node.state[0]-1,node.state[1]], node.state, node.direction, "w", node.numberparent + 1, None))
      children.append(Node([node.state[0],node.state[1]+1], node.state, node.direction, "s", node.numberparent + 1, None))
    if node.direction == "e":
      children.append(Node([node.state[0]+1,node.state[1]], node.state, node.direction, "e", node.numberparent + 1, None))
      children.append(Node([node.state[0],node.state[1]+1], node.state, node.direction, "s", node.numberparent + 1, None))
      children.append(Node([node.state[0],node.state[1]-1], node.state, node.direction, "n", node.numberparent + 1, None))
    if node.direction == "w":
      children.append(Node([node.state[0]-1,node.state[1]], node.state, node.direction, "w", node.numberparent + 1, None))
      children.append(Node([node.state[0],node.state[1]+1], node.state, node.direction, "s", node.numberparent + 1, None))
      children.append(Node([node.state[0],node.state[1]-1], node.state, node.direction, "n", node.numberparent + 1, None))
    return children

def appendAndSort(frontier, node):
  duplicated = False
  removed = False
  for i, f in enumerate(frontier):
    if f.state == node.state:
      duplicated = True
      if f.cost > node.cost:
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

def dict(node, expandsequence, childrenid):
  stringstate = ",".join([str(n) for n in node.state])
  if node.direction == "n":
    action = ["e", "w","n"]
  if node.direction == "s":
    action = ["e", "w", "s"]
  if node.direction == "e":
    action = ["e", "s", "n"]
  if node.direction == "w":
    action = ["w", "s", "n"]
  ststore = {"id": id(node), 
            "state": stringstate, 
            "expansionsequence": expandsequence,
            "children": childrenid, 
            "actions": action, 
            "removed": False,
            "parent": node.numberparent}
  return ststore

def getcost(node, foodlocation):
  distancex = abs(node.state[0]- foodlocation[0])
  distancey = abs(node.state[1]-foodlocation[1])
  cost = distancex + distancey

  return cost

class Player():
  name = "GBFS"
  group = "Ais Teh"
  members = [
    ["Hassan Azwaan", "18086157"],
    ["Lim Chze Yee", "16034357"],
    ["Khor Li Heng", "19014885"]
  ]
  informed = True

  def __init__(self, setup):
    # setup = {
    #   maze_size: [int, int],
    #   static_snake_length: bool
    # }
    self.setup = setup
  
  def run(self, problem):
    frontier = []
    explored = []
    found_goal = False
    goalie = Node()
    solution = []
    expentionsequnce = 0
    search_tree = []
    childrenid =[]
  

    initial_state = problem["snake_locations"][0]
    initial_direction = problem["current_direction"][0]
    goal_state = problem["food_locations"][0]
    initialcost = getcost(Node(initial_state,None, None, initial_direction, 0, None), goal_state)
    frontier.append(Node(initial_state,None, None, initial_direction, 0, initialcost))

    while not found_goal:
      if frontier[0].state == goal_state:
        found_goal = True
        goalie = frontier[0]
        break
    # expand the first in the frontier
      children = expandAndReturnChildren(frontier[0])
    # add children list to the expanded node
      frontier[0].addChildren(children)
      for x in children:
        childrenid.append(id(x))
        x.cost = getcost(x, goal_state)
      expentionsequnce = expentionsequnce + 1
      diction = dict(frontier[0],expentionsequnce, childrenid)
    # add to the explored list
      explored.append(frontier[0])
      search_tree.append(diction)
    # remove the expanded frontier
      del frontier[0]
    # add children to the frontier
      for child in children:
      # check if a node was expanded or generated previously
        if not (child.state in [e.state for e in explored]) and not (child.state in [f.state for f in frontier])and child.state[0]>=0 and child.state[1]>=0 and child.state[0]<=9 and child.state[1]<=9 :
          frontier = appendAndSort(frontier, child)
      print("Explored:", [e.state for e in explored])
      print("Frontier:", [(f.state, f.cost) for f in frontier])
      print("Children:", [c.state for c in children])
      print("")
  
    path = [goalie.state]
    solution = [goalie.direction]

    while goalie.parentstate is not None:
      path.insert(0, goalie.parentstate)
      solution.insert(0, goalie.parentdirection)
      for e in explored:
        if e.state == goalie.parentstate:
          goalie = e
          break
    print (path)
    del solution[0]
    print (solution)
    search_tree = []

    # the following search tree is a static search tree 
    # to show you the format of the variable 
    # to generate a search tree that can be displayed in the frontend.
    # you are required to generate the search tree based on your search algorithm
    # this function should return the solution and the search_tree
    return solution, search_tree


if __name__ == "__main__":
  p1 = Player({ "maze_size": [10,10], "static_snake_length": True })
  sol, st = p1.run({'snake_locations': [[0, 5]], 'current_direction': 'e', 'food_locations': [[3, 7]]})
  print("Solution is:", sol)
  print("Search tree is:")
  print(st)
  
