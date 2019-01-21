#!/usr/bin/env python3
"""
CSC-440: Artificial Intelligence
Dr. Andrew Watkins
David Golembiowski
January 24, 2019

This file implements the missionaries and cannibals problem using
the problem class specfied for the AIMA python search.py file

It then finds solutions to this problem using 2 different search algorithms:
Depth First and Breadth First
"""

from search import *
from collections import deque
from utils import *

class MandC(Problem):
    """ This is the Missionaries and Cannibals Problem
    it's inherited from the Problem class (see search.py).
    """
    def __init__(self, initial, goal, state):
        #You need to decide if more info is needed in the constructor
        #if so, then add another parameter to the constructor
        
        #call ths parent class's constructor
        Problem.__init__(self,initial,goal) 
        
        #initialize any other information...if needed
        self.possible_actions = {}
        self.state = state

    def actions(self,state):
        # This method should return a set of legal actions from
        # the current state
        """
        Per the instructional comment above, this method indeed 
        returns an iterable of legal actions if (for each individual 
        set element) the `all()` function returns True.

        Recall self.state[4] argument above is a 
        boolean assignment whose value is True if the location
        of the boat is on the left side of the river, and 
        is False when the boat is on the right side.
        """
        action_list = {}

        # Send one missionary from left to right
        if all([
            self.state[4] == True,
            self.state[0] >= 1,
            self.state[2]+1 >= self.state[3],
            self.state[0]-1 >= self.state[1]]):
            action_list['send_one_missionary'] = tuple([
                self.state[0]-1,
                self.state[1],
                self.state[2]+1,
                self.state[3], 
                False])

        # Send two missionaries from left to right
        if all([
            self.state[4] == True,
            self.state[0] >= 2,
            self.state[2] +2 >= self.state[3],
            self.state[0]-2 >= self.state[1]]):
            action_list['send_two_missionaries'] = tuple([
                self.state[0]-2,
                self.state[1],
                self.state[2]+2,
                self.state[3],
                False])

        # Send one cannibal from left to right
        if all([
            self.state[4] == True,
            self.state[1]>=1,
            self.state[3]+1 <= self.state[2] or self.state[2] == 0]):
            ### fix this back
            action_list['send_one_cannibal'] = tuple([
                self.state[0],
                self.state[1]-1,
                self.state[2],
                self.state[3]+1,
                False]) 

        # Send two cannibals from left to right 
        if all([
            self.state[4] == True,
            self.state[1] >= 2,
            self.state[3]+2 <= self.state[2] or self.state[2] == 0]):
            action_list['send_two_cannibals'] = tuple([
                self.state[0],
                self.state[1] -2,
                self.state[2],
                self.state[3] + 2,
                False])

        # Send one missionary and one cannibal from left to right 
        if all([
            self.state[4] == True,
            self.state[2] +1 >= self.state[3] + 1, 
            self.state[0] -1 >= self.state[1] -1]):
            action_list['send_one_each'] = tuple([
                self.state[0]-1, 
                self.state[1]-1, 
                self.state[2]+1, 
                self.state[3]+1,
                False])

        # Return one missionary from right to left
        if all([
            self.state[4] == False,
            self.state[2] >= 1,
            self.state[0] +1 >= self.state[1],
            self.state[2]-1 >= self.state[3]]):
            action_list['return_one_missionary'] = tuple([
                self.state[0] + 1, 
                self.state[1],
                self.state[2] - 1,
                self.state[3],
                True])

        # Return two missionaries from right to left 
        if all([
            self.state[4] == False,
            self.state[2]>=2,
            self.state[0]+2 >= self.state[1],
            self.state[2]-2 >= self.state[3]]):
            action_list['return_two_missionaries'] = tuple([
                self.state[0] + 2,
                self.state[1],
                self.state[2] - 2,
                self.state[3],
                True])

        # Return one cannibal from right to left
        if all([
            self.state[4] == False,
            self.state[3] >= 1,
            self.state[1] +1 <= self.state[0] or self.state[0] == 0]):
            action_list['return_one_cannibal'] = tuple([
                self.state[0],
                self.state[1] + 1,
                self.state[2],
                self.state[3] - 1,
                True])

        # Return two cannibals from right to left 
        if all([
            self.state[4] == False,
            self.state[3] >= 2, 
            self.state[1] +2 <= self.state[0] or self.state[0] == 0]):
            action_list['return_two_cannibals'] = tuple([
                self.state[0],
                self.state[1]+2,
                self.state[2],
                self.state[3]-2,
                True])

        # Return one missionary and one cannibal from right to left
        if all([
            self.state[4] == False,
            self.state[2] >= 1,
            self.state[3] >= 1,
            self.state[0]+ 1 >= self.state[1] + 1,
            self.state[2] - 1 >= self.state[3]-1]):
            action_list['return_one_each'] = tuple([
                self.state[0]+1,
                self.state[1]+1,
                self.state[2]-1,
                self.state[3]-1,
                True])

        return action_list
    
    def result(self, state, action):
        # This method returns the new state after applying action to state
        print('state:',state, 'action:',action)
        return self.evaluate_newstates(action)

    # are there additional methods you'd like to define to help solve this problem?
    def evaluate_newstates(self, action):
        newstate = {
            'send_one_missionary':tuple([
                self.state[0]-1,
                self.state[1],
                self.state[2]+1,
                self.state[3], 
                False]),
            'send_two_missionaries': tuple([
                self.state[0]-2,
                self.state[1],
                self.state[2]+2,
                self.state[3],
                False]),
            'send_one_cannibal': tuple([
                self.state[0],
                self.state[1]-1,
                self.state[2],
                self.state[3]+1,
                False]),
            'send_two_cannibals': tuple([
                self.state[0],
                self.state[1]-2,
                self.state[2],
                self.state[3] +2,
                False]),
            'send_one_each': tuple([
                self.state[0]-1, 
                self.state[1]-1, 
                self.state[2]+1, 
                self.state[3]+1,
                False]),
            'return_one_missionary': tuple([
                self.state[0] + 1, 
                self.state[1],
                self.state[2] - 1,
                self.state[3],
                True]),
            'return_two_missionaries': tuple([
                self.state[0] + 2,
                self.state[1],
                self.state[2] - 2,
                self.state[3],
                True]),
            'return_one_cannibal': tuple([
                self.state[0],
                self.state[1] + 1,
                self.state[2],
                self.state[3] - 1,
                True]),
            'return_two_cannibals': tuple([
                self.state[0],
                self.state[1]+2,
                self.state[2],
                self.state[3]-2,
                True]),
            'return_one_each': tuple([
                self.state[0]+1,
                self.state[1]+1,
                self.state[2]-1,
                self.state[3]-1,
                True])}
        return newstate[action]
    
    
