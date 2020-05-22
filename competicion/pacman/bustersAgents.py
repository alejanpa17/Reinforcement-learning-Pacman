# bustersAgents.py
# ----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import util
from game import Agent
from game import Directions
from keyboardAgents import KeyboardAgent
import inference
import busters
#from wekaI import Weka

class NullGraphics:
    "Placeholder for graphics"
    def initialize(self, state, isBlue = False):
        pass
    def update(self, state):
        pass
    def pause(self):
        pass
    def draw(self, state):
        pass
    def updateDistributions(self, dist):
        pass
    def finish(self):
        pass

class KeyboardInference(inference.InferenceModule):
    """
    Basic inference module for use with the keyboard.
    """
    def initializeUniformly(self, gameState):
        "Begin with a uniform distribution over ghost positions."
        self.beliefs = util.Counter()
        for p in self.legalPositions: self.beliefs[p] = 1.0
        self.beliefs.normalize()

    def observe(self, observation, gameState):
        noisyDistance = observation
        emissionModel = busters.getObservationDistribution(noisyDistance)
        pacmanPosition = gameState.getPacmanPosition()
        allPossible = util.Counter()
        for p in self.legalPositions:
            trueDistance = util.manhattanDistance(p, pacmanPosition)
            if emissionModel[trueDistance] > 0:
                allPossible[p] = 1.0
        allPossible.normalize()
        self.beliefs = allPossible

    def elapseTime(self, gameState):
        pass

    def getBeliefDistribution(self):
        return self.beliefs


class BustersAgent:
    "An agent that tracks and displays its beliefs about ghost positions."

    def __init__( self, index = 0, inference = "ExactInference", ghostAgents = None, observeEnable = True, elapseTimeEnable = True):
        inferenceType = util.lookup(inference, globals())
        self.inferenceModules = [inferenceType(a) for a in ghostAgents]
        self.observeEnable = observeEnable
        self.elapseTimeEnable = elapseTimeEnable
        self.random_move = 0
        self.next_random_move = 0
        self.posX_random_move = -1
        self.posY_random_move = -1
        #elf.weka= Weka()
        #self.weka.start_jvm()

    def registerInitialState(self, gameState):
        "Initializes beliefs and inference modules"
        import __main__
        self.display = __main__._display
        for inference in self.inferenceModules:
            inference.initialize(gameState)
        self.ghostBeliefs = [inf.getBeliefDistribution() for inf in self.inferenceModules]
        self.firstMove = True
        self.distancer = Distancer(gameState.data.layout, False)


    def observationFunction(self, gameState):
        "Removes the ghost states from the gameState"
        agents = gameState.data.agentStates
        gameState.data.agentStates = [agents[0]] + [None for i in range(1, len(agents))]
        return gameState

    def getAction(self, gameState):
        "Updates beliefs, then chooses an action based on updated beliefs."
        #for index, inf in enumerate(self.inferenceModules):
        #    if not self.firstMove and self.elapseTimeEnable:
        #        inf.elapseTime(gameState)
        #    self.firstMove = False
        #    if self.observeEnable:
        #        inf.observeState(gameState)
        #    self.ghostBeliefs[index] = inf.getBeliefDistribution()
        #self.display.updateDistributions(self.ghostBeliefs)
        return self.chooseAction(gameState)

    def chooseAction(self, gameState):
        "By default, a BustersAgent just stops.  This should be overridden."

        return Directions.STOP

class Cola(object):

    __datos = None

    def __init__(self):
        self.__datos = []

    def add(self, dato):
        self.__datos.insert(0, dato)

    def pop(self):
        if self.isEmpty():
            return True
        else:
            return self.__datos.pop()

    def isEmpty(self):
        return len(self.__datos) == 0

    def size(self):
        return len(self.__datos)

    def score(self, estado):
        scores = []
        scores.append(str(self.__datos[3].split(", ")[50]))
        scores.append(str(self.__datos[2].split(", ")[50]))
        scores.append(str(self.__datos[1].split(", ")[50]))
        return estado+", " + ", ".join(scores)

#import BasicAgentAA

