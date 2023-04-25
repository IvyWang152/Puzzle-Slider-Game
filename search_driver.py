import math
from puzzle_solver import Node, Solver

# initial_state = ["1", "8", "7", "3", "9", "5", "4", "6", "2"]

# goal_state = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


def print_matrix(lst):
    length = int(math.sqrt(len(lst)))
    for i in range(0, len(lst), length):
        print(" ".join(lst[i:i+length]))


def printing_a_star(initial_state, goal_state):
    sol = Solver(initial_state, goal_state)
    if sol.is_solvable():
        path = sol.a_star_search()
        if len(path):
            print(sol.output)

        print("This is a solvable puzzle!")
        print("Initial state")
        print_matrix(initial_state)

        print()

        step = 0
        for cur in reversed(path):
            print()
            print("  | ")
            print("  | ")
            print(" \\\'/ \n")
            step += 1
            print(f"Step: {step}")
            print_matrix(cur.get_state())
    else:
        print("This puzzle is unsolvable")


"""   
def main():
    #initial_state = ["1", "8", "7", "3", "9", "5", "4", "6", "2"]
    #initial_state = ["9", "1", "3", "4", "2", "5", "7", "8", "6"]
    #goal_state = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    initial_state = ["1", "3", "2", "4"]
    goal_state = ["1", "2", "3", "4"]
    #print_matrix(initial_state)
    printing_a_star(initial_state, goal_state)    

main()
"""
    
        
    
    
    

    

    
    
    
    
