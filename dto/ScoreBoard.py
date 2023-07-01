#!/usr/bin/env python

"""Position.py: INF1771 Data structure to describe positions."""
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

# <summary>
# Score Board Class
# </summary>
class ScoreBoard():

    # <summary>
    # Player name
    # </summary>
    name = ""

    # <summary>
    # Is player still connected?
    # </summary>
    connected = False

    # <summary>
    # Player score
    # </summary>
    score = 0

    # <summary>
    # Player energy
    # </summary>
    energy = 0

    # <summary>
    # Player color (R, G, B)
    # </summary>
    color = (0, 0, 0)


    # <summary>
    # Create a scoreboard DTO
    # </summary>
    # <param name="name">Player name</param>
    # <param name="connected">Is player still connected?</param>
    # <param name="score">Player score</param>
    # <param name="energy">Player energy</param>
    # <param name="color">Player color</param>
    def __init__(self, name, connected, score, energy, color):
        self.name = name
        self.connected = connected
        self.score = score
        self.energy = energy
        self.color = color

