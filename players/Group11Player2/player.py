import random
import copy 
from collections import OrderedDict

def find(pred, iterable):
    for index, element in enumerate(iterable, start=0):
        if pred(element):
            return element, index
    return None, None

class Node:
  def __init__(self, id=1, actionLeadtoThisState=None, state=None, parent=None, expansionSequence=-1, heuristicCost=0, removed=False):
    self.id = id 
    self.actionLeadtoThisState = actionLeadtoThisState
    self.state = state
    self.parent = parent
    self.childrens = []
    self.expansionSequence = expansionSequence
    self.heuristicCost = heuristicCost
    self.removed = removed

  def getSnakeHeadCoordinate(self):
    return self.state["snake_locations"][0] or None
  
  def getAllSnakeBodyCoordinate(self):
    return self.state["snake_locations"]

  def getNodeDisplayableInfo(self):
    #   This Function will format the node object to the required format by the frontend
    #
    #   {
    #     "id": 2,
    #     "state": "5,0",
    #     "expansionsequence": 2,
    #     "children": [5,6,7],
    #     "actions": ["n","s","w"],
    #     "removed": False,
    #     "parent": 1
    #   }

    nodeInfo = {
      "id": self.id,
      "state": ','.join([str(coor) for coor in self.getSnakeHeadCoordinate()]),
      "expansionsequence": self.expansionSequence,
      "children": [],
      "actions": [],
      "removed": self.removed,
      "parent": getattr(self.parent, 'id', None)
    }

    # Generate children information
    for child in self.childrens:
      nodeInfo["children"].append(child.id)
      nodeInfo["actions"].append(child.actionLeadtoThisState)
    
    return nodeInfo






