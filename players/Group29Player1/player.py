class Player():
    name = "informed_GreedyBestFirstSearch"
    informed = True
    group = "Paiseh"
    members = [
        ["Chan Wei Qi", "18102855"],
        ["Tham Yee Jin", "18003897"],
        ["Cheong Pui Yien", "18106914"]
    ]

    def __init__(self, setup):
        self.setup = setup
    
    def findActions(self, snake, maze_size):
        directions = ''
        
        if (snake[0][0] != 0 and [snake[0][0]-1,snake[0][1]] not in snake): # Not to hit wall and snake
            directions = directions + 'w'
        if (snake[0][0] != maze_size[0] - 1 and [snake[0][0]+1,snake[0][1]] not in snake): # Not to hit wall and snake
            directions = directions + 'e'      
        if (snake[0][1] != 0 and [snake[0][0],snake[0][1]-1] not in snake): # Not to hit wall and snake
            directions = directions + 'n'
        if (snake[0][1] != maze_size[1] - 1 and [snake[0][0],snake[0][1]+1] not in snake): # Not to hit wall and snake
            directions = directions + 's'

        return list(directions)
    
    def findSnakeLocations(self, snake, action):
        if action == 'n':
            snake = [[snake[0][0],snake[0][1]-1]] + snake[:-1]
        elif action == 's':
            snake = [[snake[0][0],snake[0][1]+1]] + snake[:-1]
        elif action == 'e':
            snake = [[snake[0][0]+1,snake[0][1]]] + snake[:-1]
        elif action == 'w':
            snake = [[snake[0][0]-1,snake[0][1]]] + snake[:-1]

        return snake
    
    def run(self, problem): 
        solution = []
        search_tree = []
        frontier = [] 
        explored = []
        snake = problem['snake_locations']
        food = problem['food_locations']
        maze_size = self.setup['maze_size']
        found_goal = False
        count = 1 # id for node
        expansion = 1 # expansion sequence of node
        
        # Root node
        node = {
            "id": count,
            "state": ",".join([str(num_str) for num_str in snake[0]]),
            "expansionsequence": -1,
            "children": [],
            "actions": [],
            "removed": False,
            "parent": None
        }
        
        # Append root node to search tree
        search_tree.append(node)
        
        # Append root node to frontier
        frontier.append({"parent": None, "snake": snake, "id": count, "estimateddistance": manhattan(snake, food)})

        while not found_goal and len(frontier) != 0:
            # Find actions for first element in frontier
            actions = self.findActions(frontier[0]['snake'], maze_size)
            
            # Find node from search tree
            search_node = [tree_node for tree_node in search_tree if tree_node['id'] == frontier[0]['id']]
            
            # Update node in search tree
            node = search_node[0]
            node['expansionsequence'] = expansion
            node['actions'] = actions
            
            # Update snake locations
            snake = frontier[0]['snake']
          
            # Goal test during expansion
            for f in food:
                if frontier[0]['snake'][0] == f:
                    found_goal = True
                    break
            if found_goal == True:
                break
            
            # Append node to explored
            explored.append(frontier[0]['snake'][0])
            
            # Delete first element from frontier
            del frontier[0]
            
            for action in node['actions']:
                count += 1
                new_snake = self.findSnakeLocations(snake, action)
                
                if new_snake[0] not in explored and new_snake[0] not in [f['snake'][0] for f in frontier]:
                    child_node = {
                        "id": count,
                        "state": ",".join([str(num_str) for num_str in new_snake[0]]),
                        "expansionsequence": -1,
                        "children": [],
                        "actions": [],
                        "removed": False,
                        "parent": node['id']
                    }
                    frontier.append({"parent": node['id'], "snake": new_snake, "id": count, "estimateddistance": manhattan(new_snake, food)})
                else:
                    child_node = {
                        "id": count,
                        "state": ",".join([str(num_str) for num_str in new_snake[0]]),
                        "expansionsequence": -1,
                        "children": [],
                        "actions": [],
                        "removed": True,
                        "parent": node['id']
                    }
                    
                search_tree.append(child_node)
                node['children'].append(count)
            
            # Sort frontier based on estimated distance
            frontier = sorted(frontier, key = lambda i: i['estimateddistance'])
            
            count += 1
            expansion += 1
      
        # Find solution
        while node['parent'] != None:
            parent_node = [tree_node for tree_node in search_tree if tree_node['id'] == node['parent']][0]
            index = parent_node['children'].index(node['id'])
            action = parent_node['actions'][index]
            solution = [action] + solution
            node = parent_node
        
        if found_goal == False:
            solution = solution + ['n', 's', 'e', 'w']
            
        return solution, search_tree

# Estimated distance
def manhattan(snake, food):
    return abs(food[0][0] - snake[0][0]) + abs(food[0][1] - snake[0][1])