class BustersKeyboardAgent(BustersAgent, KeyboardAgent, Cola):
    "An agent controlled by the keyboard that displays beliefs about ghost positions."

    def __init__(self, index = 0, inference = "KeyboardInference", ghostAgents = None):
        KeyboardAgent.__init__(self, index)
        BustersAgent.__init__(self, index, inference, ghostAgents)
        Cola.__init__(self)


    def getAction(self, gameState):
        return BustersAgent.getAction(self, gameState)

    def chooseAction(self, gameState):
        return KeyboardAgent.getAction(self, gameState)

    def printLineData(self, gameState):

        cadena = []
        cabecera = "@RELATION pacman-data\n\n@ATTRIBUTE posX NUMERIC\n@ATTRIBUTE posY NUMERIC\n@ATTRIBUTE dFood NUMERIC\n@ATTRIBUTE North {True, False}\n@ATTRIBUTE South {True, False}\n@ATTRIBUTE East {True, False}\n@ATTRIBUTE West {True, False}\n@ATTRIBUTE DirPACMAN {North, South, East, West, Stop}\n@ATTRIBUTE Ghost1posX NUMERIC\n@ATTRIBUTE Ghost1posY NUMERIC\n@ATTRIBUTE dghost1pacmanX NUMERIC\n@ATTRIBUTE dghost1pacmanY NUMERIC\n@ATTRIBUTE dGhost1 NUMERIC\n@ATTRIBUTE DirGhost1 {North, South, East, West, Stop, -1}\n@ATTRIBUTE Ghost2posX NUMERIC\n@ATTRIBUTE Ghost2posY NUMERIC\n@ATTRIBUTE dghost2pacmanX NUMERIC\n@ATTRIBUTE dghost2pacmanY NUMERIC\n@ATTRIBUTE dGhost2 NUMERIC\n@ATTRIBUTE DirGhost2 {North, South, East, West, Stop, -1}\n@ATTRIBUTE Ghost3posX NUMERIC\n@ATTRIBUTE Ghost3posY NUMERIC\n@ATTRIBUTE dghost3pacmanX NUMERIC\n@ATTRIBUTE dghost3pacmanY NUMERIC\n@ATTRIBUTE dGhost3 NUMERIC\n@ATTRIBUTE DirGhost3 {North, South, East, West, Stop, -1}\n@ATTRIBUTE Ghost4posX NUMERIC\n@ATTRIBUTE Ghost4posY NUMERIC\n@ATTRIBUTE dghost4pacmanX NUMERIC\n@ATTRIBUTE dghost4pacmanY NUMERIC\n@ATTRIBUTE dGhost4 NUMERIC\n@ATTRIBUTE DirGhost4 {North, South, East, West, Stop, -1}\n@ATTRIBUTE dg1g2X NUMERIC\n@ATTRIBUTE dg1g2Y NUMERIC\n@ATTRIBUTE dg1g2M NUMERIC\n@ATTRIBUTE dg1g3X NUMERIC\n@ATTRIBUTE dg1g3Y NUMERIC\n@ATTRIBUTE dg1g3M NUMERIC\n@ATTRIBUTE dg1g4X NUMERIC\n@ATTRIBUTE dg1g4Y NUMERIC\n@ATTRIBUTE dg1g4M NUMERIC\n@ATTRIBUTE dg2g3X NUMERIC\n@ATTRIBUTE dg2g3Y NUMERIC\n@ATTRIBUTE dg2g3M NUMERIC\n@ATTRIBUTE dg2g4X NUMERIC\n@ATTRIBUTE dg2g4Y NUMERIC\n@ATTRIBUTE dg2g4M NUMERIC\n@ATTRIBUTE dg3g4X NUMERIC\n@ATTRIBUTE dg3g4Y NUMERIC\n@ATTRIBUTE dg3g4M NUMERIC\n@ATTRIBUTE score0 NUMERIC\n@ATTRIBUTE score1 NUMERIC\n@ATTRIBUTE score2 NUMERIC\n@ATTRIBUTE score3 NUMERIC\n\n\n@data\n"
        cadena.append(str(gameState.getPacmanPosition()[0]))
        cadena.append(str(gameState.getPacmanPosition()[1]))
        cadena.append(str(gameState.getDistanceNearestFood()))

        cadena.append(str('North' in gameState.getLegalPacmanActions()))
        cadena.append(str('South' in gameState.getLegalPacmanActions()))
        cadena.append(str('East' in gameState.getLegalPacmanActions()))
        cadena.append(str('West' in gameState.getLegalPacmanActions()))
        cadena.append(str(gameState.data.agentStates[0].getDirection()))

        for i in range(0, gameState.getNumAgents() - 1):
            cadena.append(str(gameState.getGhostPositions()[i][0]))
            cadena.append(str(gameState.getGhostPositions()[i][1]))
            cadena.append(str(abs(gameState.getGhostPositions()[i][0]-gameState.getPacmanPosition()[0]))) #Distancia X entre pacman y fantasma
            cadena.append(str(abs(gameState.getGhostPositions()[i][1]-gameState.getPacmanPosition()[1]))) #Distancia Y entre pacman y fantasma
            cadena.append(str(gameState.data.ghostDistances[i]))
            cadena.append(str(gameState.getGhostDirections().get(i)))

        for i in range(0, gameState.getNumAgents() - 1):
                j = i + 1
                while j <  gameState.getNumAgents() - 1:
                    g1gNX = abs(gameState.getGhostPositions()[i][0]-gameState.getGhostPositions()[j][0]) #Distanica entre GN
                    g1gNY = abs(gameState.getGhostPositions()[i][1]-gameState.getGhostPositions()[j][1])
                    g1gNM = g1gNX + g1gNY
                    cadena.append(str(g1gNX)) #Distancia X entre g1 y g2
                    cadena.append(str(g1gNY)) #Distancia Y entre g1 y g2
                    cadena.append(str(g1gNM)) #Distancia manhattan entre g1 y g2
                    j += 1

        cadena.append(str(gameState.getScore()))



        for n, i in enumerate(cadena):
            if i == "None":
                cadena[n] = "-1"

        estado = ", ".join(cadena)

        ponerCabecera = False
        import os.path as path
        if (not path.exists("Output.arff")):
            ponerCabecera = True


        text_file = open("Output.arff", "a")
        if(ponerCabecera):
            text_file.write(cabecera)


        self.add(estado)

        if self.size() > 4:
            text_file.write(self.score(self.pop()))
            text_file.write("\n")
            #print self.pop()


        #print self.size()

        #print estado


