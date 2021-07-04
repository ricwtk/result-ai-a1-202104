import numpy

class Player():
    name = "informed"
    group = "HACK O' HOLICS"
    members = [
        ["Yap Cia Ing", "19075720"],
        ["Karishma Raveendran", "18038810"],
        ["Hew Chen Yang", "19071695"],
        ["Yeow Wei Zen", "19079128"]
    ]
    informed = True

    def __init__(self, setup):
        self.setup = setup
        self.body = []
        self.g = 0
        self.h = 0
        self.f = 0

    def run(self, problem):
        snake_location = problem['snake_locations'][0]
        food_location = problem['food_locations']
        maze_size = self.setup['maze_size']
        maze = []
        for y in range(maze_size[1]):
            for x in (range(maze_size[0])):
                maze.append([x, y])

        def find_neighbors(position):
            neighbors = [[position[0], position[1] - 1],
                         [position[0], position[1] + 1],
                         [position[0] - 1, position[1]],
                         [position[0] + 1, position[1]]]
            surrounding_neighbors = []

            for neighbor in neighbors:
                if neighbor in maze:
                    surrounding_neighbors.append(neighbor)
            return surrounding_neighbors
        neighbors_dict = {tuple(snake_location): find_neighbors(snake_location) for snake_location in maze}

        def check_location(position):
            if position[0] >= maze_size[0] or position[0] < 0 or position[1] >= maze_size[1] or position[1] < 0:
                return False
            for body_part in self.body:
                if body_part.snake_location == position:
                    return False
            return True

        def aStar(self, start, end):
            self.g = 0 
            self.h = 0
            self.f = 0

            visited_node_cost = []
            node_not_visited_cost = []
            count = 0
            max_count = (len(maze) // 2) ** 10

            

            queue = [start]
            visited_node = {tuple(snake_location): False for snake_location in maze}
            visited_node[start[0], start[1]] = True
            previous_node = {tuple(snake_location): None for snake_location in maze}
            
            while queue:
                node = queue.pop(0)
                neighbors = neighbors_dict[node[0], node[1]]
                for next_node in neighbors:
                    if check_location(next_node) and not visited_node[tuple(next_node)]:
                        queue.append(tuple(next_node))
                        visited_node[tuple(next_node)] = True
                        previous_node[tuple(next_node)] = node
                        visited_node_cost.append(0)
            route = list()
            parent_node = end
            start_found = False

            distance = self.f

            while not start_found:
                if previous_node[parent_node[0][0], parent_node[0][1]] is None:
                    return []
                parent_node = previous_node[parent_node[0][0], parent_node[0][1]]
                parent_node2 = list(parent_node)
                route.insert(0, parent_node2)
                parent_node = list(parent_node)
                parent_node_ls = []
                parent_node_ls.append(parent_node)
                parent_node = parent_node_ls
                if parent_node2 == start:
                    route.insert(int(len(route)), end[0])
                    return route
            
            return route

        def move_snake(route):
            result = []
            move_direction = []

            for step in range(len(route) - 1):
                move = numpy.subtract(route[step], route[step+1])
                if [move[0], move[1]] == [0, -1]:
                    move_direction = 's'
                if [move[0], move[1]] == [0, 1]:
                    move_direction = 'n'
                if [move[0], move[1]] == [-1, 0]:
                    move_direction = 'e'
                if [move[0], move[1]] == [1, 0]:
                    move_direction = 'w'
                result.append(move_direction)
            return result

        search_tree = []
        solution = []
        result = move_snake(aStar(self, snake_location, food_location))
        for m in result:
            solution.append(m)

        return solution, search_tree


if __name__ == "__main__":
    p1 = Player({"maze_size": [10, 10], "static_snake_length": True})
    sol, st = p1.run({'snake_locations': [
                     [0, 5]], 'current_direction': 'e', 'food_locations': [[6, 7]]})
    print("Solution is:", sol)
    print("Search tree is:")
    print(st)
