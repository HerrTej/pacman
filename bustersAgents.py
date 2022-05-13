from __future__ import print_function

import time

import layout
# from wekaI import Weka
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


from builtins import range
from builtins import object
import distanceCalculator
import util
from game import Agent
from game import Directions
from keyboardAgents import KeyboardAgent
import inference
import busters

from distanceCalculator import Distancer


class NullGraphics(object):
    "Placeholder for graphics"

    def initialize(self, state, isBlue=False):
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


class BustersAgent(object):
    "An agent that tracks and displays its beliefs about ghost positions."

    def __init__(self, index=0, inference="ExactInference", ghostAgents=None, observeEnable=True,
                 elapseTimeEnable=True):
        inferenceType = util.lookup(inference, globals())
        self.inferenceModules = [inferenceType(a) for a in ghostAgents]
        self.observeEnable = observeEnable
        self.elapseTimeEnable = elapseTimeEnable
        self.score_siguiente = 0
        self.ticks = 0
        # self.weka = Weka()
        # self.weka.start_jvm()

    def get_score_siguiente(self, score):
        self.score_siguiente = score

    def registerInitialState(self, gameState):
        "Initializes beliefs and inference modules"
        import __main__
        self.display = __main__._display
        for inference in self.inferenceModules:
            inference.initialize(gameState)
        self.ghostBeliefs = [inf.getBeliefDistribution() for inf in self.inferenceModules]
        self.firstMove = True

    def observationFunction(self, gameState):
        "Removes the ghost states from the gameState"
        agents = gameState.data.agentStates
        gameState.data.agentStates = [agents[0]] + [None for i in range(1, len(agents))]
        return gameState

    def getAction(self, gameState):
        "Updates beliefs, then chooses an action based on updated beliefs."
        # for index, inf in enumerate(self.inferenceModules):
        #    if not self.firstMove and self.elapseTimeEnable:
        #        inf.elapseTime(gameState)
        #    self.firstMove = False
        #    if self.observeEnable:
        #        inf.observeState(gameState)
        #    self.ghostBeliefs[index] = inf.getBeliefDistribution()
        # self.display.updateDistributions(self.ghostBeliefs)
        return self.chooseAction(gameState)

    def chooseAction(self, gameState):
        "By default, a BustersAgent just stops.  This should be overridden."
        self.ticks += 1
        distancer = Distancer(gameState.data.layout)
        estado_fantasmas = gameState.getLivingGhosts()[1:]
        listadedistanciafantasmas = []
        listadeposicionesfantasmas = gameState.getGhostPositions()
        posicionpacman = gameState.getPacmanPosition()
        marcador = gameState.getScore()
        numero_comidas = gameState.getNumFood()
        distancia_comida = gameState.getDistanceNearestFood()
        fantasmas_vivos = 0
        marcador_siguiente = marcador - 1
        if distancia_comida == None:
            distancia_comida = 100
        for item in estado_fantasmas:
            if item == True:
                fantasmas_vivos += 1
        for fantasmas in listadeposicionesfantasmas:
            distancia = distancer.getDistance((posicionpacman[0], posicionpacman[1]),
                                              (fantasmas[0], fantasmas[1]))
            listadedistanciafantasmas.append(distancia)
            listadedistanciafantasmas.append(distancia)
        # x = [5, 8, 4, 12, 12, 3, 3, 2, 7, -11, -12]
        x = [posicionpacman[0], posicionpacman[1], fantasmas_vivos, listadedistanciafantasmas[0],
             listadedistanciafantasmas[1], listadedistanciafantasmas[2], listadedistanciafantasmas[3],
             numero_comidas, distancia_comida, marcador, marcador_siguiente]
        # resultado = self.weka.predict("RandomForest.model", x, "training_tutorial1.arff")
        resultado = 0
        if resultado in gameState.getLegalPacmanActions():
            if resultado == "South":
                final = Directions.SOUTH
            elif resultado == "North":
                final = Directions.NORTH
            elif resultado == "West":
                final = Directions.WEST
            if resultado == "East":
                final = Directions.EAST
        else:
            lista = gameState.getLegalPacmanActions()
            lista.remove("Stop")
            aleatorio = random.choice(lista)

            if aleatorio == "South":
                final = Directions.SOUTH
            elif aleatorio == "North":
                final = Directions.NORTH
            elif aleatorio == "West":
                final = Directions.WEST
            if aleatorio == "East":
                final = Directions.EAST
        self.printInfo(gameState)
        return final
        # return Directions.STOP

    def printInfo(self, gameState):
        print("---------------- TICK ", self.ticks, " --------------------------")
        # Map size
        width, height = gameState.data.layout.width, gameState.data.layout.height
        print("Width: ", width, " Height: ", height)
        # Pacman position
        print("Pacman position: ", gameState.getPacmanPosition())
        # Legal actions for Pacman in current position
        print("Legal actions: ", gameState.getLegalPacmanActions())
        # Pacman direction
        print("Pacman direction: ", gameState.data.agentStates[0].getDirection())
        # Number of ghosts
        print("Number of ghosts: ", gameState.getNumAgents() - 1)
        # Alive ghosts (index 0 corresponds to Pacman and is always false)
        print("Living ghosts: ", gameState.getLivingGhosts())
        # Ghosts positions
        print("Ghosts positions: ", gameState.getGhostPositions())
        # Ghosts directions
        print("Ghosts directions: ",
              [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)])
        # Manhattan distance to ghosts
        print("Ghosts distances: ", gameState.data.ghostDistances)
        # Pending pac dots
        print("Pac dots: ", gameState.getNumFood())
        # Manhattan distance to the closest pac dot
        print("Distance nearest pac dots: ", gameState.getDistanceNearestFood())
        # Map walls
        print("Map:")
        print(gameState.getWalls())
        # Score
        print("Score: ", gameState.getScore())

    def printLineData(self, gameState, score, file):
        pass

    def create_states(self, gameState):
        pass


