# keyboardAgents.py
# -----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley.
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import Agent
from game import Directions
from distanceCalculator import Distancer
from game import GameStateData
import random


##Isa
import sys


class KeyboardAgent(Agent):
   # NOTE: Arrow keys also work.
    WEST_KEY  = 'a'
    EAST_KEY  = 'd'
    NORTH_KEY = 'w'
    SOUTH_KEY = 's'
    STOP_KEY = 'q'

    def __init__( self, index = 0 ):

        self.lastMove = Directions.STOP
        self.index = index
        self.keys = []

    def getAction( self, state):
        from graphicsUtils import keys_waiting
        from graphicsUtils import keys_pressed
        keys = keys_waiting() + keys_pressed()
        if keys != []:
            self.keys = keys

        legal = state.getLegalActions(self.index)
        move = self.getMove(legal)

        if move == Directions.STOP:
            # Try to move in the same direction as before
            if self.lastMove in legal:
                move = self.lastMove

        if (self.STOP_KEY in self.keys) and Directions.STOP in legal: move = Directions.STOP

        if move not in legal:
            move = random.choice(legal)

        self.lastMove = move
        return move

    def getMove(self, legal):
        move = Directions.STOP
        if   (self.WEST_KEY in self.keys or 'Left' in self.keys) and Directions.WEST in legal:  move = Directions.WEST
        if   (self.EAST_KEY in self.keys or 'Right' in self.keys) and Directions.EAST in legal: move = Directions.EAST
        if   (self.NORTH_KEY in self.keys or 'Up' in self.keys) and Directions.NORTH in legal:   move = Directions.NORTH
        if   (self.SOUTH_KEY in self.keys or 'Down' in self.keys) and Directions.SOUTH in legal: move = Directions.SOUTH
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








