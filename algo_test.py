from puzzle_solver import Solver
import unittest

class TestSolver(unittest.TestCase):
    def test_init(self):
        init_state = ["1", "8", "7", "3", "9", "5", "4", "6", "2"]
        goal = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        p = Solver(init_state, goal)
        self.assertEqual(p.state, init_state)

    def test_solvable(self):
        # 3*3
        init0 = ["8", "6", "7", "2", "5", "4", "3", "9", "1"]
        init = ["9", "1", "3", "4", "2", "5", "7", "8", "6"]
        goal = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        p1 = Solver(init, goal)
        self.assertEqual(p1.is_solvable(), True)
        p0 = Solver(init0, goal)
        self.assertEqual(p0.is_solvable(), True)
        
        # 2*2
        init1 = ["1", "2", "3", "4"]
        goal1 = ["1", "2", "3", "4"]
        p2 = Solver(init1, goal1)
        self.assertEqual(p2.is_solvable(), True)
        
        # 4*4
        init2 = ["6","13","7","10","8","9","11","16","15","2","12","5","14","3","1","4"]
        goal2 = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16"]
        p3 = Solver(init2, goal2)
        self.assertEqual(p3.is_solvable(), True)

    def test_not_solvable(self):
        # 2*2
        init = ["1", "3", "2", "4"]
        init1 = ["1", "4", "2", "3"]
        goal = ["1", "2", "3", "4"]
        p = Solver(init, goal)
        self.assertEqual(p.is_solvable(), False)
        p1 = Solver(init1, goal)
        self.assertEqual(p1.is_solvable(), False)

        # 3*3
        init2 = ["1", "9", "3", "2", "4", "5", "6", "7", "8"]
        goal2 = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        p2 = Solver(init2, goal2)
        self.assertEqual(p2.is_solvable(), False)
        init3 = ["7", "9", "2", "8", "5", "3", "6", "4", "1"]
        p3 = Solver(init3, goal2)
        self.assertEqual(p3.is_solvable(), False)

        # 4*4
        init4 = ["3","9","1","15","14","11","4","6","13","16","10","12","2","7","8","5"]
        goal4 = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16"]
        p4 = Solver(init4, goal4)
        self.assertEqual(p4.is_solvable(), False)

        init5 = ["1","2","3","4","5","6","7","8","9","10","11","12","13","15","14","16"]
        p5 = Solver(init5, goal4)
        self.assertEqual(p5.is_solvable(), False)

        
        
def main():
    unittest.main(verbosity=3)

main()
        

        

        
        
        
