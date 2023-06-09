# Puzzle-Slider-Game

Design thoughts on Puzzle Slider Game

----Overview:----
This project creates Puzzle Slider game mainly based on turtle module. Despite how much I hate turtle, I have to say it's a valuable experience to complete a relatively "big" project on my own, where structured thinking was especially highlighted.

----Design & instructions for use:----
I mainly created two classes, class Rectangle is used in developing the layout of user interface. Class TileGame is crucial to perform expected functionalities of this game, which takes a dictionary as one of the parameters and processes all puzzle-related behaviors. The core of class TileGame is generate_puzzle method, which generates a random scrambled list, where each element represents a matching tile whose path can be accessed from the dictionary that we pass in as one of the parameters. To record the position of each tile, I defined puzzle_matrix method and board_position method, the former turned the unordered list I generated from generate_puzzle method to a nested list, and the latter records the actual coordinates of each tile as well as its matrix position. By matrix position, I mean the number of row and the number of column the tile is currently at, starting with (0, 0). I continuously called board_position method in other methods I defined in this class, such as get valid moves around the blank tile and swapping tiles and so on. board_position method returns two important dictionaries in my code, pos_info is the dictionary records current matrix positions of all tiles, and index_info records current actual coordinates of all tiles. 

The key to make the game alive is to update all information after every valid click. The processing unscrambled list is number one I need to update. So I created an attribute called self.updated to keep track of the latest puzzle list. Also, I defined a method called update to update all related attributes of the constructor - "self" after loading a new puzzle. 

----Solvability Analysis:----
puzzle_solver.py: A * algorithm is implemented to find a shortest path from the initial game state to the goal state. 

inversion_count.py: inversion count, combined with merge sort was used to check whether a puzzle is solvable or not.

I slightly modified it in my puzzle_solver.py to suit my code for the game. To be specific, the tiles'order of the current puzzle was represented as a list consisting of numbers in string types. This is because when initializing puzzle file, my initialize_file function in game_design.py returns a dictionary containing information about each tile and its path in string types. For example, key: "3" refers the third tile. In a 4 * 4 puzzle, "16" is the blank tile. Therefore, I also remove the largest number to calculate the number of inversions, as the blank tile is not taken into account in the algorithm.


Attention:

*** I imported search_driver.py and puzzle_sover.py in the game_design.py and puzzle_game.py. It's expected to answer whether the current puzzle is solvable or not in the IDLE console. If yes, it will print the path for this puzzle in a simplified version, where each number represents a tile.

*** The game runs pretty slow in IDLE on my laptop when printing a relatively long path.
If that bothers you, you can # line 131 "self.checked() in game_design.py and line 34 "instance.checked()" in puzzle_game.py. 

----Source files:----
1.puzzle_game.py (the driver for this game)
2.game_design.py (the implementation of game design, mainly includes two classes, class Rectangle, class TileGame)
3.5001_puzzle.err(this file logs possible errors when running the code)
4.leader_board.txt(this file records winners of the game)
5.Resources/malfile.gif (the program will display this gif when the puzzle the user selects has malformed data)
6.inversion_count.py (this file defines functions to calculate the number of inversions
7.puzzle_solver.py (In this file, I implemented A* algorithm to find the shortest path to solve an unordered list)
8.algo_test.py (This is a small PyUnit test to test if the given puzzle list is solvable or not)
9.search_driver.py(This is a driver.py that you can use to print the path for any list if it is solvable. It's independent of the main driver puzzle_game.py. I leave it in the folder in case you want to take a closer look at the performance of a_star_search method defined in puzzle_solver.py)
10.other starter files


----Citations----
1.inversion count 
https://www.geeksforgeeks.org/inversion-count-in-array-using-merge-sort/
2.Introduction on Heuristics and A * algorithm
The following resources also helped me a lot to finish the algorithm part
https://www.cs.princeton.edu/courses/archive/spring21/cos226/assignments/8puzzle/specification.php
https://www.redblobgames.com/pathfinding/a-star/introduction.html
https://michael.kim/blog/puzzle
