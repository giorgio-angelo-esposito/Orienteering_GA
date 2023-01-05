class Individual:

  '''
  This class represent an individual in the population for the GA
  
  Attributes:
    - path: a list that is used for storing the direction of the path
    - fitness: a variable used for saving the value of the fitness of the individual
  '''

  def __init__(self):
    '''
    Constructor of the Individual class: path is initialized as an empty list
                                         while fitness is initialized as 0 
    '''
    self.path = []
    self.fitness = 0

  def getPath(self):
    # this method is used to retrieve the path of the individual 
    return self.path

  def getFitness(self):
    # this method is used to retrieve the fitness of the individual
    return self.fitness