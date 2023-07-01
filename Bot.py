#!/usr/bin/env python

"""Bot.py: INF1771 Bot Class."""
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

from threading import Timer
from GameAI import GameAI
import Socket.HandleClient
from Socket.HandleClient import HandleClient
from dto.PlayerInfo import PlayerInfo
from dto.ScoreBoard import ScoreBoard
import datetime

# <summary>
# Bot Class
# </summary>
class Bot():

    name = "INF1771 Bot Example1" # BOT NAME
    host = "atari.icad.puc-rio.br" # SERVER

    client = None
    gameAi = None
    timer1 = None
    
    running = True
    thread_interval = 1 # USE BETWEEN 0.1 and 1 (0.1 real setting, 1 debug settings and makes the bot slower)

    playerList = {} #new Dictionary<long, PlayerInfo>
    shotList = [] #new List<ShotInfo>
    scoreList = [] #List<ScoreBoard>
    time = 0

    gameStatus = ""
    sscoreList = ""

    msg = []
    msgSeconds = 0

    # <summary>
    # Bot Constructor
    # </summary>
    def __init__(self):

        self.client = HandleClient()
        self.gameAi = GameAI()

        # duration is in seconds
        self.timer1 = Timer(self.thread_interval, self.timer1_Tick)

        self.client.append_cmd_handler(self.ReceiveCommand)
        self.client.append_chg_handler(self.SocketStatusChange)

        self.client.connect(self.host)
        self.timer1.start()

    
    def convertFromString(self, c):

        c = c.replace('[','')
        c = c.replace(']','')
        p = c.split(',')

        #A = int(p[0][((p[0].find('=')) + 1):])
        R = int(p[1][((p[1].find('=')) + 1):])
        G = int(p[2][((p[2].find('=')) + 1):])
        B = int(p[3][((p[3].find('=')) + 1):])

        return (R, G, B)
    
    # <summary>
    # Receive Command From TCP Client
    # </summary>
    # <param name="sender">Sender object</param>
    # <param name="args">Event arguments</param>
    def ReceiveCommand(self, cmd):

        if len(cmd) > 0:
            try:
                ######################################################        

                if cmd[0] ==  "o":
                    
                    if len(cmd) > 1:
                    
                        if cmd[1].strip() == "":
                            self.gameAi.GetObservationsClean()

                        else:
                       
                            o = []

                            if cmd[1].find(",") > -1:
                            
                                os = cmd[1].split(',')
                                for i in range(0,len(os)):
                                    o.append(os[i])
                            
                            else:
                                o.append(cmd[1])

                            self.gameAi.GetObservations(o)
                        
                    else:
                        self.gameAi.GetObservationsClean()
                    
                ######################################################        

                elif cmd[0] ==  "s":
                    if len(cmd) > 1:
                    
                        self.gameAi.SetStatus(int(cmd[1]),
                                            int(cmd[2]),
                                            cmd[3],
                                            cmd[4],
                                            int(cmd[5]),
                                            int(cmd[6]))
                    
                ######################################################        

                elif cmd[0] == "player":
                    #lock (playerList)
                    
                    if len(cmd) == 8:
                        if int(cmd[1]) not in self.playerList:
                            self.playerList.append(int(cmd[1]), 
                                PlayerInfo(
                                    int(cmd[1]),
                                    cmd[2],
                                    int(cmd[3]),
                                    int(cmd[4]),
                                    int(cmd[5]),
                                    int(cmd[6]),
                                    self.convertFromString(cmd[7])))
                        else:
                            self.playerList[int(cmd[1])] = PlayerInfo(
                                int(cmd[1]),
                                cmd[2],
                                int(cmd[3]),
                                int(cmd[4]),
                                int(cmd[5]),
                                int(cmd[6]),
                                self.convertFromString(cmd[7]))
                    
                ######################################################        

                elif cmd[0] == "g":
                    if len(cmd) == 3:
                        if self.gameStatus != cmd[1]:
                            self.playerList.clear()

                        if self.gameStatus != cmd[1]:
                            print("New Game Status: " + cmd[1])

                        self.gameStatus = cmd[1]
                        self.time = int(cmd[2])
                    
                ######################################################        

                elif cmd[0] == "u":
                    if len(cmd) > 1:
                    
                        for i in range(1, len(cmd)):
                        
                            a = cmd[i].split('#')

                            if len(a) == 4:
                                self.scoreList.append(
                                    ScoreBoard(
                                    a[0],
                                    (a[1] == "connected"),
                                    int(a[2]),
                                    int(a[3]), (0, 0, 0)))
                            
                            elif len(a) == 5:
                                self.scoreList.append(
                                    ScoreBoard(
                                    a[0],
                                    (a[1] == "connected"),
                                    int(a[2]),
                                    int(a[3]), self.convertFromString(a[4])))
                        

                        self.sscoreList = ""
                        for sb in self.scoreList:
                            self.sscoreList += sb.name + "\n"
                            self.sscoreList += ("connected" if sb.connected else "offline") + "\n"
                            self.sscoreList += str(sb.energy) + "\n"
                            self.sscoreList += str(sb.score) + "\n"
                            self.sscoreList += "---\n"
                        
                        self.scoreList.clear()
                    
                    
                ######################################################        

                elif cmd[0] == "notification":
                    if len(cmd) > 1:

                        if len(self.msg) == 0:
                            self.msgSeconds = 0
                        
                        self.msg.append(cmd[1])
                    
                ######################################################        

                elif cmd[0] == "hello":
                    if len(cmd) > 1:

                        if len(self.msg) == 0:
                            self.msgSeconds = 0

                        self.msg.append(cmd[1] + " has entered the game!")
                    
                ######################################################        

                elif cmd[0] == "goodbye":
                    if len(cmd) > 1:

                        if len(self.msg) == 0:
                            self.msgSeconds = 0

                        self.msg.append(cmd[1] + " has left the game!")
                    
                ######################################################        

                elif cmd[0] == "changename":
                    if len(cmd) > 1:
                        if len(self.msg) == 0:
                            self.msgSeconds = 0

                        self.msg.append(cmd[1] + " is now known as " + cmd[2] + ".")
                   
                    
                ######################################################        

                elif cmd[0] == "h":
                    if len(cmd) > 1:
                        o = []
                        o.append("hit")
                        self.gameAi.GetObservations(o)
                        self.msg.append("you hit " + cmd[1])                    
                    
                ######################################################        

                elif cmd[0] == "d":
                    if len(cmd) > 1:
                        o = []
                        o.append("damage")
                        self.gameAi.GetObservations(o)
                        self.msg.append(cmd[1] + " hit you")                    
                    
                ######################################################        

            except Exception as ex:
                if ex != None:
                    print(ex)
                pass


    # <summary>
    # send a message to other users
    # </summary>
    # <param name="msg">message string</param>
    def sendMsg(self, msg):
        if len(msg.strip()) > 0:
            self.client.sendSay(msg)

    
    # <summary>
    # Get current game time as string
    # </summary>
    # <returns>current time as string</returns>
    def GetTime(self):
        return str(datetime.timedelta(seconds=self.time))
    
    
    # <summary>
    # Execute some decision
    # </summary>
    def DoDecision(self):

        decision = self.gameAi.GetDecision()
        if decision == "virar_direita":
            self.client.sendTurnRight()
        elif decision == "virar_esquerda":
            self.client.sendTurnLeft()
        elif decision == "andar":
            self.client.sendForward()
        elif decision ==  "atacar":
            self.client.sendShoot()
        elif decision ==  "pegar_ouro":
            self.client.sendGetItem()
        elif decision == "pegar_anel":
            self.client.sendGetItem()
        elif decision == "pegar_powerup":
            self.client.sendGetItem()
        elif decision ==  "andar_re":
            self.client.sendBackward()

        self.client.sendRequestUserStatus()
        self.client.sendRequestObservation()


    def timer1_Tick(self):
        
        self.msgSeconds += self.timer1.interval * 1000 # KEEP THIS AS IS - 1000 miliseconds = 1 second

        self.client.sendRequestGameStatus()
        if self.gameStatus == "Game":
            self.DoDecision()

        elif self.msgSeconds >= 5000: # 5 SECONDS

            print(self.gameStatus)
            print(self.GetTime())
            print("-----------------")
            print(self.sscoreList)

            self.client.sendRequestScoreboard()
        

        if self.msgSeconds  >= 5000: # 5 SECONDS

            if len(self.msg) > 0:

                for s in self.msg:
                    print(s)

                self.msg.clear()

            self.msgSeconds  = 0
        
        if self.running:
            self.timer1 = Timer(self.thread_interval, self.timer1_Tick)
            self.timer1.start()


    def SocketStatusChange(self):
    
        if self.client.connected:

            print("Connected")
            self.client.sendName(self.name)
            #self.client.sendRGB(255,0,0)  # BOT COLOR
            self.client.sendRequestGameStatus()
            self.client.sendRequestUserStatus()
            self.client.sendRequestObservation()

        else:
            print("Disconnected")
