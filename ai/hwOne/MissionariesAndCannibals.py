#!/usr/bin/env python3
"""
CSC-440: Artificial Intelligence
Dr. Andrew Watkins
David Golembiowski
January 24, 2019

This file implements the missionaries and cannibals problem
using the problem class specified for the AIMA python search.py
file.

It then finds solutions to this problem using 2 different
search algorithims:
Depth First and Breadth First
"""
from search import *
from collections import deque

class MandC(Problem):
    """ This is the Missionaries and Cannibals Problem
    it's inherited from the Problem class (see search.py).
    """
    def __init__(self, initial, goal):
        #You need to decide if more info is needed in the constructor
        #if so, then add another parameter to the constructor
        
        #call ths parent class's constructor
        Problem.__init__(self,initial,goal) 
        
    def actions(self, state):
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
        
        The data structure that returns callable, legal actions
        in `results()` for a given state depends on the action 
        passed to it from search.py, where "action" is
        denoted by its name as a string.
        """
        action_list = list()

        # Send one missionary from left to right
        if all([
            state[4] == True,
            state[0] >= 1,
            state[2]+1 >= state[3],
            state[0]-1 >= state[1]]):
            action_list.append('send_one_missionary')
        
        # Send two missionaries from left to right
        if all([
            state[4] == True,
            state[0] >= 2,
            state[2] +2 >= state[3],
            state[0] -2 >= state[1] if not state[0]-2 == 0 else True]):
            action_list.append('send_two_missionaries')

        # Send one cannibal from left to right
        if all([
            state[4] == True,
            state[1] -1 <= state[0],
            state[1] >= 1,
            any([state[3]+1 <= state[2] if state[2] != 0 else True, 
                state[3] + 1 <= state[2] if not state[2] >= state[3]+1 else True])]):
            #state[3] +1 <= state[2]]):
            action_list.append('send_one_cannibal')

        # Send two cannibals from left to right
        if all([
            state[4] == True,
            state[1] >= 2,
            state[3] + 2 <= state[2] if not state[2] == 0 else True]):
            action_list.append('send_two_cannibals')

        # Send one missionary and one cannibal from left to right
        if all([
            state[4] == True,
            state[0] >= 1,
            state[1] >= 1,
            state[0] - 1 >= state[1] - 1,
            state[2] +1 >= state[3] +1]):
            action_list.append('send_one_each')

        # Return one missionary from right to left
        if all([
            state[4] == False,
            state[2] >= 1,
            state[2] -1 >= state[3] if state[2]-1 != 0 else True,
            state[0] +1 >= state[1]]):
            action_list.append('return_one_missionary')

        # Return two missionaries from right to left
        if all([
            state[4] == False,
            state[2] >= 2,
            state[0] +2 >= state[1],
            state[2] -2 >= state[3] if state[2]-2 != 0 else True]):
            action_list.append('return_two_missionaries')

        # Return one cannibal from right to left 
        if all([
            state[4] == False,
            state[3] >= 1,
            state[1] +1 <= state[0] if state[0] != 0 else True]):
            action_list.append('return_one_cannibal')

        # Return two cannibals from right to left 
        if all([
            state[4] == False,
            state[3] >= 2,
            state[1]+2 <= state[0] if state[0] != 0 else True]):
            action_list.append('return_two_cannibals')

        # Return one missionary and one cannibal from right to left
        if all([
            state[4] == False,
            state[2] >= 1,
            state[3] >= 1,
            state[2] -1 >= state[3] - 1 if state[0] != 0 else True, #maybe trivial case
            state[0] +1 >= state[1]+1]):
            action_list.append('return_one_each')

        return action_list

    def result(self, state, action):
        """
        `getattr(self, action)(state) returns the unspecified "name"  attribute
        from mc.actions() list entries, which is a placeholder for any of 
        the MandC class definitions that relate to generating a new state, such
        as `send_one_cannibal()`, which then accepts an environment state to be
        passed as its "state" parameter.

        It returns the "next" state to be accepted by the "next" assignment 
        statement in search.py
        """
        next = getattr(self, action)(state)
        return next

    def send_one_missionary(self, state):
        next = (
            state[0]-1,
            state[1],
            state[2]+1,
            state[3],
            False)
        return next

    def send_two_missionaries(self, state):
        next = (
            state[0]-2,
            state[1],
            state[2]+2,
            state[3],
            False)
        return next

    def send_one_cannibal(self, state):
        next = (
            state[0],
            state[1]-1,
            state[2],
            state[3]+1,
            False)
        return next

    def send_two_cannibals(self, state):
        next = (
            state[0],
            state[1]-2,
            state[2],
            state[3]+2,
            False)
        return next

    def send_one_each(self, state):
        next = (
            state[0]-1,
            state[1]-1,
            state[2]+1,
            state[3]+1,
            False)
        return next

    def return_one_missionary(self, state):
        next = (
            state[0]+1,
            state[1],
            state[2]-1,
            state[3],
            True)
        return next

    def return_two_missionaries(self, state):
        next = (
            state[0]+2,
            state[1],
            state[2]-2,
            state[3],
            True)
        return next

    def return_one_cannibal(self, state):
        next = (
            state[0],
            state[1]+1,
            state[2],
            state[3]-1,
            True)
        return next

    def return_two_cannibals(self, state):
        next = (
            state[0],
            state[1]+2,
            state[2],
            state[3]-2,
            True)
        return next

    def return_one_each(self, state):
        next = (
            state[0]+1,
            state[1]+1,
            state[2]-1,
            state[3]-1,
            True)
        return next

def main():
    # Initialize with 3 missionaries and 3 cannibals on the left side
    initial_state = (3,3,0,0,True)
    goal_state = (0,0,3,3,False)
    
    mc = MandC(initial=initial_state, goal=goal_state)

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
    
