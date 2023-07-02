#!/usr/bin/env python

"""GameAI.py: INF1771 GameAI File - Where Decisions are made."""
#############################################################
#Copyright 2020 Augusto Baffa
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#############################################################
__author__      = "Augusto Baffa"
__copyright__   = "Copyright 2020, Rio de janeiro, Brazil"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "abaffa@inf.puc-rio.br"
#############################################################

import random
from Map.Position import Position

# <summary>
# Game AI Example
# </summary>
class GameAI():

    player = Position()
    state = "ready"
    dir = "north"
    score = 0
    energy = 0

    redLight = False
    greenLight = False
    blueLight = False
    blocked = False
    steps = False
    flash = False
    breeze = False


    genetics = {
        "attack": 0,
        "retreat": 0,
        "fitness_to_gold": 0,
        "how_much_explored": 0,
        "genome": 0b0
    }

    n_blocos_explorados = 0

    virado = False

    energias = []
    pocos = []
    ouro = []
    tps = []
    
    def __init__(self, genetics):
        self.genetics = genetics

    # <summary>
    # Refresh player status
    # </summary>
    # <param name="x">player position x</param>
    # <param name="y">player position y</param>
    # <param name="dir">player direction</param>
    # <param name="state">player state</param>
    # <param name="score">player score</param>
    # <param name="energy">player energy</param>
    def SetStatus(self, x, y, dir, state, score, energy):
    
        self.player.x = x
        self.player.y = y
        self.dir = dir.lower()

        self.state = state
        self.score = score
        self.energy = energy


    # <summary>
    # Get list of observable adjacent positions
    # </summary>
    # <returns>List of observable adjacent positions</returns>
    def GetObservableAdjacentPositions(self):
        ret = []

        ret.append(Position(self.player.x - 1, self.player.y))
        ret.append(Position(self.player.x + 1, self.player.y))
        ret.append(Position(self.player.x, self.player.y - 1))
        ret.append(Position(self.player.x, self.player.y + 1))

        return ret


    # <summary>
    # Get list of all adjacent positions (including diagonal)
    # </summary>
    # <returns>List of all adjacent positions (including diagonal)</returns>
    def GetAllAdjacentPositions(self):
    
        ret = []

        ret.Add(Position(self.player.x - 1, self.player.y - 1))
        ret.Add(Position(self.player.x, self.player.y - 1))
        ret.Add(Position(self.player.x + 1, self.player.y - 1))

        ret.Add(Position(self.player.x - 1, self.player.y))
        ret.Add(Position(self.player.x + 1, self.player.y))

        ret.Add(Position(self.player.x - 1, self.player.y + 1))
        ret.Add(Position(self.player.x, self.player.y + 1))
        ret.Add(Position(self.player.x + 1, self.player.y + 1))

        return ret
    

    # <summary>
    # Get next forward position
    # </summary>
    # <returns>next forward position</returns>
    def NextPosition(self):
    
        ret = None
        
        if self.dir == "north":
            ret = Position(self.player.x, self.player.y - 1)
                
        elif self.dir == "east":
                ret = Position(self.player.x + 1, self.player.y)
                
        elif self.dir == "south":
                ret = Position(self.player.x, self.player.y + 1)
                
        elif self.dir == "west":
                ret = Position(self.player.x - 1, self.player.y)

        return ret
    

    # <summary>
    # Player position
    # </summary>
    # <returns>player position</returns>
    def GetPlayerPosition(self):
        return self.player


    # <summary>
    # Set player position
    # </summary>
    # <param name="x">x position</param>
    # <param name="y">y position</param>
    def SetPlayerPosition(self, x, y):
        self.player.x = x
        self.player.y = y

    

    # <summary>
    # Observations received
    # </summary>
    # <param name="o">list of observations</param>
    def GetObservations(self, o):
        #cmd = "";
        for s in o:
        
            if s == "blocked":
                self.blocked = True
                pass
            
            elif s == "steps":
                self.steps = True
                pass
            
            elif s == "breeze":
                self.breeze = True
                pass

            elif s == "flash":
                self.flash = True
                pass

            elif s == "blueLight":
                self.blueLight = True
                pass

            elif s == "redLight":
                self.redLight = True
                pass

            elif s == "greenLight":
                self.greenLight = True
                pass

            elif s == "weakLight":
                self.weakLight = True
                pass


    # <summary>
    # No observations received
    # </summary>
    def GetObservationsClean(self):
        pass
    

    def attack_g(self):
        return 50
        
    
    def retreat_g(self):
        return 50
    
    def fitness_to_gold_g(self):
        return 50
    def fitness_to_gold(self):
        # considerando que o maximo de distancia possivel eh 100
        # e que o maximo de blocos explorado eh 59 x 34 = 2006
        # retorno deve ser de 0 a 100

        return (self.n_blocos_explorados / 2006) * (self.get_dist_to_gold())

    
    def get_dist_to_gold(self):
        return 0

    # <summary>
    # Get Decision
    # </summary>
    # <returns>command string to new decision</returns>
    def GetDecision(self):
        if self.breeze:
            self.retirada()
        elif self.flash or self.steps:
            if self.energy > self.attack_g():
                self.ataque()
            else:
                self.retirada()
        elif self.energy < self.retreat_g():
            self.retirada()
        elif self.fitness_to_gold() < self.fitness_to_gold_g():
            self.explora()
        else:
            self.ao_ouro()

    def explora(self):
        if self.virado:
            self.virado = False
            self.decisao = "andar"
        else:
            if random.random() > 0.3:
                self.decisao = "andar" if random.random() > 0.1 else "atacar"
            else:
                self.virado = True
                self.decisao = "virar_direita" if random.random() > 0.5 else "virar_esquerda"

    def retirada(self):
        self.explora()
    
    def ataque(self):
        self.explora()
    
    def retornar(self):
        self.explora()

    def ao_ouro(self):
        self.explora()
    
