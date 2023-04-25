import math
import queue
from inversion_count import inversion_count


class Node:
    def __init__(self, current_state, goal_state, level=0, parent=None):
        # current_state: a list
        self.state = current_state
        self.goal_state = goal_state
        self.level = level
        self.parent = parent
        self.children = []
        self.heuristic_score = level
        self.heuristic_cost()
        self.empty_tile = current_state.index(str(len(self.state)))

    def __hash__(self):
        return hash(str(self.state))
    
    def get_state(self):
        return self.state

    def get_level(self):
        return self.level

    def get_parent(self):
        return self.parent

    def get_score(self):
        return self.heuristic_score

    def manhattan_distance(self, x1, y1, x2, y2):
        # I used manhattan distance to calculate the heuristic cost of current node
        return abs(x1 - x2) + abs(y1 - y2)

    def heuristic_cost(self):
        """
        This method calculates the heuristic cost for current node
        to reach the goal node plus its current level, which presents the cost
        from the initial node to the current node
        """
        for tile in self.state:
            if tile == str(len(self.state)):
                continue
            current_idx = self.state.index(tile)
            goal_idx = self.goal_state.index(tile)

            current_x, current_y = current_idx // int(math.sqrt(len(self.state))), \
                current_idx % int(math.sqrt(len(self.state)))
            goal_x, goal_y = goal_idx // int(math.sqrt(len(self.state))),\
                goal_idx % int(math.sqrt(len(self.state)))
            self.heuristic_score += self.manhattan_distance(current_x, current_y, goal_x, goal_y)

    def __lt__(self, other):
        return self.heuristic_score < other.heuristic_score

    def __eq__(self, other):
        return self.heuristic_score == other.heuristic_score

    def __gt__(self, other):
        return self.heuristic_score > other.heuristic_score

    def get_move(self, empty_xy):
        """
        This function returns a nested list of tuples which represent
        matrix positions of valid tiles that can be slided into the slot of the blank tile
        Parameters: blank_xy -- tuple, refering to matrix position of the blank tile
        eg. blank_xy = (3, 3) 
        Returns: a nested list of tuples
        eg. [(3,2), (2,3)]
        """
        
        possible_moves = []
        blank_row, blank_col = empty_xy
        length = int(math.sqrt(len(self.state))) - 1
        options = ["UP", "DOWN", "LEFT", "RIGHT"]
        # 4 possible valid moves for the blank tile
        for option in options:
            if option == "UP" and blank_row - 1 >= 0:
                # blank tile is not at the first row
                possible_moves.append((blank_row - 1, blank_col))
            elif option == "DOWN" and blank_row + 1 <= length:
                # blank tile is not at the last row
                possible_moves.append((blank_row + 1, blank_col))
            elif option == "LEFT" and blank_col - 1 >= 0:
                # blank tile is not at the first column
                possible_moves.append((blank_row, blank_col - 1))
            elif option == "RIGHT" and blank_col + 1 <= length:
                # blank tile is not at the last column
                possible_moves.append((blank_row, blank_col + 1))

        return possible_moves

    def get_children(self, parent_node):
        # find all children nodes of the parent node 
        width = int(math.sqrt(len(self.state)))
        m, n = self.empty_tile // width, self.empty_tile % width
        possible_moves = self.get_move((m, n))
        level = self.level + 1
        for each in possible_moves:
            i, j = each
            new_state = self.state.copy()
            new_state[i*width+j], new_state[m*width+n] = new_state[m*width+n], new_state[i*width+j]
            self.children.append(Node(new_state, self.goal_state, level, parent_node))
        return self.children


class Solver:
    def __init__(self, current_state, goal_state):
        self.state = current_state
        self.goal_state = goal_state
        self.path = []
        self.iter_num = 200
        self.max_iter = 2500
        self.output = ""

    def is_solvable(self):
        """
        This method check if the current puzzle solvable or not by applying inversion count algorithm

        Solvability (for n * n matrix):
        1.if n is odd, the puzzle is solvable if # of inversion is even in the initial state
        2.if n is even, puzzle is solvable if
            2.1.the blank tile (the largest number in the list represents the blank tile)
            is on an even row (starting from index 0) and # of inversions is odd
            2.2. the blank tile is on an odd row and # of inversions is even
        3.for all other cases, the puzzle is not solvable

        An inversion is any pair of tile i and j where i < j but i appears after j
        
        """
        arr = []
        
        for each in self.state:
            arr.append(int(each))
        arr.remove(len(self.state))
        # remove the largest number which represents the blank tile

        n = len(arr)
        inver_count = inversion_count(arr, 0, n - 1)
        dim = int(math.sqrt(len(self.state)))
        if dim % 2 == 1 and inver_count % 2 == 0:
            return True
        elif dim % 2 == 0:
            empty_tile = self.state.index(str(len(self.state)))
            if inver_count % 2 == 1 and empty_tile // dim % 2 == 0:
                return True
            elif inver_count % 2 == 0 and empty_tile // dim % 2 == 1:
                return True
        return False

    def a_star_search(self):
        level = 0
        
        nodes = queue.PriorityQueue()
        
        init_node = Node(self.state, self.goal_state, level)
        nodes.put(init_node)
        
        explored = set()
        search = 0
        # while nodes.qsize() and search <= self.max_iter:
        while nodes.qsize():
            search += 1
            current_node = nodes.get()
            # pop and return the current node instance based on lowest priority
            current_state = current_node.get_state()

            if str(current_state) in explored:
                continue

            if current_node.get_level() > 200:
                print("This puzzle can't be solved within 200 steps")

            explored.add(str(current_state))
            
            if current_state == self.goal_state:
                self.output = f"A* took {current_node.get_level()} steps to" \
                              f" achieve the goal state, visited {search} nodes"
                while current_node.get_parent():
                    # backtracking the path
                    self.path.append(current_node)
                    current_node = current_node.get_parent()
                
                break

            for node in current_node.get_children(current_node):
                if str(node.state) not in explored:
                    nodes.put(node)

        return self.path
