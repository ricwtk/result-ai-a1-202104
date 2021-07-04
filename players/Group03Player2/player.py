
class Player():
  name = "Greedy Best First Search"
  group = "Thinkers"
  members = [
    ["Brysen Poi Yong Zhen", "17119363"],
    ["Dylan Ng Jia Jun", "18031641"],
    ["Loh Khay Wen", "18017889"]
  ]
  informed = True

  def __init__(self, setup):
    
    self.setup = setup

  def run(self, problem):
    
    row = self.setup.get('maze_size')[0]
    col = self.setup.get('maze_size')[1]
    food = problem.get('food_locations')
    snake = problem.get('snake_locations')
    current_direction = problem.get('current_direction')
    
    # Calculate which food distance and sort to find the nearest food first
    for index in range(len(food)):
        distance = funcDist(food[index],snake[0],'checkfood')
        food[index].append(distance)
    food = sorted(food,key=lambda f:f[-1])

    search_tree = []
    frontier = []
    explored = []
    solution = []
    found_food = False
    
    #Insert first node to frontier and search tree
    search_tree.append({"id":1,"state":snake[0],"expansionsequence": -1,"children":[],"actions":[],"removed":False,"parent":None})
    frontier.append({'id':1,'state':snake[0],'expansionsequence': -1,'children':[],'actions':[],'removed':False,'parent':None})
    
    expansion_seq = 1
    while not found_food:
        # If all node in frontier have been explored but food still not found, then break out the loop
        if len(frontier) == 0: 
            break
        frontier[0]["expansionsequence"] = expansion_seq
        # Get the index of current expanding node in search tree
        index_of_current_state_in_search_tree = next((i for i, state in enumerate(search_tree) if state['id'] == frontier[0].get('id')), None)
        search_tree[index_of_current_state_in_search_tree]["expansionsequence"] = expansion_seq
        #Expand the first frontier
        children ,actions = getChildren(frontier[0],col,row,snake)

        #Insert the children and actions into search_tree and frontier
        for index in range(len(children)):
            removedBool = checkRemoved(children[index],explored,frontier)
            id = len(search_tree) + 1 
            # Only insert node that we want to expand later into frontier
            if removedBool == False:
                frontier.append({'id':id,'state':children[index],'expansionsequence':-1,'children':[],'actions':[],'removed':removedBool,'parent':frontier[0].get('id')})
            
            search_tree.append({'id':id,'state':children[index],'expansionsequence':-1,'children':[],'actions':[],'removed':removedBool,'parent':frontier[0].get('id')})
            search_tree[index_of_current_state_in_search_tree].get('children').append(id)
            search_tree[index_of_current_state_in_search_tree].get('actions').append(actions[index])
            # When food found break the for loop to make sure node is in the last element of search tree
            if funcDist(children[index],[food[0][0],food[0][1]],'check_food') == 0:
                found_food = True
                break
            
        explored.append(frontier[0])
        # delete expanded state    
        del frontier[0]
        
        # Function
        # If snake length greater than 18, do not use straight line distance
        # If current direction is 'w' or 'e', move vertically, then only horizontally
        if len(snake) > 18 and (current_direction == 'w' or current_direction == 'e'):
            for state in frontier:
                rowDistance = funcDist(state.get('state'),food[0],'row')
                colDistance = funcDist(state.get('state'),food[0],'col')
                if rowDistance != 0:
                    frontier[frontier.index(state)]['distance'] = rowDistance
                if rowDistance == 0:
                    frontier[frontier.index(state)]['distance'] = colDistance
        # If current direction is 'n' or 's', move horizontally, then only vertically
        elif len(snake) > 18 and (current_direction == 'n' or current_direction == 's'):
            for state in frontier:
                rowDistance = funcDist(state.get('state'),food[0],'row')
                colDistance = funcDist(state.get('state'),food[0],'col')
                if colDistance != 0:
                    frontier[frontier.index(state)]['distance'] = colDistance
                if colDistance == 0:
                    frontier[frontier.index(state)]['distance'] = rowDistance
        # If snake length smaller than 18, use straight line distance 
        else: 
            for state in frontier:
                distance = funcDist(state.get('state'),food[0],'checkfood')
                frontier[frontier.index(state)]['distance'] = distance        
        frontier = sorted(frontier, key = lambda i: i['distance'])
        
        expansion_seq += 1
    
    #If food inserted in the last element of the search tree
    if search_tree[-1].get('state') == [food[0][0],food[0][1]]:
        goal = search_tree[-1]
        goal_path = [goal]
        while not goal_path[-1].get("parent") == None:
            for s in search_tree:
                if s.get("id")==goal_path[-1].get("parent"):
                    goal_path.append(s)
                    break
                      
        for g in range(1,len(goal_path)):
            index = goal_path[g].get('children').index(goal_path[g-1].get('id'))
            solution.append(goal_path[g].get('actions')[index])
        
        solution = list(reversed(solution))
        
    #If food not found due to the fontier is empty (closed area), forced snake to move to direction that has largest move space   
    else:
        new_state_and_action = findGreatestSpaceToMove(snake,col,row)
        solution.append(new_state_and_action[-1])
        del search_tree[1:]
        search_tree[0].get('children').clear()
        search_tree[0].get('children').append(2)
        del search_tree[0].get('actions')[:]
        search_tree[0].get('actions').append(new_state_and_action[-1])
        search_tree.append({'id':2,'state':[new_state_and_action[0],new_state_and_action[1]],'expansionsequence':-1,'children':[],'actions':[],'removed':False,'parent':1})
    
    return solution, search_tree