class BustersKeyboardAgent(BustersAgent, KeyboardAgent):
    "An agent controlled by the keyboard that displays beliefs about ghost positions."

    def __init__(self, index=0, inference="KeyboardInference", ghostAgents=None):
        KeyboardAgent.__init__(self, index)
        BustersAgent.__init__(self, index, inference, ghostAgents)

    def getAction(self, gameState):
        return BustersAgent.getAction(self, gameState)

    def chooseAction(self, gameState):
        return KeyboardAgent.getAction(self, gameState)


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
                if (height == True):
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
        legal = gameState.getLegalActions(0)  ##Legal position from the pacman
        move_random = random.randint(0, 3)
        if (move_random == 0) and Directions.WEST in legal:  move = Directions.WEST
        if (move_random == 1) and Directions.EAST in legal: move = Directions.EAST
        if (move_random == 2) and Directions.NORTH in legal:   move = Directions.NORTH
        if (move_random == 3) and Directions.SOUTH in legal: move = Directions.SOUTH
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
             if livingGhosts[i + 1]]
        return Directions.EAST


class BasicAgentAA(BustersAgent):

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        self.countActions = 0

    def get_score_siguiente(self, score):
        pass

    # Example of counting something
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if (height == True):
                    food = food + 1
        return food

    # Print the layout
    def printGrid(self, gameState):
        table = ""
        # print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table

    def printInfo(self, gameState):
        print("---------------- TICK ", self.countActions, " --------------------------")
        # Map size
        width, height = gameState.data.layout.width, gameState.data.layout.height
        print("Width: ", width, " Height: ", height)
        # Pacman position
        print("Pacman position: ", gameState.getPacmanPosition())
        # Legal actions for Pacman in current position
        print("Legal actions: ", gameState.getLegalPacmanActions())
        # Pacman direction
        print("Pacman direction: ", gameState.data.agentStates[0].getDirection())
        # Number of ghosts
        print("Number of ghosts: ", gameState.getNumAgents() - 1)
        # Alive ghosts (index 0 corresponds to Pacman and is always false)
        print("Living ghosts: ", gameState.getLivingGhosts())
        # Ghosts positions
        print("Ghosts positions: ", gameState.getGhostPositions())
        # Ghosts directions
        print("Ghosts directions: ",
              [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)])
        # Manhattan distance to ghosts
        print("Ghosts distances: ", gameState.data.ghostDistances)
        # Pending pac dots
        print("Pac dots: ", gameState.getNumFood())
        # Manhattan distance to the closest pac dot
        print("Distance nearest pac dots: ", gameState.getDistanceNearestFood())
        # Map walls
        print("Map:")
        print(gameState.getWalls())
        # Score
        print("Score: ", gameState.getScore())

    def chooseAction(self, gameState):
        distancer = Distancer(gameState.data.layout)
        self.countActions = self.countActions + 1
        self.printInfo(gameState)
        move = Directions.STOP
        legal = gameState.getLegalActions(0)  ##Legal position from the pacman
        posicionpacman = gameState.getPacmanPosition()
        listadefantasmas = gameState.getLivingGhosts()[1:]
        listademovimientospacman = gameState.getLegalPacmanActions()
        listadeposicionesfantasmas = gameState.getGhostPositions()
        listadistanciaspacman = []

        for fantasmas in listadeposicionesfantasmas:
            distancia = distancer.getDistance((posicionpacman[0], posicionpacman[1]),
                                              (fantasmas[0], fantasmas[1]))
            listadistanciaspacman.append(distancia)

        distancia_menor = min(listadistanciaspacman)
        fantasma_comer = listadistanciaspacman.index(distancia_menor)
        if listadefantasmas[fantasma_comer] == True:
            ubicaciondelfantasma = listadeposicionesfantasmas[fantasma_comer]

        listatotalesmov = []
        for i in listademovimientospacman:
            if i == "North":
                calculopospacmanX = gameState.getPacmanPosition()[0]
                calculopospacmanY = gameState.getPacmanPosition()[1]
                calculopospacmanY = calculopospacmanY + 1
                movimientostotales = distancer.getDistance((calculopospacmanX, calculopospacmanY),
                                                           (ubicaciondelfantasma[0], ubicaciondelfantasma[1]))
                listatotalesmov.append(movimientostotales)


            elif i == "South":
                calculopospacmanX = gameState.getPacmanPosition()[0]
                calculopospacmanY = gameState.getPacmanPosition()[1]
                calculopospacmanY = calculopospacmanY - 1
                movimientostotales = distancer.getDistance((calculopospacmanX, calculopospacmanY),
                                                           (ubicaciondelfantasma[0], ubicaciondelfantasma[1]))
                listatotalesmov.append(movimientostotales)


            elif i == "East":
                calculopospacmanX = gameState.getPacmanPosition()[0]
                calculopospacmanY = gameState.getPacmanPosition()[1]
                calculopospacmanX = calculopospacmanX + 1
                movimientostotales = distancer.getDistance((calculopospacmanX, calculopospacmanY),
                                                           (ubicaciondelfantasma[0], ubicaciondelfantasma[1]))
                listatotalesmov.append(movimientostotales)

            elif i == "West":
                calculopospacmanX = gameState.getPacmanPosition()[0]
                calculopospacmanY = gameState.getPacmanPosition()[1]
                calculopospacmanX = calculopospacmanX - 1
                movimientostotales = distancer.getDistance((calculopospacmanX, calculopospacmanY),
                                                           (ubicaciondelfantasma[0], ubicaciondelfantasma[1]))
                listatotalesmov.append(movimientostotales)

        minimodelista = min(listatotalesmov)
        contador = 0
        encontrado = False
        for i in listatotalesmov:
            if i == minimodelista and not encontrado:
                posiciondedireccion = contador
                encontrado = True
            else:
                contador += 1

        movimientofinal = listademovimientospacman[posiciondedireccion]

        if movimientofinal == "North":
            move = Directions.NORTH
        elif movimientofinal == "South":
            move = Directions.SOUTH
        elif movimientofinal == "West":
            move = Directions.WEST
        elif movimientofinal == "East":
            move = Directions.EAST

        return move

    def printLineData(self, gameState, score, file):
        distancer = Distancer(gameState.data.layout)
        estado_fantasmas = gameState.getLivingGhosts()[1:]
        listadedistanciafantasmas = []
        listadeposicionesfantasmas = gameState.getGhostPositions()
        posicionpacman = gameState.getPacmanPosition()
        marcador = gameState.getScore()
        movimiento = gameState.data.agentStates[0].getDirection()
        numero_comidas = gameState.getNumFood()
        distancia_comida = gameState.getDistanceNearestFood()
        # siguienteScore = siguiente_turno.getScore()
        siguienteScore = score
        for fantasmas in listadeposicionesfantasmas:
            distancia = distancer.getDistance((posicionpacman[0], posicionpacman[1]),
                                              (fantasmas[0], fantasmas[1]))
            listadedistanciafantasmas.append(distancia)
            listadedistanciafantasmas.append(distancia)

        if distancia_comida == None:
            distancia_comida = 100
        fantasmas_vivos = 0
        for item in estado_fantasmas:
            if item == True:
                fantasmas_vivos += 1
        contador = 0

        if movimiento != "Stop":
            for item in listadedistanciafantasmas:
                if item > 100:
                    listadedistanciafantasmas[contador] = 100
                    contador += 1
            texto = str(posicionpacman[0]) + "," + str(posicionpacman[1]) + "," + str(fantasmas_vivos) + "," + \
                    str(listadedistanciafantasmas[0]) + "," + str(listadedistanciafantasmas[1]) + "," + \
                    str(listadedistanciafantasmas[2]) + "," + str(listadedistanciafantasmas[3]) + "," + \
                    str(numero_comidas) + "," + str(distancia_comida) + "," + str(marcador) + "," + \
                    str(siguienteScore) + "," + str(movimiento)
            file.write("\n" + texto)


