import random

class Player():
	name = "uninformed search player"
	group = "Smart AI"
	members = [
	["Theysigan", "17072182"],
	["Raguram", "18068718"],
	["Puvanesh", "16029423"],
	["Muhammad Mahad Niaz","19053131"]
	]
	informed = False

	def __init__(self, setup):
		# setup = {
		#   maze_size: [int, int],
		#   static_snake_length: bool
		# }
		self.setup = setup

	def run(self, problem):
		# problem = {
		#   snake_locations: [[int,int],[int,int],...],
		#   current_direction: str,
		#   food_locations: [[int,int],[int,int],...],
		# }
		sz = self.setup["maze_size"]
		src = problem["snake_locations"][0]
		destination = problem["food_locations"][0]
		search_tree = []
		solution = []
		direction = "nsew"

		visited = [[False for i in range(sz[0])] for j in range(sz[1])]
		visited[src[0]][src[1]] = True
		currId = 1
		seq = 1
		search_tree.append({"id": currId, "state": str(src[0])+","+str(src[1]), "expansionsequence": seq, "children": [], "actions": [], "removed": False, "parent": None})

		idx = 0
		while idx < len(search_tree):
			idx += 1
			if(search_tree[idx-1]["removed"] == True):
				continue
			
			node = [int(x) for x in search_tree[idx-1]["state"].split(",")]
			parID = search_tree[idx-1]["id"]
			if(node == destination):
				parIdx = search_tree[idx-1]["parent"]-1
				while (parIdx != None):
					parNode = [int(x) for x in search_tree[parIdx]["state"].split(",")]
					if(parNode[0]-node[0] == 1):
						solution.append("w")
					elif(parNode[0]-node[0] == -1):
						solution.append("e")
					elif(parNode[1]-node[1] == 1):
						solution.append("n")
					else:
						solution.append("s")
					
					node = parNode
					parIdx = search_tree[parIdx]["parent"]
					if(parIdx != None):
						parIdx -= 1
				solution.reverse()
				break

			childs = [[node[0], node[1]-1], [node[0], node[1]+1], [node[0]+1, node[1]], [node[0]-1, node[1]]]
			for i in range(len(childs)):
				if(childs[i][0] >= 0 and childs[i][0] < sz[0] and childs[i][1] >= 0 and childs[i][1] < sz[1]):
					currId += 1
					seq += 1
					search_tree.append({"id": currId, "state": str(childs[i][0])+","+str(childs[i][1]), "expansionsequence": seq, "children": [], "actions": [], "removed": False, "parent": parID})

					search_tree[parID-1]["children"].append(currId)
					search_tree[parID-1]["actions"].append(direction[i])
					if(visited[childs[i][0]][childs[i][1]] == True):
						seq -= 1
						search_tree[currId-1]["expansionsequence"] = -1
						search_tree[currId-1]["removed"] = True
					else:
						visited[childs[i][0]][childs[i][1]] = True

		# this function should return the solution and the search_tree
		return solution, search_tree


if __name__ == "__main__":
	p1 = Player({ "maze_size": [10,10], "static_snake_length": True })
	sol, st = p1.run({'snake_locations': [[0, 5]], 'current_direction': 'e', 'food_locations': [[6, 7]]})
	print("Solution is:", sol)
	print("Search tree is:")
	print(st)