# function to calculate the distance (Greedy Best First Search)
def funcDist(firstPoint,secondPoint, coordinate):
    
    x1 = firstPoint[0]
    x2 = secondPoint[0]
    y1 = firstPoint[1]
    y2 = secondPoint[1]
    
    if coordinate == 'row' and y1 == y2 :
        distance = -1
    elif coordinate == 'col' and x1 == x2:
        distance = -1
    elif coordinate == 'row':
        distance = ((y1-y2)**2)**0.5
    elif coordinate == 'col':
        distance = ((x1-x2)**2)**0.5
    else:
        distance = ((x1-x2)**2 + (y1-y2)**2)**0.5
    
    return distance

# get children and actions function
def getChildren(state_to_expand,col,row,snake_loc):
    children = []
    actions = []
    for direction in ('n','s','w','e'):
        if direction=='n':
            child_state = [state_to_expand.get('state')[0],state_to_expand.get("state")[1]-1]
            # check if the snake is already at the top row and
            if (state_to_expand.get('state')[1]!=0) and not (child_state in [s for s in snake_loc]):
                children.append(child_state)
                actions.append(direction)
            
        if direction=='s':
            child_state = [state_to_expand.get("state")[0],state_to_expand.get("state")[1]+1]
             # check if the snake is already at the bottom row
            if (state_to_expand.get('state')[1]!=row-1) and not (child_state in [s for s in snake_loc]):
                children.append(child_state)
                actions.append(direction)
                
        if direction=='w':
            child_state = [state_to_expand.get("state")[0]-1,state_to_expand.get("state")[1]]
            # check if the snake is already at the most left row
            if (state_to_expand.get('state')[0]!=0) and not (child_state in [s for s in snake_loc]):
                children.append(child_state)
                actions.append(direction)
                
        if direction=='e':
            child_state = [state_to_expand.get("state")[0]+1,state_to_expand.get("state")[1]]
            # check if the snake is already at the most right row
            if (state_to_expand.get('state')[0]!=col-1) and not (child_state in [s for s in snake_loc]):
                children.append(child_state)
                actions.append(direction)
    
    return children, actions
    

def checkRemoved(child_state,explored,frontier):
    
    removedBool = False
    if not (child_state in [f.get('state')for f in frontier]) and not (child_state in [e.get('state') for e in explored]):
        removedBool = False
    else: 
        removedBool = True
    
    return removedBool

def findGreatestSpaceToMove(snake_loc,col,row):
    new_move = []
    for direction in ('n','s','w','e'):
        count = 0
        increment = 1
        if direction == 'n':
            while True:
                if not ([snake_loc[0][0],snake_loc[0][1]-increment] in [s for s in snake_loc]):
                    if not (snake_loc[0][1]-increment) == -1:
                        count+=1
                        increment+=1
                    else:
                        break
                else:
                    break
            new_move.append([snake_loc[0][0],snake_loc[0][1]-1,count,'n'])
        if direction == 's':
            while True:
                if not ([snake_loc[0][0],snake_loc[0][1]+increment] in [s for s in snake_loc]):
                    if not (snake_loc[0][1]+increment) == row:
                        count+=1
                        increment+=1
                    else:
                        break
                else:
                    break
            new_move.append([snake_loc[0][0],snake_loc[0][1]+1,count,'s'])
        if direction == 'w':
            while True:
                if not ([snake_loc[0][0]-increment,snake_loc[0][1]] in [s for s in snake_loc]):
                    if not (snake_loc[0][0]-increment) == -1:
                        count+=1
                        increment+=1
                    else:
                        break
                else:
                    break
            new_move.append([snake_loc[0][0]-1,snake_loc[0][1],count,'w'])
        if direction == 'e':
            while True:
                if not ([snake_loc[0][0]+increment,snake_loc[0][1]] in [s for s in snake_loc]):
                    if not (snake_loc[0][0]+increment) == col:
                        count+=1
                        increment+=1
                    else:
                        break
                else:
                    break
            new_move.append([snake_loc[0][0]+1,snake_loc[0][1],count,'e'])
            
    new_move = sorted(new_move, key = lambda i: i[-2])
    
    return new_move[-1]

if __name__ == "__main__":
  p1 = Player({ "maze_size": [10,10], "static_snake_length": True })
  # snake_location [col,row]
  sol, st = p1.run( {'snake_locations': [[7, 9], [6, 9], [5, 9], [5, 8], [5, 7], [5, 6], [5, 5], [5, 4], [6, 4], [6, 3], [6, 2], [7, 2], [7, 1], [8, 1], [9, 1], [9, 2], [8, 2], [8, 3]], 'current_direction': 'e', 'food_locations': [[1,6]]})
  print("Solution is:", sol)
  print("Search tree is:",[s for s in st])
  