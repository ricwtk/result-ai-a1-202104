class Player():
  name = "bfs"
  informed = False
  group = "5Heads"
  members = [
    ["Leo Paul Larkin", "18088971"],
    ["Thevendren", "18067074"],
    ["Fun Kok Fui", "18047829"],
    ["Ng Jun Ren", "17098302"]
  ]
  


  def __init__(self, setup):
    setup = {
        'maze_size': [10,10],
        'static_snake_length': True
      }
    self.setup = setup
  
  def run(self, problem):
    self.setup["maze_size"]
    self.setup["static_snake_length"]
    problem = {
        'snake_locations': [],
        'current_direction': 'e',
        'food_locations': [],
        }
    search_tree = [
      {
        "id": 1,
        "state": "0,5",
        "expansionsequence": 1,
        "children": [2,3,4],
        "actions": ["n","w","e"],
        "removed": False,
        "parent": None
      }
      ]
    directions = 'nswe'
    snake_location = problem.get('snake_locations')[0]
    current_direction = problem.get('current_direction')
    food_location = problem.get('food_locations')[0]
    solution = []
    Visited= []
    Frontier= []
    foodFound = False 
    inbound = False
    #direction vectors
    dx = [-1,+1,0,0] #row
    dy = [0,0,+1,-1] #column
    x1 = snake_location[0]
    y1 = snake_location[1]
    x = x1
    y = y1
    loc = [x,y]
    Frontier.append(loc)
    cycle = 0
    ids = [0]
    parents = []
    children = []
    while not foodFound:
      cycle+=1
      ## explore the adjacent squares
      for i in range(4):
        #direction vectors
        dx = [+1,-1,0,0] #row
        dy = [0,0,+1,-1] #column
        #checking if any squares are out of bounds
        xx = x + dx[i] 
        yy = y + dy[i]
        new = [xx, yy]
        if xx < 0 or yy < 0: 
            continue
        if xx >= 10 or yy >= 10: 
            continue
        #checking if the squares are visited
        if new in Visited:
            continue
        Frontier.append(new)
      Visited.append(Frontier[0])
      del Frontier[0]
      x = Frontier[0][0]
      y = Frontier[0][1]
      i = 0
      #Test for
      for i in range(len(Frontier)): 
        if food_location[0] == Frontier[i]:
          foodFound = True
          for u in range(len(Visited)):
                #creates the directions that go into solution
                x1 = Visited[u][0]
                y1 = Visited[u][1]
                totalx = food_location[0][0] - x1 #finding distance between current location and food
                totaly = food_location[0][1] - y1
                if totalx < 0:
                  #convert any negative values to positive
                    movex = -1*totalx 
                else: movex = totalx
                if totaly < 0:
                    movey = -1*totaly
                else: movey = totaly
                j = 0
                #determine the direction
                for j in range(movex):
                    if totalx > 0:
                        solution.append('e')
                    elif totalx < 0:
                        solution.append('w')
                j = 0 
                for j in range(movey):
                    if totaly > 0:
                        solution.append('n')
                    elif totaly < 0:
                        solution.append('s')
                #generate the search tree
                search_tree.append({"id": (ids[-1]),
                  "state": snake_location,
                  "expansionsequence": 1,
                  "children": children,
                  "actions": ["n","w","e"],
                  "removed": False,
                  "parent": parents[cycle]})
    
    return solution, search_tree


if __name__ == "__main__":
  bfs = Player({ "maze_size": [10,10], "static_snake_length": True })
  sol, st = bfs.run({"snake_locations": [[0, 5]], "current_direction": 'e', "food_locations": [[6, 7]]})
  print("Solution is:", sol)
  print("Search tree is:")
  print(st)
