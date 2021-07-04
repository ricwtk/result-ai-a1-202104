class Node:
    id = 1

    def __init__(self, position, parent=None, cost=0, functionCost=0):
        self.id = Node.id
        self.position = position
        self.expansion_sequence = -1
        self.cost = cost
        self.functionCost = functionCost
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
                "children": [child.id for child in self.children],
                "actions": self.actions,
                "removed": self.removed,
                "parent": self.parent.id
            }
        else:
            return {
                "id": self.id,
                "state": str(self.position)[1:-1],
                "expansionsequence": self.expansion_sequence,
                "children": [child.id for child in self.children],
                "actions": self.actions,
                "removed": self.removed,
                "parent": None
            }

    def expand(self, maze_size, expansion_sequence, snake_locations):
        # Generate side locations
        points = [
            [self.position[0], max(self.position[1]-1, 0)
             ],                 # North
            [self.position[0], min((self.position[1]+1),
                                   maze_size[0]-1)],  # South
            [min(self.position[0]+1, maze_size[0]-1),
             self.position[1]],     # East
            [max(self.position[0]-1, 0), self.position[1]
             ]                   # West
        ]
        actions = ["n", "s", "e", "w"]

        # Remove center duplicates
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
            self.children.append(Node(
                point, self, (self.cost+1), (self.cost + 1 + Player.grid[point[0]][point[1]])))

        # Modify actions, and expansion sequence
        self.actions = actions
        self.expansion_sequence = expansion_sequence

        return self.children


class Player():
    name = "A* Search"
    informed = True
    group = "Artificial Codeine"
    members = [
        ["Michael Lu Han Xien", "18081588"],
        ["Anjali Radha Krishna", "16009847"],
        ["Garv Sudhir Nair", "19073535"],
        ["Yong Tze Min", "19079748"]
    ]

    def __init__(self, setup):
        Player.maze_size = setup["maze_size"]
        Player.grid = []
        self.static_length = setup["static_snake_length"]

    def generateGrid(snake_locations, food_locations):
        Player.grid.clear()
        temp = []
        for x in range(Player.maze_size[0]):
            for y in range(Player.maze_size[1]):
                temp.append(None)
            Player.grid.append(temp.copy())
            temp.clear()

        for food in food_locations:
            Player.spreadFoodDistance(food[0], food[1], 1)

        for [x, y] in snake_locations:
            Player.grid[x][y] = "X"

    def spreadFoodDistance(x, y, point):
        if Player.grid[x][y] == None:
            Player.grid[x][y] = point
            Player.spreadFoodDistance(
                x, min(y+1, Player.maze_size[1]-1), point+1)  # North
            Player.spreadFoodDistance(x, max(y-1, 0), point+1)  # South
            Player.spreadFoodDistance(max(x-1, 0), y, point+1)  # Left
            Player.spreadFoodDistance(
                min(x+1, Player.maze_size[0]-1), y, point+1)  # Right

        elif Player.grid[x][y] > point:
            Player.grid[x][y] = point
            Player.spreadFoodDistance(
                x, min(y+1, Player.maze_size[1]-1), point+1)  # North
            Player.spreadFoodDistance(x, max(y-1, 0), point+1)  # South
            Player.spreadFoodDistance(max(x-1, 0), y, point+1)  # Left
            Player.spreadFoodDistance(
                min(x+1, Player.maze_size[0]-1), y, point+1)  # Right

    def run(self, problem):
        snake_locations = problem["snake_locations"]
        current_direction = problem["current_direction"]
        food_locations = problem["food_locations"]
        Player.generateGrid(snake_locations, food_locations)
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

            children = frontiers[0].expand(
                Player.maze_size, expansion_sequence, snake_locations)
            node_list.extend(children)
            checked.append(frontiers[0].position)

            for child in children:
                if child.position not in checked:
                    if child.position in [f.position for f in frontiers]:
                        index = [f.position for f in frontiers].index(
                            child.position)
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
            frontiers = sorted(
                frontiers, key=lambda x: x.functionCost, reverse=False)

        while traceback.parent != None:
            next_node = traceback
            traceback = traceback.parent

        if next_node == None:
            solution = current_direction
        else:
            solution = traceback.actions[traceback.children.index(next_node)]
        search_tree = [node.toDict() for node in node_list]

        return solution, search_tree
