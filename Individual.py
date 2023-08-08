class Individual:

  '''
  This class represent an individual in the population for the GA

  Attributes:
    - path: a list that is used for storing the direction of the path
    - fitness: a variable used for saving the value of the fitness of the individual
    - number_of_cp_reached: a variable used for checking how many control points the individual has reached
    - cp_index: a dictionary used for checking at which number of steps the individual has reached a control point
  '''

  def __init__(self):
    '''
    Constructor of the Individual class: path is initialized as an empty list,
                                         fitness is initialized as 0,
                                         number_of_cp_reached is initialized as 0,
                                         cp_index is initialized with a single key:value element

    '''
    self.path = []
    self.fitness = 0
    self.number_of_cp_reached = 0
    self.cp_index = {0:0}

  # this method is used to retrieve the path of the individual
  def get_path(self):
    return self.path

  # this method is used to retrieve the fitness of the individual
  def get_fitness(self):
    return self.fitness

  # this method implements the concept of compass that each player can use to orient himself
  def compass(self,current_point,control_point):

    # the logic is very clear: given the (x,y) coordinate in which the player is
    # check in which direction go by comparing the next control point (x,y) coordinate


    if current_point[0] >= control_point[0] and current_point[1] >= control_point[1]:
      direction1 = 0
      direction2 = 1
    elif current_point[0] >= control_point[0] and current_point[1] <= control_point[1]:
      direction1 = 1
      direction2 = 2
    elif current_point[0] <= control_point[0] and current_point[1] <= control_point[1]:
      direction1 = 2
      direction2 = 3
    elif current_point[0] <= control_point[0] and current_point[1] >= control_point[1]:
      direction1 = 0
      direction2 = 3


    return direction1, direction2

  def __repr__(self):
        return "(Path: " + str(self.path) + ", fitness: " + str(self.fitness) + ", number_of_cp_reached: "+ str(self.number_of_cp_reached) + ", cp_index: " + str(self.cp_index) + ")"
