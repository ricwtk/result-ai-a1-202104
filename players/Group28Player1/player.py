import json

# * ESTIMATED COST BETWEEN SNAKE HEAD AND FOOD CAN BE CALCULATED USING THE MANHATTAN DISTANCE
# * In a plane with p1 at (x1, y1) and p2 at (x2, y2), it is |x1 - x2| + |y1 - y2|

# ! HOW DO WE CALCULATE THE MANHATTAN DISTANCE FOR MULTIPLE FOOD LOCATIONS?
# ! ONCE THE MANHATTAN DISTANCE FOR EACH FOOD IS CALCULATED, HOW DO WE CHOOSE WHICH NODE TO EXPAND?
# ! WE JUST CHOOSE THE NODE WHICH CONTAINS THAT HAS THE SMALLEST MANHATTAN DISTANCE IN ARRAY

# * PLAYER SHOULD BE AWARE OF THREE THINGS:
# * 1. SNAKE LOCATIONS. TO AVOID BUMPING INTO ITSELF.
# * 2. MAZE BOUNDARIES. TO AVOID BUMPING INTO THE WALLS.
# * 3. LOCATION(S) OF THE FOOD.

# ! WHAT KIND OF INFORMED SEARCH WE SHOULD USE?
# ? Greedy Best-First Search (Curently Selected)
# ? A* Search


def generate_new_id_from_search_tree(search_tree):
    temp_search_tree = search_tree.copy()
    temp_search_tree.sort(key=lambda item: item.get('id'), reverse=True)
    return temp_search_tree[0]['id'] + 1


def get_manhattan_distance(first, second):
    # first = [int, int]
    # second = [int, int]
    return abs(first[0] - second[0]) + abs(first[1] - second[1])


def get_estimated_cost_list(current_coords, food_coords_list):
    # start_coords = [int, int]
    # current_coords = [int, int]
    # food_coords_list = [[int,int],[int,int],...]

    estimated_cost_list = []

    for food_coords in food_coords_list:
        h_n = get_manhattan_distance(current_coords, food_coords)
        estimated_cost_list.append(h_n)

    # * Returns the estimated cost of the cheapest path to food_coords
    return estimated_cost_list


