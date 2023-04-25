import turtle
import random
import math
import time
import os
from search_driver import *


def initialize_file(filename: str):
    # this functions reads information from the file
    # returns a dictionary
    try:
        with open(filename, "r") as infile:
            puzzle_info = {}
            for lines in infile:
                lines = lines.strip("\n").split(": ")
                puzzle_info[lines[0]] = lines[1]

            return puzzle_info
    except TypeError:
        with open("5001_puzzle.err", "a") as infile:
            infile.write(f"{time.ctime(time.time())}: Error: filename should be string type"
                         f"LOCATION: initialize_file()\n")


###########################
# Part 1: Class Rectangle #
###########################

"""
Class Rectangle is used to develop layout of the game interface
"""


class Rectangle:

    def __init__(self, width, length, pencolor="black", fillcolor="white", pensize=5):
        self.width = width
        self.length = length
        self.pencolor = pencolor
        self.fillcolor = fillcolor
        self.pensize = pensize

    def draw(self, coordinate_x, coordinate_y):
        turtle.fillcolor(self.fillcolor)
        turtle.pencolor(self.pencolor)
        turtle.pensize(self.pensize)
        turtle.hideturtle()
        turtle.speed(0)
        turtle.penup()
        turtle.goto(coordinate_x - self.width / 2, coordinate_y + self.length / 2)
        turtle.pendown()
        turtle.begin_fill()
        for i in range(2):
            turtle.forward(self.width)
            turtle.right(90)
            turtle.forward(self.length)
            turtle.right(90)
        turtle.end_fill()


##########################
# Part 2: Class TileGame #
##########################

"""
Class TileGame is designed to achieve various functionalities of the puzzle game
"""


