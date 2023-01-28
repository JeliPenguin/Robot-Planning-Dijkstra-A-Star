'''
Created on 2 Jan 2022

@author: ucacsjj
'''

from math import sqrt
from queue import PriorityQueue

from .planner_base import PlannerBase

class DijkstraPlanner(PlannerBase):

    # This implements Dijkstra. The priority queue is the path length
    # to the current position.
    
    def __init__(self, occupancy_grid):
        PlannerBase.__init__(self, occupancy_grid)
        self.priority_queue = PriorityQueue()

    # Q1d:
    # Modify this class to finish implementing Dijkstra
    def _euclidean_dist(self, cell1, cell2):
        (x1, y1) = cell1.coords()
        (x2, y2) = cell2.coords()
        return sqrt(pow(x1-x2, 2) + pow(y1-y2, 2))
    
    def _update_priority_queue(self, newcell):
        queue_tuples = []

        # ensure queue not empty
        while not self.priority_queue.empty():
            path_cost, cell = self.priority_queue.get() 

            # update if match
            if cell.coords() == newcell.coords():
                for tup in queue_tuples:
                    self.priority_queue.put(tup)
                    self.priority_queue.put(newcell.path_cost, newcell)

            # keep track of items taken out
            queue_tuples.append((path_cost, cell))

            # go next
            path_cost, cell = self.priority_queue.get()
    
    # This method pushes a cell onto the queue Q. Its implementation
    # depends upon the type of search algorithm used. If necessary,
    # (self) could also do things like update path costs as well.
    # This used in lines 2 and 11 of the pseudocode    
    def push_cell_onto_queue(self, cell):
        self.priority_queue.put((cell.path_cost, cell))

    # This method returns a boolean - true if the queue is empty,
    # false if it still has some cells on it. Its implementation
    # depends upon the the type of search algorithm used.
    # This is used in line 3 of the pseudocode    
    def is_queue_empty(self):
        return self.priority_queue.empty()

    # Handle the case that a cell has been visited already. This is
    # used by some algorithms to rewrite paths to identify the
    # shortest path.
    # This corresponds to line 13 of the pseudocode    
    def resolve_duplicate(self, cell, parent_cell):
        old_path_cost = cell.path_cost
        # here euclidean works since its just one cell apart
        current_path_cost = parent_cell.path_cost + self._euclidean_dist(cell, parent_cell)

        if current_path_cost < old_path_cost:
            cell.set_parent(parent_cell)
            cell.path_cost = current_path_cost
            # need to update queue
            self._update_priority_queue(cell)
        

    # This method finds the first cell (at the head of the queue),
    # removes it from the queue, and returns it. Its implementation
    # depends upon the the type of search algorithm used.
    # This corresponds to line 4 of the pseudocode    
    def pop_cell_from_queue(self):
        _, cell =  self.priority_queue.get()
        return cell
