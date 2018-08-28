'''
a company builds chairs and tables
the chairs require 15ft of wood and 6h of labor
the tables require 24ft of wood and 5h of labor
the chairs give a profit of $12USD and the tables $24USD
There are only 300ft of wood and 120h of labor
'''
# solved by ortools constraint solver
from ortools.constraint_solver import pywrapcp
solver = pywrapcp.Solver('carpenter')
# create variables
chairs = solver.IntVar(0, 20, 'chairs')
tables = solver.IntVar(0, 12, 'tables')
# create restrictions between variables
solver.Add((chairs * 15)+(tables * 24) <= 300)
solver.Add((chairs * 6)+(tables * 5) <= 120)
# configure solver
wood_builder = solver.Phase(
  [chairs, tables],
  solver.CHOOSE_FIRST_UNBOUND,
  solver.ASSIGN_MIN_VALUE
)
# solve the thing
solver.Solve(wood_builder)
# iterate solutions
print(f'{chairs.Value()} chairs and {tables.Value()} tables')
# TODO: restriction to optimize, instead of just feasible solutions