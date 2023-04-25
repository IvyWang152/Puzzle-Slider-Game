import turtle
import time
from game_design import Rectangle, TileGame, initialize_file


def set_board():
    # This function draws the layout of the game interface
    play_board = Rectangle(460, 500)
    play_board.draw(-125, 70)
    leader_board = Rectangle(230, 500, pencolor="blue")
    leader_board.draw(240, 70)
    status_board = Rectangle(710, 90)
    status_board.draw(0, -280)   
                

def main():
    s = turtle.Screen()
    s.setup(width=840, height=840)
    s.title("CS5001 Sliding Puzzle Game")
    
    s.addshape("Resources/splash_screen.gif")
    initial = turtle.Turtle()
    initial.shape("Resources/splash_screen.gif")
    time.sleep(1)
    s.clear()
    
    user = s.textinput("CS5001 Puzzle Slide", "Your Name:")
    
    num = s.numinput("5001 Puzzle Slide - Moves",
                     "Enter the number of moves (chances) you want (5-200)?", minval=5, maxval=200)
        
    set_board()
    puzzle_info = initialize_file("yoshi.puz")
    instance = TileGame(puzzle_info, user, num)
    instance.checked()  # check if the initial puzzle solvable
    instance.status_button()  # load status button
    instance.load_leaders()  # load leaders
    instance.load_puzzle()  # load puzzles
    instance.load_sample()  # load sample picture for the puzzle
    s.onclick(instance.get_click)

    turtle.done()

    
if __name__ == "__main__":
    main()
