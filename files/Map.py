import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class Map:

  '''
  This class is used to create the map where the Orieentiring take place:
  it is a mxn array (m and n are given as parameter) where a certain number of
  obstacles and control points are placed.

  Attributes:
    - rows: the number of rows of the map (the m dimension)
    - colums: the numbers of the map (the n dimension)
    - number_of_obstacles: the number of obstacles that will appear on the map
    - number_of_cp: number of control points that will appear on the map
    - cp_list: a list containing all the coordinates of the control points.
               Initially contains the start point at (0,0)
  '''

  def __init__(self, rows, columns, number_of_obstacles, number_of_cp):

    '''
    The constructor of the map: lenght and height represent the dimension of the map (array)
    while number_of_obstacles and number_of_cp represent the number of obstacles and the number
    of control points that will be placed on the map, respectively.
    '''

    self.rows = rows
    self.columns = columns
    self.number_of_obstacles = number_of_obstacles
    self.number_of_cp = number_of_cp
    self.cp_list = []

  def create_map(self):

    '''
    This method is used to fill the array: the 'walkable ground' will be the cells that contains 0, the obstacle
    will be the cells containing 1 and the control points will be the cells contains 2, including the start and
    ending points.
    '''

    map_array = np.zeros((self.rows, self.columns)) #i nitially, we create a matrix with all 0s

    for i in range(self.number_of_obstacles): # iterate over the number of obstacles

      # randomically, create the coordinates where to put the obstacle
      x_obstacle = np.random.randint(0,self.rows)
      y_obstacle = np.random.randint(0,self.columns)

      # check if the coordinate corresponds with a control point, the start or the end
      if map_array[x_obstacle][y_obstacle] == 2:
        # if true, do not place the obstacle
        continue
      else:
        # else, place the obstacle
        map_array[x_obstacle][y_obstacle] = 1

    # next, place the control point
    for i in range(self.number_of_cp):

      while True:
        # randomically, create the coordinates where to put the control point
        x_cp = np.random.randint(1, self.rows - 1)
        y_cp = np.random.randint(1, self.columns - 1)

        # check if one of the djacent_cells contains an obstacles
        adjacent_cells = [(x_cp + dx, y_cp + dy) for dx, dy in [[0, -1], [-1, 0], [0, 1], [1, 0]]]
        if any(map_array[x][y] == 1 for x, y in adjacent_cells):
            # if there is, find new coordinates for the control points
            continue
        else:
            # else, place the control point
            map_array[x_cp][y_cp] = 2
            self.cp_list.append([x_cp, y_cp])
            self.number_of_cp -= 1
            break


    # I have decided to sort the control point vertically or horizontally based on a random number
    probability = np.random.uniform(0,1,1)

    if probability >= 0.5:
      self.cp_list.sort(key = lambda point: point[1])
    else:
      self.cp_list.sort()

    return map_array, self.cp_list # return the array and the list


  def getControlPointList(self):
    '''
    this method is used for obtain the list of control points
    '''
    return self.cp_list

  def visualizeMap(self,map):

    '''
    this method is used for plotting the map
    '''
    # set the dimension of the plot
    plt.figure(figsize=(12,12))

    #use a heatmap for plotting, so the same value will have the same color
    ax = sns.heatmap(map, cbar = False, cmap = sns.color_palette("coolwarm", 12),linewidth = 1)

    # get the x and y coordinate for each point, and sum 0.5, so the line will start at the centre of the square
    x = [self.cp_list[i][1] + 0.5 for i in range(len(self.cp_list))]
    y = [self.cp_list[i][0] + 0.5 for i in range(len(self.cp_list))]

    # plot the lines
    plt.plot(x, y, 'ro-')

    # add text near the point
    plt.text(x[0] - 0.15, y[0] - 0.15, 'Start')
    for i in range(1,len(x)-1):
      plt.text(x[i] + 0.15, y[i] + 0.15, str(i))
    plt.text(x[-1] - 0.20, y[-1] - 0.20, 'End')

    ax.invert_yaxis()

    plt.ylim(0,self.rows)
    plt.xlim(0,self.columns)

    # show the plot
    plt.show()

  def visualizeIndividual(self, map, individual):

    '''
    This method is used to visualize an individual on the map
    '''

    map_copy = map.copy() # make a copy of the map
    moves = [[0, -1], [-1, 0], [0, 1], [1, 0]]
    point = self.getControlPointList()[0] # get the starting point

    for m in individual.path: # follow the individual path
      point = [point[0] + moves[m][0], point[1] + moves[m][1]]

      if point[0] >= self.rows or point[1] >= self.columns or point[0] < 0 or point[1] < 0: # check if the path leads out of the map
        point = [point[0] - moves[m][0], point[1] - moves[m][1]] # if yes go back
        continue

      # here we change the value of the cell the individual moves on, so they will appear of a different color when we call the method
      # we change color also when the individual finds a control point
      if map_copy[point[0]][point[1]] == 2:
        map_copy[point[0]][point[1]] = 3
      else:
        map_copy[point[0]][point[1]] = 3

    plt.figure(figsize=(12,12))

    ax = sns.heatmap(map_copy, cbar = False, cmap = sns.color_palette("coolwarm", 12),linewidth = 1)
    ax.invert_yaxis()

    x = [self.cp_list[i][1] + 0.5 for i in range(len(self.cp_list))]
    y = [self.cp_list[i][0] + 0.5 for i in range(len(self.cp_list))]

    # plot the lines
    plt.plot(x, y, 'ro-')

    # add text near the point
    plt.text(x[0] - 0.25, y[0] - 0.25, 'Start')
    for i in range(1,len(x)-1):
      plt.text(x[i] + 0.15, y[i] + 0.15, str(i))
    plt.text(x[-1] - 0.20, y[-1] - 0.20, 'End')

    plt.ylim(0,self.rows)
    plt.xlim(0,self.columns)

    # show the plot
    plt.show()
