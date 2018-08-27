'''
Problem at hand:
generate a model and solver that can print any possible sudoku game
'''
from ortools.constraint_solver import pywrapcp
# Here, we can add our specific restrictions to find a certain sudoku solution:
# Change 0's for the numbers you want to fix in the board:
my_board = []
my_board.append([1, 2, 3, 0, 0, 0, 0, 0, 0])
my_board.append([4, 5, 6, 0, 0, 0, 0, 0, 0])
my_board.append([7, 8, 9, 0, 0, 0, 0, 0, 0])
my_board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
my_board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
my_board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
my_board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
my_board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
my_board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
solver = pywrapcp.Solver('Sudoku')
# restrictions (Sudoku cells)
board = [
  [solver.IntVar(1, 9, 'Cell') for i in range(0, 9)]
    for j in range(0, 9)
]
# relations between restrictions (unique numbers per row/column, square 3x3)
# First, the rows:
for row in board:
  solver.Add(solver.AllDifferent(row))
# Then, the columns:
for col in zip(*board):
  solver.Add(solver.AllDifferent(list(col)))
# for the 3x3 squares, we need a helper function:
def constrain_quadrant(row, col):
    quadrant = []
    for i in range(3):
        for j in range(3):
            quadrant.append(board[row+i][col+j])
    solver.Add(solver.AllDifferent(quadrant))
# We loop through the 9 quadrant's top left corners
# and place constraints
for i in range(0, 9, 3):
    for j in range(0, 9, 3):
        constrain_quadrant(i, j)
# Add specific restrictions
for i, r in enumerate(my_board):
  for j, c in enumerate(r):
    if(c != 0):
      solver.Add(board[i][j] == c) # Add restrictions
# configure solver to generate random sudoku boards
# first, we unwrap the board to a 1-D List
from itertools import chain
cells = chain.from_iterable(board)
sudoku_phase = solver.Phase(
  list(cells),
  solver.CHOOSE_FIRST_UNBOUND,
  solver.ASSIGN_RANDOM_VALUE
)
# make sure we always start with a different solution
from random import random as rand
solver.ReSeed(int(rand() * 1000000))
# Solve the problem!
solver.Solve(sudoku_phase)
# helper function to print the board
def printSudokuBoard():
  for i, r in enumerate(board):
    if(i in [3, 6]):
      print('-----------------------')
    text = '['
    for j, c in enumerate(r):
      if(j in [3, 6]):
        text += '| '
      text += f'{c.Value()} '
    text = text.strip(' ') + ']'
    print(text)
# generate first solution:
if(solver.NextSolution()):
  print('Solution found! use printSudokuBoard() to view the graphic solution')
  print('or solver.NextSolution() to get another one')
else:
  print('Solution not found :(')
  print('Check your restrictions on my_board')