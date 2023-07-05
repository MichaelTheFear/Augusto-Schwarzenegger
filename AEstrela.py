# Classe para representar um nó no mapa
import heapq
from random import randint

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # Custo do caminho do nó inicial até este nó
        self.h = 0  # Heurística (distância estimada) do nó até o nó final
        self.f = 0  # Custo total (g + h) do nó

    def __lt__(self, other):
        return self.f < other.f

#Blocks Astar

class Mapa():
    coluna = 36
    linha = 61
    goldArray = [] # x,y,cooldown
    powerArray = [] # x,y cooldown
    teleportArray = [] # x,y cooldown
    mapa =[[]] # mapa
    n_blocos_explorados = 0

    nao_visitados =[] # lista de blocos não visitados

    c_peso_bloco_inexplorado = 999 # peso de um bloco inexplorado
    ultimos_passos = [] # ultimos passos
    t_err = 0 # erro de distancia

    def __init__(self,a_estrela:int):
        #adiciona uma borda em volta do mapa
        self.c_peso_bloco_inexplorado = a_estrela
        for i in range(self.linha): # inicializa o mapa
            self.mapa.append([])
            for j in range(self.coluna):
                if i == 0 or j == 0 or i == self.linha-1 or j == self.coluna-1:
                    self.mapa[i].append("🚩")
                else:
                    self.mapa[i].append("⬛")
                    self.nao_visitados.append((i,j))

        self.BLOCKS = { # dicionario de blocos
            "🚩": float('inf'),
            "⬛": self.c_peso_bloco_inexplorado,
            "🟨": 1,
            "🟩": 1,
            "🟦": 1,
            "⬜": 1,
            }

                
        
        

    def distance(self, current_cord:tuple[int,int], goal_cord:tuple[int,int]): # distancia de manhattan
        return abs(current_cord[0] - goal_cord[0]) + abs(current_cord[1] - goal_cord[1])

    def closestGold(self, current_cord:tuple[int,int]): # pega o ouro mais proximo
        max = 999
        max_coord = (-1,-1)
        for x in self.goldArray:
            dist = self.distance(current_cord, (x[0],x[1]))
            if x[2] <= dist+self.t_err:
                if dist < max:
                    max = dist
                    max_coord = (x[0],x[1])

        return None if max_coord else max_coord
    
    def closestPower(self, current_cord:tuple[int,int]): # pega o powerup mais proximo
        max = 999
        max_coord = (-1,-1)
        for x in self.powerArray:
            dist = self.distance(current_cord, (x[0],x[1]))
            if x[2] <= dist+self.t_err:
                if dist < max:
                    max = dist
                    max_coord = (x[0],x[1])

        return None if max_coord else max_coord
    
    def closestTeleport(self, current_cord:tuple[int,int]): # pega o teleport mais proximo
        max = 999
        max_coord = (-1,-1)
        for x in self.teleportArray:
            dist = self.distance(current_cord, (x[0],x[1]))
            if dist < max:
                max = dist
                max_coord = (x[0],x[1])

        return None if max_coord else max_coord
    
    def remove_nao_visitado(self, pos:tuple[int,int]): # remove um bloco da lista de nao visitados
        try:
            self.nao_visitados.remove(pos)
        except ValueError:
            pass
    
    def get_nao_visitado_aleatorio(self): # pega um bloco aleatorio da lista de nao visitados
        return self.nao_visitados[randint(0,len(self.nao_visitados)-1)] if len(self.nao_visitados) > 0 else (-1,-1)
    
    def get_nao_visitado_mais_proximo(self, pos:tuple[int,int]): # pega o bloco nao visitado mais proximo
        min = 999
        min_coord = (-1,-1)
        for x in self.nao_visitados:
            dist = self.distance(pos, x)
            if dist < min:
                min = dist
                min_coord = x

        return min_coord
    
    def get_vizinhanca(self, pos:tuple[int,int]): # pega a vizinhanca valida de um bloco
        vizinhanca = []


        if self.mapa[pos[0]-1][pos[1]] == "⬛":
            vizinhanca.append((pos[0]-1,pos[1]))
        if self.mapa[pos[0]+1][pos[1]] == "⬛":
            vizinhanca.append((pos[0]+1,pos[1]))
        if self.mapa[pos[0]][pos[1]-1] == "⬛":
            vizinhanca.append((pos[0],pos[1]-1))
        if self.mapa[pos[0]][pos[1]+1] == "⬛":
            vizinhanca.append((pos[0],pos[1]+1))
        return vizinhanca
    


    def set_obeservations(self,blocked,breeze,flash,bluelight,redlight,direction,pos):
        # atualiza o mapa com as observações

        if self.mapa[pos[0]][pos[1]] == "⬛" or self.mapa[pos[0]][pos[1]] == "⬜":

            self.mapa[pos[0]][pos[1]] = "⬜"
            if self.mapa[pos[0]][pos[1]] == "⬛":
                self.remove_nao_visitado((pos[0],pos[1]))

            if bluelight == True: # se tiver luz azul, pode ser gold
                self.mapa[pos[0]][pos[1]] = "🟨"
                self.goldArray.append((pos[0],pos[1],10))
            if redlight == True:
                self.mapa[pos[0]][pos[1]] = "🟩" # se tiver luz vermelha, pode ser power
                self.powerArray.append((pos[0],pos[1],10))
            if flash == True:
                self.mapa[pos[0]][pos[1]] = "🟦"
                self.teleportArray.append((pos[0],pos[1]))
            
            
            self.n_blocos_explorados += 1

        #caso formos bloqueados, posicionamos uma flag na frente do bot
        if blocked == True:
            print("blocked")
            try:
                if direction == "west":
                    self.mapa[pos[0]-1][pos[1]] = "🚩"
                    self.remove_nao_visitado((pos[0]-1,pos[1]))
                elif direction == "east":
                    self.mapa[pos[0]+1][pos[1]] = "🚩"
                    self.remove_nao_visitado((pos[0]+1,pos[1]))
                elif direction == "south":
                    self.mapa[pos[0]][pos[1]+1] = "🚩"
                    self.remove_nao_visitado((pos[0],pos[1]+1))
                elif direction == "north":
                    self.mapa[pos[0]][pos[1]-1] = "🚩"
                    self.remove_nao_visitado((pos[0],pos[1]-1))

            except IndexError:
                pass

        
        if breeze == True:
            try: 
                # se tiver brisa, os blocos ao redor podem ser buracos
                # caso ja estejam sabemos o que eh, ignoramos
                if self.mapa[pos[0]][pos[1]+1] == "⬛":
                    self.mapa[pos[0]][pos[1]+1] = "🚩"
                    self.remove_nao_visitado((pos[0],pos[1]+1))
                    
                if self.mapa[pos[0]][pos[1]-1] == "⬛":
                    self.mapa[pos[0]][pos[1]-1] = "🚩"
                    self.remove_nao_visitado((pos[0],pos[1]-1))
                    
                if self.mapa[pos[0]+1][pos[1]] == "⬛":
                    self.mapa[pos[0]+1][pos[1]] = "🚩"
                    self.remove_nao_visitado((pos[0]+1,pos[1]))
                    
                if self.mapa[pos[0]-1][pos[1]] == "⬛":
                    self.mapa[pos[0]-1][pos[1]] = "🚩"
                    self.remove_nao_visitado((pos[0]-1,pos[1]))
                    
                    
            except IndexError:
                pass
        
    
    # Valores dos blocos
    # ∎ = self.c_peso_bloco_inexplorado
    # ∙ = 1
    # 🚩 = infito
    


    # Função para encontrar o caminho usando o algoritmo A*
    def astar(self,start, end):
        if end == None:
            return None
        open_list = []
        closed_set = set()

        # Criar nós inicial e final
        start_node = Node(start)
        end_node = Node(end)

        # Adicionar o nó inicial na lista de nós abertos
        heapq.heappush(open_list, start_node)

        # Loop principal
        while open_list:
            # Obter o nó com menor custo total (f) da lista de nós abertos
            current_node = heapq.heappop(open_list)

            # Verificar se o nó atual é o nó final
            if current_node.position == end_node.position:
                path = []
                while current_node:
                    path.append(current_node.position)
                    current_node = current_node.parent
                path.pop()
                return path[::-1]

            # Adicionar o nó atual ao conjunto de nós fechados
            closed_set.add(current_node)

            # Gerar os nós vizinhos
            neighbors = []
            for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor_position = (current_node.position[0] + move[0], current_node.position[1] + move[1])

                # Verificar se o vizinho está dentro dos limites do mapa
                if (0 <= neighbor_position[0] < len(self.mapa)) and (0 <= neighbor_position[1] < len(self.mapa[0])):
                    try:
                        if self.mapa[neighbor_position[0]][neighbor_position[1]] != '🚩':
                            neighbor_node = Node(neighbor_position, current_node)
                            neighbors.append(neighbor_node)
                    except:
                        print(neighbor_position)

            # Calcular os custos e atualizar os nós vizinhos
            for neighbor in neighbors:
                # Calcular o custo do caminho até o vizinho
                neighbor.g = current_node.g + self.BLOCKS[self.mapa[neighbor.position[0]][neighbor.position[1]]]

                # Calcular a heurística (distância estimada) do vizinho até o nó final
                neighbor.h = self.distance(neighbor.position, end_node.position)

                # Calcular o custo total (g + h) do vizinho
                neighbor.f = neighbor.g + neighbor.h

                # Verificar se o vizinho já está na lista de nós abertos ou fechados
                if neighbor in closed_set:
                    continue

                # Verificar se o vizinho tem um custo de caminho menor do que outros caminhos já encontrados
                if any(neighbor.position == node.position and neighbor.g >= node.g for node in open_list):
                    continue

                # Adicionar o vizinho à lista de nós abertos
                heapq.heappush(open_list, neighbor)



        
    def passar_tempo(self): # passa o tempo e diminui o tempo dos blocos
        for x in self.goldArray:
            x = (x[0],x[1],x[2]-1)
        for x in self.powerArray:
            x = (x[0],x[1],x[2]-1)
    
    def resetGold(self,pos): # reseta o tempo do bloco
        for x in self.goldArray:
            if x[0] == pos[0] and x[1] == pos[1]:
                x = (x[0],x[1],15)
                break
    
    def resetPower(self,pos): # reseta o tempo do bloco
            for x in self.powerArray:
                if x[0] == pos[0] and x[1] == pos[1]:
                    x = (x[0],x[1],15)
                    break

    def print_map(self,pos):
        #transform to a string
        mapa_str = ""
        for (ix,x) in enumerate(self.mapa):
            for (iy,y) in enumerate(x):
                if (ix,iy) == pos:
                    mapa_str += "🤖" # printa o robo
                else:
                    mapa_str += y
            mapa_str += "\n"
        print(mapa_str)
    
    def clear_map(self):
        for i in range(self.linha):
            self.mapa.append([])
            for j in range(self.coluna):
                if i == 0 or j == 0 or i == self.linha-1 or j == self.coluna-1:
                    self.mapa[i].append("🚩")
                else:
                    self.mapa[i].append("⬛")

        self.teleportArray = []
        self.goldArray = []
        self.powerArray = []
        self.n_blocos_explorados = 0
