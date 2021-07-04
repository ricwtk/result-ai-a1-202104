# -*- coding: utf-8 -*-
"""
Created on Mon May 10 21:54:59 2021

@author: New
"""

class Player():
    name = "Chun Hou"
    group = "bt smeli"
    members = [
        ["Bryan Tang", "18041772"],
        ["Chun Hou", "18043547"],
        ["Wei Jun", "18034223"],
        ["Weng Xi", "18043521"]
      ]

    informed = True
    #informed search using Greedy Best-First Search

    def __init__(self,setup):
        self.setup = setup
        #accesing value in items in setup dictionary 
        for key, value in setup.items():
            if key == "maze_size":
                #set the value of maze size acquired in the UI to variable maze_size
                self.maze_size = value
        
    def run(self, problem):   
        solution = []
        #accesing value in items in problem dictionary 
        for key, value in problem.items(): 
            if key =="snake_locations":
                #set the value of snake current location acquired in the UI to variable snake_locations                       
                snake_locations=value
            if key =="food_locations":
                #set the value of food 
                food_locations=value    
        
        [solution, tree] = informedSearch(snake_locations, food_locations)             
                  
        return solution,tree
    

class Node():
    def __init__(self, state=None, parent=None,directionFromParent=None, identity = None):
        self.state = state
        self.parent = parent
        self.directionFromParent = directionFromParent        
        self.identity = identity

def expandAndReturnChild(current, check, node_id):
    children = []
    up = current.state[1]-1
    down = current.state[1]+1
    left = current.state[0]-1
    right = current.state[0]+1
    
    #boolean variable check is to determine if it's checking vertically or horizontally
    if check == True: #checking vertically (y-axis)
        moveUp = Node([current.state[0],up], current.state, 'n',node_id+1)
        moveDown = Node([current.state[0],down], current.state, 's',node_id+2)
        children.append(moveUp)
        children.append(moveDown)
    elif check == False: #checking vertically (x-axis)
        moveLeft = Node([left, current.state[1]], current.state, 'w',node_id+1)
        moveRight = Node([right,current.state[1]], current.state, 'e',node_id+2)
        children.append(moveLeft)
        children.append(moveRight)
        
    number_of_nodes_added = len(children)
    #removeRedundantCoordinate(children,current)    
    return(children, number_of_nodes_added)

def checkRemoved(node,children):
    for child in children:
        if node.state == child.state:
            return True
        return False
    
def getParentId(node,explored):
    for e in explored:
        if node.parent == e.state:
            return e.identity
    return None
        
def removeRedundantCoordinate(children,current):
    for i,child in enumerate(children):
        if (child.state == current):
            del children[i]
    return children             
    
def createTree(node,children,expansionsequence,explored):
    
    Dict = {}
    
    Dict["id"] = node.identity
    Dict["state"] = node.state
    Dict["expansionsequence"] = expansionsequence
    Dict["children"] = [child.identity for child in children]
    Dict["actions"] =  [child.directionFromParent for child in children]
    Dict["removed"] = checkRemoved(node,children)
    Dict["parent"] = getParentId(node,explored)

    return Dict

    
    
def findBestFirstPath(initial,food):
    #calculate distance between initial location of snake and food    
    y_diff = abs(food.state[1] - initial.state[1])
    x_diff = abs(food.state[0] - initial.state[0])
    
   
    y_dict = ['n','s','w','e', 1,0, True, False] #dictionary if y-axis have lower cost
    x_dict = ['w','e','n','s', 0,1, False, True] #dictionary if x-axis have lower cost
    


    if (x_diff < y_diff):
        return x_dict
    else:
        return y_dict


def informedSearch(snake_locations, food_locations):
    expansionsequence=0
    node_id=1
    found_goal = False
    solution = []
    frontier = []
    explored = []
    Tree = []
    food = Node(food_locations[0], None, None,None)
    frontier.append(Node(snake_locations[0], None,None, 1))
    #returned dictionary will be used to determine which axis to be search first 
    axisDict = findBestFirstPath(frontier[0], food)
    
    while not found_goal:
        expansionsequence+=1
        if frontier[0].state != food.state:
            explored.append(frontier[0])
            #checking axis based on the axisDictionary
            #if returned dictionary is y-axis, it will search vertically first
            #with 4th index of axis dictionary == 1 for y-axis and 0 for x-axis
            if (frontier[0].state[axisDict[4]] != food.state[axisDict[4]]): 
                #6th index of axis dictionary = True for y-axis and False for x-axis
                #to sync with the expandAndReturnChild function to determine checking vertically or horizontally                
                children, counter = expandAndReturnChild(frontier[0], axisDict[6], node_id)
                #e.g. axis == y-axis
                #if snake yaxis is larger than food yaxis == snake is below food
                if (frontier[0].state[axisDict[4]]>food.state[axisDict[4]]):
                    #hence direction == 'n' shown in axis Dictionary
                    direction = axisDict[0]
                    frontier.append(children[0])
                else:
                    direction = axisDict[1]
                    frontier.append(children[1])           
            else:
                children, counter = expandAndReturnChild(frontier[0], axisDict[7], node_id)
                if (frontier[0].state[axisDict[5]]>food.state[axisDict[5]]):
                    direction = axisDict[2]
                    frontier.append(children[0])           
                else:
                    direction = axisDict[3]
                    frontier.append(children[1]) 
                    
            node_id+=counter
            Tree.append(createTree(frontier[0],children,expansionsequence,explored))
            solution.append(direction)
            del(frontier[0])

        else:
            found_goal = True
        
    return solution, Tree


if __name__ == "__main__":
    p1 = Player({"maze_size":[10,10], "static_snake_length": True})
    sol, tree= p1.run({'snake_locations': [[1, 3]], 'current_direction': 'e', 'food_locations': [[5, 9]]})
    print("Solution is: ", sol)
    print("Tree is: ", tree)
    

    