from distanceCalculator import Distancer
from game import Actions
from game import Directions
import random, sys

'''Random PacMan Agent'''
class RandomPAgent(BustersAgent):

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)

    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food

    ''' Print the layout'''
    def printGrid(self, gameState):
        table = ""
        ##print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table

    def chooseAction(self, gameState):
        move = Directions.STOP
        legal = gameState.getLegalActions(0) ##Legal position from the pacman
        move_random = random.randint(0, 3)
        if   ( move_random == 0 ) and Directions.WEST in legal:  move = Directions.WEST
        if   ( move_random == 1 ) and Directions.EAST in legal: move = Directions.EAST
        if   ( move_random == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
        if   ( move_random == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH
        return move

class GreedyBustersAgent(BustersAgent):
    "An agent that charges the closest ghost."

    def registerInitialState(self, gameState):
        "Pre-computes the distance between every two points."
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)

    def chooseAction(self, gameState):
        """
        First computes the most likely position of each ghost that has
        not yet been captured, then chooses an action that brings
        Pacman closer to the closest ghost (according to mazeDistance!).

        To find the mazeDistance between any two positions, use:
          self.distancer.getDistance(pos1, pos2)

        To find the successor position of a position after an action:
          successorPosition = Actions.getSuccessor(position, action)

        livingGhostPositionDistributions, defined below, is a list of
        util.Counter objects equal to the position belief
        distributions for each of the ghosts that are still alive.  It
        is defined based on (these are implementation details about
        which you need not be concerned):

          1) gameState.getLivingGhosts(), a list of booleans, one for each
             agent, indicating whether or not the agent is alive.  Note
             that pacman is always agent 0, so the ghosts are agents 1,
             onwards (just as before).

          2) self.ghostBeliefs, the list of belief distributions for each
             of the ghosts (including ghosts that are not alive).  The
             indices into this list should be 1 less than indices into the
             gameState.getLivingGhosts() list.
        """
        pacmanPosition = gameState.getPacmanPosition()
        legal = [a for a in gameState.getLegalPacmanActions()]
        livingGhosts = gameState.getLivingGhosts()
        livingGhostPositionDistributions = \
            [beliefs for i, beliefs in enumerate(self.ghostBeliefs)
             if livingGhosts[i+1]]
        return Directions.EAST

class BasicAgentAAux(BustersAgent, Cola):

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        self.countActions = 0
        Cola.__init__(self)


    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food

    ''' Print the layout'''
    def printGrid(self, gameState):
        table = ""
        #print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table

    def printInfo(self, gameState):
        '''print "---------------- TICK ", self.countActions, " --------------------------"
        # Dimensiones del mapa
        width, height = gameState.data.layout.width, gameState.data.layout.height
        print "Width: ", width, " Height: ", height
        # Posicion del Pacman
        print "Pacman position: ", gameState.getPacmanPosition()
        # Acciones legales de pacman en la posicion actual
        print "Legal actions: ", gameState.getLegalPacmanActions()
        # Direccion de pacman
        print "Pacman direction: ", gameState.data.agentStates[0].getDirection()
        # Numero de fantasmas
        print "Number of ghosts: ", gameState.getNumAgents() - 1
        # Fantasmas que estan vivos (el indice 0 del array que se devuelve corresponde a pacman y siempre es false)
        print "Living ghosts: ", gameState.getLivingGhosts()
        # Posicion de los fantasmas
        print "Ghosts positions: ", gameState.getGhostPositions()
        # Direciones de los fantasmas
        print "Ghosts directions: ", [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)]
        # Distancia de manhattan a los fantasmas
        print "Ghosts distances: ", gameState.data.ghostDistances
        # Puntos de comida restantes
        print "Pac dots: ", gameState.getNumFood()
        # Distancia de manhattan a la comida mas cercada
        print "Distance nearest pac dots: ", gameState.getDistanceNearestFood()
        # Paredes del mapa
        print "Map:  \n", gameState.getWalls()
        # Puntuacion
        print "Score: ", gameState.getScore()'''


    def chooseAction(self, gameState):
        self.countActions = self.countActions + 1
        self.printInfo(gameState)
                #move = Directions.STOP
        #legal = gameState.getLegalActions(0) ##Legal position from the pacman

        #Atributos de cada instancia que se quiere clasificar.
        posX = gameState.getPacmanPosition()[0]
        posY = gameState.getPacmanPosition()[1]
        north= str('North' in gameState.getLegalPacmanActions())
        south= str('South' in gameState.getLegalPacmanActions())
        east= str('East' in gameState.getLegalPacmanActions())
        west= str('West' in gameState.getLegalPacmanActions())


        pg1X= gameState.getGhostPositions()[0][0]
        pg1Y= gameState.getGhostPositions()[0][1]
        d1X =  abs(gameState.getGhostPositions()[0][0]-gameState.getPacmanPosition()[0])
        d1Y= abs(gameState.getGhostPositions()[0][1]-gameState.getPacmanPosition()[1])
        d1 = gameState.data.ghostDistances[0]
        dirg1 = str(gameState.getGhostDirections().get(0))


        pg2X= gameState.getGhostPositions()[1][0]
        pg2Y= gameState.getGhostPositions()[1][1]
        d2X = abs(gameState.getGhostPositions()[1][0]-gameState.getPacmanPosition()[0])
        d2Y=abs(gameState.getGhostPositions()[1][1]-gameState.getPacmanPosition()[1])
        d2=gameState.data.ghostDistances[1]
        dirg2 = str(gameState.getGhostDirections().get(1))

        pg3X= gameState.getGhostPositions()[2][0]
        pg3Y= gameState.getGhostPositions()[2][1]
        d3X = abs(gameState.getGhostPositions()[2][0]-gameState.getPacmanPosition()[0])
        d3Y=abs(gameState.getGhostPositions()[2][1]-gameState.getPacmanPosition()[1])
        d3=gameState.data.ghostDistances[2]
        dirg3 = str(gameState.getGhostDirections().get(2))
        df =  gameState.getDistanceNearestFood()


        pg4X= gameState.getGhostPositions()[3][0]
        pg4Y= gameState.getGhostPositions()[3][1]
        d4X = abs(gameState.getGhostPositions()[3][0]-gameState.getPacmanPosition()[0])
        d4Y=abs(gameState.getGhostPositions()[3][1]-gameState.getPacmanPosition()[1])
        d4= gameState.data.ghostDistances[3]
        dirg4 = str(gameState.getGhostDirections().get(3))

        g1g2X = abs(gameState.getGhostPositions()[0][0]-gameState.getGhostPositions()[1][0]) #Distanica entre GN
        g1g2Y = abs(gameState.getGhostPositions()[0][1]-gameState.getGhostPositions()[1][1])
        d1d2= g1g2X + g1g2Y

        g1g3X = abs(gameState.getGhostPositions()[0][0]-gameState.getGhostPositions()[2][0]) #Distanica entre GN
        g1g3Y = abs(gameState.getGhostPositions()[0][1]-gameState.getGhostPositions()[2][1])
        d1d3= g1g3X + g1g3Y

        g1g4X = abs(gameState.getGhostPositions()[0][0]-gameState.getGhostPositions()[3][0]) #Distanica entre GN
        g1g4Y = abs(gameState.getGhostPositions()[0][1]-gameState.getGhostPositions()[3][1])
        d1d4 = g1g4X + g1g4Y

        g2g3X = abs(gameState.getGhostPositions()[1][0]-gameState.getGhostPositions()[2][0]) #Distanica entre GN
        g2g3Y = abs(gameState.getGhostPositions()[1][1]-gameState.getGhostPositions()[2][1])
        d2d3 = g2g3X + g2g3Y

        g2g4X = abs(gameState.getGhostPositions()[1][0]-gameState.getGhostPositions()[3][0]) #Distanica entre GN
        g2g4Y = abs(gameState.getGhostPositions()[1][1]-gameState.getGhostPositions()[3][1])
        d2d4= g2g4X+g2g4Y

        g3g4X = abs(gameState.getGhostPositions()[2][0]-gameState.getGhostPositions()[3][0]) #Distanica entre GN
        g3g4Y = abs(gameState.getGhostPositions()[2][1]-gameState.getGhostPositions()[3][1])
        d3d4= g3g4X + g3g4Y

        score0 = gameState.getScore()






        dirpacman = str(gameState.data.agentStates[0].getDirection())

        #P1
        #x = [posX,posY, df, north,south,east,west, pg1X, pg1Y, d1X,d1Y,d1, dirg1, pg2X, pg2Y, d2X, d2Y,d2, dirg2, pg3X, pg3Y, d3X, d3Y,d3, dirg3, pg4X, pg4Y, d4X, d4Y,d4, dirg4, g1g2X, g1g2Y, d1d2, g1g3X, g1g3Y, d1d3, g1g4X, g1g4Y, d1d4, g2g3X, g2g3Y, d2d3, g2g4X, g2g4Y, d2d4, g3g4X, g3g4Y, d3d4, score0]
        #x = [posX, posY]



        #P3
        x = [posX,posY, north,south,east,west, d1X, d1Y, d1, d2X, d2Y, d2, d3X, d3Y, d3,  d4X,d4Y, d4, g1g2X,g1g2Y,d1d2, g1g3X, g1g3Y, d1d3, g1g4X, g1g4Y, d1d4, g2g3X, g2g3Y, d2d3, g2g4X, g2g4Y, d2d4, g3g4X, g3g4Y, d3d4]

        #P3.1
        #x = [posX,posY, north,south,east,west, d1X, d1Y, d1, d2X, d2Y, d2, d3X, d3Y, d3,  d4X,d4Y, d4]

        #P3.2
        #x = [posX,posY, north,south,east,west, d1, d2,  d3,  d4]

        #Para eliminar los NONE y ponerle -1 que es lo que se tienen en los .arff
        for i in range (0, len(x)):

            if x[i]==None:
                x[i] = -1
            print(x[i])


        #a = self.weka.predict("./smoP3.model", x, "./training_keyboardP3.arff")


        if a in gameState.getLegalPacmanActions():
            return a


        move = Directions.STOP
        legal = gameState.getLegalActions(0) ##Legal position from the pacman
        random_n = random.randint(0,10)
        if(random_n%2 == 0):
            move_random = random.randint(0, 3)
            if   ( move_random == 0 ) and Directions.WEST in legal:  move = Directions.WEST
            if   ( move_random == 1 ) and Directions.EAST in legal: move = Directions.EAST
            if   ( move_random == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
            if   ( move_random == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH
            return move
        else:
            move_random = random.randint(0, 3)
            if   ( move_random == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH
            if   ( move_random == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
            if   ( move_random == 1 ) and Directions.EAST in legal: move = Directions.EAST
            if   ( move_random == 0 ) and Directions.WEST in legal:  move = Directions.WEST
            return move







    def printLineData(self, gameState):

        cadena = []
        cabecera = "@RELATION pacman-data\n\n@ATTRIBUTE posX NUMERIC\n@ATTRIBUTE posY NUMERIC\n@ATTRIBUTE dFood NUMERIC\n@ATTRIBUTE North {True, False}\n@ATTRIBUTE South {True, False}\n@ATTRIBUTE East {True, False}\n@ATTRIBUTE West {True, False}\n@ATTRIBUTE DirPACMAN {North, South, East, West, Stop}\n@ATTRIBUTE Ghost1posX NUMERIC\n@ATTRIBUTE Ghost1posY NUMERIC\n@ATTRIBUTE dghost1pacmanX NUMERIC\n@ATTRIBUTE dghost1pacmanY NUMERIC\n@ATTRIBUTE dGhost1 NUMERIC\n@ATTRIBUTE DirGhost1 {North, South, East, West, Stop, -1}\n@ATTRIBUTE Ghost2posX NUMERIC\n@ATTRIBUTE Ghost2posY NUMERIC\n@ATTRIBUTE dghost2pacmanX NUMERIC\n@ATTRIBUTE dghost2pacmanY NUMERIC\n@ATTRIBUTE dGhost2 NUMERIC\n@ATTRIBUTE DirGhost2 {North, South, East, West, Stop, -1}\n@ATTRIBUTE Ghost3posX NUMERIC\n@ATTRIBUTE Ghost3posY NUMERIC\n@ATTRIBUTE dghost3pacmanX NUMERIC\n@ATTRIBUTE dghost3pacmanY NUMERIC\n@ATTRIBUTE dGhost3 NUMERIC\n@ATTRIBUTE DirGhost3 {North, South, East, West, Stop, -1}\n@ATTRIBUTE Ghost4posX NUMERIC\n@ATTRIBUTE Ghost4posY NUMERIC\n@ATTRIBUTE dghost4pacmanX NUMERIC\n@ATTRIBUTE dghost4pacmanY NUMERIC\n@ATTRIBUTE dGhost4 NUMERIC\n@ATTRIBUTE DirGhost4 {North, South, East, West, Stop, -1}\n@ATTRIBUTE dg1g2X NUMERIC\n@ATTRIBUTE dg1g2Y NUMERIC\n@ATTRIBUTE dg1g2M NUMERIC\n@ATTRIBUTE dg1g3X NUMERIC\n@ATTRIBUTE dg1g3Y NUMERIC\n@ATTRIBUTE dg1g3M NUMERIC\n@ATTRIBUTE dg1g4X NUMERIC\n@ATTRIBUTE dg1g4Y NUMERIC\n@ATTRIBUTE dg1g4M NUMERIC\n@ATTRIBUTE dg2g3X NUMERIC\n@ATTRIBUTE dg2g3Y NUMERIC\n@ATTRIBUTE dg2g3M NUMERIC\n@ATTRIBUTE dg2g4X NUMERIC\n@ATTRIBUTE dg2g4Y NUMERIC\n@ATTRIBUTE dg2g4M NUMERIC\n@ATTRIBUTE dg3g4X NUMERIC\n@ATTRIBUTE dg3g4Y NUMERIC\n@ATTRIBUTE dg3g4M NUMERIC\n@ATTRIBUTE score0 NUMERIC\n@ATTRIBUTE score1 NUMERIC\n@ATTRIBUTE score2 NUMERIC\n@ATTRIBUTE score3 NUMERIC\n\n\n@data\n"
        cadena.append(str(gameState.getPacmanPosition()[0]))
        cadena.append(str(gameState.getPacmanPosition()[1]))
        cadena.append(str(gameState.getDistanceNearestFood()))

        cadena.append(str('North' in gameState.getLegalPacmanActions()))
        cadena.append(str('South' in gameState.getLegalPacmanActions()))
        cadena.append(str('East' in gameState.getLegalPacmanActions()))
        cadena.append(str('West' in gameState.getLegalPacmanActions()))
        cadena.append(str(gameState.data.agentStates[0].getDirection()))

        for i in range(0, gameState.getNumAgents() - 1):
            cadena.append(str(gameState.getGhostPositions()[i][0]))
            cadena.append(str(gameState.getGhostPositions()[i][1]))
            cadena.append(str(abs(gameState.getGhostPositions()[i][0]-gameState.getPacmanPosition()[0]))) #Distancia X entre pacman y fantasma
            cadena.append(str(abs(gameState.getGhostPositions()[i][1]-gameState.getPacmanPosition()[1]))) #Distancia Y entre pacman y fantasma
            cadena.append(str(gameState.data.ghostDistances[i]))
            cadena.append(str(gameState.getGhostDirections().get(i)))

        for i in range(0, gameState.getNumAgents() - 1):
                j = i + 1
                while j <  gameState.getNumAgents() - 1:
                    g1gNX = abs(gameState.getGhostPositions()[i][0]-gameState.getGhostPositions()[j][0]) #Distanica entre GN
                    g1gNY = abs(gameState.getGhostPositions()[i][1]-gameState.getGhostPositions()[j][1])
                    g1gNM = g1gNX + g1gNY
                    cadena.append(str(g1gNX)) #Distancia X entre g1 y g2
                    cadena.append(str(g1gNY)) #Distancia Y entre g1 y g2
                    cadena.append(str(g1gNM)) #Distancia manhattan entre g1 y g2
                    j += 1

        cadena.append(str(gameState.getScore()))



        for n, i in enumerate(cadena):
            if i == "None":
                cadena[n] = "-1"

        estado = ", ".join(cadena)

        ponerCabecera = False
        import os.path as path
        if (not path.exists("Output.arff")):
            ponerCabecera = True


        text_file = open("Output.arff", "a")
        if(ponerCabecera):
            text_file.write(cabecera)


        self.add(estado)

        if self.size() > 4:
            text_file.write(self.score(self.pop()))
            text_file.write("\n")
            #print self.pop()



from distanceCalculator import Distancer


class BasicAgentAA(BustersAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)
    """

    def __init__(self, index = 0, inference="ExactInference", ghostAgents=None):
        "Initialize Q-values"
        inferenceType= util.lookup(inference, globals())
        self.inferenceModules = [inferenceType(a)  for a in ghostAgents]
        self.inferenceModules
        self.actions = {"North":0, "South":1, "East":2,  "West":3}
        self.table_file = open("qtable.txt", "r+")
        self.q_table = self.readQtable()
        self.epsilon = 0.0
        self.alpha = 0.0
        self.discount = 0.8
        self.lastState = None
        self.lastAction = None
        self.countActions = 0
        self.food = 0
        self.ghostPositions = None
        self.option = 1


    def readQtable(self):
	"Read qtable from disc"
        table = self.table_file.readlines()
        q_table = []

        for i, line in enumerate(table):
            row = line.split()
            row = [float(x) for x in row]
            q_table.append(row)

        return q_table

    def writeQtable(self):
	"Write qtable to disc"
        self.table_file.seek(0)
        self.table_file.truncate()

        for line in self.q_table:
            for item in line:
                self.table_file.write(str(item)+" ")
            self.table_file.write("\n")

    def __del__(self):
	"Destructor. Invokation at the end of each episode"
        self.writeQtable()
        self.table_file.close()

    def computePosition(self, state):
	"""
	Compute the row of the qtable for a given state.
	For instance, the state (3,1) is the row 7
	"""
        #d1X =  abs(state.getGhostPositions()[0][0]-state.getPacmanPosition()[0])
        #d1Y = abs(state.getGhostPositions()[0][1]-state.getPacmanPosition()[1])
        #dis = d1X + d1Y
        if self.option == 0:
            state_0 = self.dirNearGhostWallDisc(state)
            state_1 = self.dirNearFoodWallDisc(state)
            state_2 = self.distNearGhostWallDisc(state)
            state_3 = self.distNearFoodWallDisc(state)
            return state_0 + 4*state_1 + 20*state_2 + 80*state_3

        if self.option == 1:
            state_0 = self.dirNearGhostWallDisc(state)
            state_1 = self.dirNearFoodWallDisc(state)
            state_2 = 0
            if self.distNearGhostWall(state) <= self.distNearFoodWall(state):
                state_2 = 1
            return state_0 + 4*state_1 + 20*state_2




    def getQValue(self, state, action):

        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        position = self.computePosition(state)
        action_column = self.actions[action]

        return self.q_table[position][action_column]


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
     	legalActions = state.getLegalActions(0)
        if len(legalActions)==0:
          return 0
        return max(self.q_table[self.computePosition(state)])

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        legalActions = state.getLegalActions(0)
        if "Stop" in legalActions:
            legalActions.remove("Stop")

        if len(legalActions)==0:
          return "Exit"

        best_actions = [legalActions[0]]
        best_value = self.getQValue(state, legalActions[0])
        for action in legalActions:
            value = self.getQValue(state, action)
            if value == best_value:
                best_actions.append(action)
            if value > best_value:
                best_actions = [action]
                best_value = value
        return random.choice(best_actions)

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.
        """
        if self.countActions == 0:
            self.food = state.getNumFood()
            self.ghostPositions = state.getGhostPositions()


        # Pick Action
        legalActions = state.getLegalActions(0)
        if "Stop" in legalActions:
            legalActions.remove("Stop")

        action = "Exit"
        reward = 0


        if len(legalActions) == 0:
            print "NONE"
            return action

        flip = util.flipCoin(self.epsilon)

        if flip:
            action = random.choice(legalActions)
        else:
            action = self.getPolicy(state)

        reward = self.frefuerzo(state)

        if self.lastState != None:
            self.update(self.lastState, self.lastAction, state, reward)

        self.lastState = state
        self.lastAction = action
        self.countActions = self.countActions + 1

        return action


    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here
        """

        legalActionsNextState = nextState.getLegalActions(0)
        position = self.computePosition(state)
        action_column = self.actions[action]
        if len(legalActionsNextState)==0:
            #estado terminal
            self.q_table[position][action_column] = (1-self.alpha) * (self.q_table[position][action_column]) + self.alpha * (reward + 0)

        #estado no terminal.
        else:
            self.q_table[position][action_column] = (1-self.alpha) * (self.q_table[position][action_column]) + self.alpha * (reward + self.discount *  max(self.q_table[self.computePosition(nextState)]))


    def getPolicy(self, state):
	"Return the best action in the qtable for a given state"
        return self.computeActionFromQValues(state)

    def getValue(self, state):
	"Return the highest q value for a given state"
        return self.computeValueFromQValues(state)


    def frefuerzo(self, state):

        #200 puntos si consigue comerse un fantasmas
        for i in range(0, state.getNumAgents()-1):

            if state.getPacmanPosition() == self.ghostPositions[i]:
                self.ghostPositions = state.getGhostPositions()
                return 200

        #Si llega a una comida cercana entonces refuerzo 100
        if self.food > state.getNumFood():
            self.food -= 1
            return 100
        else:
            return 0


    def printLineData(self, gameState):
        "coment"


    '''Ultimo estado, se come a todos los fantasmas'''
    def final(self, state):
        reward = self.frefuerzo(state)
        if self.lastState != None:
            self.update(self.lastState, self.lastAction, state, reward)


    '''Calcula la distancia de Manhattan entre dos posiciones '''
    def manhattan (self, origin, target):
        return abs(origin[0] - target[0]) + abs(origin[1] + target [1])


    '''Comprueba si esta en un tunel'''
    def inTunnel(self, state):
        acclegales = state.getLegalActions(0)
        if len(acclegales) == 2 and ("North" in acclegales and "South" in acclegales) or ("East" in acclegales and "West" in acclegales) :
            return True
        return False


    '''Distancia Manhattan al fantasma mas cercano esquivando muros'''
    def distNearGhostWall (self, state):
        nearest_distance = 9999999
        for i in range (0, state.getNumAgents() - 1):
            if state.getLivingGhosts()[i+1]:
                distance = self.distancer.getDistance(state.getPacmanPosition(), state.getGhostPositions()[i])
                if distance[0] < nearest_distance:
                        nearest_distance = distance[0]
        #print nearest_distance
        return nearest_distance


    '''Distancia Manhattan al fantasma mas cercano esquivando muros discretizado'''
    def distNearGhostWallDisc (self, state):
        nearest_distance = self.distNearGhostWall(state)
        if nearest_distance <= 1:
            return 0
        if nearest_distance > 1 and nearest_distance <= 3:
            return 1
        if nearest_distance > 3 and nearest_distance <= 8:
            return 2
        if nearest_distance >= 8:
            return 3


    '''Distancia Manhattan a la comida mas cercana esquivando muros'''
    def distNearFoodWall (self, state):
        nearest_distance = 9999999
        width, height = state.data.layout.width, state.data.layout.height
        for i in range(0, width):
            for j in range(0, height):
                if state.data.food[i][j]:
                    distance = self.distancer.getDistance(state.getPacmanPosition(), (i, j))
                    if distance[0] < nearest_distance:
                        nearest_distance = distance[0]
        #print nearest_distance
        return nearest_distance


    '''Distancia Manhattan a la comida mas cercana esquivando muros discretizado'''
    def distNearFoodWallDisc (self, state):
        nearest_distance = self.distNearFoodWall(state)
        if nearest_distance <= 3:
            return 0
        if nearest_distance > 3 and nearest_distance <= 12:
            return 1
        if nearest_distance > 12:
            return 2


    '''Direccion Manhattan al fantasma mas cercano esquivando muros'''
    def dirNearGhostWall (self, state):
        nearest_distance = 9999999
        direccion = "Stop"
        for i in range (0, state.getNumAgents() - 1):
            if state.getLivingGhosts()[i+1]:
                distance = self.distancer.getDistance(state.getPacmanPosition(), state.getGhostPositions()[i])
                if distance[0] < nearest_distance:
                        nearest_distance = distance[0]
                        if distance[1] == "North":
                            direccion = "South"
                        elif distance[1] == "South":
                            direccion = "North"
                        elif distance[1] == "East":
                            direccion = "West"
                        elif distance[1] == "West":
                            direccion = "East"
        #print "FANTASMA EN: ", direccion
        return direccion


    '''Direccion Manhattan al fantasma mas cercano esquivando muros discretizado'''
    def dirNearGhostWallDisc (self, state):
        direction = self.dirNearGhostWall(state)
        if direction == "North":
            return 0
        if direction == "South":
            return 1
        if direction == "East":
            return 2
        if direction == "West":
            return 3


    '''Direccion Manhattan a la comida mas cercana esquivando muros'''
    def dirNearFoodWall (self, state):
        nearest_distance = 9999999
        width, height = state.data.layout.width, state.data.layout.height
        direccion = "Stop"
        for i in range(0, width):
            for j in range(0, height):
                if state.data.food[i][j]:
                    distance = self.distancer.getDistance(state.getPacmanPosition(), (i, j))
                    if distance[0] < nearest_distance:
                        nearest_distance = distance[0]
                        if distance[1] == "North":
                            direccion = "South"
                        elif distance[1] == "South":
                            direccion = "North"
                        elif distance[1] == "East":
                            direccion = "West"
                        elif distance[1] == "West":
                            direccion = "East"
        return direccion


    '''Direccion Manhattan a la comida mas cercana esquivando muros discretizado'''
    def dirNearFoodWallDisc (self, state):
        direction = self.dirNearFoodWall(state)
        if direction == "North":
            return 0
        if direction == "South":
            return 1
        if direction == "East":
            return 2
        if direction == "West":
            return 3
        if direction == "Stop":
            return 4


    '''Distancia Manhattan  al fantasma mas cercano'''
    def distNearGhost (self, state):

        nearest_distance = 9999999
        for i in range (0, state.getNumAgents() - 1):
            if state.getLivingGhosts()[i+1]:
                distance = state.data.ghostDistances[i]
                if distance < nearest_distance:
                    nearest_distance = distance
        return nearest_distance


    '''Distancia Manhattan al fantasma mas cercano discretizado '''
    def distNearGhostDisc (self, state):

        nearest_distance = self.distNearGhost(state)

        if nearest_distance <= 3:
            return 0
        if nearest_distance > 3 and nearest_distance <= 6:
            return 1
        if nearest_distance > 6 and nearest_distance <= 10:
            return 2
        if nearest_distance >= 10:
            return 3



    def positionNearestGhost(self, state):
        nearest_distance = 9999999
        nearest_position = (0, 0)
        for i in range (0, state.getNumAgents() - 1):
            if state.getLivingGhosts()[i+1]:
                distance = state.data.ghostDistances[i]
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_position = state.getGhostPositions()[i]
        return nearest_position




    def getZoneNearestGhost(self, state):

        pacmanPosition = state.getPacmanPosition()
        nearest_position = self.positionNearestGhost(state)

        if pacmanPosition[0] == nearest_position[0]:

            if nearest_position[1] > pacmanPosition[1]:
                #print "NORTE", pacmanPosition
                return 0
            else:
                #print "SUR", pacmanPosition
                return 1


        if pacmanPosition[1] == nearest_position[1]:

            if nearest_position[0] < pacmanPosition[0]:
                #print "OESTE", pacmanPosition
                return 2
            else:
                #print "ESTE", pacmanPosition
                return 3


        if pacmanPosition[0] > nearest_position[0]:

            if nearest_position[1] > pacmanPosition[1]:

                #print "NOROESTE", pacmanPosition
                return 4
            else:
                #print "SUROESTE", pacmanPosition
                return 5

        if pacmanPosition[0] < nearest_position[0]:

            if nearest_position[1] > pacmanPosition[1]:

                #print "NOR--ESTE", pacmanPosition
                return 6
            else:
                #print "SUR--ESTE", pacmanPosition
                return 7
