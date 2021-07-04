# Expand all possible moves
def expandNode(maxBound, parentNode, startingID, expSeq, currentDirection, snakePos=None):
    # Map out movement based on direction and remove opposite side (We do not consider backwards)
    opposites = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}
    movement = {'n': [0, -1], 's': [0, 1], 'w': [-1, 0], 'e': [1, 0]}
    availableDirections = 'nswe'.replace(opposites[currentDirection], "")
    children = []

    # Search all states
    for x in list(availableDirections):
        startingID += 1
        pstate = parentNode['state'].split(",")
        state = [int(pstate[0]) + movement[x][0], int(pstate[1]) + movement[x][1]]
        removal = False

        # Checks for bounds
        if (state[0] < 0 or state[0] >= maxBound[0]) or (state[1] < 0 or state[1] >= maxBound[1]):
            removal = True

        # Checks for collision with other snake parts
        elif state in snakePos:
            removal = True

        # Update snake Loc
        currSnakePos = list(snakePos)
        currSnakePos.pop()
        currSnakePos.insert(0, state)

        # Generate possible children
        children.append([{
            "id": startingID,
            "state": "{},{}".format(state[0], state[1]),
            "expansionsequence": -1,
            "children": [],
            "actions": [],
            "removed": removal,
            "parent": parentNode['id']
        }, x, currSnakePos])

        # Update parent node information
        parentNode['children'] = [x[0]['id'] for x in children]
        parentNode['expansionsequence'] = expSeq
        parentNode['actions'] = list(availableDirections)

    return children, parentNode, startingID


def compileSolution(endNode, searchTree, currentDirection):
    opposites = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}
    solution = [currentDirection]
    parentID = endNode["parent"]
    while parentID is not None:
        directionFacing = "nswe".replace(endNode["actions"][0], "").replace(endNode["actions"][1], "").replace(
            endNode["actions"][2], "")  # ['n','s','w']
        directionFacing = opposites[directionFacing]
        solution.insert(0, directionFacing)
        for x in searchTree:
            if x['id'] == parentID:
                endNode = x
                parentID = x['parent']
                break
    return solution


class Player:
    name = "January Sky (BFS)"
    # Breath-First-Search
    informed = False
    group = "yes"
    # Change it later
    members = [
        ["Zahaen Hilmie", "17076407"],
        ["Kok Wui Lee", "17069469"],
        ["Goh Wai Hoong", "17068826"],
        ["Lee Jyh Yong", "17074683"]
    ]

    def __init__(self, setup):
        self.maxBound = setup["maze_size"]
        self.staticsize = setup['static_snake_length']

    def run(self, problem):
        game_ended = False
        search_tree = []
        frontier = []
        solution = []
        explored = []

        # Initialize the initial node
        initialState = problem['snake_locations'][0]
        foodLoc = problem["food_locations"][0]
        initialNode = {
            "id": 1,
            "state": "{},{}".format(initialState[0], initialState[1]),
            "expansionsequence": -1,
            "children": [],
            "actions": [],
            "removed": False,
            "parent": None
        }
        search_tree.append(initialNode)

        ## Frontier consists of [{Node information}, Distance of food from Node, The snake's current body position]
        frontier.insert(0, [initialNode, problem['current_direction'], problem['snake_locations']])
        currentNodeID = 1
        nodeExpanded = 1

        # Keeps looping until goal is found
        while not game_ended:

            snakeLoc = frontier[0][2]
            currentDirection = frontier[0][1]

            # Expand from current position
            children, updatedParentNode, currentNodeID = expandNode(self.maxBound, frontier[0][0], currentNodeID,
                                                                    nodeExpanded, currentDirection, snakeLoc)

            explored.append(frontier[0])

            # Update parent in search tree
            for x in search_tree:
                if x['id'] == updatedParentNode['id']:
                    x['expansionsequence'] = updatedParentNode['expansionsequence']
                    x['actions'] = updatedParentNode['actions']
                    x['children'] = updatedParentNode['children']
                    break

            # Confirmed that we expanded a node
            nodeExpanded += 1

            del frontier[0]


            for child in children:

                # No loopy
                if child[0]["state"] in [e[0]["state"] for e in explored]:
                    child[0]["removed"] = True

                # No frontier repeats
                elif child[0]["state"] in [f[0]["state"] for f in frontier]:
                    child[0]["removed"] = True

                # Add children regardless to search tree for documentation
                search_tree.append(child[0])

                if child[0]["state"] == "{},{}".format(foodLoc[0],foodLoc[1]):
                    game_ended = True
                    solution = compileSolution(updatedParentNode, search_tree, child[1])

                elif child[0]["removed"] == False:
                    frontier.append(child)

            # Program ends here if it gets stuck and won't return solution
            if len(frontier) < 1:
                print("No solution can be found! Stopping search...")
                game_ended = True


        return solution, search_tree


if __name__ == "__main__":
    p1 = Player({"maze_size": [10, 10], "static_snake_length": False})
    # sol,st = p1.run()

    ## to test without webapp
    sol, st = p1.run({'snake_locations': [[9, 5], [8, 5], [7, 5], [6, 5], [5, 5], [5, 6], [5, 7], [5, 8], [5, 9]],
                      'current_direction': 'e', 'food_locations': [[2, 6]]})

    # print("Search tree is:")
    # print(st)