class TileGame:

    def __init__(self, puzzle_info, user, times):
        """
        Constructs all the necessary attributes for TileGame object

        Parameters
        ----------
            puzzle_info: dictionary
                a dictionary that contains all information extracted from relevant puzzle file
            user: str
            times: int
                the maximum number of moves to play the puzzle
        """
        self.puzzle_info = puzzle_info
        self.name = self.puzzle_info["name"]
        self.size = int(puzzle_info["size"])
        self.num = puzzle_info["number"]
        self.dim = int(math.sqrt(int(self.num)))
        self.goal = self.get_goal()
        self.puzzle = self.generate_puzzle()
        self.updated = self.puzzle  # type: list
        self.back_times = times  # back up the original value of times the user input
        self.times = times
        self.user = user
        self.counting = 0

    def get_goal(self):
        """
        This function returns the goal for the puzzle,
        which is a list consisting of strings, in a sorted way
        eg. ["1","2","3","4","5","6","7","8","9"]
        """
        goal = []
        for key in self.puzzle_info:
            goal.append(key)
        goal = goal[4:]
        return goal

    def update_self(self, new_puzzle_info):
        new_instance = TileGame(new_puzzle_info, self.user, self.back_times)

        self.puzzle_info = new_instance.puzzle_info.copy()
        self.name = new_instance.puzzle_info["name"]
        self.size = int(new_instance.puzzle_info["size"])
        self.num = new_instance.puzzle_info["number"]
        self.dim = int(math.sqrt(int(self.num)))

        self.goal = self.get_goal()
        self.puzzle = self.generate_puzzle()
        self.times = self.back_times
        self.counting = 0
        self.updated = self.puzzle
        self.load_puzzle()
        self.load_sample()
        self.show_moves()
        self.checked()

    ################################
    # Additional: Check Solvability#
    ################################

    def checked(self):
        # check if current puzzle solvable or not
        init_state = self.puzzle
        print(f"init: {init_state}")
        goal_state = self.get_goal()
        print(f"goal: {goal_state}")
        Solver(self.puzzle, self.get_goal)
        printing_a_star(init_state, goal_state)

    #########################
    # 2.1: Playboard basics #
    #########################

    def generate_puzzle(self):
        """
        This function generates a scrambled list, where each element
        represents the number of a tile in the puzzle
        """
        puzzle = []
        goal = [each for each in self.goal]  # deep copy
        while len(goal) > 0:
            selected = random.choice(goal)
            puzzle.append(selected)
            goal.remove(selected)
        return puzzle

    def puzzle_matrix(self):
        """
        This function returns a nested list according to the total number of tiles
        eg. [["1","2","3","4"],["5","6","7","8"],["9","10","11","12"],["13","14","15","16"]]
        """
        pos_matrix = []
        puzzle_lst = self.updated
        # self.updated(list) represents the current tile order
        for each in range(self.dim):
            pos_matrix.append(puzzle_lst[0:self.dim])
            puzzle_lst = puzzle_lst[self.dim:]
        return pos_matrix

    def board_position(self):
        """
        This function returns two dictionaries,
            one records all tiles' coordinates
            eg. pos_info = {"1": x1, y1, "2": x2, y2, "3": ....}
            the other records tiles' matrix position,
            eg. index_info = {"1":(0,0),"2":(0,1),...}
        Returns:
            pos_info: dict
            index_info: dict
        """
        pos_matrix = self.puzzle_matrix()
        # nested list of the current tile order
        pos_info = {}
        index_info = {}
        x, y = self.size / 2 - 325, 280 - self.size / 2
        for row in range(len(pos_matrix)):
            for column in range(len(pos_matrix[row])):
                pos_info[pos_matrix[row][column]] = x + (self.size + 2) * column, y - (self.size + 2) * row
                index_info[pos_matrix[row][column]] = row, column

        return pos_info, index_info

    def load_puzzle(self):
        """
        This function loads tile gifs on the user interface
        based on the current tile order
        """
        try:
            s = turtle.Screen()
            pos_info, index_info = self.board_position()
            whiteboard = Rectangle(440, 480, pencolor="white")
            whiteboard.draw(-125, 70)
            for each in pos_info:
                x, y = pos_info[each]
                Rectangle(self.size + 1.5, self.size + 1.5, pensize=2).draw(x, y)
                s.addshape(self.puzzle_info[each])
                s.tracer(1)
                turtle.hideturtle()
                turtle.speed(0)
                turtle.penup()
                turtle.goto(pos_info[each])
                turtle.pendown()
                turtle.shape(self.puzzle_info[each])
                turtle.stamp()
        except:
            with open("5001_puzzle.err", "a") as infile:
                infile.write(f"{time.ctime(time.time())}: Error: could not open {self.puzzle_info[each]} "
                             f"LOCATION: load_puzzle()\n")
            self.load_msg("Resources/malfile.gif")

    #################################
    # 2.2: Tile Swaping & Recording #
    #################################

    def blankposition(self):
        """
        Returns the matrix position of the blank tile
        eg. in ordered version for 16 tiles, the blank position is (3, 3)
        index starting from 0
        """
        target = self.puzzle_info["number"]
        pos_info, index_info = self.board_position()
        blank_xy = index_info[target]
        return blank_xy

    def get_move(self, blank_xy):
        """
        This function returns a nested list of tuples which represent
        matrix positions of valid tiles that can be slided into the slot of the blank tile
        Parameters: blank_xy -- tuple, refering to matrix position of the blank tile
        eg. blank_xy = (3, 3) 
        Returns: a nested list of tuples
        eg. [(3,2), (2,3)]
        """
        possible_moves = []
        blank_row, blank_col = blank_xy
        length = self.dim - 1
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

    def matching_to_matrix(self, coordinate_x, coordinate_y):
        """
        Parameters: coordinate_x, coordinate_y represent the actual coordinates
        check the corresponding matrix for that coordinate
        note: as long as the coordinate is within a certain tile, return the matrix position
        for that tile. If not, return the matrix index of blank position
        """
        size = self.size
        pos_info, index_info = self.board_position()
        possible_moves = self.get_move(index_info[self.num])
        for each in pos_info:
            x, y = pos_info[each]
            if abs(coordinate_x - x) < size / 2 and abs(coordinate_y - y) < size / 2:
                return index_info[each]

        return index_info[self.num]

    def is_valid_move(self, target: tuple):
        """
        This function checks if target belongs to valid tiles that
        can be slided into the slot where the current blank tile is
        Parameter:
            target: tuple
        Returns: True if target is one of the valid tiles, False if not
        """
        possible_moves = self.get_move(self.blankposition())
        if target in possible_moves:
            return True
        else:
            return False

    def swap_tile(self, x, y):
        """
        x, y represents matrix pos 
        """
        pos_info, index_info = self.board_position()
        for each in pos_info:
            if index_info[each] == (x, y):
                idx = each

        s = turtle.Screen()
        turtle.hideturtle()
        s.addshape(self.puzzle_info[idx])
        s.addshape(self.puzzle_info[self.num])
        turtle.penup()
        turtle.speed(0)
        turtle.goto(pos_info[self.num])
        turtle.pendown()
        turtle.shape(self.puzzle_info[idx])
        turtle.stamp()

        turtle.penup()
        turtle.goto(pos_info[idx])
        turtle.pendown()
        turtle.shape(self.puzzle_info[self.num])
        turtle.stamp()

    #########################
    # 2.3: Game Interaction #
    #########################

    def get_click(self, coordinate_x, coordinate_y):
        """
        x, y represents the coordinate of the click 
        """
        x, y = self.matching_to_matrix(coordinate_x, coordinate_y)
        s = turtle.Screen()

        option = self.status_option(coordinate_x, coordinate_y)

        if self.is_valid_move((x, y)) and self.times > 0:

            self.swap_tile(x, y)
            target_tile_pos = x * self.dim + y
            x0, y0 = self.blankposition()
            blank_pos = x0 * self.dim + y0
            # update tiles position after swapping
            self.updated[target_tile_pos], self.updated[blank_pos] = self.updated[blank_pos], self.updated[
                target_tile_pos]

            self.times = self.times - 1
            self.move_counting()
            self.show_moves()
            if self.checking():
                self.record_winner()
                self.load_msg("Resources/winner.gif")
                turtle.exitonclick()

        elif self.times == 0:
            # stop onclick function
            # when the number of clicks exceeds the input number
            self.load_msg("Resources/Lose.gif")
            self.load_msg("Resources/credits.gif")
            turtle.exitonclick()

        elif option == "Reset":
            self.times = self.back_times
            self.counting = 0
            self.reset_puzzle()

        elif option == "Load":
            self.load_new_puzzle()

        elif option == "Quit":
            self.load_msg("Resources/quitmsg.gif")
            turtle.exitonclick()

    def load_msg(self, path: str):
        # loads message gif according to the parameter
        # Parameter: path, representing the path for the target gif
        s = turtle.Screen()
        s.tracer(1)
        t = turtle.Turtle()
        s.addshape(path)
        t.shape(path)
        time.sleep(2)
        t.hideturtle()

    def reset_puzzle(self):
        # reset the puzzle to the original version, the ideal one
        self.updated = self.goal
        self.load_puzzle()

    def status_option(self, coordinate_x: float, coordinate_y: float):
        """
        based on status_button() method, we can identify area within reset button,
        load button, and quit button respectively
        rest button: center(60, -280), size(80 * 80)
        load button: center(150, -280), size(80 * 76)
        quit button: center(240, -280), size(80 * 53)
        """
        if 20 <= coordinate_x <= 100 and -320 <= coordinate_y <= -240:
            option = "Reset"
        elif 110 <= coordinate_x <= 190 and -318 <= coordinate_y <= -242:
            option = "Load"
        elif 200 <= coordinate_x <= 280 and -306.5 <= coordinate_y <= -253.5:
            option = "Quit"
        else:
            option = "None"
        return option

    def print_files(self, puzzle_lst):
        # this function prints the name of all puzzle files
        if len(puzzle_lst) > 10:
            # load file_warning gif when more than 10 puzzle files
            self.load_msg("Resources/file_warning.gif")
            with open("5001_puzzle.err", "a") as infile:
                infile.write(f"{time.ctime(time.time())}: Error: More than 10 files loaded "
                             "LOCATION: TileGame.print_files(puzzle_lst)\n")
            self.print_files(puzzle_lst[:10])
        if len(puzzle_lst) == 1:
            return puzzle_lst[0]
        else:
            return puzzle_lst[0] + "\n" + self.print_files(puzzle_lst[1:])

    def load_new_puzzle(self):
        try:
            puzzle_files = self.read_puzzle_files()
            output = self.print_files(puzzle_files)

            target = turtle.textinput(f"Load Puzzle", "Enter the name of the puzzle"
                                                      f"you wish to load. Choices are:\n"
                                                      f"{output}")

            puzzle_info = initialize_file(target)
            dim = int(math.sqrt(int(puzzle_info["number"])))
            # raise error if the number is not a perfect square
            if dim * dim != int(puzzle_info["number"]):
                raise ValueError
            self.update_self(puzzle_info)

        except FileNotFoundError:
            self.load_msg("Resources/file_error.gif")

            with open("5001_puzzle.err", "a") as infile:
                infile.write(f"{time.ctime(time.time())}: Error: File {target} does not exist "
                             f"LOCATION: TileGame.load_new_puzzle()\n")

        except ValueError:
            with open("5001_puzzle.err", "a") as infile:
                infile.write(f"{time.ctime(time.time())}: Error: File {target} "
                             f"has malformed data "
                             f"LOCATION: TileGame.load_new_puzzle()\n")
            self.load_msg("Resources/malfile.gif")

    def checking(self):
        self.goal = self.get_goal()
        if self.updated == self.goal:
            return True
        else:
            return False

    def read_puzzle_files(self):
        # this function reads all puzzle files in the current directory
        current_path = os.getcwd()
        lst = os.listdir(current_path)
        puzzle_file = []
        for each in lst:
            if os.path.splitext(each)[1] == ".puz":
                puzzle_file.append(each)

        return puzzle_file

    #####################
    # 2.4: Status board #
    #####################

    def status_button(self):
        s = turtle.Screen()
        lst = ["Resources/resetbutton.gif", "Resources/loadbutton.gif", "Resources/quitbutton.gif"]
        for i in range(len(lst)):
            turtle.hideturtle()
            s.addshape(lst[i])
            turtle.penup()
            turtle.goto(60 + 90 * i, -280)
            turtle.pendown()
            turtle.shape(lst[i])
            turtle.stamp()

    def move_counting(self):
        # this functions updates the number of moves
        self.counting += 1

    def show_moves(self):
        # create whiteboard to show the number of moves
        t = turtle.Turtle()
        t.speed(0)
        t.hideturtle()
        t.fillcolor("white")
        t.pencolor("white")
        t.penup()
        t.goto(-90, -245)
        t.pendown()
        t.begin_fill()
        for i in range(2):
            t.forward(80)
            t.right(90)
            t.forward(70)
            t.right(90)
        t.end_fill()

        m = turtle.Turtle()
        turtle.tracer(0)
        m.hideturtle()
        m.penup()
        m.goto(-290, -300)
        m.pendown()
        m.pencolor("black")
        style = ('arial', 30, 'bold')
        # write number of moves on the whiteboard
        m.write(f'Player Moves: {self.counting}', font=style, align='left')
        turtle.update()

    #####################
    # 2.5: Leader board #
    #####################

    def load_sample(self):
        """
        This function loads the sample image for the user to follow
        when unscrambling the puzzle tiles
        """
        try:
            whiteboard = Rectangle(120, 120, pencolor="white")
            whiteboard.draw(320, 290)

            # create a whiteboard to display the sample gif
            s = turtle.Screen()
            path = self.puzzle_info["thumbnail"]
            s.addshape(path)
            turtle.hideturtle()
            turtle.speed(0)
            turtle.penup()
            turtle.goto(320, 290)
            turtle.pendown()
            turtle.shape(path)
            turtle.stamp()
        except:
            with open("5001_puzzle.err", "a") as infile:
                infile.write(f"{time.ctime(time.time())}: Error: could not open {path} "
                             f"LOCATION: load_puzzle()\n")
            self.load_msg("Resources/malfile.gif")

    def record_winner(self):
        """
        This function records the number of moves of the winner
        if there is one
        """
        with open("leader_board.txt", mode="a") as infile:
            infile.write(f"{self.name}: {self.user}: {self.counting}\n")

    def read_leaderboard_file(self):
        # read leader_board.txt file and return a list
        # consisting of previous winners
        info = []
        try:
            with open("leader_board.txt", mode="r") as infile:
                for lines in infile:
                    lines = lines.strip("\n").split(": ")
                    # if lines[0] == self.name:
                    info.append(lines[1:])
                return info
        except FileNotFoundError:
            with open("5001_puzzle.err", mode="a") as infile:
                infile.write(f"{time.ctime(time.time())}: Error: Could not open leader_board.txt. "
                             "LOCATION: TileGame.read_leaderboard_file()\n")
            self.load_msg("Resources/leaderboard_error.gif")

    def fn(self, sub_lst: list):
        """
        This function is used to access the second element of the list
        We will use its returning value as the key to sort a nested list
        """
        return int(sub_lst[1])

    def load_leaders(self):
        # load previous winners to the leader board
        info = self.read_leaderboard_file()
        # only load leaders when info is not empty
        if info:
            info.sort(key=self.fn)
            info = info[0:10]  # limit the length of list to 10
            turtle.hideturtle()
            turtle.penup()
            turtle.goto(140, 270)
            turtle.pendown()
            turtle.pencolor("blue")
            style = ('arial', 25, 'bold')
            turtle.write('Leaders:', font=style, align='left')
            for i in range(len(info)):
                turtle.hideturtle()
                turtle.penup()
                turtle.goto(140, 230 - i * 35)
                turtle.pendown()
                style = ('arial', 20, 'normal')
                turtle.write(f' {info[i][1]}: {info[i][0]}', font=style, align='left')
