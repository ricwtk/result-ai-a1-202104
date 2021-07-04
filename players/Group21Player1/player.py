
class Player():
  name = "Informed Search - player 1 A*"
  group = "walao"
  members = [
    ["Ong Yu Mhing", "18098517"],
    ["Tristan Elisha Chong Ze Han", "18125799"],
    ["Chuah Kim Hooi", "18123588"],
    ["Tan Ju Bhin", "15025034"]
  ]
  informed = True

  def __init__(self, setup):
  # setup = {
  #   maze_size: [int, int],
  #   static_snake_length: bool
  # }
    self.setup = setup
        
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
    
    #For maze_size
    for key, value in self.setup.items():
        if key == 'maze_size':
            maze = value
     
    try:
        results,search_tree = astar(snake,','.join(map(str,snake[0])), ','.join(map(str,food[0])), maze)
        
        symbols = '() '
        newlist = []    
        
        for element in results:
            temp = ""
            for ch in element:
                if ch not in symbols:
                    temp += ch
    
            newlist.append(temp)
            
        coord_int = []
        for coord in newlist:
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
   
    
   ##Catch if no other way to move
    except Exception as e:
        print(e)
        solution = ['n']
        search_tree = []
    return solution, search_tree
    
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
    
def astar(body, start, end, maze):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""
    
    bodies=[]
    for i in body:
        bodies.append(i)
    print("BOD: ", bodies)
    #Create start and end node
    startnode = Node(None, start)
    startnode.g = startnode.h = startnode.f = 0
    endnode = Node(None, end)
    endnode.g = endnode.h = endnode.f = 0

    #Initialize both open and closed list
    openlist = []
    closedlist = []
    explored = []
    result = []
    
    #Add the start node
    openlist.append(startnode)
    
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
    
    #prevents infinite loop
    outer_loop = 0
    max_loop = (len(state_space))
    #Loop until goal found
    while len(openlist) > 0:
        outer_loop += 1
        # Get the current node
        currentnode = openlist[0]
        currentindex = 0
        for index, item in enumerate(openlist):
            if item.f < currentnode.f:
                currentnode = item
                currentindex = index
     
        # Pop current off open list, add to closed list
        openlist.pop(currentindex)
        closedlist.append(currentnode)
        
        x = str(currentnode.position[0])
        y=str(currentnode.position[-1])
        
        # Found the goal
        if x == endnode.position[0] and y == endnode.position[-1]:
            path = []
            current = currentnode
            while current is not None:
                path.append(str(current.position))
                current = current.parent
            
            return path[::-1],result # Return reversed path

        # Generate children
        children = []
        
        xcurr = int(currentnode.position[0])
        ycurr = int(currentnode.position[-1])
        
        for newposition in [(xcurr-1,ycurr),(xcurr+1,ycurr),(xcurr,ycurr-1),(xcurr,ycurr+1)]: # Adjacent squares
                

            # Get node position
            nodeposition = newposition  
            # Create new node
            newnode = Node(currentnode, nodeposition)

            # Append
            children.append(newnode)    
            
            # Make sure within range
            if nodeposition[0] > (maze[0] -1) or nodeposition[0] < 0 or nodeposition[1] > (maze[1] - 1) or nodeposition[1] < 0:
                children.remove(newnode)
            
            #Remove if same coordinate as snake body
            for cordx, cordy in bodies:
                # print("Value: ", cordx,cordy, nodeposition[0], nodeposition[1])
                if cordx == nodeposition[0] and cordy == nodeposition[1]:
                    # print("DELETE")
                    children.remove(newnode)
                    
        # Loop through children
        for child in children:
            # Child is on the closed list
            for closedchild in closedlist:
                if child == closedchild:
                    for i in bodies:
                        if i == closedchild.position:
                            continue
            
            xend = int(endnode.position[0])
            yend = int(endnode.position[-1])
            
            # Create the f, g, and h values
            child.g = currentnode.g + 1
            child.h = ((child.position[0] - xend) ** 2) + ((child.position[1] - yend) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for opennode in openlist:
                if child == opennode and child.g > opennode.g:
                    continue
            # Add the child to the open list
            openlist.append(child)
            
            print('Parent of child',child.position, 'is ',child.parent.position)
            # print("BODS: ",bodies)
            for i in openlist:
                a = i.position
                b = i.f
                explored.append((a,b))       
           
            for i in explored:
               if i not in result:
                   result.append(i)
                    
        if outer_loop > max_loop:
            print("Search over node limit, code is looping")
            path = []
            current = currentnode
            while current is not None:
                path.append(str(current.position))
                current = current.parent
            loop_next_node = []
            loop_next_node.append(path[-1])
            loop_next_node.append(path[-2])
            print("The next node: ",loop_next_node)
            return loop_next_node,result
                    
if __name__ == "__main__":
  p1 = Player({ "maze_size": [10,10], "static_snake_length": False })
  sol, st = p1.run({'snake_locations': [[0, 5]], 'current_direction': 'e', 'food_locations': [[6, 7]]})
  print("Search tree is:")
  print(st)
  print("Solution is:", sol)