class Node():
  def __init__(self, id, state=None, parent=None):
    self.id = id
    self.state = state #coordinates of the maze
    self.expansionSequence = -1
    self.children = [] #an array of IDs
    self.actions =  ["n","e","w","s"] 
    self.removed = False
    self.parent = parent #is an ID
    self.sld = None

  def addChildren(self, children):
    self.children.extend(children)

  def genSearchTree(self):
    st =  {
            "id": self.id,
            "state": self.state,
            "expansionsequence": self.expansionSequence,
            "children": self.children,
            "actions": self.actions,
            "removed": self.removed,
            "parent": self.parent
        }
    return st

class Player():
  name = "Greedy"
  group = "TBC"
  members = [
    ["Yan Yi Cheng", "17109505"],
    ["Ian How Yu Xuan", "18032649"],
    ["Christine Law Han Ni", "18056796"],
    ["Bryan Eeo Zhe Yu", "20016960"]
  ]
  informed = True

  def __init__(self, setup): #state space
    self.expansionSequence = 0
    self.setup = setup

  def heu(self, node, problem):
    dx = abs(node.state[0] - problem[0][0])
    dy = abs(node.state[1] - problem[0][1])
    d = dx+dy
    node.sld = d 
    return d
       
  def expandAndReturnChildren(self, id, node, body):
    id_counter = id
    children = []
    [maze_col, maze_row] = self.setup["maze_size"]
    [x, y] = node.state
    sd = body
    moveup = False
    movedown = False
    moveleft = False
    moveright = False

    # check for borders and snake body then remove unavailable actions
    if ( x == maze_col-1 or [x+1,y] in sd):
      moveright = True
    if ( x == 0 or [x-1,y] in sd):
      moveleft = True
    if ( y == maze_row-1 or [x,y+1] in sd):
      movedown = True
    if ( y == 0 or [x,y-1] in sd):
      moveup = True

    if moveup:
      node.actions.remove("n")
    
    if movedown:
      node.actions.remove("s")

    if moveleft:
      node.actions.remove("w")

    if moveright:
      node.actions.remove("e")
 
    # take action
    for direction in node.actions:

      if (direction == "n"):
        children.append(Node(id_counter, [x, y-1], node.id))
      elif (direction == "e"):
        children.append(Node(id_counter, [x+1, y], node.id))
      elif (direction == "w"):
        children.append(Node(id_counter, [x-1, y], node.id))
      elif (direction == "s"):
        children.append(Node(id_counter, [x, y+1], node.id))
      id_counter += 1

    self.expansionSequence += 1
    node.expansionSequence = self.expansionSequence

    children_id = [c.id for c in children]
    node.children = children_id
    return children

  def run(self, problem): #your search algorithm 
    
    id = 1
    frontier = []
    explored = []
    solution = []
    found_goal = False
    goal = problem["food_locations"][0]
    frontier.append(Node(id, problem["snake_locations"][0], None))
    id += 1
    search_tree = []

    # start of Greedy algorithm
    while not found_goal: 
      if frontier[0].state == goal: #goal test before expansion
        found_goal = True
        goalie = frontier[0]

      else:
        children = self.expandAndReturnChildren(id,frontier[0], problem["snake_locations"])
        explored.append(frontier[0])
        search_tree.append(frontier[0].genSearchTree())
        
        del frontier[0]
        id += len(children)

        # checking for redundant and loopy paths, then adding heuristics into each node
        for child in children:
          if not (child.state in [e.state for e in explored]) and not (child.state in [f.state for f in frontier]):
            distance = self.heu(child, problem["food_locations"])
            child.sld = distance
            frontier.append(child)
          
          else:
            child.removed = True
            search_tree.append(child.genSearchTree())

        # sorting frontier array based on shortest distance 
        frontier.sort(key= lambda n:n.sld)
  
    #search tree
    for i in frontier:
      search_tree.append(i.genSearchTree())

    # filling in solution array
    while goalie.parent is not None:      
      self.expansionSequence = 0
      for e in explored:
        if e.id == goalie.parent:
          index = e.children.index(goalie.id)
          solution.insert(0, e.actions[index])
          goalie = e
          break
    
    print("Solution: ",solution)
    print("SEARCH TREEEEEEEEEEEEEEEEEEEEEE")
    for i in search_tree:
      print(i)

    return solution, search_tree