#!/usr/bin/env python

"""PlayerInfo.py: INF1771 Data structure to describe another players."""
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

from enum import Enum 

'''Player Direction Type'''
class Direction(Enum):
    north = 1 # Direction North
    east = 2 # Direction East
    south = 3 # Direction South
    west = 4 # Direction West

'''Player State Type'''
class State(Enum):
    ready = 1 # Player is Ready
    game = 2 # Player in Game
    dead = 3 # Player is Dead
    gameover = 4 # Player Gameover

''' Player Information '''
class PlayerInfo():

    node = -1 # Player node id
    name = "" # Player name
    x, y = -1, -1  # Player position x, y

    '''Player direction (north,south, east or west)'''
    dir = Direction.north
    
    '''Player state (ready, game, dead or gameover)'''
    state = State.ready
    
    '''Player color (R, G, B)'''
    color = (0,0,0)
        
    # Create a new PlayerInfo DTO
    #################################
    # <param name="node">Player  node id</param>
    # <param name="name">Player name</param>
    # <param name="x">Player position x</param>
    # <param name="y">Player position y</param>
    # <param name="dir">Player direction (north, southk, east or west)</param>
    # <param name="state">Player state (ready, game, dead or gameover)</param>
    # <param name="color">Player color (R, G, B)</param>
    def __init__(self, node, name, x, y, dir, state, color):
        self.node = node
        self.name = name
        self.x = x
        self.y = y
        self.dir = dir
        self.state = state
        self.color = color
