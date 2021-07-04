# - INFORMED AGENT
# - Used Best First Search

import heapq as heap 


# NODE class
# for using inside the MIN-HEAP
class Node:
	def __init__(self, head, dir, info, distance):
		self.head = head
		self.dir = dir
		self.info = info
		self.distance = distance

	# - class comparator
	# - smaller distance will come earlier
	def __lt__(self, nxt):
		return self.distance < nxt.distance

class Player():

	name = "Player2_INFORMED_AGENT"
	# informed = False # lecturer commented
	informed = True # lecturer added
	group = "MILO"
	members = [
        ["TEOH SHI HONG","19072735"],
        ["LAU WEI XUAN","19081199"],
        ["SENG WEN LONG","20076105"],
        ["RUSHIL BHATT","18043299"],
        ]
	def __init__(self, setup):
		self.setup = setup
		self.N = setup['maze_size'][0]
		self.M = setup['maze_size'][1]
		self.maze = [ [ 0 for j in range(self.M) ] for i in range(self.N) ]


	# - it updates the maze and 
	# - marks the current location of Snake's Body and Food
	def updateMaze(self, snake_locations, food):
		self.maze = [[ 0 for j in range(self.M) ] for i in range(self.M)]
		self.maze[food[1]][food[0]] = 'F'
		for s in snake_locations:
			self.maze[s[1]][s[0]] = 'S'

	# - It moves the Snake after getting the desired path
	def moveSnake(self, snake_locations, path):
        # w = left , e = right, s = down, n = up
		# - Snake's head is moved and new head is generated and the tail is chopped off
		# - Its similar to a Queue (First in Last out) - Add at front and remove from last
		for p in path:
			hx,hy = snake_locations[0][1], snake_locations[0][0]
			if p=='s':
				nx, ny = hx+1, hy

				# chop the tail
				snake_locations.pop(-1)

				# insert the new head
				snake_locations.insert(0,[ny,nx])

			elif p=='n':
				nx, ny = hx-1, hy
				snake_locations.pop(-1)
				snake_locations.insert(0,[ny,nx])
			elif p=='e':
				nx, ny = hx, hy+1
				snake_locations.pop(-1)
				snake_locations.insert(0,[ny,nx])
			elif p=='w':
				nx, ny = hx, hy-1
				snake_locations.pop(-1)
				snake_locations.insert(0,[ny,nx])
		return snake_locations


	# - Best First Search Algo
	# - Heuristic Used - Min Remaining Manhattan Distance From Food
	def bestFirstSearch(self, snake, curDir, f):
		# w, e, s, n
		dirs = [ [0,-1,'w'], [0,1,'e'], [1,0,'s'], [-1,0,'n'] ]
		id = 1
		searchTree = []
		exp = 1 
		finalPath = []
		for food in f:
			# update the maze
			self.updateMaze(snake, food)
			# create the visited array
			vis = [[ self.maze[i][j] for j in range(self.M) ] for i in range(self.N)]
			vis[ snake[0][1] ][ snake[0][0] ] = 3
		
			# generate node to be used for the search Tree
			newNode = {
						"id":id, 
						"state":""+str(snake[0][1])+","+str(snake[0][0]), 
						"expansionSequence":1, 
						"children":[], 
						"actions":[], 
						"removed":False, 
						"parent":None,
						"path":""
					}
			searchTree.append(newNode)
		
			id += 1
			# print(snake[0], food)

			# calulate the Manhattan Distance from the food.
			distance = abs(snake[0][0]-food[0]) +abs(snake[0][1]-food[1])
			q = [ Node(snake[0],curDir, newNode, distance) ]
			heap.heapify(q)

			# start the BFS by enqueing in the Q
			# in this case the Q will be Min-Heap (since we always process the node which is nearest to the food)
			curPath = []
			while len(q):
				f = heap.heappop(q)
				vis[ f.head[1] ][ f.head[0] ] = 3
				# if snake reached the food
				# store the the path and start for the next food
				if self.maze[f.head[1]][f.head[0]] == 'F':
					finalPath += f.info['path']
					curPath = f.info['path']
					break

				# explore the 4 directions
				for d in dirs:
					nx, ny = f.head[1] + d[0], f.head[0] + d[1]

					# if its a valid cell.
					# not visited or it contains a food
					if 0 <= nx < self.N and 0 <= ny < self.M and (vis[nx][ny] == 0 or vis[nx][ny]=='F'):
						f.info['actions'].append(d[2])
						exp += 1
						f.info['children'].append(id)
						newNode = {
								"id":id, 
								"state":""+str(ny)+","+str(nx), 
								"expansionSequence": exp, 
								"children":[], 
								"actions":[], 
								"removed":False, 
								"parent":f.info['id'],
								"path":f.info['path'] + d[2]
							}
						id += 1
						vis[nx][ny] = 3
						searchTree.append(newNode)
						newPoint = [ny,nx]

						# calulate the Manhattan Distance and push it to the Q (Min-Heap)
						distance = abs(newPoint[0]-food[0]) +abs(newPoint[1]-food[1])
						heap.heappush(q, Node( newPoint, d[2], newNode, distance))

			# now we have generated the path from snake's head to the food
			# now move the snake over that path
			snake = self.moveSnake(snake, curPath)

		return finalPath, searchTree
		

	def run(self, problem):
		self.problem = problem
		snake_locations = problem['snake_locations']
		curDir = problem['current_direction']
		solution = []
		path, searchTree = self.bestFirstSearch(snake_locations, curDir, problem['food_locations'])
		
		solution += path
		return solution, searchTree


if __name__ == "__main__":
	p1 = Player( { "maze_size": [10,10], "static_snake_length": True } )
	p1.run( {'snake_locations': [[0,5]], 'current_direction': 'e', 'food_locations': [[6,7]]} )
