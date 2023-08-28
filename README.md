# OrienteeringGA
OrienteeringGA is my project for the course Artificial Intelligence Fundamentals. I have developed a genetic algorithm that play orieentiring: given a map (a grid) where are defined a starting point, a specified number of control points and an arrival point, the algorithm finds the optimal path form the starting point, passing through all the control points and finish in the arrival point.

You can find the project either as a notebook or as a .py files, in the file folder. For the latter, the following libraries are requested:

 - `Matplotlib`
 - `Numpy`
 - `Seaborn`
 - `argparse`
 
You can execute the 'orieentiring_ga.py' file on terminal, giving the following arguments:
 - **POP_DIM**: the dimension of the starting population;
 - **ITERATION**: the number of maximum iteration;
 - **MUTATION_RATE**: the mutation rate;
 - **ROWS**: the number of rows of the matrix representing the map;
 - **COLUMNS**: the number of columns of the matrix representing the map;
 - **NUM_OBSTACLES**: represent the number of obstacles that will be randomlly positioned in the map;
 - **NUM_CONTROL_POINTS**: represent the number of control points that will be randomlly positioned in the map;

You can use the command `-h` or `--help`, after the file name, to display an help message. 

