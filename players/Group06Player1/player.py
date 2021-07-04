import random

class Player():
  name = "Informed player"
  group = "IDK"
  members = [
    ["Hong Ren Shen", "18088880"],
    ["Eric Chong Chi Kit", "18084491"]
  ]
  informed = True

  def __init__(self, setup):
    # setup = {
    #   maze_size: [int, int],
    #   static_snake_length: bool
    # }
    self.setup = setup

  def run(self, problem):
    # problem = {
    #   snake_locations: [[int,int],[int,int],...],
    #   current_direction: str,
    #   food_locations: [[int,int],[int,int],...],
    # }
    solution = []
    directions = "nswe"
    
    #Coding section?
    
    if problem["snake_locations"][0][0] > problem["food_locations"][0][0]:
        directions = "w"
            
    if problem["snake_locations"][0][0] < problem["food_locations"][0][0]:
        directions = "e"
        
    if problem["snake_locations"][0][0] == problem["food_locations"][0][0]:
        if problem["snake_locations"][0][1] < problem["food_locations"][0][1]:
            directions = "s"
        elif problem["snake_locations"][0][1] > problem["food_locations"][0][1]:
                directions = "n"
                
    if problem["current_direction"] == "e" and directions == "w":
        for x in range(len(problem["snake_locations"])) : 
            if problem["snake_locations"][0][0]+1 != 10 or problem["snake_locations"][0][0]+1 != problem["snake_locations"][x][0]:
                directions = "e"
            if problem["snake_locations"][0][0]+1 == 10 or problem["snake_locations"][0][0]+1 == problem["snake_locations"][x][0]:
                directions ="s"
            elif problem["snake_locations"][0][1]+1 == 10 or problem["snake_locations"][0][1]+1 == problem["snake_locations"][x][1]:
                directions = "n"
                
    if problem["current_direction"] == "w" and directions == "e":
        for x in range(len(problem["snake_locations"])) : 
            if problem["snake_locations"][0][0]-1 != -1 or problem["snake_locations"][0][0]-1 != problem["snake_locations"][x][0]:
                directions = "w"
            if problem["snake_locations"][0][0]-1 == -1 or problem["snake_locations"][0][0]-1 == problem["snake_locations"][x][0]:
                directions ="n"
            elif problem["snake_locations"][0][1]-1 == -1 or problem["snake_locations"][0][1]-1 == problem["snake_locations"][x][1]:
                directions = "s"
                
        
    if problem["current_direction"] == "n" and directions == "s":
        for x in range(len(problem["snake_locations"])) : 
            if problem["snake_locations"][0][1]-1 != -1 or problem["snake_locations"][0][1]-1 != problem["snake_locations"][x][1]:
                directions = "n"
            if problem["snake_locations"][0][1]-1 == -1 or problem["snake_locations"][0][1]+1 == problem["snake_locations"][x][1]:
                directions ="e"
            elif problem["snake_locations"][0][0]+1 == 10 or problem["snake_locations"][0][0]+1 == problem["snake_locations"][x][0]:
                directions = "w"
                
    if problem["current_direction"] == "s" and directions == "n":
        for x in range(len(problem["snake_locations"])) : 
            if problem["snake_locations"][0][1]+1 != 10 or problem["snake_locations"][0][1]+1 != problem["snake_locations"][x][1]:
                directions = "s"
            if problem["snake_locations"][0][1]+1 == 10 or problem["snake_locations"][0][1]+1 == problem["snake_locations"][x][1]:
                directions ="w"
            elif problem["snake_locations"][0][0]-1 == -1 or problem["snake_locations"][0][0]-1 == problem["snake_locations"][x][0]:
                directions = "e"
                
    
                
    # the following algorithm is NOT a valid algorithm
    # it randomly generates solution that is invalid
    # its purpose is to show you how this class will work
    # not a guide to how to write your algorithm
    solution = [directions for step in range(random.randint(1,1))]
    # the following search tree is a static search tree 
    # to show you the format of the variable 
    # to generate a search tree that can be displayed in the frontend.
    # you are required to generate the search tree based on your search algorithm
    
    #n = problem["snake_locations"][0][0] ,problem["snake_locations"][0][1] - 1
    #s = problem["snake_locations"][0][0] ,problem["snake_locations"][0][1] + 1
    #w = problem["snake_locations"][0][0] - 1 ,problem["snake_locations"][0][1]
    #e = problem["snake_locations"][0][0] + 1 ,problem["snake_locations"][0][1]
    
    
    search_tree = [
      {
        "id": 1,
        "state": problem["snake_locations"][0],
        "expansionsequence": 1,
        "children": [2,3,4,5],
        "actions": ["n","s","w","e"],
        "removed": False,
        "parent": None
      },
      {
        "id": 2,
        "state": str([problem["snake_locations"][0][0] ,problem["snake_locations"][0][1] - 1]),
        "expansionsequence": 2,
        "children": [6,7,8,9],
        "actions": ["n","s","w","e"],
        "removed": False,
        "parent": 1
      },
      {
        "id": 3,
        "state": str([problem["snake_locations"][0][0] ,problem["snake_locations"][0][1] + 1]),
        "expansionsequence": 2,
        "children": [10,11,12,13],
        "actions": ["n","s","w","e"],
        "removed": False,
        "parent": 1
      },
      {
        "id": 4,
        "state": str([problem["snake_locations"][0][0] - 1 ,problem["snake_locations"][0][1]]),
        "expansionsequence": 2,
        "children": [14,15,16,17],
        "actions": ["n","s","w","e"],
        "removed": False,
        "parent": 1
      },
      {
        "id": 5,
        "state": str([problem["snake_locations"][0][0] + 1 ,problem["snake_locations"][0][1]]),
        "expansionsequence": 2,
        "children": [18,19,20,21],
        "actions": ["n","s","w","e"],
        "removed": False,
        "parent": 1
      },
      {
        "id": 6,
        "state": str([problem["snake_locations"][0][0] ,problem["snake_locations"][0][1] - 2]),
        "expansionsequence": -1,
        "children": [],
        "actions": [],
        "removed": False,
        "parent": 2
      },
      {
        "id": 7,
        "state": str([problem["snake_locations"][0][0] ,problem["snake_locations"][0][1]]),
        "expansionsequence": -1,
        "children": [],
        "actions": [],
        "removed": True,
        "parent": 2
      },
      {
        "id": 8,
        "state": str([problem["snake_locations"][0][0] - 1,problem["snake_locations"][0][1] - 1]),
        "expansionsequence": -1,
        "children": [],
        "actions": [],
        "removed": False,
        "parent": 2
      },
      {
        "id": 9,
        "state": str([problem["snake_locations"][0][0] + 1,problem["snake_locations"][0][1] - 1]),
        "expansionsequence": -1,
        "children": [],
        "actions": [],
        "removed": False,
        "parent": 2
      },
      {
        "id": 10,
        "state": str([problem["snake_locations"][0][0] ,problem["snake_locations"][0][1]]),
        "expansionsequence": -1,
        "children": [],
        "actions": [],
        "removed": True,
        "parent": 3
      },
      {
        "id": 11,
        "state": str([problem["snake_locations"][0][0] ,problem["snake_locations"][0][1] + 2]),
        "expansionsequence": -1,
        "children": [],
        "actions": [],
        "removed": False,
        "parent": 3
      },
      {
        "id": 12,
        "state": str([problem["snake_locations"][0][0] - 1,problem["snake_locations"][0][1] + 1]),
        "expansionsequence": -1,
        "children": [],
        "actions": [],
        "removed": False,
        "parent": 3
      },
      {
        "id": 13,
        "state": str([problem["snake_locations"][0][0] + 1,problem["snake_locations"][0][1] + 1]),
        "expansionsequence": -1,
        "children": [],
        "actions": [],
        "removed": False,
        "parent": 3
      },
      {
        "id": 14,
        "state": str([problem["snake_locations"][0][0] - 1 ,problem["snake_locations"][0][1] - 1]),
        "expansionsequence": -1,
        "children": [],
        "actions": [],
        "removed": True,
        "parent": 4
      },
      {
        "id": 15,
        "state": str([problem["snake_locations"][0][0] - 1 ,problem["snake_locations"][0][1] + 1]),
        "expansionsequence": -1,
        "children": [],
        "actions": [],
        "removed": True,
        "parent": 4
      },
      {
        "id": 16,
        "state": str([problem["snake_locations"][0][0] - 2 ,problem["snake_locations"][0][1]]),
        "expansionsequence": -1,
        "children": [],
        "actions": [],
        "removed": False,
        "parent": 4
      },
      {
        "id": 17,
        "state": str([problem["snake_locations"][0][0] ,problem["snake_locations"][0][1]]),
        "expansionsequence": -1,
        "children": [],
        "actions": [],
        "removed": True,
        "parent": 4
      },
      {
        "id": 18,
        "state": str([problem["snake_locations"][0][0] + 1 ,problem["snake_locations"][0][1] - 1]),
        "expansionsequence": -1,
        "children": [],
        "actions": [],
        "removed": True,
        "parent": 5
      },
      {
        "id": 19,
        "state": str([problem["snake_locations"][0][0] + 1 ,problem["snake_locations"][0][1] + 1]),
        "expansionsequence": -1,
        "children": [],
        "actions": [],
        "removed": True,
        "parent": 5
      },
      {
        "id": 20,
        "state": str([problem["snake_locations"][0][0] ,problem["snake_locations"][0][1]]),
        "expansionsequence": -1,
        "children": [],
        "actions": [],
        "removed": True,
        "parent": 5
      },
      {
        "id": 21,
        "state": str([problem["snake_locations"][0][0] + 2 ,problem["snake_locations"][0][1]]),
        "expansionsequence": -1,
        "children": [],
        "actions": [],
        "removed": False,
        "parent": 5
      }      
    ]
    # this function should return the solution and the search_tree
    return solution, search_tree


if __name__ == "__main__":
  p1 = Player({ "maze_size": [10,10], "static_snake_length": True })
  sol, st = p1.run({'snake_locations': [[0, 5]], 'current_direction': 'e', 'food_locations': [[6, 7]]})
  print("Solution is:", sol)
  print("Search tree is:")
  print(st)