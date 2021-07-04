import random
import copy 
from collections import OrderedDict
import numpy as np
import cv2

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






class BestFirstSearch:
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

  def sortFrontierList(self):
    #sort by lowest total cost -> g(x) + h(x)
    self.frontier.sort(key=lambda ft: ft.heuristicCost)

  def bfs(self, state, goalState):
    # A Breath First search
    state = copy.deepcopy(state) # Make a deep copy to prevent unaware modification to the existing state

    frontier = [Node(state=state)]
    explored = []

    foundGoal = False

    goalNode = None

    while not foundGoal:
      if len(frontier) == 0:
        break

      currentNode = copy.deepcopy(frontier.pop(0))
      
      snakePositionOfExpandingNode = currentNode.state["snake_locations"]
      currentSnakeHeadPosition = currentNode.state["snake_locations"][0]
      explored.append(currentNode)

      for currentAction, move in self.getPosibleMovesForNode(currentNode).items():
        newHeadPosition = [currentSnakeHeadPosition[0] + move[0], currentSnakeHeadPosition[1] + move[1]]

        hitWall = currentSnakeHeadPosition[0] + move[0] > self.mazeSize[0] - 1 or currentSnakeHeadPosition[0] + move[0] < 0 or currentSnakeHeadPosition[1] + move[1] > self.mazeSize[1]-1 or currentSnakeHeadPosition[1] + move[1] < 0 #Check if after action will go out of maze. **Prevent index out of bound
        bitItself = newHeadPosition in snakePositionOfExpandingNode #Check if after action will bite itself

        if not hitWall and not bitItself:
          newSnakeLocation = copy.deepcopy(currentNode.state["snake_locations"]) #copy the parent node state snake locations

          #Calculate the new snake body after the action (e,s,w,n)
          newSnakeLocation.insert(0,newHeadPosition) # insert the new head position

          if newHeadPosition not in currentNode.state["food_locations"]:
            #because if the new snake location is food, ur taill will extend by one
            newSnakeLocation.pop() # remove the last element of snake body **Note: Because a snake move forward, so it tails need to move forward also


          newStateForSnake = {
            "snake_locations": newSnakeLocation,
            "current_direction": currentAction,
            "food_locations": copy.deepcopy(currentNode.state["food_locations"]),
          }

          childNode = Node(state=newStateForSnake, actionLeadtoThisState=currentAction, parent=currentNode)
          
          if childNode.state["snake_locations"][0] not in [f.state["snake_locations"][0] for f in frontier] and childNode.state["snake_locations"][0] not in [e.state["snake_locations"][0] for e in explored]:
            # Goal test
            if newSnakeLocation[0] == goalState:
              foundGoal = True
              goalNode = childNode

            # add child to the frontiers
            frontier.append(childNode)
        
        if foundGoal:
          break
      
    if foundGoal:
      solutionToSnakeTail = []
      tmpGoalNode = copy.deepcopy(goalNode)
      while tmpGoalNode.parent is not None:
        solutionToSnakeTail.insert(0, tmpGoalNode.actionLeadtoThisState) #Retrieve the list of action to it tails (shallowest)
        tmpGoalNode = tmpGoalNode.parent # Make the goal node to parent. Cause we are tracing backwards

      numberOfStepToReachTail = len(solutionToSnakeTail) # the step is retrive by how many actions(e,s,w,n) needed to go back to snake tails
    
      return [solutionToSnakeTail, goalNode]
    else:
      return None # if not solution found, we return a very high heuristic cost to prevent this path to be chosen. **Note: this is because if there are no path going back to tail, we will die

  def calculateMinimumStepNeededFromSnakeHeadToItTails(self, state):
    # This will return the minimum number of step needed to go back to snake tail position from its head position
    # Return [seriesOfactions, finalGoalNodeObject]     ----> if a solution is found 
    #        None                                       ----> if a solution is not found
    #
    # Example of a sucess return
    # [['e','s','w'], finalGoalNode(Instance of Node class)]

    return self.bfs(state,  state["snake_locations"][-1]) # We are looking for the shallowest / minimum step, Therefore we use BreathFirstSearch
  
  def calculateMinimumStepNeededFromSnakeHeadToFood(self, state):
    # This will return the minimum number of step needed to go to the first food in foodLocation array from its head position
    # Return [seriesOfactions, finalGoalNodeObject]     ----> if a solution is found 
    #        None                                       ----> if a solution is not found
    #
    # Example of a sucess return
    # [['e','s','w'], finalGoalNode(Instance of Node class)]

    return self.bfs(state,  self.initialState["food_locations"][0]) # We are looking for the shallowest / minimum step, Therefore we use BreathFirstSearch

  def calculateHeuristicCost(self, state):
    #Section: Gather required information
    constant = (self.mazeSize[0] * self.mazeSize[1])
    isDeadState = False # Flag to indicate if this new state will lead to dead end of the game
    isNoPathAfterEatingFood = False

    snakeHeadPositionOfThisState = state["snake_locations"][0]
    foodLocation = state["food_locations"][0]

    # Section: Calculation on detached region in the snake board
    # To calculate this, we will first generate the board state in an array and use connectedComponentLabelling concept acquire from our (Digital Image Processing and Computer Vision course)
    # **NOTE: Detached region refer to empty coordinate that is seperated by the snake body in the game    
    #      
    # Example of board state in 5x5 snake game
    # 0 represent snake body
    # 1 represent a empty region in board
    #
    # [
    #   [1,1,1,0,1],
    #   [1,1,1,0,1],
    #   [0,0,0,0,1],
    #   [0,1,1,1,1],
    #   [0,0,1,1,1],
    # ]
    # 
    # As shown in the example, we could see 2 detached region(intensity value 1) which are located at top left can bottom right.
    
    
    # Generate the current board state
    boardArray = np.ones([self.mazeSize[0],self.mazeSize[1]],dtype=np.uint8)
     
    for [coorY, coorX] in state["snake_locations"]:
      if coorX < 0 or coorX >self.mazeSize[0]-1 or  coorY < 0 or coorY >self.mazeSize[1]-1:
        continue
      
      boardArray[coorX,coorY] = 0


    # After getting board state, perform connected componnet labelling
    numOfLabel,labelledArray = cv2.connectedComponents(boardArray, connectivity=4)

    numberOfDetachedRegion = numOfLabel - 1 # deduct 1 because we need to exclude the label generated by the snake body
    detachedRegionScore = numberOfDetachedRegion * constant # Lower is better. The more the number of detached region, the higher the score

    # Section: Calculation on 
    # Condition 1: If this new state has a path to go to the food ?
    # Condition 2: After eating the food with path generated in condition 1, Do we have a path to go back to our tail ?
    solutionToGoToFood = self.calculateMinimumStepNeededFromSnakeHeadToFood(state)
    longestPathToTailScore = 0 # lower means has a longer path. The longer the path to tail, the lower the score
    
    # Check if has a path to go to food
    if solutionToGoToFood is not None:
      # Has Path To foods
      solution, goalNode = solutionToGoToFood
      # Check if the snake length is more than 4
      # **Note: Snake length is less than 4, Means it is not posible to bite ourself. So, We do not need to perform a check if there is a path to our tail
      if len(state["snake_locations"]) > 4:
        solutionToGoToTailAfterEatingFood = self.bfs(goalNode.state,  goalNode.state["snake_locations"][-1])
        # Check if has a path to go to our tail after eatting the food
        if solutionToGoToTailAfterEatingFood is not None:
          sol, gnode = solutionToGoToTailAfterEatingFood
          longestPathToTailScore = constant - len(sol) # the breath first search return minimum step to the tail but we want longer step to gave lower score. So to achive this, we use a constant to substract with the minimum step.
        else:
          isNoPathAfterEatingFood = True
    else:
      # No Path To food

      
      # Check if the snake length is more than 4
      # **Note: Snake length is less than 4, Means it is not posible to bite ourself. So, We do not need to perform a check if there is a path to our tail
      if len(state["snake_locations"]) > 4:
        stepToGoBackToOurTail = self.calculateMinimumStepNeededFromSnakeHeadToItTails(state) # this will return the optimal step to go back to our tail, A Large Value if no solution is found
        # Check if this new state has a path to go to tail
        if stepToGoBackToOurTail is not None:
          solution, goalNode = stepToGoBackToOurTail

          longestPathToTailScore = constant - len(solution)
        else:
          isDeadState = True
        

    finalHeuristicCost = detachedRegionScore + longestPathToTailScore # Final heuristicc score, Less is better

    if solutionToGoToFood is None or isNoPathAfterEatingFood:
      # this new state has no path to food, we will higher the cost to avoid this path
      finalHeuristicCost = finalHeuristicCost * 2
    
    if isDeadState:
      # this new state will lead to die
      return constant * 100 # Return a very high score to block this path

    return finalHeuristicCost

  #function to expand the first node in frontier
  def expandNextNodeInFrontier(self):
    self.currentNumberOfExpansion = self.currentNumberOfExpansion + 1

    targetExpandNode = self.frontier[0] #expand the next node
    del self.frontier[0] 

    targetExpandNodeInSearchTree, tIndex = find(lambda n: n.id == targetExpandNode.id,  self.nodes)

    snakePositionOfExpandingNode = targetExpandNode.getAllSnakeBodyCoordinate() # Retrieve array of all snake coordinate
    snakeHeadPositionOfExpandingNode = targetExpandNode.getSnakeHeadCoordinate() # Retrieve coordinate of snake head

    self.nodes[targetExpandNode.id-1].expansionSequence = self.currentNumberOfExpansion # update Expansion sequence     
    
    # Perform a goal check before expanding child node
    if targetExpandNode.getSnakeHeadCoordinate() == self.initialState["food_locations"][0]:
      # Best First Search Perform Goal check before expanding the node
      self.isGoalFound = True # Notify that the goal is found
      self.goalNode = targetExpandNode # Set the goal node for finding final solution later


    # If Goal is not found, Proceed with expanding child node.

    possibleAction = self.getPosibleMovesForNode(targetExpandNode) # This will only return posible move. If our snake head is moving in direction 'e', posible actions will be 'e','s','n' only.

    # For each possible move expand the child node.
    for currentAction, move in possibleAction.items():

      newHeadPosition = [snakeHeadPositionOfExpandingNode[0] + move[0], snakeHeadPositionOfExpandingNode[1] + move[1]] # Calculate the new head position after current move

      hitWall = False # Flag to indicate if a snake will hit the wall after current move
      bitItself = False # Flag to indicate if a snake will bit itself after current move

      # Section: Check if after current action, snake will go out of maze or not ?
      if snakeHeadPositionOfExpandingNode[0] + move[0] > self.mazeSize[0] - 1 or snakeHeadPositionOfExpandingNode[0] + move[0] < 0: 
        # After current action, snake will go outside of Maze Horizontally. This implies snake will hit the wall
        hitWall = True # Set the hitWall Flag to True
      elif snakeHeadPositionOfExpandingNode[1] + move[1] > self.mazeSize[1]-1 or snakeHeadPositionOfExpandingNode[1] + move[1] < 0: 
        # After current action, snake will go outside of Maze Vertically. This implies snake will hit the wall
        hitWall = True # Set the hitWall Flag to True


      
      # Section: Check if after current action, snake will bite itself or not ? 
      if newHeadPosition in snakePositionOfExpandingNode: 
        # After current action, snake will bite it body.
        bitItself = True # Set the bitItself Flag to True
      
      
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
        # Then, this is a possible child node which can be add into the frontier



        heuristicCost = self.calculateHeuristicCost(newStateForSnake) # Calculate the heuristic cost of this new child node
        
        newChildNode.heuristicCost = heuristicCost # set the heuristic cost into the child node

        # Check if the new coordinate state has already been explored
        element, index = find(lambda n: n.getSnakeHeadCoordinate() == newChildNode.getSnakeHeadCoordinate() and n.removed is False,  self.nodes)

        isUnexploredNode = element is None 

        if isUnexploredNode:
          # The new coordinate state, is not explored yet
          # This means we could directly add into the frontier

          self.frontier.append(newChildNode)# Directly add to frontier
          self.nodes.append(newChildNode) # Directly add to explored list

          targetExpandNodeInSearchTree.childrens.append(newChildNode) # Update current expanding node with its new children in search tree         

        else:
          # The new coordinate state already in frontier
          # This means we need to keep the node with the lowest h(x) heuristic cost

          
          # Check if the new child node has a lower heuristic cost than the existing node
          if element.heuristicCost > newChildNode.heuristicCost:
            # The new child node has a lower heuristic cost, Remove the existing node and add new child node to the frontier

            e, i = find(lambda n: n.getSnakeHeadCoordinate() == newChildNode.getSnakeHeadCoordinate() and n.removed is False,  self.frontier) # Find the existing element's index in the frontier array

            existsInFrontierList = i is not None
            if existsInFrontierList:
              del self.frontier[i] # Remove old existing node in frontier array

            self.nodes[index].removed = True # Update old existing node in generated node list to removed

            self.nodes.append(newChildNode) # Add the new child node into explored list
            self.frontier.append(newChildNode) # Add the new child node into frontier array

            targetExpandNodeInSearchTree.childrens.append(newChildNode) # Update current expanding node with its new children in search tree
          else:
            # The new child node has a higher heuristic cost, remove the new child node.
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
      self.sortFrontierList()# Sort the frontier array before Expanding a node in the frontier
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
  name = "NoviceAI's Informed Search (Greedy best-first search)"
  group = "NoviceAI"
  members = [
    ["Lim Bing Xuan", "17075748"],
    ["Ow Yeong Mun Yin", "17076431"],
    ["Tan Wen Kang", "17060955"],
    ["Arun Alagusunthram a/l Venkatachalam","17035668"]
  ]
  informed = True
  

  def __init__(self, setup):
    # setup = {
    #   maze_size: [int, int],
    #   static_snake_length: bool
    # }
    self.setup = setup

  def run(self, problem):
    bestFirstSearchObj = BestFirstSearch(problem["snake_locations"], problem["current_direction"], problem["food_locations"], self.setup["maze_size"]) # pass it into our obj
    
    # this function should return the solution and the search_tree
    return bestFirstSearchObj.searchAndReturnSolution() # return solution

# **NOTE: Section For unit test only.
if __name__ == "__main__":
  p1 = Player({ "maze_size": [6,6], "static_snake_length": True })
  sol, st = p1.run({'snake_locations': [[3, 0], [4, 0], [5, 0], [5, 1], [5, 2], [4, 2], [4, 3], [5, 3], [5, 4], [5, 5], [4, 5], [4, 4], [3, 4], [3, 5], [2, 5], [1, 5], [0, 5], [0, 4], [1, 4], [2, 4], [2, 3], [3, 3]], 'current_direction': 'w', 'food_locations': [[3, 2]]})
  print("Solution is:", sol)
  print("Search tree is:")
  print(st)

