import math

class Player():
    name = "Informed player"
    group = "Kung Fu Pandas"
    members = [
        ["Siow Woon Kang", "18042135"],
        ["Wong Yuen-Yi ", "17112723"],
        ["Wong Wei Chean ", "18000133"],
        ["Yash Aubeeluck ", "19059401"]
    ]
    informed = True
    
    def __init__(self, setup):
        # setup = {
        #      maze_size: [int, int],
        #      static_snake_length: bool
        # }
        self.setup = setup
    
    #function to find the distance between snake and food
    def distance(self, x1, y1, x2, y2):
        ans = (math.sqrt(((x1-x2)**2) + ((y1-y2)**2)))
        return ans
    
    #function to find which node already went through and it's a loopy path
    def findRedundant(self, all_locations, x1, y1):
        for i in range (len(all_locations)):
            #remove if it's a loopy path
            if x1 == all_locations[i][0] and y1 == all_locations[i][1]:
                return True
        return False

    #function find direction
    def find_direction(self, x1, y1, x2, y2):
        if (x1 < y1):
            direction = 'w'
        elif (x1 > y1):
            direction = 'e'
        elif (x2 > y2):
            direction = 's'
        elif (x2 < y2):
            direction = 'n'
        return direction
    
    #function to add dictionary into the search tree
    def add_dict(self, search_tree, tree_id, tree_state_column, tree_state_row, tree_expansionsequence, 
                 tree_removed, tree_parent):
        #append a new search tree
        search_tree.append({
            "id": tree_id,
            "state": str(tree_state_column) + "," + str(tree_state_row),
            "expansionsequence": tree_expansionsequence,
            "children": [],
            "actions": [],
            "removed": tree_removed,
            "parent": tree_parent
            })
        return search_tree
    
    #function to fill in the existing search tree values
    def insert_list(self, ori_list, id_change, children, action, exp_seq):
        ori_list[id_change-1]['children'].append(children)
        ori_list[id_change-1]['actions'].append(action)
        ori_list[id_change-1]['expansionsequence']=exp_seq
        return ori_list
    # def add_values_in_dict(self, sample_dict, key, list_of_values):
    #     if key not in sample_dict:
    #         sample_dict[key] = list()
    #     sample_dict[key].extend(list_of_values)
    #     return sample_dict

    def greedy_bfs(self, snake_loc, food_loc, search_tree):
        # 10x10
        #0<x<11, 0<y<11
        #find the shortest distance
        shortest_distance = (math.sqrt((abs(food_loc[0]-snake_loc[0])**2) + (abs(food_loc[1]-snake_loc[1])**2)))
        #pq is PriorityQueue that stores all the shortest distance and snake's location
        pq = [[shortest_distance, snake_loc[0], snake_loc[1], 1]] #last num is id number
        #to store all possible snake location without removing 
        all_locations = [[snake_loc[0], snake_loc[1]]]
        all_directions = []
        #count id
        next_id_count = 1
        #count expansion sequence number
        exp_seq = 0
        #while loop, to store values in PriorityQueue until the distance is 0, which indicates snake's location is on food
        while pq[0][0]!=0 :
            exp_seq = exp_seq + 1
            #to store the latest location of the snake
            latest_location = [pq[0][1], pq[0][2]]
            #if the snake's location is not out of the maze size
            if 0<=pq[0][1]-1<=9:
                next_id_count = next_id_count + 1
                #PriorityQueue has a new array value
                pq.append([self.distance(pq[0][1]-1, pq[0][2], food_loc[0], food_loc[1]), pq[0][1]-1, pq[0][2], next_id_count])
                #find direction from the latest location of the snake to the new location
                direction = self.find_direction(pq[0][1]-1, latest_location[0], pq[0][2], latest_location[1])
                #fill in value for the particular dictionary of the search tree
                search_tree = self.insert_list(search_tree, pq[0][3], next_id_count, direction, exp_seq)
                #add a new dictionary in the search tree
                search_tree = self.add_dict(search_tree, next_id_count, pq[0][1]-1, pq[0][2], -1, self.findRedundant(all_locations, pq[0][1]-1, pq[0][2]), pq[0][3])
                #Has all the locations considered in all locations
                all_locations.append([pq[0][1]-1, pq[0][2]])
                
            if 0<=pq[0][1]+1<=9:
                next_id_count = next_id_count +1
                pq.append([self.distance(pq[0][1]+1, pq[0][2], food_loc[0], food_loc[1]), pq[0][1]+1, pq[0][2], next_id_count])
                direction = self.find_direction(pq[0][1]+1, latest_location[0], pq[0][2], latest_location[1])
                search_tree = self.insert_list(search_tree, pq[0][3], next_id_count, direction, exp_seq)
                search_tree = self.add_dict(search_tree, next_id_count, pq[0][1]+1, pq[0][2], -1, self.findRedundant(all_locations, pq[0][1]+1, pq[0][2]), pq[0][3])
                all_locations.append([pq[0][1]+1, pq[0][2]])
                
            if 0<=pq[0][2]+1<=9:
                #pq[0][1], pq[0][2]+1
                next_id_count = next_id_count +1
                pq.append([self.distance(pq[0][1], pq[0][2]+1, food_loc[0], food_loc[1]), pq[0][1], pq[0][2]+1, next_id_count])
                direction = self.find_direction(pq[0][1], latest_location[0], pq[0][2]+1, latest_location[1])
                search_tree = self.insert_list(search_tree, pq[0][3], next_id_count, direction, exp_seq)
                search_tree = self.add_dict(search_tree, next_id_count, pq[0][1], pq[0][2]+1, -1, self.findRedundant(all_locations, pq[0][1], pq[0][2]+1), pq[0][3])
                all_locations.append([pq[0][1], pq[0][2]+1])
                
            if 0<=pq[0][2]-1<=9:
                #pq[0][1], pq[0][2]-1
                next_id_count = next_id_count +1
                pq.append([self.distance(pq[0][1], pq[0][2]-1, food_loc[0], food_loc[1]), pq[0][1], pq[0][2]-1, next_id_count])
                direction = self.find_direction(pq[0][1], latest_location[0], pq[0][2]-1, latest_location[1])
                search_tree = self.insert_list(search_tree, pq[0][3], next_id_count, direction, exp_seq)
                search_tree = self.add_dict(search_tree, next_id_count, pq[0][1], pq[0][2]-1, -1, self.findRedundant(all_locations, pq[0][1], pq[0][2]-1), pq[0][3])
                all_locations.append([pq[0][1], pq[0][2]-1])
                
            # save first row of pq, in [x, y]
            prev_loc = [pq[0][1], pq[0][2]]
            # remove first row of pq
            del pq[0]
            #sort PriorityQueue from lowest to highest
            pq = sorted(pq, key=lambda x: x[0])
            #find the directions went of the solution
            all_directions.append(self.find_direction(pq[0][1], prev_loc[0], pq[0][2], prev_loc[1]))
        return all_directions, search_tree
    
    def run(self, problem):
        # problem = {
        #   snake_locations: [[int,int],[int,int],...],
        #   current_direction: str,
        #   food_locations: [[int,int],[int,int],...],
        # }
        food_loc = problem['food_locations'][0]
        snake_loc = problem['snake_locations'][0]
        search_tree = [
            {
            "id": 1,
            "state": str(snake_loc[0]) +"," + str(snake_loc[1]),
            "expansionsequence": -1,
            "children": [],
            "actions": [],
            "removed": False,
            "parent": None
            }
            ]
        solution, search_tree = self.greedy_bfs(snake_loc, food_loc, search_tree)
        return solution, search_tree
            
#test 
if __name__ == "__main__":
    p1 = Player({ "maze_size": [10,10], "static_snake_length": True })
    sol, st = p1.run({'snake_locations': [[5, 5]], 'current_direction': 'e', 'food_locations': [[7, 8]]})
    print("Solution is:", sol)
    for i in range(len(st)):
        print("Search tree " + str(i+1) + " is: ")
        print(st[i])
        print("--------------------------------------------------")