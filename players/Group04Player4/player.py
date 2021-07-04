# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 10:52:47 2021

@author: HP
"""

class Node:
  def __init__(self, iD=None,state=None,expansionSequence=None,children=None, parent=None,actions=None,removed=False):
    self.state = state
    self.parent = parent
    self.children = []
    self.iD = iD
    self.expansionSequence = expansionSequence
    self.actions = actions
    self.removed = removed
        
class Player():
    name = "Challenge 2 Uninformed"
    group = "Pleb Bois"
    members = [
      ["Chang Jin Hung", "18034033"],
      ["Yap Tzec Tom", "18031161"],
      ["Marcus Ho Kai Shuen", "18022293"],
      ["Ho Hui Sien","15071459"]
    ]
    informed = False
    
    frontier=[]
    explored=[]
    exploredWChildren=[]
    goal_child=[]
    regenerate=True
    solutionList=[]
    oldSnackPos=[10000,10000]
    newSnackPos=[]
    searchTreeList=[]
    IDnum=1
    ExpSeq=0



    def __init__(self, setup):
        self.size=setup["maze_size"]
        self.setup = setup
    
    def run(self, problem):
        self.newSnackPos=problem["food_locations"][0]
        # check if path needs to be regenerated when snack is obtained (all solutions taken)
        if self.newSnackPos!=self.oldSnackPos:
        # if self.runs==self.runLength:
        #     self.runs=0
            self.oldSnackPos=self.newSnackPos
            self.regenerate=True
            self.frontier=[]
            self.explored=[]
            self.exploredWChildren=[]
            self.goal_child=[]
            self.solutionList=[]
            self.IDnum=1
            self.ExpSeq=0
            self.searchTreeList=[]


        if self.regenerate==True:
            self.regenerate=False
            # format of starting_point: [0,5,'null']
            starting_point=problem["snake_locations"][0]
            
            
            self.frontier.append(Node(self.IDnum,starting_point,None,None,None,None,False))

            # format of goal: [6,7]
            goal=problem["food_locations"][0]
            # When a solution hasnt been found, keep performing breadth first search
            found=False
            while found!=True:
                # frontier:[[col,row]]
                children = []
                dirList=[]
                childIDList=[]
                maze_size=self.size
                row=self.frontier[0].state[1]
                coll=self.frontier[0].state[0]
                
                if coll!=0:
                    self.IDnum=self.IDnum+1
                    # w
                    dirList.append('w')
                    childIDList.append(self.IDnum)
                    children.append(Node(self.IDnum,[coll-1,row],-1,None,self.frontier[0],None,False))
                if coll!=maze_size[1]-1:
                    self.IDnum=self.IDnum+1
                    # e
                    dirList.append('e')
                    childIDList.append(self.IDnum)
                    children.append(Node(self.IDnum,[coll+1,row],-1,None,self.frontier[0],None,False))
                if row!=0:
                    # n
                    self.IDnum=self.IDnum+1
                    dirList.append('n')
                    childIDList.append(self.IDnum)
                    children.append(Node(self.IDnum,[coll,row-1],-1,None,self.frontier[0],None,False))
                if row!=maze_size[0]-1:
                    # s
                    self.IDnum=self.IDnum+1
                    dirList.append('s')
                    childIDList.append(self.IDnum)
                    children.append(Node(self.IDnum,[coll,row+1],-1,None,self.frontier[0],None,False))
                self.frontier[0].actions=dirList
                self.frontier[0].children=childIDList
                self.ExpSeq=self.ExpSeq+1
                self.frontier[0].expansionSequence=self.ExpSeq
                
                self.explored.append(self.frontier[0])
                self.exploredWChildren.append(self.frontier[0])
                del self.frontier[0]
                for child in children:
                    
                    if (child.state in [front.state for front in self.frontier]) or (child.state in [expl.state for expl in self.explored]) or (child.state in [snake[0:2] for snake in problem["snake_locations"]]):
                        child.removed=True
                    self.exploredWChildren.append(child)
                    if not(child.state in [front.state for front in self.frontier]) and not (child.state in [expl.state for expl in self.explored]) and not (child.state in [snake[0:2] for snake in problem["snake_locations"]]):
                        if child.state==goal:
                            self.goal_child=child
                            children=[]
                            found=True
                        else:
                            self.frontier.append(child)
                            
            stop=False
            while stop!=True:
                
                x1=self.goal_child.state[0]
                y1=self.goal_child.state[1]
                x2=self.goal_child.parent.state[0]
                y2=self.goal_child.parent.state[1]
                if x1-x2==-1:
                    self.solutionList.insert(0,'w')
                if x1-x2==1:
                    self.solutionList.insert(0,'e')
                if y1-y2==-1:
                    self.solutionList.insert(0,'n')
                if y1-y2==1:
                    self.solutionList.insert(0,'s')
                self.goal_child=self.goal_child.parent
                
                if self.goal_child.parent==None:
                    stop=True
                    break
            # search tree here
            self.searchTreeList=[]
            for expl in range(len(self.exploredWChildren)):
                if self.exploredWChildren[expl].parent==None:
                     self.searchTreeList.insert(len(self.searchTreeList),
                    {"id":self.exploredWChildren[expl].iD,
                     "state":self.exploredWChildren[expl].state,
                     "expansionsequence":self.exploredWChildren[expl].expansionSequence,
                     "children": self.exploredWChildren[expl].children,
                     "actions":self.exploredWChildren[expl].actions ,
                     "removed": self.exploredWChildren[expl].removed,
                     "parent":None
                        })
                else:
                    self.searchTreeList.insert(len(self.searchTreeList),
                                       {"id":self.exploredWChildren[expl].iD,
                                        "state":self.exploredWChildren[expl].state,
                                        "expansionsequence":self.exploredWChildren[expl].expansionSequence,
                                        "children": self.exploredWChildren[expl].children,
                                        "actions":self.exploredWChildren[expl].actions ,
                                        "removed": self.exploredWChildren[expl].removed,
                                        "parent":self.exploredWChildren[expl].parent.iD
                                           })
            
        solution=self.solutionList
        search_tree=self.searchTreeList
        
        
        
        

        
          # this function should return the solution and the search_tree
        return solution, search_tree
    
if __name__ == "__main__":
  p1 = Player({ "maze_size": [10,10], "static_snake_length": True })
  sol, st = p1.run({'snake_locations': [[0, 5]], 'current_direction': 'e', 'food_locations': [[6, 7]]})
  
  print("Solution is:", sol)
  print("Search tree is:")
  print(st)
