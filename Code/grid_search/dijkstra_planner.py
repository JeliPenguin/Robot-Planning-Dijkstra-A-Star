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
        # ensure queue not empty
        new = PriorityQueue()
        while not self.priority_queue.empty():
            path_cost, cell = self.priority_queue.get()
            # update if match
            if cell.coords() == newcell.coords():
                new.put((newcell.path_cost, newcell))
            else:
                new.put((path_cost, cell))
        self.priority_queue = new

    # This method pushes a cell onto the priority queue Q,
    # according to its priority, which is its cost to come.
    # This used in lines 2 and 11 of the pseudocode
    def push_cell_onto_queue(self, cell):
        cost_to_come = cell.path_cost
        # Handles the case where the cell is the start
        if cell.parent is not None:
            cost_to_come = self._euclidean_dist(
                cell, cell.parent) + cell.parent.path_cost
            cell.path_cost = cost_to_come
        self.priority_queue.put((cost_to_come, cell))

    # This method returns a boolean - true if the queue is empty,
    # false if it still has some cells on it. When Empty and the goal still hasn't been visited,
    # then the goal could not be reached.
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
        current_path_cost = parent_cell.path_cost + \
            self._euclidean_dist(cell, parent_cell)

        if current_path_cost < old_path_cost:
            cell.set_parent(parent_cell)
            cell.path_cost = current_path_cost
            # need to update queue
            self._update_priority_queue(cell)

    # This method removes an element from the queue, and returns it.
    # In this case since it's a priority queue, it pops element with highest priority (minimum path cost)
    # This corresponds to line 4 of the pseudocode

    def pop_cell_from_queue(self):
        _, cell = self.priority_queue.get()
        return cell