class Player():
    name = "Informed Player"
    group = "Old Driver"
    members = [
        ["Teoh Zhan Tao", "15022999"],
        ["Ang Yu Hern", "17107202"],
        ["Chong Chein Yeap", "17119876"],
        ["Eng Janson", "17102047"]
    ]
    informed = True

    def __init__(self, setup):
        # setup = {
        #   maze_size: [int, int],
        #   static_snake_length: bool
        # }
        self.setup = setup

    # * Using Greedy Best-First Search as the search algorithm
    def run(self, problem):
        # problem = {
        #   snake_locations: [[int,int],[int,int],...],
        #   current_direction: str,
        #   food_locations: [[int,int],[int,int],...],
        # }

        found_goal = False
        # ? Solution should only be finalized when we have found the steps from snake to the food
        solution = []
        directions = "nswe"

        # ? GOAL TEST FOR GREEDY BEST-FIRST SEARCH IS DONE DURING EXPANSION, NOT CREATION

        # * FOREACH object in search_tree
        # * object.removed = True if:
        # * object.state IN snake_locations
        # * Redundant = True
        # * object.state out of bounds.
        search_tree = [
            {
                "id": 1,
                "state": f"{problem['snake_locations'][0][0]},{problem['snake_locations'][0][1]}",
                "expansionsequence": -1,
                "children": [],
                "actions": [],
                "removed": False,
                "parent": None,
                "snake_locations": problem['snake_locations'],
                "estimated_costs": get_estimated_cost_list(problem['snake_locations'][0], problem['food_locations'])
            }
        ]

        while not found_goal:
            temp_search_tree = [
                element for element in search_tree if element['expansionsequence'] != -1
            ]
            temp_search_tree.sort(key=lambda item: min(item.get('estimated_costs')), reverse=True)
            latest_expansionsequence = temp_search_tree[0]['expansionsequence'] if len(
                temp_search_tree) else 0

            search_tree_without_expansionsequence_and_removed = [
                element for element in search_tree if element['expansionsequence'] == -1 and element['removed'] is False]

            if len(search_tree_without_expansionsequence_and_removed) == 0:
                # * EXIT IF SOLUTION TO FOOD CANNOT BE FOUND
                print("SOLUTION CANNOT BE FOUND!")
                # exit(0) # lecturer removed
                raise Exception("Solution cannot be found") # lecturer added

            # * Greedy Best-First Search always expands the node with the lowest estimated cost
            search_tree_without_expansionsequence_and_removed.sort(
                key=lambda item: min(item.get('estimated_costs')))

            current_element = search_tree_without_expansionsequence_and_removed[0]
            current_element_id = current_element['id']
            current_element_index = search_tree.index(
                list(filter(lambda n: n.get('id') == current_element_id, search_tree))[0])
            current_element_snake_locations = current_element['snake_locations']
            current_element_state = current_element['state']
            current_element_parent_id = current_element['parent']
            current_element_direction = problem['current_direction']
            current_element_estimated_costs = current_element['estimated_costs']

            print('LATEST EXPANSION SEQUENCE IS')
            print(latest_expansionsequence)

            print("CURRENT ELEMENT IS")
            print(current_element_id)

            # * Gets direction of current element under parent
            if current_element_parent_id is not None:
                current_element_parent = next(
                    (element for element in search_tree if element['id'] == current_element_parent_id), None)
                index_of_current_element_inside_parent = current_element_parent['children'].index(
                    current_element_id)
                direction_of_current_element_inside_parent = current_element_parent[
                    'actions'][index_of_current_element_inside_parent]
                current_element_direction = direction_of_current_element_inside_parent

            directions = ["n", "w", "s", "e"]

            # * Removes the opposite direction that the current element is travelling in
            # * Since the head of the snake is not allowed to perform a u-turn
            # * (This only applies when the length of snake == 1)
            if current_element_direction == "n":
                directions.remove("s")
            elif current_element_direction == "w":
                directions.remove("e")
            elif current_element_direction == "s":
                directions.remove("n")
            else:
                directions.remove("w")

            search_tree[current_element_index]["expansionsequence"] = latest_expansionsequence + 1

            # * Goal test (For Greedy Best-First Search, goal test is done during the expansion of the node)
            if 0 in current_element_estimated_costs:
                # * Head of snake is in one of the food locations
                found_goal = True
                active_element = current_element
                while active_element["parent"] is not None:
                    parent_element = next(
                        (element for element in search_tree if element["id"] == active_element["parent"]), None)
                    index_of_active_element_inside_parent = parent_element["children"].index(
                        active_element["id"])
                    direction_of_active_element_inside_parent = parent_element[
                        "actions"][index_of_active_element_inside_parent]
                    solution.insert(
                        0, direction_of_active_element_inside_parent)
                    active_element = parent_element

            for direction in directions:
                current_element_state_array = current_element_state.split(",")

                current_state_x = int(current_element_state_array[0])
                current_state_y = int(current_element_state_array[1])

                new_state_x = current_state_x
                new_state_y = current_state_y

                if direction == "n":
                    new_state_y = new_state_y - 1
                elif direction == "w":
                    new_state_x = new_state_x - 1
                elif direction == "s":
                    new_state_y = new_state_y + 1
                elif direction == "e":
                    new_state_x = new_state_x + 1

                new_element_snake_locations = current_element_snake_locations.copy()
                new_element_snake_locations.insert(
                    0, [new_state_x, new_state_y])
                new_element_snake_locations.pop(-1)

                new_element = {
                    "id": generate_new_id_from_search_tree(search_tree=search_tree),
                    "state": f"{new_state_x},{new_state_y}",
                    "expansionsequence": -1,
                    "children": [],
                    "actions": [],
                    "removed": False,
                    "parent": current_element_id,
                    "snake_locations": new_element_snake_locations,
                    "estimated_costs": get_estimated_cost_list([new_state_x, new_state_y], problem['food_locations'])
                }

                if [new_state_x, new_state_y] in current_element_snake_locations:
                    # * Snake collided with its own tail
                    new_element["removed"] = True
                elif new_state_x < 0 or new_state_x > self.setup["maze_size"][0] - 1 or new_state_y < 0 or new_state_y > self.setup["maze_size"][1] - 1:
                    # * Snake has bumped into the boundaries of the maze
                    new_element["removed"] = True

                search_tree[current_element_index]["children"].append(
                    new_element["id"])
                search_tree[current_element_index]["actions"].append(direction)
                search_tree.append(new_element)

        return solution, search_tree


if __name__ == "__main__":
    p1 = Player({"maze_size": [10, 10], "static_snake_length": True})
    sol, st = p1.run({'snake_locations': [
                     [0, 5]], 'current_direction': 'e', 'food_locations': [[6, 7]]})
    print("Solution is:", sol)
    print("Search tree is:")
    # print(st)
    print(json.dumps(st))
