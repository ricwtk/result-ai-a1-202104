import random
import numpy as np


class Player():
    name = "Informed Agent"
    group = "AIPeople"
    members = [
        ["Akmal Ikraam", "18010157"],
        ["Daniesha Jayasinghe", "16044760"],
        ["Tan Li Siang", "17103060"],
        ["Tan Pee Aun", "17037177"]
    ]
    # informed = False # lecturer commented
    informed = True # lecturer added

    def __init__(self, setup):
        # setup = {
        #   maze_size: [int, int],
        #   static_snake_length: bool
        # }
        self.setup = setup

    def breakLoop(self, problem):
        snakeLoc = problem['snake_locations']
        # foodLoc = problem['food_locations']'
        mazeY = self.setup['maze_size'][0] - 1
        mazeX = self.setup['maze_size'][1] - 1
        result = []

        EnextStep = np.clip(
            [snakeLoc[0][0]+1, snakeLoc[0][1]], 0, mazeX).tolist()
        if(EnextStep not in snakeLoc):
            print("E NSTEP ", EnextStep not in snakeLoc)
            result.append('e')
            print("NEW SOL ", result)

        WnextStep = np.clip(
            [snakeLoc[0][0]-1, snakeLoc[0][1]], 0, mazeX).tolist()
        if(WnextStep not in snakeLoc):
            print("W NSTEP ", WnextStep not in snakeLoc)
            result.append('w')
            print("NEW SOL ", result)

        NnextStep = np.clip(
            [snakeLoc[0][0], snakeLoc[0][1] - 1], 0, mazeY).tolist()
        if(NnextStep not in snakeLoc):
            print("N NSTEP ", NnextStep not in snakeLoc)
            result.append('n')
            print("NEW SOL ", result)

        SnextStep = np.clip(
            [snakeLoc[0][0], snakeLoc[0][1] + 1], 0, mazeY).tolist()
        if(SnextStep not in snakeLoc):
            print("S NSTEP ", SnextStep not in snakeLoc)
            result.append('s')
            print("NEW SOL ", result)

        finalRes = result[random.randint(0, len(result)-1)]
        print("SOLUTIONS ==> ", result)
        print("SELECTED SOL ==> ", finalRes)
        return finalRes

    def search(self, problem):
        snakeLoc = problem['snake_locations']
        foodLoc = problem['food_locations']
        mazeY = self.setup['maze_size'][0] - 1
        mazeX = self.setup['maze_size'][1] - 1

        if(snakeLoc[0][1] < foodLoc[0][1]):
            nextStep = np.clip(
                [snakeLoc[0][0], snakeLoc[0][1] + 1], 0, mazeY).tolist()
            if(nextStep not in snakeLoc):
                solution = 's'
            else:
                solution = self.breakLoop(problem)
        elif(snakeLoc[0][1] > foodLoc[0][1]):
            nextStep = np.clip(
                [snakeLoc[0][0], snakeLoc[0][1] - 1], 0, mazeY).tolist()
            if(nextStep not in snakeLoc):
                solution = 'n'
            else:
                solution = self.breakLoop(problem)
        elif(snakeLoc[0][0] < foodLoc[0][0]):
            nextStep = np.clip(
                [snakeLoc[0][0]+1, snakeLoc[0][1]], 0, mazeX).tolist()
            if(nextStep not in snakeLoc):
                solution = 'e'
            else:
                solution = self.breakLoop(problem)
        elif(snakeLoc[0][0] > foodLoc[0][0]):
            nextStep = np.clip(
                [snakeLoc[0][0]-1, snakeLoc[0][1]], 0, mazeX).tolist()
            if(nextStep not in snakeLoc):
                solution = 'w'
            else:
                solution = self.breakLoop(problem)

        return solution

    def run(self, problem):
        directions = "nswe"
        # the following algorithm is NOT a valid algorithm
        # it randomly generates solution that is invalid
        # its purpose is to show you how this class will work
        # not a guide to how to write your algorithm

        solution = self.search(problem)

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
