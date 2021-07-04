# import random

class Player():
  name = "Uninformed Search - player 2 bfs"
  group = "walao"
  members = [
    ["Ong Yu Mhing", "18098517"],
    ["Tristan Elisha Chong Ze Han", "18125799"],
    ["Chuah Kim Hooi", "18123588"],
    ["Tan Ju Bhin", "15025034"]
  ]
  informed = False

  def __init__(self, setup):
  # setup = {
  #   maze_size: [int, int],
  #   static_snake_length: bool
  # }
    self.setup = setup


  def addChildren(self, children):
    self.children.extend(children)

        
  def run(self, problem):
    self.problem = problem
     # problem = {
     #   snake_locations: [[int,int],[int,int],...],
     #   current_direction: str,
     #   food_locations: [[int,int],[int,int],...],
     # }
    solution = []
    search_tree = []
    food = []
    snake = []
     ##gather food and snake location starting value 
    for key, value in problem.items():
        if key == 'food_locations':
             food = value
        if key == 'snake_locations':
             snake = value
     
     #For every other food pallet
    print(','.join(map(str,snake)),food)
 
    for key, value in self.setup.items():
        if key == 'maze_size':
             maze = value
     
     ##All states neighbour
    state_space = []
    for x in range (maze[0]):
        for y in range (maze[1]):
            value1 = [x,y]
            value2 = [x,y+1]
            value3 = [x+1,y]
            a = ','.join(map(str,value1))
            b = ','.join(map(str, value2))
            c = ','.join(map(str,value3))
            state_space.append([a,b,1])
            state_space.append([a,c,1])
            
    ##Prevent error when no path is available
    try:
        [answer, cost, tree] = bfs(state_space, ','.join(map(str,snake[0])), ','.join(map(str,food[0])), snake)
    
        print("Food: ", food)
            
        ##Change back to integers
        coord_int = []
        for coord in answer:
            ##Split the string and convert to int
            actual_coord = list(map(int, coord.split(',')))
            coord_int.append(actual_coord)
        ##Compare to see direction
        for coord1 in range(len(coord_int)):
            for coord2 in range(coord1 + 1, len(coord_int)):
                ##Side by side comparison only
                if coord2 == coord1 + 1:
                    ##Check if column same
                    if coord_int[coord1][0] == coord_int[coord2][0]:
                        ##Check if N or S
                        if  coord_int[coord1][1] > coord_int[coord2][1]:
                            direction = 'n'
                        else:
                            direction = 's'
                    else:
                        ##Check if W or E
                        if  coord_int[coord1][0] > coord_int[coord2][0]:
                            direction = 'w'
                        else:
                            direction = 'e'         
                    solution.append(direction)
        
        search_tree = tree
    
         
         ##Expansion Sequence
        expseq = 0
        for state in answer:
            # print(state)
            node_item = 0
            for node in tree:
                for key, value in node.items():
                    if (key == "state") and (value == state):
                        expseq += 1
                        dictvalue = {"expansionsequence": expseq}
                        # print("Test search")
                        # print(key, value, state, node_item)
                        search_tree[node_item].update(dictvalue)
                        # print(search_tree[node_item])
                        
                node_item += 1
        # print(answer)
        
    #Catch when theres no more ways to move
    except Exception as e:
        print(e)
        solution = ['n']
        search_tree = []
        
    print("Solution: ",solution)
    return solution, search_tree
    
class Node:
  def __init__(self, state=None, parent=None):
    self.state = state
    self.parent = parent
    self.children = []

  def addChildren(self, children):
    self.children.extend(children)

def expandAndReturnChildren(state_space, node):
  children = []
  for [m,n,c] in state_space:
    if m == node.state:
      children.append(Node(n, node.state))
    elif n == node.state:
      children.append(Node(m, node.state))
  return children