#Now you should test this:
    
def main():
    """
    -Define `initial_state` for mc as 
    [num_Missionaries_L = 3, num_Cannibals_L = 3,
        num_Missionaries_R = 0, num_Cannibals_R = 0,
        boat_location_Left = True] and 
    
    -Define `goal_state` for mc as
    [num_Missionaries_L = 0, num_Cannibals_L = 0,
        num_Missionaries_R = 3, num_Cannibals_R = 3,
        boat_location_Left = False]
    """
    initial_state = (3,3,0,0,True)
    goal_state = (0,0,3,3,False)
    mc = MandC(initial=initial_state, goal=goal_state, state=initial_state)
    #???some_actions = mc.actions(mc.state)

    soln = depth_first_graph_search(mc)
    print("Depth First Search")
    print("Solution Length: " + str(len(soln.path())))
    print("Nodes Traversed:")
    print(soln.path())
    print("Actions Taken:")
    print(soln.solution())
    
    soln = breadth_first_search(mc)
    print("Breadth First Search")
    print("Solution Length: " + str(len(soln.path())))
    print("Nodes Traversed:")
    print(soln.path())
    print("Actions Taken:")
    print(soln.solution())

if __name__ == "__main__":
    main()
    # Observations:
    # MandC.goal_test(mc, mc.current_state) should return True
    
