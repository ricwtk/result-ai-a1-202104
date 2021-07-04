class Node:
    id = 1

    def __init__(self, position, parent=None, cost=0):
        self.id = Node.id
        self.position = position
        self.expansion_sequence = -1
        self.cost = cost
        self.children = []
        self.actions = []
        self.removed = False
        self.parent = parent
        Node.id += 1

    def remove(self):
        self.removed = True

    def toDict(self):
        if self.parent != None:
            return {
                "id": self.id,
                "state": str(self.position)[1:-1],
                "expansionsequence": self.expansion_sequence,
                "children" : [child.id for child in self.children],
                "actions" : self.actions,
                "removed" : self.removed,
                "parent" : self.parent.id
            }
        else:
            return {
                "id": self.id,
                "state": str(self.position)[1:-1],
                "expansionsequence": self.expansion_sequence,
                "children" : [child.id for child in self.children],
                "actions" : self.actions,
                "removed" : self.removed,
                "parent" : None
            }
    
    def expand(self, maze_size, expansion_sequence, snake_locations):
        # Generate side locations
        points = [
            [self.position[0], max(self.position[1]-1, 0)],                 # North
            [self.position[0], min((self.position[1]+1), maze_size[0]-1)],  # South
            [min(self.position[0]+1, maze_size[0]-1),self.position[1]],     # East
            [max(self.position[0]-1, 0),self.position[1]]                   # West
        ]
        actions = ["n", "s", "e", "w"]

        # Remove location duplicates
        for i in range(points.count(self.position)):
            del actions[points.index(self.position)]          
            del points[points.index(self.position)]      

        # Remove snake locations
        for snake in snake_locations:
            if snake in points:
                del actions[points.index(snake)]
                del points[points.index(snake)]

        # Create child object and add them into the parent's children 
        for point in points:
            self.children.append(Node(point, self, (self.cost+1)))
        
        # Modify actions, and expansion sequence
        self.actions = actions
        self.expansion_sequence = expansion_sequence

        return self.children    

class Player():
    name = "Uniform-Cost Seach"
    informed = False
    group = "Artificial Codeine"
    members = [
        ["Michael Lu Han Xien", "18081588"],
        ["Anjali Radha Krishna", "16009847"],
        ["Garv Sudhir Nair", "19073535"],
        ["Yong Tze Min", "19079748"]
    ]

    def __init__(self, setup):
        Player.maze_size = setup["maze_size"]
        self.static_length = setup["static_snake_length"]

    def run(self, problem):
        snake_locations = problem["snake_locations"]
        current_direction = problem["current_direction"]
        food_locations = problem["food_locations"]
        
        frontiers = [Node(snake_locations[0])]
        node_list = frontiers.copy()
        checked = snake_locations.copy()
        expansion_sequence = 1
        food_found = False
        traceback = None
        next_node = None
        while not food_found:
            if frontiers[0].position in food_locations:
                food_found = True
                traceback = frontiers[0]
                continue

            children = frontiers[0].expand(Player.maze_size, expansion_sequence, snake_locations)
            node_list.extend(children)
            checked.append(frontiers[0].position)
            
            for child in children:
                if child.position not in checked:
                    if child.position in [f.position for f in frontiers]:
                        index = [f.position for f in frontiers].index(child.position)
                        if child.cost < frontiers[index].cost:
                            frontiers[index].remove()
                            del frontiers[index]
                            frontiers.append(child)
                        else:
                            child.remove()
                    else:
                        frontiers.append(child)
            
            if len(frontiers) == 1 and food_found == False:
                food_found = True
                traceback = frontiers[0]

            expansion_sequence += 1
            del frontiers[0]
            frontiers = sorted(frontiers, key=lambda x: x.cost, reverse=False)

        while traceback.parent != None:
            next_node = traceback
            traceback = traceback.parent

        if next_node == None:
            solution = current_direction
        else:
            solution = traceback.actions[traceback.children.index(next_node)]
        search_tree = [node.toDict() for node in node_list]

        return solution, search_tree