def bfs(state_space, initial_state, goal_state,snake):
    
  ##Prevent snake from going to places its body was at
  temp = []
  for index, value in enumerate(state_space):
      a = value[0]
      b = value[1]
      c = list(map(int, a.split(',')))
      d = list(map(int, b.split(',')))
      temp.append([c,d])
    
  new_sp = []
  for index, point in enumerate(temp):
    for i in snake[1:]:
        if i in point:
            new_sp.append(index)
    
  temp2 = []    
  for i in (new_sp):
      temp2.append(state_space[i])
     
  for s in temp2:
      if s in state_space:
          state_space.remove(s)
  
    
  frontier = []
  explored = []
  found_goal = False
  goalie = Node()
  solution = []
  # add initial state to frontier
  frontier.append(Node(initial_state, None))
  bfs_search_tree = []
  loop = 0
  # expanded_on = 0
  child_id = 1
  parent_value = []
  while not found_goal:
    loop += 1
    ##Create a copy that doesnt change from initial copy object
    old_frontier = frontier.copy()

    # expand the first in the frontier
    children = expandAndReturnChildren(state_space, frontier[0])
    # add children list to the expanded node
    frontier[0].addChildren(children)
    # add to the explored list
    explored.append(frontier[0])
    # remove the expanded frontier
    del frontier[0]
    # add children to the frontier
    print("old_frontier: ", [o.state for o in old_frontier])
    childs_parent = 0
    for child in children:
      # check if a node was expanded or generated previously
      if not (child.state in [e.state for e in explored]) and not (child.state in [f.state for f in frontier]):
        childs_parent += 1
        # goal test
        if child.state == goal_state:
          found_goal = True
          goalie = child
        frontier.append(child)
        
        
        ##Break if no solution found
    if [f.state for f in frontier] == [] and found_goal == False:
        solution = []
        if loop == 1:            
            solution.append(explored[0].state)
            solution.append(frontier[0].state)
        else:
            solution.append(explored[0].state)
            solution.append(explored[1].state)    
        path_cost = 0
        bfs_search_tree = []
        print("No Path Found")
        return solution, path_cost, bfs_search_tree
    
    print("Explored:", [e.state for e in explored])
    print("Frontier:", [f.state for f in frontier])
    print("Children:", [c.state for c in children])
    # print("old_frontier: ", [o.state for o in old_frontier])
    print("")
    parent_value.append(childs_parent)
    ##Check direction of children
    search_visit = [e.state for e in explored]
    search_child = [c.state for c in children if not (c.state in [o.state for o in old_frontier]) and not (c.state in [e.state for e in explored])]
    print(search_child)
    search_action = []
    search_child_id = []
    for kid in search_child:
        ##Check if column same
        #Kid and search_visit uses string, has (val, ',', val)
      if kid[0] == search_visit[loop - 1][0]:
            ##Check if N or S
        if  kid[2] > search_visit[loop - 1][2]:
            direction = 's'
        else:
            direction = 'n'
      else:
            ##Check if W or E
        if  kid[0] > search_visit[loop - 1][0]:
            direction = 'e'
        else:
            direction = 'w'  
      search_action.append(direction)
      child_id += 1
      search_child_id.append(child_id)


    ##Parent
    if loop == 1:
        search_parent = None
    if loop == 2:
        search_parent = 1
        parent_value[0] += 1
    ##Saving the search tree values
    bfs_search_tree.append(
        {
        "id": loop,
        "state": search_visit[loop - 1],
        "expansionsequence": 0,
        "children": search_child_id,
        "actions": search_action,
        "removed": False,
        "parent": search_parent
      }
    )
    # print(bfs_search_tree)
    ##Checking if expanded

    if parent_value[0] != 1:
        parent_value[0] -= 1
    else:
        del parent_value[0]
        if search_parent != None:
            search_parent += 1
   

  ##Not in while loop
  solution = [goalie.state]
  path_cost = 0
  while goalie.parent is not None:
    solution.insert(0, goalie.parent)
    for e in explored:
      if e.state == goalie.parent:
        path_cost += getCost(state_space, e.state, goalie.state)
        goalie = e
        break
  return solution, path_cost, bfs_search_tree
  
def getCost(state_space, state0, state1):
  for [m,n,c] in state_space:
    if [state0,state1] == [m,n] or [state1,state0] == [m,n]:
      return c
  
    
  
if __name__ == "__main__":
  p1 = Player({ "maze_size": [10,10], "static_snake_length": True })
  sol, st = p1.run({'snake_locations': [[0, 5]], 'current_direction': 'e', 'food_locations': [[16, 7]]})
  print("Solution is:", sol)
  print("Search tree is:")
  # print(st)