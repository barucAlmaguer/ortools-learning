# Reference: https://twitter.com/barubaruc/status/1033774083660570628
# 
from ortools.constraint_solver import pywrapcp
# constraints
solver = pywrapcp.Solver('Bill')
mixed_fruit = solver.IntVar(0, 7, 'mixed fruit')
french_fries = solver.IntVar(0, 5, 'french fries')
side_salad = solver.IntVar(0, 5, 'side salad')
hot_wings = solver.IntVar(0, 4, 'hot wings')
cheese_sticks = solver.IntVar(0, 3, 'cheese sticks')
sampler = solver.IntVar(0, 2, 'sampler')
#relationships between vars:
solver.Add(
  (215 * mixed_fruit)
  + (275 * french_fries)
  + (335 * side_salad)
  + (355 * hot_wings)
  + (420 * cheese_sticks)
  + (580 * sampler) == 1505)
# decision builder
xkcd_phase = solver.Phase(
  [mixed_fruit,
  french_fries,
  side_salad,
  hot_wings,
  cheese_sticks,
  sampler],
  solver.CHOOSE_FIRST_UNBOUND,
  solver.ASSIGN_MIN_VALUE
)
# solve the problem
solver.Solve(xkcd_phase)
solution_count = 0
while solver.NextSolution():
  solution_count += 1
  print(f'Solution #{solution_count}')
  print('The bill includes:')
  print(f' {mixed_fruit.Value()} mixed fruits,')
  print(f' {french_fries.Value()} french fries,')
  print(f' {side_salad.Value()} side salads,')
  print(f' {hot_wings.Value()} hot wings,')
  print(f' {cheese_sticks.Value()} cheese sticks,')
  print(f' {sampler.Value()} samplers')
