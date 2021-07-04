import random
#list out of range. need try catch
# Node class. Represents a coordinate.

class Node:
    
    def __init__(self, x, y, parent = None):

    	# Coordinates of the node
        self.x = x
        self.y = y

        # Parent of the node. The node that the snake came from to reach current node
        self.parent = parent

        # List of children of the node. The nodes the snake can get to from current node
        self.children = []

# Returns the children of the given node. m and n are the dimensions of the grid
def expandAndReturnChildren(node, m, n):
    dx = [0, 0, 1, -1]
    dy = [1, -1, 0, 0]
    children = []
    for i in range(4):

    	# (x, y) represent all possible places the snake can go
    	x = node.x+dx[i]
    	y = node.y+dy[i]

    	# The parent of the node cannot be its child
    	if (node.parent is not None and node.parent.x == x and node.parent.y == y):
    		continue

    	# If node falls off the grid, ignore it
    	if (x < 0 or y < 0 or x >= m or y >= n):
    		continue

    	# Add the node to the children array
    	children.append(Node(x, y, node))

    return children

class Player():
  name = "A*Player"
  group = "Four Stooges"
  members = [
    ["Amrita Menon", "17029596"],
    ["Marcus Teow", "19024371"],
    ["Muhammad Hafiz", "16027344"],
    ["Liew Tze Chen", "18032730"]
  ]
  informed = True

  def __init__(self, setup):
    # setup = {
    #   maze_size: [int, int],
    #   static_snake_length: bool
    # }
    self.setup = setup

  def func(self, problem):

  	# Source and destination coordinates
    src = problem["snake_locations"][0]
    dest = problem["food_locations"][0]
    
    # Frontier is our BFS queue
    frontier = []

    # Explored contains the visited nodes
    explored = []

    # Final solution
    solution = []

    # Final search tree
    search_tree = []

    # When we reach our destination, found_goal will become True
    found_goal = False

    # Destination node
    goalie = Node(dest[0], dest[1])

    # Adding source node to frontier queue
    frontier.append(Node(src[0], src[1]))

    # cnt is used for ids of the search_tree nodes
    cnt = 1

    # Source node for our search tree
    d = {}

    # Setting parameters
    d["id"] = cnt
    cnt = cnt+1
    d["state"] = str(frontier[0].x)+","+str(frontier[0].y)
    d["coor"] = [frontier[0].x, frontier[0].y]
    d["parent"] = None
    d["actions"] = []
    d["removed"] = False
    d["children"] = []
    d["expansionsequence"] = 1

    # Adding dict entry to search_tree
    search_tree.append(d)

    while not found_goal:
        # Break out of loop when no nodes in frontier
    	try:
            frontier[0]
    	except:
            break
        
    	# Children of the top node in BFS queue(frontier[0])
    	children = expandAndReturnChildren(frontier[0], self.setup["maze_size"][0], self.setup["maze_size"][1])

    	# A* implementation. Sorts children based on Manhattan distance. Remove this line to convert algo to normal BFS
    	children = sorted(children, key = lambda p: abs(p.x-dest[0])+abs(p.y-dest[1]))

    	# Finding top node in BFS queue in search tree
    	for node in search_tree:
    		if (node["coor"] == [frontier[0].x, frontier[0].y]):
    			# dc is now the dictionary entry for the parent of the nodes in children array
    			dc = node
    			break
    	for node in search_tree:
    		if (frontier[0].parent is not None and node["coor"] == [frontier[0].parent.x, frontier[0].parent.y]):
    			# Since we are currently expanding frontier[0], its expansion sequence will be 1 more than that of its parent
    			dc["expansionsequence"] = node["expansionsequence"]+1
    			break

    	# This loop creates the search tree
    	for child in children:
    		# For each child, we create a dict entry and add it to the search_tree
    		d = {}
    		d["id"] = cnt
    		cnt = cnt+1
    		d["state"] = str(child.x)+","+str(child.y)
    		d["coor"] = [child.x, child.y]
    		d["children"] = []
    		d["actions"] = []
    		d["parent"] = dc["id"]
    		d["expansionsequence"] = -1

    		# dc is the parent dict element. So we need to add current child id in its children array
    		dc["children"].append(d["id"])

    		# The code below fills up the action array of the parent node
    		diffx = child.x-frontier[0].x
    		diffy = child.y-frontier[0].y
    		if diffx == 0 and diffy == -1:
    			dc["actions"].append("n")
    		elif diffx == 0 and diffy == 1:
    			dc["actions"].append("s")
    		elif diffx == 1 and diffy == 0:
    			dc["actions"].append("e")
    		elif diffx == -1 and diffy == 0:
    			dc["actions"].append("w")

    		# If child is explored or currently in BFS queue or is a part of the snake's body, then that node can't be expanded further. So its removed value is True
    		if ([child.x, child.y] in [[e.x, e.y] for e in explored]) or ([child.x, child.y] in [[f.x, f.y] for f in frontier]) or [child.x, child.y] in problem["snake_locations"]:
    			d["removed"] = True

    		# Adding the dictionary element we created to the search_tree
    		search_tree.append(d)

    	# Normal BFS algo continues after finding search_tree

    	# First node is popped and inserted into the explored array
    	explored.append(frontier[0])
    	del frontier[0]

    	# Only those children that are neither explored nor in the frontier queue and not part of the snake's body must be pushed to the frontier queue
    	for child in children:
    		if not ([child.x, child.y] in [[e.x, e.y] for e in explored]) and not ([child.x, child.y] in [[f.x, f.y] for f in frontier]) and [child.x, child.y] not in problem["snake_locations"]:
    			
    			# If the child node is our destination
    			if child.x == dest[0] and child.y == dest[1]:
    				found_goal = True
    				goalie = child
    			frontier.append(child)


    final_path = [goalie]
    while goalie.parent is not None:

    	# Keep adding the parent to the front of the array till the node has no parent. This would give us the final path
    	final_path.insert(0, goalie.parent)
    	goalie = goalie.parent

	# We are out of the BFS loop and we have our final path but it is in the form of coordinates. This loop changes them to the n,s,e,w format
    for i in range(len(final_path)-1):
        diffx = final_path[i+1].x - final_path[i].x
        diffy = final_path[i+1].y - final_path[i].y
        if diffx == 0 and diffy == -1:
            solution.append("n")
        elif diffx == 0 and diffy == 1:
            solution.append("s")
        elif diffx == 1 and diffy == 0:
            solution.append("e")
        elif diffx == -1 and diffy == 0:
            solution.append("w")

    return solution, search_tree



  def run(self, problem):
    # problem = {
    #   snake_locations: [[int,int],[int,int],...],
    #   current_direction: str,
    #   food_locations: [[int,int],[int,int],...],
    # }
    solution = []
    directions = "nswe"
    # the following algorithm is NOT a valid algorithm
    # it randomly generates solution that is invalid
    # its purpose is to show you how this class will work
    # not a guide to how to write your algorithm
    solution, search_tree = self.func(problem)
    # the following search tree is a static search tree 
    # to show you the format of the variable 
    # to generate a search tree that can be displayed in the frontend.
    # you are required to generate the search tree based on your search algorithm
    # search_tree = [
    #   {
    #     "id": 1,
    #     "state": "0,0",
    #     "expansionsequence": 1,
    #     "children": [2,3,4],
    #     "actions": ["n","w","e"],
    #     "removed": False,
    #     "parent": None
    #   },
    #   {
    #     "id": 2,
    #     "state": "5,0",
    #     "expansionsequence": 2,
    #     "children": [5,6,7],
    #     "actions": ["n","s","w"],
    #     "removed": False,
    #     "parent": 1
    #   },
    #   {
    #     "id": 3,
    #     "state": "0,3",
    #     "expansionsequence": -1,
    #     "children": [],
    #     "actions": [],
    #     "removed": False,
    #     "parent": 1
    #   },
    #   {
    #     "id": 4,
    #     "state": "0,4",
    #     "expansionsequence": -1,
    #     "children": [],
    #     "actions": [],
    #     "removed": False,
    #     "parent": 1
    #   },
    #   {
    #     "id": 5,
    #     "state": "5,0",
    #     "expansionsequence": -1,
    #     "children": [],
    #     "actions": [],
    #     "removed": True,
    #     "parent": 2
    #   },
    #   {
    #     "id": 6,
    #     "state": "5,3",
    #     "expansionsequence": -1,
    #     "children": [],
    #     "actions": [],
    #     "removed": False,
    #     "parent": 2
    #   },
    #   {
    #     "id": 7,
    #     "state": "1,0",
    #     "expansionsequence": -1,
    #     "children": [],
    #     "actions": [],
    #     "removed": False,
    #     "parent": 2
    #   }
    # ]
    # this function should return the solution and the search_tree
    return solution, search_tree


if __name__ == "__main__":
  p1 = Player({ "maze_size": [10,10], "static_snake_length": True })
  sol, st = p1.run({'snake_locations': [[0, 5]], 'current_direction': 'e', 'food_locations': [[6, 7]]})
  print("Solution is:", sol)
  print("Search tree is:")
  print(st)

