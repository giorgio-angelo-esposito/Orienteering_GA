import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
from Map import Map
from Individual import Individual
import argparse



def getNumberOfStepBetweenPoits(p1, p2):

  return (abs(p1[0] - p2[0])) + abs((p1[1] - p2[1])) # return the sum of the difference of points coordinates

"""# Function to get minimun number of steps between the start and end, passing through each control point"""

def getTotalNumberOfSteps(list_of_point):

  total_steps = 0 # initialize a variable that will count the total number of steps

  for i in range(0,len(list_of_point)-1): # iterate over the control points

    # for each control point get the distance between itself and the next and sum them up
    total_steps += getNumberOfStepBetweenPoits(list_of_point[i],list_of_point[i+1])

  return total_steps # return the total number of steps between the starting point and the ending point

def checkOutOfMap(point):

  # compare the coordiates of the current point the individual is upon with the matrix dimension (map limit)
  if point[0] < 0 or point[1] < 0 or point[0] > map_instance.rows -1 or point[1] > map_instance.columns - 1:
    return True

  return False

def checkObstacle(point):

  # compare the value of the cell given by the point coordinate with the obstacle variable
  if mappa[point[0]][point[1]] == 1:
    return True

  return False


def checkControlPoint(point, cp):

  # compare the coordinate of the point in which the individual is with the given control point coordinate
  if point[0] == cp[0] and point[1] == cp[1]:
    return True

  return False


def avoid_obstacle(moves, current_point, movement):

  # create a boolean variable and set it to false
  found = False
  # get the coordinate where the individual where before stambling on an obstacle
  current_point = [current_point[0] - movement[0], current_point[1] - movement[1]]
  # from all the available moves, remove the one that lead the individual over the obstacle
  remain_moves = moves.copy()
  remain_moves.remove(movement)

  # iterate over the remain moves
  for points in remain_moves:
    # calculate the new point
    point = [current_point[0] + points[0], current_point[1] + points[1]]

    # check if this new movement get the individual out of the map
    if checkOutOfMap(point):
      # if true, move the next available moves
      continue

    # check if the new movement get the individual over an obstacle
    if checkObstacle(point):
      # if true, move the next available moves
      continue
    else:
      # set the current point as the new point reached with the new movement
      current_point = point
      # set the boolean variable as true
      found = True
      # return the new point, the boolean variable and the new movement
      return current_point, found, points


def initPopulation(population_dim):

  population = [] # create an empty list that will contain the individuals
  # cp_list = map_instance.getControlPointList() # get the list of control points coordinates
  moves = [[0, -1], [-1, 0], [0, 1], [1, 0]] # available moves

  for ind in range(population_dim): # for each individual:
    number_of_cp_reached = 0 # initialize the number of control point reached as 0
    reached = False # initialize a random variable that is used to indicate that an individual has reached or not a control point
    blocked = False # initialize a random variable that is used to indicate that an individual has reached or not an obstacle
    individual = Individual() # create an Individual object
    current_point = cp_list[0] # get the first control point coordinate and set it as the current point (this is the starting point)
    steps = 0 # set the number of steps to 0

    for i in range(1, len(cp_list)): # iterate over the control points number
      reached = False
      control_point = cp_list[i] # get the coordinates of the next control point

      while not reached: # while the individual has not reached the control point

        if steps % 3 == 0: # every 3 steps the individial use the compass to orient itself toward the actual control point
          d1,d2 = individual.compass(current_point, control_point)
          movement = random.choice([moves[d1],moves[d2]])
        else:
          # otherwise the individual moves randomically selecting a move
          movement = random.choice(moves)

        individual.path.append(moves.index(movement)) # add to the individual path the index of the move selected
        steps += 1 # increment the number of steps of the individual by one
        current_point = [current_point[0] + movement[0], current_point[1] + movement[1]] # update the current position of the individual

        # check if the new point is out of the map
        if checkOutOfMap(current_point):
          # if yes, go back, remove the index from the path and decrease by 1 the steps taken by the individual
          current_point = [current_point[0] - movement[0], current_point[1] - movement[1]]
          individual.path.pop()
          steps -= 1

        # check if the new point is an obstacle
        if checkObstacle(current_point):
          # if yes avoid it, using the avoid_obstacle function
          current_point, found, new_movement = avoid_obstacle(moves, current_point, movement)
          steps -= 1 # decrease the total number of steps

          # check if the individual has found a way to avoid the obstacle
          if found:
            # if yes, then we remove from its path the old move and add the new one, used to avoid the obstacle
            individual.path.pop()
            individual.path.append(moves.index(new_movement))
            steps += 1 # increase the number of steps, because the individual has moved into a new direction
          else:
            # if cannot find a way, stop the loop for this individual
            blocked = True
            break

        # check if the new point is the control point
        if checkControlPoint(current_point, control_point):
          # if yes increment the number of control point reached by 1 and set it to the Individual variable
          number_of_cp_reached += 1
          individual.number_of_cp_reached = number_of_cp_reached
          individual.cp_index[i] = steps # set the total number of steps used to reach the control point
          reached = True # change the variable so the individual will now search the next control point

      # if the individual is blocked, stop the loop
      if blocked:
        break

    # after the loop, if the individual was blocked (and hasn't reached all the control points)
    if individual.number_of_cp_reached != len(cp_list) - 1:
      # set its fitness to infinite
      individual.fitness = np.inf
    else:
      # otherwise, set its fitness as the ration between the steps has used and the optimal one
      individual.fitness = steps/optimal_steps

    # add the individual to the population list
    population.append(individual)

  #return the population list
  return population


