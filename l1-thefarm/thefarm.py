'''
Problem at hand:
Suppose we are in a farm and in a pen we see 56 legs and 20 heads of cows and chickens. 
Then, how many cows and how many chickens are we seeing?
'''
from ortools.constraint_solver import pywrapcp
solver = pywrapcp.Solver('Farm')
# this constraints restrict the amount of heads
cows = solver.IntVar(0, 20, 'Cows')
chicks = solver.IntVar(0, 20, 'Chickens')
# with this, we can start adding relationships between variables
solver.Add((cows * 4) + (chicks * 2) == 56)
solver.Add((cows * 1) + (chicks * 1) == 20)
# configure solver
decision_builder = solver.Phase(
  [cows, chicks],
  solver.CHOOSE_FIRST_UNBOUND,
  solver.ASSIGN_MIN_VALUE
)
# Solve the problem!
solver.Solve(decision_builder)
# Problem solved, we hope
solution_count = 0
while solver.NextSolution():
  solution_count += 1
  print(f'Solution #{solution_count}')
  print(f'I see {cows.Value()} cows and {chicks.Value()} chickens')
  print(f'There are {cows.Value() + chicks.Value()} heads in total')