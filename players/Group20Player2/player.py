from .greedy import Greedy

class Player():
  name = "greedy"
  group = "Jimmy Neurons"
  members = [
    ["Nicholas Lee Choon Sin", "18073957"],
    ["Cheong Keng Son", "18074229"],
    ["Adrian Ching Liansheng", "18063685"],
    ["Ng Wei Jinn", "18064154"]
  ]

  informed = True

  def __init__(self, setup):
    self.setup = setup

  def run(self, problem):
    try:
      # Informed Search Solution - Greedy Best-First Search
      greedy = Greedy(problem['snake_locations'], problem['food_locations'], self.setup['maze_size'])
      solution, search_tree = greedy.greedy()
    except IndexError:
      # Catch Index out of Bounds problem
      # Means that the solution can't be found, and all possible coordinates are explored already
      # Take the tail as the new goal state to ensure that the snake continues moving / will potentially find a path to the food
      problem['food_locations'].append(problem['snake_locations'][-1])
      k_value = int(len(problem['snake_locations']) / 4)
      res = problem['snake_locations'][: len(problem['snake_locations']) - k_value]

      # Informed Search Solution - Greedy Best-First Search
      greedy = Greedy(res, problem['food_locations'], self.setup['maze_size'])
      solution, search_tree = greedy.greedy()

    return solution, search_tree


if __name__ == "__main__":
  p1 = Player({ "maze_size": [10,10], "static_snake_length": True })
  sol, st = p1.run({'snake_locations': [[0, 5]], 'current_direction': 'e', 'food_locations': [[6, 7]]})
  print("Solution is:", sol)
  print("Search tree is:")
  print(st)