class QLearningAgent(BustersAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)
    """

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        self.countActions = 0
        self.actions = {"North": 0, "East": 1, "South": 2, "West": 3, "exit": 4, "Stop": 5}
        self.table_file = open("qtable.txt", "r+")
        #        self.table_file_csv = open("qtable.csv", "r+")
        self.q_table = self.readQtable()
        self.epsilon = 0.8
        self.alpha = 0.5
        self.discount = 1
        self.accumTrainRewards = 0.0
        self.accumTestRewards = 0.0
        self.episodesSoFar = 0
        self.numTraining = 100
        self.gameState = gameState
        self.legalActions = self.gameState.getLegalPacmanActions()
        numero_de_partidas = 1
        lista = sys.argv[1:]
        if "-n" in lista:
            numero_de_partidas = lista.index("-n") + 1
        # if self.episodesSoFar == 0:
        #    print('Beginning %d episodes of Training' % (int(lista[numero_de_partidas])))

    def create_initial_state(self, gameState):
        width, height = gameState.data.layout.width, gameState.data.layout.height
        zona = (width / 2, height / 2)
        distancer = Distancer(gameState.data.layout)
        listadeposicionesfantasmas = gameState.getGhostPositions()
        posicionpacman = gameState.getPacmanPosition()
        listadistanciaspacman = []

        for fantasmas in listadeposicionesfantasmas:
            distancia = distancer.getDistance((posicionpacman[0], posicionpacman[1]),
                                              (fantasmas[0], fantasmas[1]))
            listadistanciaspacman.append(distancia)

        distancia_menor = min(listadistanciaspacman)
        fantasma_comer = listadistanciaspacman.index(distancia_menor)
        posicion_fantasma_cercano = listadeposicionesfantasmas[fantasma_comer]
        comida_mas_cercana = gameState.getDistanceNearestFood()
        posicion_x_comida = 0
        posicion_y_comida = 0
        for i in range(width):
            for j in range(height):
                if gameState.hasFood(i, j):
                    posicion_x_comida = i
                    posicion_y_comida = j
        comida_mas_cercana = distancer.getDistance((posicionpacman[0], posicionpacman[1]),
                                              (posicion_x_comida, posicion_y_comida))
        posicion_pacman = gameState.getPacmanPosition()
        posicion_x_pacman = posicion_pacman[0]
        posicion_y_pacman = posicion_pacman[1]

        return posicion_fantasma_cercano, posicion_x_comida, posicion_y_comida, distancia_menor, comida_mas_cercana

    def direccion_fantasma(self, state):
        fila = 0
        posicion_pacman = state.getPacmanPosition()
        posicion_x_pacman = posicion_pacman[0]
        posicion_y_pacman = posicion_pacman[1]
        posicion_fantasma_mas_cercano = self.create_initial_state(state)[0]
        posicion_x_fantasma = posicion_fantasma_mas_cercano[0]
        posicion_y_fantasma = posicion_fantasma_mas_cercano[1]
        # norte
        if posicion_x_pacman == posicion_x_fantasma and posicion_y_pacman < posicion_y_fantasma:
            fila = 0
        # sur
        elif posicion_x_pacman == posicion_x_fantasma and posicion_y_pacman > posicion_y_fantasma:
            fila = 1
        # este
        elif posicion_x_pacman < posicion_x_fantasma and posicion_y_pacman == posicion_y_fantasma:
            fila = 2
        # oeste
        elif posicion_x_pacman > posicion_x_fantasma and posicion_y_pacman == posicion_y_fantasma:
            fila = 3
        # noreste
        elif posicion_x_pacman < posicion_x_fantasma and posicion_y_pacman < posicion_y_fantasma:
            fila = 4
        # noroeste
        elif posicion_x_pacman > posicion_x_fantasma and posicion_y_pacman < posicion_y_fantasma:
            fila = 5
        # sureste
        elif posicion_x_pacman < posicion_x_fantasma and posicion_y_pacman > posicion_y_fantasma:
            fila = 6
        # suroeste
        elif posicion_x_pacman > posicion_x_fantasma and posicion_y_pacman > posicion_y_fantasma:
            fila = 7
        return fila

    def direccion_comida(self, state):
        fila = 0
        posicion_pacman = state.getPacmanPosition()
        posicion_x_pacman = posicion_pacman[0]
        posicion_y_pacman = posicion_pacman[1]
        posicion_x_comida = self.create_initial_state(state)[1]
        posicion_y_comida = self.create_initial_state(state)[2]
        distancia_comida_mas_cercana = self.create_initial_state(state)[4]
        # norte
        if posicion_x_pacman == posicion_x_comida and posicion_y_pacman < posicion_y_comida:
            fila = 8
        # sur
        elif posicion_x_pacman == posicion_x_comida and posicion_y_pacman > posicion_y_comida:
            fila = 9
        # este
        elif posicion_x_pacman < posicion_x_comida and posicion_y_pacman == posicion_y_comida:
            fila = 10
        # oeste
        elif posicion_x_pacman > posicion_x_comida and posicion_y_pacman == posicion_y_comida:
            fila = 11
        # noreste
        elif posicion_x_pacman < posicion_x_comida and posicion_y_pacman < posicion_y_comida:
            fila = 12
        # noroeste
        elif posicion_x_pacman > posicion_x_comida and posicion_y_pacman < posicion_y_comida:
            fila = 13
        # sureste
        elif posicion_x_pacman < posicion_x_comida and posicion_y_pacman > posicion_y_comida:
            fila = 14
        # suroeste
        elif posicion_x_pacman > posicion_x_comida and posicion_y_pacman > posicion_y_comida:
            fila = 15
        return fila

    def estados_muros(self, gameState, mas_cerca):
        posicions_q_tabla_pacman = {"Norte": 0, "Sur": 1, "Este": 2, "Oeste": 3, "Noreste": 4,
                                    "Noroeste": 5, "Sureste": 6, "Suroeste": 7}
        posicion_pacman = gameState.getPacmanPosition()
        posicion_x_pacman = posicion_pacman[0]
        posicion_y_pacman = posicion_pacman[1]
        arriba = (posicion_x_pacman, posicion_y_pacman + 1)
        abajo = (posicion_x_pacman, posicion_y_pacman - 1)
        izquierda = (posicion_x_pacman - 1, posicion_y_pacman)
        derecha = (posicion_x_pacman + 1, posicion_y_pacman)
        diagonal_derecha_arriba = (posicion_x_pacman + 1, posicion_y_pacman + 1)
        diagonal_izquierda_arriba = (posicion_x_pacman - 1, posicion_y_pacman + 1)
        diagonal_derecha_abajo = (posicion_x_pacman + 1, posicion_y_pacman - 1)
        diagonal_izquierda_abajo = (posicion_x_pacman - 1, posicion_y_pacman - 1)
        muros = [arriba, abajo, izquierda, derecha, diagonal_derecha_arriba, diagonal_izquierda_arriba,
                 diagonal_derecha_abajo, diagonal_izquierda_abajo]
        donde_hay_muro = []
        devolver = False
        fantasma = self.direccion_fantasma(gameState)
        comida = self.direccion_comida(gameState)
        for item in muros:
            hay_muro = gameState.hasWall(item[0], item[1])
            donde_hay_muro.append(hay_muro)
        # techo
        if posicion_y_pacman + 1 == 10:
            techo = (posicion_x_pacman, posicion_y_pacman + 1)
            if gameState.hasWall(techo[0], techo[1]):
                donde_hay_muro[0] = False
        # suelo
        if posicion_y_pacman - 1 == 3:
            suelo = (posicion_x_pacman, posicion_y_pacman - 1)
            if gameState.hasWall(suelo[0], suelo[1]):
                donde_hay_muro[1] = False
        # pared izq
        if posicion_x_pacman - 1 == 0:
            pared = (posicion_x_pacman - 1, posicion_y_pacman)
            if gameState.hasWall(pared[0], pared[1]):
                donde_hay_muro[2] = False
        # pared derecha
        if posicion_x_pacman + 1 == 13:
            pared = (posicion_x_pacman + 1, posicion_y_pacman)
            if gameState.hasWall(pared[0], pared[1]):
                donde_hay_muro[3] = False
        prueba = False
        if True in donde_hay_muro:
            prueba = None
        print(mas_cerca)
        if prueba == None:
            if mas_cerca == "pacman":
                # muro a la derecha y fantasma en noroeste
                if donde_hay_muro[3] and fantasma == 5:
                    devolver = 20
                # muro a la derecha a fantasma noreste
                elif donde_hay_muro[4] and fantasma == 4:
                    devolver = 21
                # muro a la derecha y fantasma en sureste
                elif donde_hay_muro[3] and fantasma == 6:
                    devolver = 22
                # muro a la izquierda y fantasma en suroeste
                elif donde_hay_muro[4] and fantasma == 7:
                    devolver = 23
                # hay muro arriba, izq y diagonal dcha
                elif donde_hay_muro[0] and donde_hay_muro[4] and donde_hay_muro[2] and fantasma == 0:
                    devolver = 16
                # muro arriba, diagonal izq y a la derecha
                elif donde_hay_muro[0] and donde_hay_muro[5] and donde_hay_muro[3] and fantasma == 0:
                    devolver = 17
                # muro largo arriba y fantasma en el noreste
                elif donde_hay_muro[0] and donde_hay_muro[5] and donde_hay_muro[4] and (fantasma == 4 or fantasma == 0):
                    devolver = 18
                # muro largo arriba y fantasma en el noroeste
                elif donde_hay_muro[0] and donde_hay_muro[5] and donde_hay_muro[4] and (fantasma == 5 or fantasma == 0):
                    devolver = 19
                # hay muro abajo, izq y diagonal dcha abajo
                elif donde_hay_muro[1] and donde_hay_muro[6] and donde_hay_muro[2] and fantasma == 1:
                    devolver = 24
                # muro arriba, diagonal izq y a la derecha fantasma en el sur
                elif donde_hay_muro[1] and donde_hay_muro[7] and donde_hay_muro[3] and fantasma == 1:
                    devolver = 25
                # muro largo abajo y fantasma en el sureste
                elif donde_hay_muro[1] and donde_hay_muro[6] and donde_hay_muro[7] and (fantasma == 6 or fantasma == 1):
                    devolver = 26
                # muro largo abajo y fantasma en el suroeste
                elif donde_hay_muro[1] and donde_hay_muro[6] and donde_hay_muro[7] and (fantasma == 7 or fantasma == 1):
                    devolver = 27
                # muro izq y diagonal izquierda arriba fantasma en noroeste
                elif donde_hay_muro[2] and donde_hay_muro[5] and fantasma == 5:
                    devolver = 28
                # muro derecha y diagonal derecha arriba fantasma en noreste
                elif donde_hay_muro[3] and donde_hay_muro[4] and fantasma == 4:
                    devolver = 29
                # muro izq y diagonal izquierda abajo fantasma en suroeste
                elif donde_hay_muro[2] and donde_hay_muro[7] and fantasma == 7:
                    devolver = 29
                # muro derecha y diagonal derecha abajo fantasma en sureste
                elif donde_hay_muro[3] and donde_hay_muro[7] and fantasma == 6:
                    devolver = 30
                # muro largo izquierda fantasma noroeste
                elif donde_hay_muro[2] and fantasma == 5:
                    devolver = 31
                # muro largo derecha fantasma noreste
                elif donde_hay_muro[3] and fantasma == 4:
                    devolver = 32
                # muro largo izquierda fantasma suroeste
                elif donde_hay_muro[2] and fantasma == 7:
                    devolver = 33
                # muro largo derecha fantasma sureste
                elif donde_hay_muro[3] and fantasma == 6:
                    devolver = 34
                # muro a la derecha y fantasma al este
                elif donde_hay_muro[3] and fantasma == 2:
                    devolver = 35
                # muro a la izquierda y fantasma al este
                elif donde_hay_muro[2] and fantasma == 3:
                    devolver = 36
            elif mas_cerca == "comida":
                '''
                posicions_q_tabla_pacman = {"Norte": 8, "Sur": 9, "Este": 10, "Oeste": 11, "Noreste": 12,
                                                        "Noroeste": 13, "Sureste": 14, "Suroeste": 15}'''
                # muro a la derecha y comida en noroeste
                if donde_hay_muro[3] and comida == 13:
                    devolver = 37
                # muro a la derecha a comida noreste
                elif donde_hay_muro[4] and comida == 12:
                    devolver = 38
                # muro a la derecha y comida en sureste
                elif donde_hay_muro[3] and comida == 14:
                    devolver = 39
                # muro a la izquierda y comida en suroeste
                elif donde_hay_muro[4] and comida == 15:
                    devolver = 40
                # hay muro arriba, izq y diagonal dcha
                elif donde_hay_muro[0] and donde_hay_muro[4] and donde_hay_muro[2] and comida == 8:
                    devolver = 41
                # muro arriba, diagonal izq y a la derecha
                elif donde_hay_muro[0] and donde_hay_muro[5] and donde_hay_muro[3] and comida == 8:
                    devolver = 42
                # muro largo arriba y comida en el noreste
                elif donde_hay_muro[0] and donde_hay_muro[5] and donde_hay_muro[4] and (comida == 12 or comida == 8):
                    devolver = 43
                # muro largo arriba y comida en el noroeste
                elif donde_hay_muro[0] and donde_hay_muro[5] and donde_hay_muro[4] and (comida == 13 or comida == 8):
                    devolver = 44
                # hay muro abajo, izq y diagonal dcha abajo
                elif donde_hay_muro[1] and donde_hay_muro[6] and donde_hay_muro[2] and comida == 1:
                    devolver = 45
                # muro arriba, diagonal izq y a la derecha comida en el sur
                elif donde_hay_muro[1] and donde_hay_muro[7] and donde_hay_muro[3] and comida == 1:
                    devolver = 46
                # muro largo abajo y comida en el sureste
                elif donde_hay_muro[1] and donde_hay_muro[6] and donde_hay_muro[7] and (comida == 14 or comida == 9):
                    devolver = 47
                # muro largo abajo y comida en el suroeste
                elif donde_hay_muro[1] and donde_hay_muro[6] and donde_hay_muro[7] and (comida == 15 or comida == 9):
                    devolver = 48
                # muro izq y diagonal izquierda arriba comida en noroeste
                elif donde_hay_muro[2] and donde_hay_muro[5] and comida == 13:
                    devolver = 49
                # muro derecha y diagonal derecha arriba comida en noreste
                elif donde_hay_muro[3] and donde_hay_muro[4] and comida == 12:
                    devolver = 50
                # muro izq y diagonal izquierda abajo comida en suroeste
                elif donde_hay_muro[2] and donde_hay_muro[7] and comida == 15:
                    devolver = 51
                # muro derecha y diagonal derecha abajo comida en sureste
                elif donde_hay_muro[3] and donde_hay_muro[7] and comida == 14:
                    devolver = 52
                # muro largo izquierda comida noroeste
                elif donde_hay_muro[2] and comida == 13:
                    devolver = 53
                # muro largo derecha comida noreste
                elif donde_hay_muro[3] and comida == 12:
                    devolver = 54
                # muro largo izquierda comida suroeste
                elif donde_hay_muro[2] and comida == 15:
                    devolver = 55
                # muro largo derecha comida sureste
                elif donde_hay_muro[3] and comida == 14:
                    devolver = 56
                # muro a la derecha y comida al este
                elif donde_hay_muro[3] and comida == 10:
                    devolver = 57
                # muro a la izquierda y comida al este
                elif donde_hay_muro[2] and comida == 11:
                    devolver = 58

            '''
            muros = [arriba, abajo, izquierda, derecha, diagonal_derecha_arriba, diagonal_izquierda_arriba,
                 diagonal_derecha_abajo, diagonal_izquierda_abajo]
                 '''
        #print("Estado de muro numero -->",devolver)
        return devolver

    # ver si esta va a por comida o fantasma y luego elegir fila

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
        # self.table_file = open("qtable.txt", "r+")
        self.table_file.seek(0)
        self.table_file.truncate()
        for line in self.q_table:
            for item in line:
                self.table_file.write(str(item) + " ")
            self.table_file.write("\n")
        self.table_file.close()

    #         self.table_file_csv.seek(0)
    #         self.table_file_csv.truncate()
    #         for line in self.q_table:
    #             for item in line[:-1]:
    #                 self.table_file_csv.write(str(item)+", ")
    #             self.table_file_csv.write(str(line[-1]))
    #             self.table_file_csv.write("\n")

    def printQtable(self):
        "Print qtable"
        for line in self.q_table:
            print(line)
        print("\n")

    def __del__(self):
        "Destructor. Invokation at the end of each episode"
        self.writeQtable()
        self.table_file.close()

    def getLegalActions(self):
        return self.gameState.getLegalPacmanActions()

    def computePosition(self, gameState):
        """
        Compute the row of the qtable for a given state.
        For instance, the state (3,1) is the row 7
        """

        width, height = gameState.data.layout.width, gameState.data.layout.height
        zona = (width / 2, height / 2)
        fila = 0
        movimiento = 0
        posicion_pacman = gameState.getPacmanPosition()
        posicion_x_pacman = posicion_pacman[0]
        posicion_y_pacman = posicion_pacman[1]
        posicion_fantasma_mas_cercano = self.create_initial_state(gameState)[0]
        posicion_x_fantasma = posicion_fantasma_mas_cercano[0]
        posicion_y_fantasma = posicion_fantasma_mas_cercano[1]

        posicion_x_comida = self.create_initial_state(gameState)[1]
        posicion_y_comida = self.create_initial_state(gameState)[2]
        distancia_comida_mas_cercana = self.create_initial_state(gameState)[4]
        if distancia_comida_mas_cercana is None:
            distancia_comida_mas_cercana = 1000000000
        distancia_fantasma_mas_cercano = self.create_initial_state(gameState)[3]
        muro = True
        if distancia_fantasma_mas_cercano <= distancia_comida_mas_cercana:
            mas_cerca = "pacman"
            print(mas_cerca)
            muro = self.estados_muros(gameState, mas_cerca)
        elif distancia_fantasma_mas_cercano > distancia_comida_mas_cercana:
            mas_cerca = "comida"
            print(mas_cerca)
            muro = self.estados_muros(gameState, mas_cerca)
        if False != muro:
            fila = muro
        # if True:
        elif muro == False:
            if distancia_fantasma_mas_cercano <= distancia_comida_mas_cercana:
                # norte
                if posicion_x_pacman == posicion_x_fantasma and posicion_y_pacman < posicion_y_fantasma:
                    fila = 0
                # sur
                elif posicion_x_pacman == posicion_x_fantasma and posicion_y_pacman > posicion_y_fantasma:
                    fila = 1
                # este
                elif posicion_x_pacman < posicion_x_fantasma and posicion_y_pacman == posicion_y_fantasma:
                    fila = 2
                # oeste
                elif posicion_x_pacman > posicion_x_fantasma and posicion_y_pacman == posicion_y_fantasma:
                    fila = 3
                # noreste
                elif posicion_x_pacman < posicion_x_fantasma and posicion_y_pacman < posicion_y_fantasma:
                    fila = 4
                # noroeste
                elif posicion_x_pacman > posicion_x_fantasma and posicion_y_pacman < posicion_y_fantasma:
                    fila = 5
                # sureste
                elif posicion_x_pacman < posicion_x_fantasma and posicion_y_pacman > posicion_y_fantasma:
                    fila = 6
                # suroeste
                elif posicion_x_pacman > posicion_x_fantasma and posicion_y_pacman > posicion_y_fantasma:
                    fila = 7
            # comida mas cerca del pacman
            elif distancia_fantasma_mas_cercano > distancia_comida_mas_cercana:
                # norte
                if posicion_x_pacman == posicion_x_comida and posicion_y_pacman < posicion_y_comida:
                    fila = 8
                # sur
                elif posicion_x_pacman == posicion_x_comida and posicion_y_pacman > posicion_y_comida:
                    fila = 9
                # este
                elif posicion_x_pacman < posicion_x_comida and posicion_y_pacman == posicion_y_comida:
                    fila = 10
                # oeste
                elif posicion_x_pacman > posicion_x_comida and posicion_y_pacman == posicion_y_comida:
                    fila = 11
                # noreste
                elif posicion_x_pacman < posicion_x_comida and posicion_y_pacman < posicion_y_comida:
                    fila = 12
                # noroeste
                elif posicion_x_pacman > posicion_x_comida and posicion_y_pacman < posicion_y_comida:
                    fila = 13
                # sureste
                elif posicion_x_pacman < posicion_x_comida and posicion_y_pacman > posicion_y_comida:
                    fila = 14
                # suroeste
                elif posicion_x_pacman > posicion_x_comida and posicion_y_pacman > posicion_y_comida:
                    fila = 15
            # fantasma mas cerca del pacman

        return fila

    def getQValue(self, gameState, action):

        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        position = self.computePosition(gameState)
        action_column = self.actions[action]
        return self.q_table[int(position)][int(action_column)]

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        legalActions = state.getLegalPacmanActions()
        if len(legalActions) == 0:
            return 0
        lista = self.q_table[self.computePosition(state)]
        maximo = max(lista)
        indice = lista.index(maximo)
        movimiento_en_letras = self.get_key(indice)
        return movimiento_en_letras

    def get_key(self, val):
        for key, value in self.actions.items():
            if val == value:
                return key

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        legalActions = state.getLegalPacmanActions()
        if "Stop" in legalActions:
            legalActions.remove("Stop")
        if len(legalActions) == 0:
            return None

        best_actions = [legalActions[0]]
        best_value = self.getQValue(state, legalActions[0])
        for action in legalActions:
            value = self.getQValue(state, action)
            if value == best_value:
                best_actions.append(action)
            if value > best_value:
                best_actions = [action]
                best_value = value
        movimiento = random.choice(best_actions)
        return movimiento

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.
        """

        # Pick Action
        legalActions = state.getLegalPacmanActions()
        if "Stop" in legalActions:
            legalActions.remove("Stop")
        action = None

        if len(legalActions) == 0:
            return action

        flip = util.flipCoin(self.epsilon)

        if flip:
            movimiento = random.choice(legalActions)
            return movimiento
        return self.getPolicy(state)

    def update(self, state, action, nextState, reward):
        """
        The parent class calls this to observe a
        state = action => nextState and reward transition.
        You should do your Q-Value update here

        Good Terminal state -> reward 1
        Bad Terminal state -> reward -1
        Otherwise -> reward 0

        Q-Learning update:

        if terminal_state:
        Q(state,action) <- (1-self.alpha) Q(state,action) + self.alpha * (r + 0)
        else:
        Q(state,action) <- (1-self.alpha) Q(state,action) + self.alpha * (r + self.discount * max a' Q(nextState, a'))

        """

        # TRACE for transition and position to update. Comment the following lines if you do not want to see that trace
        # print("Update Q-table with transition: ", state, action, nextState, reward)
        # position = self.computePosition(state)
        # action_column = self.actions[action]
        # print("Corresponding Q-table cell to update:", position, action_column)

        "*** YOUR CODE HERE ***"
        estado = self.getQValue(state, action)
        position = self.computePosition(state)
        action_column = self.actions[action]
        siguiente_accion = self.computeValueFromQValues(state)
        # siguiente_accion = self.computeActionFromQValues(state)
        siguiente_estado = 0.0
        if siguiente_accion == 0:
            siguiente_accion = action
        if siguiente_accion is not None or siguiente_accion != 0:
            siguiente_estado = self.getQValue(nextState, siguiente_accion)
        if nextState.isWin():
            estado = (1 - self.alpha) * estado + self.alpha * (reward + 0)
            self.q_table[position][action_column] = estado
            self.writeQtable()
        else:
            estado = (1 - self.alpha) * estado + self.alpha * (reward + self.discount * siguiente_estado)
            self.q_table[position][action_column] = estado

        # self.q_table[self.computePosition(state)]
        # TRACE for updated q-table. Comment the following lines if you do not want to see that trace
        # print("Q-table:")
        # self.printQtable()

    def getPolicy(self, state):
        "Return the best action in the qtable for a given state"
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        "Return the highest q value for a given state"
        return self.computeValueFromQValues(state)
