'''
Problem at hand:
generate a model and solver that can print any possible sudoku game
'''
from ortools.constraint_solver import pywrapcp
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
def printSudokuBoard(board):
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
solver.NextSolution()