def findIndividualFitness(individual):

  moves = [[0, -1], [-1, 0], [0, 1], [1, 0]]
  point = map_instance.getControlPointList()[0]
  steps = 0

  for m in individual.path: # loop over the individual path to get the number of steps of the individual
    point = [point[0] + moves[m][0], point[1] + moves[m][1]]
    steps += 1

    if checkOutOfMap(point):
      point = [point[0] - moves[m][0], point[1] - moves[m][1]]
      steps -= 1

    if checkObstacle(point):
      steps -= 1

  # compute the individual fitness as ration between number of its steps and the optimal ones
  individual.fitness = steps/optimal_steps


def findFitness(population):

  # for every individual in the population, compute its fitness by using the findIndividualFitness function
  for individual in population:

    findIndividualFitness(individual)

def rankPopulation(population):

  # sort the population by the fitness in increasing order
  return sorted(population, key = lambda individual: individual.fitness)


def rouletteWheelSelection(population_ranked):

    # compute the total fitness and the individual probabilities
    total_fitness = sum([1 / individual.fitness for individual in population_ranked])
    individual_probabilities = [(1 / individual.fitness) / total_fitness for individual in population_ranked]

    # create the cumulative probabilities, so each individual has an interval over the roulette
    # individual with bigger fitness will have bigger portion in the roulette wheel
    cumulative_probabilities = [individual_probabilities[0]]
    for value in individual_probabilities[1:]:
        cumulative_probabilities.append(cumulative_probabilities[-1] + value)

    # get a random number between 0 and 1
    random_number = np.random.uniform(0, 1)

    # check for the interval into which the random number fall and select that individual
    for i, value in enumerate(cumulative_probabilities):
        if random_number < value:
            return population_ranked[i]

    # if the random number is exactly 1, return the last individual
    return population_ranked[-1]


def matingPool(population_ranked):

  # create a list that will be used to store individual selected with the Roulette Wheel selection
  mating_pool = []

  for i in range(len(population_ranked)): # loop over all the individual

    selected_individual = rouletteWheelSelection(population_ranked) # select and individual using the roulette wheel selection
    population_ranked.remove(selected_individual) # remove the selected individual from the population
    mating_pool.append(selected_individual) # add the selected individual to the mating pool

  # return the mating pool
  return mating_pool


def retrievePathToCP(individual, cp):

  # get the number of steps to which the individual has reached a specific control point
  i = individual.cp_index.get(cp)

  # return the path of the individual till the index selected
  return individual.path[:i]


def retrievePathToEnd(individual,cp):

  # get the number of steps to which the individual has reached a specific control point
  i = individual.cp_index.get(cp)

  # return the path of the individual from the index selected to the end
  return individual.path[i:]


def reproduce(parent1, parent2):

  # instantiate a new Individual object
  child = Individual()

  # select a random control point
  cp_index = random.randint(1,len(map_instance.getControlPointList()) - 2)

  # get the path of the first parent till the selected control point
  a = retrievePathToCP(parent1,cp_index)

  # get the path of the second parent from the selected control point till the end
  b = retrievePathToEnd(parent2,cp_index)

  # assign to the path of the child the union of the two paths from the parents
  child.path = a + b

  # assign to the number of control point reached by the child as the number of control point reached by the first parent
  child.number_of_cp_reached = parent1.number_of_cp_reached


  for i in range(1,cp_index+1): # loop over the control point till the one randomically selected

    # assign to the dictionary of indeces of the child the one of the first parent, from the starting point till the selected control point
    child.cp_index[i] = parent1.cp_index.get(i)


  for i in range(cp_index+1,len(map_instance.getControlPointList())): # loop over the control point from the randomically selected till the ending point

    # get the difference between the number of steps of two consecutive control points
    diff = parent2.cp_index.get(i) - parent2.cp_index.get(i-1)

    # sum the number of steps to the previous control point plus the difference computed in the previous step
    v = child.cp_index.get(i-1) + diff

    # assing the number of steps used to reach the control point as the sum computed in the previous step
    child.cp_index[i] = v

  # return the child
  return child


