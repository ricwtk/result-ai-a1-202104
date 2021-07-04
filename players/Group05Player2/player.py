class Player():
  name = "uninformed player"
  group = "Island Coders"
  members = [
    ["Muhammad Nabeel Rasheed Varsally", "19025634"],
    ["Raveesh Shibchurn", "19053156"],
    ["Yutashna Gunnoo", "19063304"],
    ["Eltigani Hamadelniel Elfatih", "17087610"]
  ]
  informed = False
  search_tree = []
  ids = 1
  xpansionsequence = 0

  def __init__(self, setup):
#     setup = {
#       maze_size: [int, int],
#       static_snake_length: bool
#     }
     self.setup = setup


  def getChildren(self,x,y):
      children = []
      children_direction = []
      xx = self.setup["maze_size"][0] - 1
      yy = self.setup["maze_size"][1] - 1
      if x == 0:
          if y == 0:
              children.append([x + 1, y])  # E
              children_direction.append("e")
              children.append([x, y + 1])  # S
              children_direction.append("s")
          elif y == (yy):
              children.append([x, yy - 1])  # N
              children_direction.append("n")
              children.append([x + 1, yy])  # E
              children_direction.append("e")
          else:
              children.append([x, y - 1])  # N
              children_direction.append("n")
              children.append([x + 1, y])  # E
              children_direction.append("e")
              children.append([x, y + 1])  # S
              children_direction.append("s")
      if y == 0:
          if x == 0:
              pass
          elif x == (xx):
              children.append([x - 1, y])  # W
              children_direction.append("w")
              children.append([x, y + 1])  # S
              children_direction.append("s")
          else:
              children.append([x + 1, y])  # E
              children_direction.append("e")
              children.append([x, y + 1])  # S
              children_direction.append("s")
              children.append([x - 1, y])  # W
              children_direction.append("w")
      if x == xx:
          if y == 0:
              pass
          elif y == yy:
              children.append([xx, yy - 1])  # N
              children_direction.append("n")
              children.append([xx - 1, yy])  # W
              children_direction.append("w")
          else:
              children.append([x, y - 1])  # N
              children_direction.append("n")
              children.append([x, y + 1])  # S
              children_direction.append("s")
              children.append([x - 1, y])  # W
              children_direction.append("w")
      if y == yy:
          if x == 0:
              pass
          elif x == xx:
              pass
          else:
              children.append([x, y - 1])  # N
              children_direction.append("n")
              children.append([x + 1, y])  # E
              children_direction.append("e")
              children.append([x - 1, y])  # W
              children_direction.append("w")
      if (0 < x < xx) & (0 < y < yy):
          children.append([x, y - 1])  # N
          children_direction.append("n")
          children.append([x + 1, y])  # E
          children_direction.append("e")
          children.append([x, y + 1])  # S
          children_direction.append("s")
          children.append([x - 1, y])  # W
          children_direction.append("w")

      return children, children_direction



  def getsolutionDirection(self,path_x,path_y,sol_x,sol_y):
      r1 = sol_x - path_x
      r2 = sol_y - path_y
      if r1 == 1:
        return "e"
      if r1 == -1:
        return "w"
      if r2 == 1:
          return "s"
      if r2 == -1:
        return "n"

  def generateSearchTree(self,x,y,px,py,children,children_direction):
      # block of code responsible for generating search tree
      Player.xpansionsequence += 1

      
      parent_state = str(px) + "," + str(py)
      # if the node is not the first one to be expanded and has a parent which is already in the search tree
      if len(Player.search_tree) != 0:
          for st in Player.search_tree:
              if  st["state"] == parent_state:
                  st["actions"] = children_direction
                  st["expansionsequence"] = Player.xpansionsequence
                  for c in children:
                      child_state = str(c[0]) + "," + str(c[1])
                      Player.search_tree.append(
                          {"id": Player.ids, "state": parent_state, "expansionsequence": -1, "children": [],
                           "actions": [], "removed": False, "parent": st["id"]})
                      st["children"].append(Player.ids)
                      Player.ids += 1

      # if the node is the first one to be expanded and has no parent
      else:

          first_node = {"id": Player.ids, "state": parent_state,
                        "expansionsequence": Player.xpansionsequence,
                        "children": [], "actions": children_direction, "removed": False, "parent": None}
          Player.search_tree.append(first_node)
          Player.ids += 1
          for c in children:
              child_state = str(c[0]) + "," + str(c[1])
              Player.search_tree.append(
                  {"id": Player.ids, "state": parent_state, "expansionsequence": -1, "children": [], "actions": [],
                   "removed": False, "parent": first_node["id"]})
              first_node["children"].append(Player.ids)
              Player.ids += 1



  def run(self, problem):
