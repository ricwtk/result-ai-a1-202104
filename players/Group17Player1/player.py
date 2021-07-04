class Player():
    name = "A* search"
    group = "1G3I"
    members = [
        ["Peng Shao Wei", "19084227"],
        ["Koh Jia Yi", "17063470"],
        ["Ng J-Han", "18042507"],
	["Gan Kai Wen", "16007940"]
    ]
    informed = True
    

    def __init__(self, setup):
        self.maze_size = setup["maze_size"]
        self.setup = setup

    def run(self, problem):
        food_locations = problem["food_locations"]
        initial = problem["snake_locations"]
        initialNode = self.generateInitialNode(initial)
        solution = []

        for i in range(len(food_locations)):
            goal = f"{food_locations[i][0]},{food_locations[i][-1]}"

            searchAlgo = AStar(self.maze_size, len(problem["snake_locations"]) + i)
            searchAlgo.clearExploredState()

            sol = searchAlgo.run(initialNode, goal)
            
            result = self.formatSolution(sol[0], sol[-1])
            
            st = self.tidySearchTree(sol[-1], result[-1])
            
            initialNode = sol[0]
            initialNode["cost"] = 0
            initialNode["estimatedCost"] = self.maze_size[0] * self.maze_size[-1]
            initialNode["parent"] = None
            solution += result[0]
     
        return [solution, st]


    def formatSolution(self, solution, search_tree):
        result = []
        newST = []
        currentNode = solution

        while not currentNode["parent"] == None:
            result.insert(0, currentNode["previousAction"])
            newST.append(currentNode["id"])
            for item in search_tree:
                if item["id"] == currentNode["parent"]:
                    currentNode = item
                    break
        newST.append(currentNode["id"])
        return [result, newST]

    def tidySearchTree(self, st, stateId):
        result = st[:]
        for node in result:
            if node["id"] not in stateId:
                node["expansionsequence"] = -1
        return result

    def generateInitialNode(self, location):
        return {
            "id": 1,
            "state":  f"{location[0][0]},{location[0][-1]}",
            "expansionsequence": 1,
            "children": [],
            "actions": ["n","s","e","w"],
            "removed": False,
            "parent": None,
            "cost": 0,
            "estimatedCost": self.maze_size[0] * self.maze_size[-1],
            "occupiedState": location
        }

class Search():
    stateId = 1
    exploredState = []
    snakeLen = 1

    def __init__(self, maze_size, snakeLen):
        self.maze_size = maze_size
        self.snakeLen = snakeLen
        
    def checkIfExplored(self, state):
        if state in self.exploredState:
            return True
        return False

    def clearExploredState(self):
        self.exploredState = []

    def generateNewAction(self, location):
        result = []
        location = location.split(",")
        if int(location[0]) + 1 < self.maze_size[0]:
            result.append("e")
        if int(location[0]) - 1 >= 0:
            result.append("w")
        if int(location[-1]) - 1 >= 0:
            result.append("n")
        if int(location[-1]) + 1 < self.maze_size[-1]:
            result.append("s")
        return result

    def generateNewStateFromAction(self, action, node):
        state = node["state"].split(",")
        if action == "w":
            newState = f"{int(state[0])-1},{int(state[-1])}"
            newStateArr = newState.split(",")
            if int(state[0]) - 1 > -1 and [int(newStateArr[0]),int(newStateArr[-1])] not in node["occupiedState"]:
                return newState
        if action == "e":
            newState = f"{int(state[0])+1},{int(state[-1])}"
            newStateArr = newState.split(",")
            if int(state[0]) + 1 < self.maze_size[0] and [int(newStateArr[0]),int(newStateArr[-1])] not in node["occupiedState"]:
                return newState
        if action == "n":
            newState = f"{int(state[0])},{int(state[-1])-1}"
            newStateArr = newState.split(",")
            if int(state[-1]) - 1 > -1 and [int(newStateArr[0]),int(newStateArr[-1])] not in node["occupiedState"]:
                return newState
        if action == "s":
            newState = f"{int(state[0])},{int(state[-1])+1}"
            newStateArr = newState.split(",")
            if int(state[-1]) + 1 < self.maze_size[-1] and [int(newStateArr[0]),int(newStateArr[-1])] not in node["occupiedState"]:
                return newState

        return None

    def expandAndReturnChildren(self, node, goalNode="0,0"):
        children = []
        for action in node["actions"]:
            self.stateId += 1
            newState = self.generateNewStateFromAction(action, node)
       
            if newState is not None:
                newStateArr = newState.split(",")
                child = {
                    "id": self.stateId,
                    "state": newState,
                    "expansionsequence": node["expansionsequence"] + 1,
                    "children": [],
                    "actions": self.generateNewAction(newState),
                    "removed": self.checkIfExplored(newState),
                    "parent": node["id"],
                    "previousAction": action,
                    "occupiedState": [[int(newStateArr[0]), int(newStateArr[-1])]] + node["occupiedState"][0: self.snakeLen-1] 
                }
            
                children.append(child)
                node["children"].append(self.stateId)
        return children

    
class AStar(Search):
    def run(self, initial_state, goal_state):
        self.clearExploredState()
        self.stateId = initial_state["id"]
        frontier = []
        found_goal = False
        frontier.append(initial_state)  
        search_tree = []
        search_tree.append(initial_state)
        
        while not found_goal:
            frontier.sort(key=lambda x: (x["estimatedCost"] + x["cost"], x["estimatedCost"]))
            
            if frontier[0]["state"] == goal_state:
                found_goal = True
                solution = frontier[0]
                break
            children = self.expandAndReturnChildren(frontier[0], goal_state)

            self.exploredState.append(frontier[0]["state"])
            
            del frontier[0]


            for child in children:
                search_tree.append(child)
                if (
                    not (child["removed"])
                    and not (child["state"] in [f["state"] for f in frontier])
                    and child["state"] not in self.exploredState
                ):
    
                    frontier.append(child)
        search_tree.append(solution)
        return [solution, search_tree]


    def getDistance(self, currentState, destination):
        currentState = currentState.split(",")
        destination = destination.split(",")
        return abs(int(destination[0]) - int(currentState[0])) + abs(int(destination[-1]) - int(currentState[-1]))


    def expandAndReturnChildren(self, node, goalNode="0,0"):
        children = []
        for action in node["actions"]:
            self.stateId += 1
            newState = self.generateNewStateFromAction(action, node)
            if newState is not None:
                newStateArr = newState.split(",")
                child = {
                    "id": self.stateId,
                    "state": newState,
                    "expansionsequence": node["expansionsequence"] + 1,
                    "children": [],
                    "actions": self.generateNewAction(newState),
                    "removed": self.checkIfExplored(newState),
                    "parent": node["id"],
                    "previousAction": action,
                    "cost": node["cost"] + 1,
                    "estimatedCost": self.getDistance(newState, goalNode),
                    "previousAction": action,
                    "occupiedState": [[int(newStateArr[0]), int(newStateArr[-1])]] + node["occupiedState"][0: self.snakeLen-1] 
                }
            
                children.append(child)
                node["children"].append(self.stateId)
        return children


if __name__ == "__main__":
    p1 = Player({"maze_size": [20, 20], "static_snake_length": False})
    sol, st = p1.run({'snake_locations': [[8, 12], [8, 11], [8, 10], [8, 9], [8, 8], [8, 7], [8, 6]], 
    'current_direction': 's', 'food_locations': [[2, 1], [8, 1]]})
    print("Solution is:", sol)
    print("Search tree is:")
    #print(st)

