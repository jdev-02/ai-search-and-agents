#[author]
#CS3310 Lab 3
from collections import deque
import pandas as pd
import numpy as np
from pathlib import Path
import math #for heuristics
import heapq #for informed search
#from utils import *

class Problem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError


# ______________________________________________________________________________


class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return hash(self.state)

#----------------------Informed Search and Heuristics--------------------------------------------

def manhattan_distance(state,problem):
    '''works as a heuristic (h1) for connected unit cost grids'''
    (row,col) = state
    (goal_row,goal_col) = problem.goal
    return abs(row-goal_row) + abs(col-goal_col)

def euclidean_distance(state,problem):
    (row,col) = state
    (goal_row,goal_col) = problem.goal
    return math.hypot(row-goal_row,col-goal_col)

def greedy_search(problem, h):
    '''implements greedy search using heuristic(state,problem) for node selection
    returns the solution node and the nodes generated'''
    frontier_node_l = []
    explored_nodes = set() #dont want deupes of explored nodes so use set
    start_node = Node(problem.initial)
    tie = 0 #init counter for tie
    heapq.heappush(frontier_node_l,(h(start_node.state,problem),tie,start_node)) #push on the node plus the h value
    #priority for heappush is the heuristic, then the tie
    frontier_states = {start_node.state}
    nodes_generated = 0 #init counter for nodes
    #now search algo
    while frontier_node_l: #while theres something in queue
        _,_, current_node = heapq.heappop(frontier_node_l) #current node is whatever the lowest h is
        frontier_states.discard(current_node.state) 
        if problem.goal_test(current_node.state):
            return current_node, nodes_generated #edge case for first node is goal
        explored_nodes.add(current_node.state) #poppped it off -> visited
        for child in current_node.expand(problem): #for children of current node in problem given
            nodes_generated += 1 #increment counter for print at end
            if child.state not in explored_nodes and child.state not in frontier_states: #if childs not been explored and not in queue already
                if problem.goal_test(child.state): #if the child is goal we made it!
                    return child, nodes_generated
                #otherwise not there yet gotta keep going
                tie += 1
                heapq.heappush(frontier_node_l, (h(child.state,problem), tie, child))
                #push the child on pri of heuristic, then the tie
                frontier_states.add(child.state)
    #if we went through everything
    return None, nodes_generated

def greedy_search_manhattan(problem):
    return greedy_search(problem, manhattan_distance)

def greedy_search_euclidean(problem):
    return greedy_search(problem, euclidean_distance)

def astar_search(problem, h):
    '''implements a* search using formula of f(n) = g(n) + h(n)
    where g(n) is accumulative path cost from init state to n
    and h(n) is estimated cost from n to goal state
    returns solution node and nodes generated to get there'''
    frontier_node_l = []  #priority queue (min-heap): (f, tie, Node)
    explored_nodes = set()  #dont want dupes of explored nodes so use a set
    start_node = Node(problem.initial)
    tie = 0  #init counter for tie-breaking
    #g for start = 0; f = g + h
    best_g = {start_node.state: 0}
    heapq.heappush(frontier_node_l, (best_g[start_node.state] + h(start_node.state, problem), tie, start_node))
    frontier_states = {start_node.state}  #mirrors bfs-style "in frontier"
    nodes_generated = 0  #init counter for nodes

    while frontier_node_l:  #while theres something in the queue
        _, _, current_node = heapq.heappop(frontier_node_l)  #pop lowest f
        frontier_states.discard(current_node.state)

        #if this node is not the best-known g for its state, skip bc useless
        if current_node.path_cost > best_g.get(current_node.state, float('inf')):
            continue

        if problem.goal_test(current_node.state):
            return current_node, nodes_generated  #handles if start is goal edge case

        explored_nodes.add(current_node.state)  #once we popped it off we count as visited

        for child in current_node.expand(problem):  #for children of current node
            nodes_generated += 1  #increment counter for print at end
            s = child.state
            g = child.path_cost  #g(n) carried in Node.path_cost via Problem.path_cost

            #only push if we found a better g for this state
            if g < best_g.get(s, float('inf')):
                best_g[s] = g
                tie += 1
                f = g + h(s, problem)
                heapq.heappush(frontier_node_l, (f, tie, child))  #priority by f, then tie
                frontier_states.add(s)

    #if we went through everything
    return None, nodes_generated

def astar_search_manhattan(problem):
    return astar_search(problem, manhattan_distance)

def astar_search_euclidean(problem):
    return astar_search(problem, euclidean_distance)

class MazeProblem_Lab3(Problem):
    '''this class instantiates a maze problem in line with the mymaze.xlsx boolean outlay maze
    walls are 1s and channels are 0s'''
    def __init__(self, maze_path="my_maze.xlsx",start=(15,2),goal=(1,16)):
        '''initialize initial state and goal state'''
        '''specific to this file, new file would have to check coords of start and goal unless you built in functionality for color checking and etc'''
        
        maze = pd.read_excel("my_maze.xlsx", header=None).to_numpy(dtype=int)
        
        assert maze[start] == 0 and maze[goal] == 0, "Start/goal must be channels 0" #validation assertion
        super().__init__(initial=start, goal=goal) #init base Problem object with start and goal states
        
        self.maze = maze
        self.n_rows, self.n_cols = maze.shape
        #action math
        self._delta = {
            'Up':    (-1, 0),
            'Down':  ( 1, 0),
            'Left':  ( 0,-1),
            'Right': ( 0, 1),
        }

    def actions(self, state):
        """return actions that can be executed from a given state - which is move up,down,left,right
        (so long as the intended direction's cell val is not a 1)"""
        r, c = state
        legal_moves = []
        for move, (delta_r,delta_c) in self._delta.items(): #for all of the possible directions to move row and column wise
            rr,cc = r+delta_r, c+delta_c #take where you were at and try to increment
            if 0 <= rr < self.n_rows and 0 <= cc < self.n_cols and self.maze[rr,cc] == 0: #if the resulting addition is legal in confines of the maze constraints of value of 0s being allowable places on map
                legal_moves.append(move)
        return legal_moves #list of actions allowed

    def result(self, state, action):
        """results of executing some action (built in actions method) from the given state to get to next state"""
        delta_r, delta_c = self._delta[action]
        row, col = state
        return (row+delta_r, col+delta_c)
    
    def goal_test(self, state):
        '''returns true if state is a goal from inherited class problem'''
        return super().goal_test(state)