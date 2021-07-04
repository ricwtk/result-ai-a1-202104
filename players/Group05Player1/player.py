class Player():
  name = "informed player"
  group = "Island Coders"
  members = [
    ["Muhammad Nabeel Rasheed Varsally", "19025634"],
    ["Raveesh Shibchurn", "19053156"],
    ["Yutashna Gunnoo", "19063304"],
    ["Eltigani Hamadelniel Elfatih", "17087610"]
  ]
  informed = True
  search_tree = []
  ids = 1
  xpansionsequence = 0


  def __init__(self, setup):
#     setup = {
#       maze_size: [int, int],
#       static_snake_length: bool
#     }
     self.setup = setup
     

  def run(self, problem):
#     problem = {
#       snake_locations: [[int,int],[int,int],...],
#       current_direction: str,
#       food_locations: [[int,int],[int,int],...],
#     }
     children = []
     children_direction = []
     
     # Put the x and y coordinates of the head of the snake in variables x and y respectively
     [x,y] = problem["snake_locations"][0]
     
     # Put the x and y coordinates of the last square of the maze in variables xx and yy respectively
     xx = self.setup["maze_size"][0] - 1
     yy = self.setup["maze_size"][1] - 1
     
     # block of code below is used to find the children of the snake head
     
     if x == 0:
         
          if y == 0: #snake head is in upper right corner
              
                 children.append([x+1,y]) #Append square east of snake to list children
                 children_direction.append("e")
                 children.append([x,y+1]) #Append square south of snake to list children
                 children_direction.append("s")
                 
          elif y == (yy): #snake head is in lower right corner
              
                 children.append([x,yy-1]) #North
                 children_direction.append("n")
                 children.append([x+1,yy]) #East
                 children_direction.append("e")
                 
          else: #snake head is adjacent to left side border of grid
              
                 children.append([x,y-1]) #North
                 children_direction.append("n")
                 children.append([x+1,y]) #East
                 children_direction.append("e")
                 children.append([x,y+1]) #South
                 children_direction.append("s")
                 
     if y == 0:
         
           if x == 0:
                 pass # skipped since it was already executed in lines 43 to 50
             
           elif x == (xx):
                 children.append([x-1,y]) #West
                 children_direction.append("w")
                 children.append([x,y+1]) #South
                 children_direction.append("s")
                 
           else:
                 children.append([x+1,y]) #East
                 children_direction.append("e")
                 children.append([x,y+1]) #South
                 children_direction.append("s")
                 children.append([x-1,y]) #West
                 children_direction.append("w")
                 
     if x == xx:
            if y == 0:
                pass
            elif y == yy:
                children.append([xx,yy-1]) #North
                children_direction.append("n")
                children.append([xx-1,yy]) #West
                children_direction.append("w")
            else:
                 children.append([x,y-1]) #North
                 children_direction.append("n")
                 children.append([x,y+1]) #South
                 children_direction.append("s")
                 children.append([x-1,y]) #West
                 children_direction.append("w")
                 
     if y == yy:
             if x == 0:
                pass
             elif x == xx:
                pass
             else:
                 children.append([x,y-1]) #North
                 children_direction.append("n")
                 children.append([x+1,y]) #East
                 children_direction.append("e")
                 children.append([x-1,y]) #Weste
                 children_direction.append("w")
                 
     if (0 < x < xx) & (0 < y < yy):
         children.append([x,y-1]) #North
         children_direction.append("n")
         children.append([x+1,y]) #East
         children_direction.append("e")
         children.append([x,y+1]) #South
         children_direction.append("s")
         children.append([x-1,y]) #West
         children_direction.append("w")
       
     
     solution = []
     distance_to_food_list = []
     
     #calculate distance from each child to each food location and choose the closest food
     for c in children:
         distance_to_food1 = abs(c[0] - problem["food_locations"][0][0]) + abs(c[1] - problem["food_locations"][0][1])
         
         if len(problem["food_locations"]) == 2:
             distance_to_food2 = abs(c[0] - problem["food_locations"][1][0]) + abs(c[1] - problem["food_locations"][1][1])
             if distance_to_food1 < distance_to_food2:
                 distance_to_food_list.append(distance_to_food1)
             else:
                 distance_to_food_list.append(distance_to_food2)
         else:
             distance_to_food_list.append(distance_to_food1)
             
             
      
    # # block of code responsible for generating search tree
    #  Player.xpansionsequence+=1
    #  current_state = str(x)+ "," + str(y)
     
    #  #if the node is not the first one to be expanded and has a parent which is already in the search tree
    #  if len(Player.search_tree) != 0:
    #      for st in Player.search_tree:
    #          if st["state"] == current_state:
    #              st["actions"] = children_direction
    #              st["expansionsequence"] = Player.xpansionsequence
    #              for c in children: 
    #                  child_state = str(c[0])+"," + str(c[1])
    #                  Player.search_tree.append({"id": Player.ids, "state": child_state, "expansionsequence": -1, "children": [], "actions": [], "removed": False, "parent": st["id"]})
    #                  st["children"].append(Player.ids)
    #                  Player.ids+=1
           
    #  #if the node is the first one to be expanded and has no parent
    #  else:
    #     first_node = {"id": Player.ids, "state": current_state, "expansionsequence": Player.xpansionsequence, "children": [], "actions": children_direction, "removed": False, "parent": None}
    #     Player.search_tree.append(first_node)
    #     Player.ids+=1
    #     for c in children: 
    #         child_state = str(c[0])+"," + str(c[1])
    #         Player.search_tree.append({"id": Player.ids, "state": child_state, "expansionsequence": -1, "children": [], "actions": [], "removed": False, "parent": first_node["id"]})
    #         first_node["children"].append(Player.ids)
    #         Player.ids+=1
                 

    #delete child if it the snake body is in the square (dynamic length)
     for s in problem["snake_locations"]:
        for i in range(len(children)):
             if s == children[i]:
                 # for st in Player.search_tree:
                 #     if st["state"] == (str(children[i][0])+ "," + str(children[i][1])) and st["expansionsequence"] == -1:
                 #         st["removed"] = True
                 del children[i]
                 del distance_to_food_list[i]
                 del children_direction[i]
                 break
    
    #choose child closest to food location and choose its respective direction in children_direction as solution
     for i in range(len(children)):
         if distance_to_food_list[i] == min(distance_to_food_list):
             solution = [(children_direction[i])]
             break
   
     dummy_search_tree = []
     return solution, dummy_search_tree

    
if __name__ == "__main__":
  p1 = Player({ "maze_size": [10,10], "static_snake_length": True })
  sol, st = p1.run({'snake_locations': [[1, 1]], 'current_direction': 'e', 'food_locations': [[9, 9]]})
  print("Solution is:", sol)
  print("Search tree is:")
  print(st)