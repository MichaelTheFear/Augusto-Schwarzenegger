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
from AEstrela import Mapa
from Endgame import EndGame

# <summary>
# Game AI Example
# </summary>
class GameAI():

    player = Position()
    state = "ready"
    dir = "north"
    score = 0
    energy = 1

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
        "genome": 0b0,
        "a_estrela": 0
    }

    observacoes = {
            "blocked": False,
            "breeze": False,
            "power": False,
            "gold": False,
            "inimigo": False,
            "teleport": False,
            "pos" : (-1,-1),
            "dir": dir
        }
    
    override = {
        "flag": False,
        "caminho": []
    }

    acoes = []
    flag = False
    virado = False
    n_blocos_explorados = 1
    
    def get_ultimos_passos(self):
        return [x for x in self.acoes if x != "atacar"]
    
    def insert_acao(self, acao):
        self.acoes.insert(0, acao)
        if len(self.acoes) > 7:
            self.acoes.pop()

    def __init__(self, genetics):
        self.genetics = genetics
        self.mapa = Mapa(genetics["a_estrela"])

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
        self.observacoes = {
            "blocked": False,
            "breeze": False,
            "power": False,
            "gold": False,
            "inimigo": False,
            "teleport": False,
            "pos" : (-1,-1),
            "dir": self.dir
        }
        for s in o:
        
            if s == "blocked":
                self.blocked = True
                self.observacoes["blocked"] = True
                pass
            
            elif s == "steps":
                self.steps = True
                pass
            
            elif s == "breeze":
                self.breeze = True
                self.observacoes["breeze"] = True
                pass

            elif s == "flash":
                self.observacoes["teleport"] = True
                self.flash = True
                pass

            elif s == "blueLight":
                self.blueLight = True
                self.observacoes["gold"] = True
                pass

            elif s == "redLight":
                self.redLight = True
                self.observacoes["power"] = True
                pass

            elif s == "greenLight":
                self.greenLight = True
                pass

            elif s == "weakLight":
                self.weakLight = True
                pass
            elif "enemy" in s:
                self.observacoes["inimigo"] = True



    # <summary>
    # No observations received
    # </summary>
    def GetObservationsClean(self):
        pass
    

    def attack_g(self):
        return self.genetics["attack"]
    
    def retreat_g(self):
        return self.genetics["retreat"]
    
    def fitness_to_gold_g(self):
        return self.genetics["fitness_to_gold"]
    
    def fitness_to_gold(self):
        # considerando que o maximo de distancia possivel eh 100
        # e que o maximo de blocos explorado eh 59 x 34 = 2006
        # retorno deve ser de 0 a 100
        
        return (self.n_blocos_explorados / 2006) * (self.get_dist_to_gold())

    
    def get_dist_to_gold(self):
        pos = self.GetPlayerPosition()
        t_pos = (pos.x +1, pos.y+1)
        gold = self.mapa.closestGold(t_pos)
        if abs(gold[0] + gold[1]) == (gold[1] + gold[0]):
            return self.mapa.distance(t_pos, gold)
        return 1000

    # <summary>
    # Get Decision
    # </summary>
    # <returns>command string to new decision</returns>
    def GetDecision(self):
        
        self.ratio = 0.1
        posicao = self.GetPlayerPosition()
        t_pos = (posicao.x +1, posicao.y+1)
        self.observacoes["pos"] = t_pos
        self.mapa.set_obeservations(self.observacoes)
        decisao_atual = ""
        if self.observacoes["inimigo"]:
            self.decisao = "atacar"
            decisao_atual = "atacar"
        elif self.override["flag"]:
            self.proximo_passo()
            self.flag = False
            decisao_atual = "continuar"
        elif (self.observacoes["gold"] or self.observacoes["power"]) and not self.flag:
            self.decisao = "pegar_anel"
            self.flag = True
            decisao_atual = "pegar_anel"
            self.override["flag"] = False
            if self.observacoes["gold"]:
                self.mapa.resetGold(t_pos)
            elif self.observacoes["power"]:
                self.mapa.resetPower(t_pos)
        elif self.observacoes["blocked"]:
            self.retornar(t_pos)
            self.flag = False
            decisao_atual = "retornar"
            self.override["flag"] = False
        else:
            self.flag = False
            self.override["flag"] = False
            if self.breeze: #caso sentir uma brisa
                self.retornar(t_pos) #retornar pelo caminho que veio
                decisao_atual = "retornar_arvore"
            elif self.steps:
                if self.energy > self.attack_g():
                    self.ratio = 0.5
                    self.explora()
                    decisao_atual = "explorar_arvore"
                else:
                    self.retirada(t_pos)
                    decisao_atual = "retirada_arvore"
            elif self.energy < self.retreat_g():
                self.assistencia()
                decisao_atual = "assistencia_arvore"
            elif self.fitness_to_gold() < self.fitness_to_gold_g():
                self.explora()
                decisao_atual = "explorar_arvore"
            else:
                self.ao_ouro(t_pos)
                decisao_atual = "ao_ouro_arvore"
                
        if self.energy >0:
            obs = ""
            obs+= self.decisao+ " " + decisao_atual + " "
            if self.observacoes["blocked"]:
                obs += "blocked "
            if self.observacoes["breeze"]:
                obs += "breeze "
            if self.observacoes["power"]:
                obs += "power "
            if self.observacoes["gold"]:
                obs += "gold "
            
            self.mapa.print_map(t_pos)
            

        self.observacoes ={
            "blocked": False,
            "breeze": False,
            "power": False,
            "gold": False,
            "inimigo": False,
            "teleport": False,
            "dir": self.dir,
            "pos" : (-1,-1)
        }
        
        self.insert_acao(self.decisao)
        self.mapa.passar_tempo()
        
        return self.decisao


    def explora(self):
        if random.random() > 0.3:
            self.decisao = "andar" if random.random() > self.ratio else "atacar"
        else:
            self.virado = True
            self.decisao = "virar_direita" if random.random() > 0.5 else "virar_esquerda"

    def retirada(self,pos):
        x,y = self.mapa.closestTeleport(pos)
        if x == -1 or y == -1:
            self.assistencia()
            return
        else:
            self.override = {
                "flag" : True,
                "caminho": self.mapa.astar(pos,(x,y))
            }
            self.proximo_passo()

        

    def assistencia(self):
        pos = self.GetPlayerPosition()
        pos = (pos.x+1,pos.y+1)
        x,y = self.mapa.closestPower(pos)
        if x == -1 or y == -1:
            self.explora()
            return
        else:
            caminho = self.mapa.astar(pos,(x,y))
            if caminho == None or caminho == []:
                self.explora()
                return
            else:
                caminho = caminho
                self.override = {
                    "flag" : True,
                    "caminho": caminho
                }
                self.proximo_passo()
        
    
    
    def retornar(self,pos): 
        x,y = self.mapa.get_nao_visitado_mais_proximo(pos)
        if x+y == abs(x+y):
            self.override = {
                "flag" : True,
                "caminho": self.mapa.astar(pos,(x,y))
            }
            self.proximo_passo()

    def ultimos_passos(self):
        return self.ultimos_passos
        

    def ao_ouro(self,pos):
        x,y = self.mapa.closestGold(pos)
        if x == -1 or y == -1:
            self.explora()
            return
        else:
            caminho = self.mapa.astar(pos,(x,y))
            if caminho == None or caminho == []:
                self.explora()
                return
            else:
                caminho = caminho
                self.override = {
                    "flag" : True,
                    "caminho": caminho
                }
        self.proximo_passo()

    
    def genome(self):
        return self.genetics["genome"]


    def proximo_passo(self):
        if self.override["flag"]:
            caminho = self.override["caminho"]
            if caminho == None or caminho == []:
                self.override["flag"] = False
                self.explora()
            else:
                proximo = caminho.pop()
                pos = self.GetPlayerPosition()
                x = pos.x + 1
                y = pos.y + 1
                if proximo == (x,y+1): #subir
                    if self.dir == 'south':
                        self.decisao = "andar"
                    elif self.dir == 'west':
                        self.decisao = "virar_direita"
                    else:
                        self.decisao = "virar_esquerda"
                elif proximo == (x,y-1): #descer
                    if self.dir == 'north':
                        self.decisao = "andar"
                    elif self.dir == 'west':
                        self.decisao = "virar_esquerda"
                    else:
                        self.decisao = "virar_direita"
                elif proximo == (x+1,y): #direita
                    if self.dir == 'west':
                        self.decisao = "andar"
                    elif self.dir == 'north':
                        self.decisao = "virar_direita"
                    else:
                        self.decisao = "virar_esquerda"
                elif proximo == (x-1,y): #esquerda
                    if self.dir == 'east':
                        self.decisao = "andar"
                    elif self.dir == 'north':
                        self.decisao = "virar_esquerda"
                    else:
                        self.decisao = "virar_direita"
                else:
                    self.override["flag"] = False
                    self.explora()
                # tem que levar em cosideracao o self.dir e a prox posicao
                
                

        

                
            

    