class BreathFirstSearch:
  def __init__(self, snake_location, current_direction, food_locations, mazeSize, nodes=[]):
    self.initialState = {
      "snake_locations": snake_location,
      "current_direction": current_direction,
      "food_locations": food_locations,
    }
    self.nodes = [
      Node(id=1, state=self.initialState)
    ]
    self.frontier = [self.nodes[0]]
    self.currentNumberOfExpansion = 0
    self.mazeSize = mazeSize
    self.isGoalFound = False
    self.goalNode = None

  def getPosibleMovesForNode(self,node):
    currentHeadDirection = node.state["current_direction"]
    actions = OrderedDict([
      ('e', [1, 0]),
      ('s', [0, 1]),
      ('w', [-1, 0]),        
      ('n', [0, -1])
    ])

    #Remove in posible action
    if currentHeadDirection == 'e':
      del actions['w']
    elif currentHeadDirection == 's':
      del actions['n']
    elif currentHeadDirection == 'w':
      del actions['e']
    elif currentHeadDirection == 'n':
      del actions['s']    
    
    return actions

  #function to expand the first node in frontier
  def expandNextNodeInFrontier(self):
    self.currentNumberOfExpansion = self.currentNumberOfExpansion + 1
    
    targetExpandNode = self.frontier[0] #expand the next node
    del self.frontier[0] 

    targetExpandNodeInSearchTree, tIndex = find(lambda n: n.id == targetExpandNode.id,  self.nodes)

    snakePositionOfExpandingNode = targetExpandNode.getAllSnakeBodyCoordinate() # Retrieve array of all snake coordinate
    snakeHeadPositionOfExpandingNode = targetExpandNode.getSnakeHeadCoordinate() # Retrieve coordinate of snake head

    self.nodes[targetExpandNode.id-1].expansionSequence = self.currentNumberOfExpansion # update Expansion sequence     
    

    possibleAction = self.getPosibleMovesForNode(targetExpandNode) # This will only return posible move. If our snake head is moving in direction 'e', posible actions will be 'e','s','n' only.

    # For each posible move expand the child node.
    for currentAction, move in possibleAction.items():

      newHeadPosition = [snakeHeadPositionOfExpandingNode[0] + move[0], snakeHeadPositionOfExpandingNode[1] + move[1]] # Calculate the new head position after current move

      hitWall = False # Flag to indicate if a snake will hit the wall after current move
      bitItself = False # Flag to indicate if a snake will bit itself after current move

      # Section: Check if after current action, snake will go out of maze or not ?
      if snakeHeadPositionOfExpandingNode[0] + move[0] > self.mazeSize[0] - 1 or snakeHeadPositionOfExpandingNode[0] + move[0] < 0: 
        # After current action, snake will go outside of Maze Horizontally. This implies snake will hit the wall
        hitWall = True # Set the isHittedWall Flag to True
      elif snakeHeadPositionOfExpandingNode[1] + move[1] > self.mazeSize[1]-1 or snakeHeadPositionOfExpandingNode[1] + move[1] < 0: 
        # After current action, snake will go outside of Maze Vertically. This implies snake will hit the wall
        hitWall = True # Set the isHittedWall Flag to True


      
      # Section: Check if after current action, snake will bite itself or not ? 
      if newHeadPosition in snakePositionOfExpandingNode: 
        # After current action, snake will bite it body.
        bitItself = True # Set the isBittedItself Flag to True
      
      
      # Generate a new child node

      newNodeId = len(self.nodes) + 1 # Generate new node id

      deepCopyOfParentNode = copy.deepcopy(targetExpandNode) # Copy the parent node state snake locations **Note: Deepcopy because, we dont want modification to affect the parent node.

      #Calculate new snake body coordinates
      newSnakeLocation = deepCopyOfParentNode.state["snake_locations"]

      # Calculate the new snake body after the current action (e,s,w,n)
      newSnakeLocation.insert(0,newHeadPosition) # Insert the new head position

      # **Note: We only move the tail forward if a snake does not eat the food because if the after eating the food will tail will extend by 1
      # Check if the new head position touches a food 
      if newHeadPosition not in self.initialState["food_locations"]:
        # new head position is not a food
        newSnakeLocation.pop() # remove the last element of snake body **Note: Because a snake move forward, so it tails need to move forward also

      newStateForSnake = {
        "snake_locations": newSnakeLocation,
        "current_direction": currentAction,
        "food_locations": targetExpandNode.state["food_locations"],
      }

      newChildNode = Node(id=newNodeId, actionLeadtoThisState=currentAction, state=newStateForSnake, parent=targetExpandNode)

      if not hitWall and not bitItself:
        # If The snake will not hit the wall and will not bite itself after this current action
        # Then, this is a posible child node which can be add into the frontier

        # Check if the new state has already been explored
        if newChildNode.getSnakeHeadCoordinate() not in [f.getSnakeHeadCoordinate() for f in self.frontier] and newChildNode.getSnakeHeadCoordinate() not in [explored.getSnakeHeadCoordinate() for explored in [e for e in self.nodes if e.removed is False]]:
            # Goal test
            if newChildNode.getSnakeHeadCoordinate() == self.initialState["food_locations"][0]:
              self.isGoalFound = True # Notify that the goal is found
              self.goalNode = newChildNode # Set the goal node for finding final solution later

            # add child to the frontiers
            self.frontier.append(newChildNode)
            self.nodes.append(newChildNode) # Directly add to explored list

            targetExpandNodeInSearchTree.childrens.append(newChildNode) # Update current expanding node with its new children in search tree
        else:
          # The new child node is already explored
          # We still record it in search tree.

          newChildNode.removed = True # Update new child node to removed
          self.nodes.append(newChildNode) # add the new child node to explored list

          targetExpandNodeInSearchTree.childrens.append(newChildNode) # Update current expanding node with its new children in search tree

              
      else:
        # If The snake will hit the wall or will bite itself after current action
        # then this is a removed Node, Record in Tree
        
        newChildNode.removed = True # set the removed to True  
        self.nodes.append(newChildNode) # We still added as generate node for removed child node

        targetExpandNodeInSearchTree.childrens.append(newChildNode)# Update current expanding node with its new children in search tree
        
  def getSearchTree(self):
    searchTree = []
    for node in self.nodes:
      searchTree.append(node.getNodeDisplayableInfo())
    
    return searchTree

  def searchAndReturnSolution(self):
    # Continue loop while the goal is not found and there are still node in the frontier
    while not self.isGoalFound and len(self.frontier) != 0:
      self.expandNextNodeInFrontier()# Expand the first node in frontier
    
    
    #Check if goal is found
    if self.isGoalFound:
      # Goal is found

      
      tempGoalNode = self.goalNode # set the goal node as temparory
      solution = []

      # Perform a traceback from the goal node to find the solution
      while tempGoalNode.parent:
        solution.insert(0, tempGoalNode.actionLeadtoThisState) # Add to solution
        tempGoalNode = tempGoalNode.parent # Make the goal node to parent. Cause we are tracing backwards

      
      return solution, self.getSearchTree()
    else:
      # Goal is not found
      # This means there is not solution to the food in the game

      # **Note: To avoid the algorithm to stuck the game. We decide to sucide by sending a hardcoded series of action and search tree
      solution = ['e','e','e','e','e']
      searchTree = [
      {
        "id": 1,
        "state": "0,0",
        "expansionsequence": 1,
        "children": [2,3,4],
        "actions": ["n","w","e"],
        "removed": False,
        "parent": None
      },
      {
        "id": 2,
        "state": "5,0",
        "expansionsequence": 2,
        "children": [5,6,7],
        "actions": ["n","s","w"],
        "removed": False,
        "parent": 1
      },
      {
        "id": 3,
        "state": "0,3",
        "expansionsequence": -1,
        "children": [],
        "actions": [],
        "removed": False,
        "parent": 1
      },
      ]

      return solution, searchTree

    
class Player():
  name = "NoviceAI's Uninformed Search (BFS)"
  group = "NoviceAI"
  members = [
    ["Lim Bing Xuan", "17075748"],
    ["Ow Yeong Mun Yin", "17076431"],
    ["Tan Wen Kang", "17060955"],
    ["Arun Alagusunthram a/l Venkatachalam","17035668"]
  ]
  informed = False
  

  def __init__(self, setup):
    # setup = {
    #   maze_size: [int, int],
    #   static_snake_length: bool
    # }
    self.setup = setup

  def run(self, problem):
    breathFirstSearchObj = BreathFirstSearch(problem["snake_locations"], problem["current_direction"], problem["food_locations"], self.setup["maze_size"]) # pass it into our obj
    
    # this function should return the solution and the search_tree
    return breathFirstSearchObj.searchAndReturnSolution() # return solution

# **NOTE: Section For unit test only.
if __name__ == "__main__":
  p1 = Player({ "maze_size": [6,6], "static_snake_length": True })
  sol, st = p1.run({'snake_locations': [[3, 0], [4, 0], [5, 0], [5, 1], [5, 2], [4, 2], [4, 3], [5, 3], [5, 4], [5, 5], [4, 5], [4, 4], [3, 4], [3, 5], [2, 5], [1, 5], [0, 5], [0, 4], [1, 4], [2, 4], [2, 3], [3, 3]], 'current_direction': 'w', 'food_locations': [[3, 2]]})
  print("Solution is:", sol)
  print("Search tree is:")
  print(st)

