import random
import numpy as np


class Player():
    name = "Uninformed Agent"
    group = "AIPeople"
    members = [
        ["Akmal Ikraam", "18010157"],
        ["Daniesha Jayasinghe", "16044760"],
        ["Tan Li Siang", "17103060"],
        ["Tan Pee Aun", "17037177"]
    ]
    informed = False

    def __init__(self, setup):
        # setup = {
        #   maze_size: [int, int],
        #   static_snake_length: bool
        # }
        self.setup = setup

    def newSearch(self, problem):
        mazeY = self.setup['maze_size'][0] - 1
        mazeX = self.setup['maze_size'][1] - 1
        snakeLoc = problem['snake_locations']
        possibleSol = []

        EnextStep = np.clip(
            [snakeLoc[0][0]+1, snakeLoc[0][1]], 0, mazeX).tolist()
        WnextStep = np.clip(
            [snakeLoc[0][0]-1, snakeLoc[0][1]], 0, mazeX).tolist()
        NnextStep = np.clip(
            [snakeLoc[0][0], snakeLoc[0][1] - 1], 0, mazeY).tolist()
        SnextStep = np.clip(
            [snakeLoc[0][0], snakeLoc[0][1] + 1], 0, mazeY).tolist()

        if(EnextStep not in snakeLoc):
            if(EnextStep[0] <= mazeY and EnextStep[1] <= mazeX):
                print("CURRENTLOC: ", snakeLoc)
                print("E NEXT STEP: ", EnextStep)
                possibleSol.append('e')

        if(WnextStep not in snakeLoc):
            if(WnextStep[0] <= mazeY and EnextStep[1] <= mazeX):
                print("CURRENTLOC: ", snakeLoc)
                print("W NEXT STEP: ", WnextStep)
                possibleSol.append('w')

        if(SnextStep not in snakeLoc):
            if(SnextStep[0] <= mazeY and EnextStep[1] <= mazeX):
                print("CURRENTLOC: ", snakeLoc)
                print("S NEXT STEP: ", SnextStep)
                possibleSol.append('s')

        if(NnextStep not in snakeLoc):
            if(NnextStep[0] <= mazeY and EnextStep[1] <= mazeX):
                print("CURRENTLOC: ", snakeLoc)
                print("N NEXT STEP: ", NnextStep)
                possibleSol.append('n')

        selectedSol = possibleSol[random.randint(0, len(possibleSol)-1)]

        print("POSSIBLE SOL: ", possibleSol)
        print("SELECTED SOL: ", selectedSol)

        return selectedSol

    def run(self, problem):
        directions = "nswe"
        # the following algorithm is NOT a valid algorithm
        # it randomly generates solution that is invalid
        # its purpose is to show you how this class will work
        # not a guide to how to write your algorithm

        solution = self.newSearch(problem)

        # the following search tree is a static search tree
        # to show you the format of the variable
        # to generate a search tree that can be displayed in the frontend.
        # you are required to generate the search tree based on your search algorithm
        search_tree = [
            {
                "id": 1,
                "state": "0,0",
                "expansionsequence": 1,
                "children": [2, 3, 4],
                "actions": ["n", "w", "e"],
                "removed": False,
                "parent": None
            }

        ]
        # this function should return the solution and the search_tree
        return solution, search_tree


if __name__ == "__main__":
    p1 = Player({"maze_size": [10, 10], "static_snake_length": False})
    sol, st = p1.run({'snake_locations': [
                     [0, 5]], 'current_direction': 'e', 'food_locations': [[6, 7]]})
    print("Solution is:", sol)
    print("Search tree is:")
    print(st)