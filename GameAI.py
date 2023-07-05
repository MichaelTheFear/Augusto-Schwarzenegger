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

# <summary>
# Game AI Example
# </summary>
class GameAI():

    player = Position()
    state = "ready"
    dir = "north"
    score = 0
    energy = 0

    genetics = { # genes
        "attack": 30,
        "retreat": 10,
        "fitness_to_gold": 100,
        "how_much_explored": 10,
        "genome": 0b0,
        "a_estrela": 20
    }



    decisao_atual = ""
    t_pos = (-1,-1)
    decisao = ""
    obs = []
    running = False

    enemy = False # flags
    flash = False
    blocked = False
    steps = False
    breeze = False
    redlight = False
    bluelight = False
    pos = (1,1) # posicao atual


    def __init__(self, genetics):
        self.genetics = genetics
        self.mapa = Mapa(genetics["a_estrela"])
        self.decision_maker = self.run_decision() # gerador de decisão

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
    def GetObservations(self, obs):
        print("Observations: ", obs)
        for o in obs: # seta observação
            if "enemy" in o:
                self.enemy = True
            else:
                self.enemy = False
            if o=="blocked":
                self.blocked = True
            else:
                self.blocked = False
            
            if "flash" == o:
                self.flash = True
            else:
                self.flash = False
                 
            if "steps"==o:
                self.steps = True
            else:
                self.steps = False

            if "breeze"==o:
                self.breeze = True
            else:
                self.breeze = False   
        
            if "redLight"==o:
                self.redlight = True
            else:
                self.redlight = False

            if "blueLight"==o:
                self.bluelight = True
            else:
                self.bluelight = False
        


    # <summary>
    # Player position
    # </summary>
    # <returns>player position</returns>
    def GetPlayerPosition(self):
        return self.player


    # <summary>
    # No observations received
    # </summary>
    def GetObservationsClean(self):
        self.enemy = False # limpa observações
        self.flash = False
        self.blocked = False
        self.steps = False
        self.breeze = False
        self.redlight = False
        self.bluelight = False
        pass
    

    def attack_g(self):
        return self.genetics["attack"]
    
    def retreat_g(self):
        return self.genetics["retreat"]
    
    def fitness_to_gold_g(self):
        return self.genetics["fitness_to_gold"]
    
    def fitness_to_gold(self,pos): # fitness para procurar ouro
        return (self.mapa.n_blocos_explorados / 2006) * (self.get_dist_to_gold(pos))

    
    def get_dist_to_gold(self,t_pos):
        gold = self.mapa.closestGold(t_pos)
        if gold == None:
            return 1000
        if abs(gold[0] + gold[1]) == (gold[1] + gold[0]):
            return self.mapa.distance(t_pos, gold)
        return 1000

    #transforma o caminho gerado pelo a_estrela para uma lista de açoes do bot
    def gerar_comandos(self,coordenadas, direcao, coordenada_atual):
        comandos = [] # lista de comandos
        x_atual, y_atual = coordenada_atual
        dir_atual = direcao
        for coordenada in coordenadas:
            x_destino, y_destino = coordenada
            if x_destino > x_atual:
                #para o leste
                if dir_atual == "north":
                    comandos.append("virar_direita")
                    comandos.append("andar")
                elif dir_atual == "south":
                    comandos.append("virar_esquerda")
                    comandos.append("andar")
                elif dir_atual == "west":
                    comandos.append("virar_esquerda")
                    comandos.append("virar_esquerda")
                    comandos.append("andar")
                elif dir_atual == "east":
                    comandos.append("andar")

                dir_atual = "east"

            elif x_destino < x_atual:
                #para o oeste
                if dir_atual == "north":
                    comandos.append("virar_esquerda")
                    comandos.append("andar")
                elif dir_atual == "south":
                    comandos.append("virar_direita")
                    comandos.append("andar")
                elif dir_atual == "west":
                    comandos.append("andar")
                elif dir_atual == "east":
                    comandos.append("virar_esquerda")
                    comandos.append("virar_esquerda")
                    comandos.append("andar")

                dir_atual = "west"

            elif y_destino < y_atual:
                #para o norte
                if dir_atual == "north":
                    comandos.append("andar")
                elif dir_atual == "south":
                    comandos.append("virar_esquerda")
                    comandos.append("virar_esquerda")
                    comandos.append("andar")
                elif dir_atual == "west":
                    comandos.append("virar_direita")
                    comandos.append("andar")
                elif dir_atual == "east":
                    comandos.append("virar_esquerda")
                    comandos.append("andar")

                dir_atual = "north"
            elif y_destino > y_atual:
                #para o sul
                if dir_atual == "north":
                    comandos.append("virar_esquerda")
                    comandos.append("virar_esquerda")
                    comandos.append("andar")
                elif dir_atual == "south":
                    comandos.append("andar")
                elif dir_atual == "west":
                    comandos.append("virar_esquerda")
                    comandos.append("andar")
                elif dir_atual == "east":
                    comandos.append("virar_direita")
                    comandos.append("andar")

                dir_atual = "south"

        x_atual,y_atual = x_destino, y_destino
        return comandos



        
    def micro_decision(self) -> list[str]: # decisao de acao pequenas
        resp = []
        if self.bluelight or self.redlight:
            resp = ["pegar_anel"]
        elif self.blocked or self.breeze:
            return resp + self.recuar()
        elif self.enemy or self.steps:
            return resp + self.decide_atacar()
        
        return resp
        
    def macro_decision(self) -> list[str]: # decisao de acoes grandes
        return self.decisao_genetica()
    
    def behavior(self,decision) -> list[str]: # decisao de acoes grandes
        magro_game = self.micro_decision()
        if magro_game != []:
            return magro_game + decision

        return self.macro_decision()
        
    def decide_atacar(self): # decide se ataca ou foge
        self.running = True
        if self.energy > self.attack_g():
            return ["atacar","atacar","virar_direita","atacar"] 
        else:
            return self.healar()
        
    def healar(self): # I need healing (foge)
        pos = self.pos
        direcao = self.dir
        heal = self.mapa.closestPower(pos)
        caminho = None
        if pos == None:
            heal = self.mapa.get_nao_visitado_mais_proximo(pos)
            caminho = self.mapa.astar(pos, heal)
        else:
            caminho = self.mapa.astar(pos, heal)

        if caminho == None or caminho == [] or caminho == [pos]:
            return self.anda_vizinhanca(self.pos,self.dir)
            
        return self.gerar_comandos(caminho,direcao,pos)
        
    def decisao_genetica(self): # decide se procura ouro ou explora mais
        self.running = True
        pos = self.pos
        if self.fitness_to_gold(pos) > self.fitness_to_gold_g():
            print("ouro")
            return self.ao_ouro(pos)
        else:
            print("explorar")
            return self.anda_vizinhanca(self.pos,self.dir)

    def ao_ouro(self,pos): # vai ate o ouro
        self.running = True
        gold = self.mapa.closestGold(pos)
        caminho = None
        if gold == None:
            gold = self.mapa.get_nao_visitado_mais_proximo(pos)
            caminho = self.mapa.astar(pos, gold)
        else:
            caminho = self.mapa.astar(pos, gold)

        if caminho == None or caminho == [] or caminho == [pos]:
            return self.anda_vizinhanca(self.pos,self.dir)

        return self.gerar_comandos(caminho,self.dir,pos)

    def run_decision(self): # pega proxima decisao
        decision = ["andar"]
        while True:

            decision = self.behavior(decision)
            if decision == [] or decision == None:
                decision = self.anda_vizinhanca(self.pos,self.dir)

            if decision.count("pega_anel") > 1:
                decision.remove("pega_anel")
            
            if self.energy > 0:
                print(decision)
            yield decision.pop(0)
            
    
    def anda_vizinhanca(self,pos,direcao): # anda em volta
        vizinhos = self.mapa.get_vizinhanca(pos)
        if vizinhos == []:
            if random.random() < 0.2:
                return [random.choice(["virar_direita","virar_esquerda"])]
            else:
                return ["atacar"] if random.random() < 0.3 else [random.choice(["andar_re","andar"])]

        return self.gerar_comandos([vizinhos.pop(0)],direcao,pos)

    
    def recuar(self): # bater retirada
        print("rodando recuar")
        self.running = True
        pos_atual = self.pos
        direcao = self.dir
        pos_final = self.mapa.closestTeleport(pos_atual)
        caminho = None
        if pos_final == None:
            pos_final = self.mapa.get_nao_visitado_mais_proximo(pos_atual)
            caminho = self.mapa.astar(pos_atual, pos_final)
        else:
            caminho = self.mapa.astar(pos_atual, pos_final)

        if caminho == None or caminho == [] or caminho == [pos_atual]:
            return self.anda_vizinhanca(self.pos,self.dir)

        return self.gerar_comandos(caminho,direcao,pos_atual)
    

    def print_obs(self):
        obs = ""
        if self.blocked:
            obs += "blocked "
        if self.breeze:
            obs += "breeze "
        if self.flash:
            obs += "flash "
        if self.bluelight:
            obs += "bluelight "
        if self.redlight:
            obs += "redlight "
        if self.enemy:
            obs += "enemy "
        if self.steps:
            obs += "steps "
        print(self.score,obs)


    # <summary>
    # Get Decision
    # </summary>
    # <returns>command string to new decision</returns>
    def GetDecision(self):
        self.pos = (self.player.x+1 , self.player.y+1)
        self.mapa.set_obeservations(
                self.blocked,
                self.breeze,
                self.flash,
                self.bluelight,
                self.redlight,
                self.dir,
                self.pos
            )
        decisao = next(self.decision_maker)
        self.mapa.passar_tempo()
        if self.energy > 0:
            self.mapa.print_map(self.pos)
            self.print_obs()
        return decisao