def reproducePopulation(mating_pool):

  # create an empty list where to store the child created by using the reproduction function
  children = []

  for i in range(0,len(mating_pool)-1,2): # loop over the individual in the mating pool, selecting 2 individual at time

    # create a child
    child = reproduce(mating_pool[i],mating_pool[i+1])

    # add the new child to the list
    children.append(child)

  # return the list of children
  return children


def getPathBetweenCP(individual, index):

  # get the number of steps used to arrive at the control point before the one passed as argument
  i = individual.cp_index.get(index-1)

  # get the number of steps used to arrive at the control point passed as argument
  j = individual.cp_index.get(index)

  # return the two indeces and the path between these two
  return i,j,individual.path[i:j]


def swap(path):

  # randomically select two indeces in the path
  i = random.randint(0,len(path)-1)
  j = random.randint(0,len(path)-1)

  # swap the movements in the path corresponding to the selected indeces
  path[i], path[j] = path[j],path[i]

  # return the path with swapped movement
  return path


def mutateIndividual(individual):

  # randomically select a control point
  cp_index = random.randint(1,len(map_instance.getControlPointList())-1)

  # get the path between the selected control point and the previous one
  i,j,path = getPathBetweenCP(individual, cp_index)

  # do the swap
  shuffled_path = swap(path)

  # get the new index for the control point
  j = i + len(shuffled_path)

  # update the path of the individual by replacing the old path with the swapped one
  individual.path = individual.path[:i] + shuffled_path + individual.path[j:]


def mutatePopulation(population, mutation_rate):

  for individual in population: # loop over the population

    # get a random number
    index = np.random.uniform(0,1)

    # condition to which apply the mutation
    if index < mutation_rate:

      # if the random number is lower than the mutation rate, the apply the mutation to the actual individual
      mutateIndividual(individual)

def nextPopulation(actualPopulation, mutation_rate):

  # rank the actual population
  ranked_pop = rankPopulation(actualPopulation)

  # get the mating pool
  mating_pool = matingPool(ranked_pop)

  # get the new population by reproduction
  next_population = reproducePopulation(mating_pool)

  # apply mutation
  mutatePopulation(next_population,mutation_rate)

  # get the fitness of the new population
  findFitness(next_population)

  # return the new population
  return next_population


def geneticAlgorithm(pop_dim, iteration, mutation_rate):

  # craete the first population
  pop = initPopulation(pop_dim)

  # craete new population for a specified number of iteration
  for i in range(iteration):
    pop = nextPopulation(pop, mutation_rate)

    # since we use the roulette wheel selection, we halve the population at every iteration
    # so, if the population has less than 5 individual, we stop
    if len(pop) < 5:
      break

  # return the final population
  return pop


def getBestIndividual(population):
    # sort the final population in increasing order
    sorted_population = sorted(population, key=lambda individual: individual.fitness)

    # return the first element of the sorted population
    return sorted_population[0]


parser = argparse.ArgumentParser(description="Genetic algorithm for orieentiring")
parser.add_argument("--pop_dim", type=int, required=True, help="Population dimension")
parser.add_argument("--iteration", type=int, required=True, help="Number of iterations")
parser.add_argument("--mutation_rate", type=float, required=True, help="Mutation rate")
parser.add_argument("--rows", type=int, required=True, help="Number of rows for the map")
parser.add_argument("--columns", type=int, required=True, help="Number of columns for the map")
parser.add_argument("--num_obstacles", type=int, required=True, help="Number of obstacles for the map")
parser.add_argument("--num_control_points", type=int, required=True, help="Number of control points for the map")
args = parser.parse_args()

map_instance = Map(args.rows, args.columns, args.num_obstacles, args.num_control_points)
mappa, lanterne = map_instance.create_map()
map_instance.visualizeMap(mappa)
print('\n Control points coordinates:')
cp_list = map_instance.getControlPointList()
print(cp_list)
optimal_steps = getTotalNumberOfSteps(cp_list)

def main():

  pop = geneticAlgorithm(args.pop_dim, args.iteration, args.mutation_rate)

  best = getBestIndividual(pop)

  map_instance.visualizeIndividual(mappa,best)

if __name__ == "__main__":
    main()
