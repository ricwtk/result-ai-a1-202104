from .bfs import BFS

class Player():
  name = "bfs"
  group = "Jimmy Neurons"
  members = [
    ["Nicholas Lee Choon Sin", "18073957"],
    ["Cheong Keng Son", "18074229"],
    ["Adrian Ching Liansheng", "18063685"],
    ["Ng Wei Jinn", "18064154"]
  ]

  informed = False

  def __init__(self, setup):
    self.setup = setup

  def run(self, problem):
    try:
      # Uninformed Search Solution - Breadth First Search
      bfs = BFS(problem['snake_locations'], problem['food_locations'], self.setup['maze_size'])
      solution, search_tree = bfs.bfs()
    except IndexError:
      # Catch Index out of Bounds problem
      # Means that the solution can't be found, and all possible coordinates are explored already
      # Take the tail as the new goal state to ensure that the snake continues moving / will potentially find a path to the food
      problem['food_locations'].append(problem['snake_locations'][-1])
      del problem['snake_locations'][-1]

      # Uninformed Search Solution - Breadth First Search
      bfs = BFS(problem['snake_locations'], problem['food_locations'], self.setup['maze_size'])
      solution, search_tree = bfs.bfs()

    return solution, search_tree


if __name__ == "__main__":
  p1 = Player({ "maze_size": [10,10], "static_snake_length": True })
  sol, st = p1.run({'snake_locations': [[0, 5]], 'current_direction': 'e', 'food_locations': [[6, 7]]})
  print("Solution is:", sol)
  print("Search tree is:")
  print(st)