#     problem = {
#       snake_locations: [[int,int],[int,int],...],
#       current_direction: str,
#       food_locations: [[int,int],[int,int],...],
#     }

     #declaring required variables
     found_goal = False
     solution = []
     frontier = []
     frontier_direction = []
     explored = []
     explored_direction = []
     solution_path = []



     #appending initial state
     frontier.append(problem["snake_locations"][0])
     frontier_direction.append(problem["current_direction"])

     while  found_goal == False:
        #generating the children for the frontier at index 0

        children, children_direction = self.getChildren(frontier[0][0],frontier[0][1])

        #appending expanded frontier
        explored.append(frontier[0])
        explored_direction.append(frontier_direction[0])


        #deleting expanded frontier from the list
        del frontier[0]
        del frontier_direction[0]


        #checking if snake location is the same as the children locations
        for s in enumerate(problem["snake_locations"],start=1):
            for i in range(len(children)-1):
                if s == children[i]:
                    del children[i]
                    del children_direction[i]


        #looping through the children list
        for child in children:
            # check if a node was expanded or generated previously
            if not (child in explored) and not (child in frontier):

                #check if child is goal
                if child == problem["food_locations"][0]:
                    found_goal = True
                    #after goal is found, calculate the distance between the snake and the goal
                    distance_x = problem["food_locations"][0][0] - problem["snake_locations"][0][0]
                    distance_y = problem["food_locations"][0][1] - problem["snake_locations"][0][1]
                    sp = problem["snake_locations"][0][0]
                    last_element_x = sp + distance_x

                    #trackback the sets required to reach the goal
                    if distance_x < 0:
                        for row_distance in range(1,abs(distance_x)+1):
                            dis1 = [problem["snake_locations"][0][0] - row_distance, problem["snake_locations"][0][1]]
                            if dis1[0] >= 0 and dis1[0] <= 9:
                                solution_path.append(dis1)

                    else:
                        for row_distance in range(1,abs(distance_x)+1):
                            dis1 = [problem["snake_locations"][0][0] + row_distance, problem["snake_locations"][0][1]]
                            if dis1[0] >= 0 and dis1[0] <= 9:
                                solution_path.append(dis1)

                    if distance_y < 0:


                        for col_distance in range(1,abs(distance_y)+1):
                            dis2 = [last_element_x,problem["snake_locations"][0][1]-col_distance]
                            if dis2[1] >= 0 and dis2[1] <= 9:
                                solution_path.append(dis2)
                    else:
                        for col_distance in range(1,abs(distance_y)+1):
                            dis2 = [last_element_x,problem["snake_locations"][0][1]+col_distance]
                            if dis2[1] >= 0 and dis2[1] <= 9:
                                solution_path.append(dis2)
                                
                                
                    #appending the first direction
                    solution.append(self.getsolutionDirection(problem["snake_locations"][0][0],problem["snake_locations"][0][1],solution_path[0][0], solution_path[0][1]))
                    #appending the direction for each step
                    for i in range(len(solution_path)-1):
                        direction = self.getsolutionDirection(solution_path[i][0],solution_path[i][1],solution_path[i+1][0],solution_path[i+1][1])
                        solution.append(direction)
                #appending the next child
                frontier.append(child)
                frontier_direction.append(children_direction[children.index(child)])

        #printing all the lists at each iteration
        print("Explored:", [e for e in explored])
        print("Explored Direction:", [e for e in explored_direction])
        print("Frontier:", [f for f in frontier])
        print("Frontier Direction:", [f for f in frontier_direction])
        print("Children:", [c for c in children])
        print("Children Direction:", [d for d in children_direction])
        print("")
        print("Solution Path", solution_path)
        # block of code responsible for generating search tree
        # declaring required variables for search tree
        Player.xpansionsequence += 1
        x = explored[0][0]
        y = explored[0][1]
        px = explored[-1][0]
        py = explored[-1][1]

        # this function should return the solution and the search_tree
        # this line has been commented out to prevent the program from being unresponsive
        # self.generateSearchTree(x, y, px, py, children, children_direction)


     return solution, Player.search_tree

if __name__ == "__main__":
  p1 = Player({ "maze_size": [10,10], "static_snake_length": False })
  sol, st =  p1.run({'snake_locations': [[5, 5]], 'current_direction': 'e', 'food_locations': [[9,9]]})
  print("Solution is:", sol)
  print("Search tree is:")
  print(st)
