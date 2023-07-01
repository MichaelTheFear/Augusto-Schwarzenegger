#!/usr/bin/env python

"""HandleClient.py: INF1771 Controls Socket Connection to Server."""
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

import socket
import sys
#from multiprocessing import Process
import threading
import time

# <summary>
# TCP Client Class
# </summary>
class HandleClient():


    # <summary>
    # Command Event Handler
    # </summary>
    #public static event EventHandler CommandEvent;
    __cmd_event_handlers = []

    # <summary>
    # Status Change Event Handler
    # </summary>
    #public static event EventHandler ChangeStatusEvent;
    __chg_event_handlers = []

    # <summary>
    # Is Client Connected?
    # </summary>
    connected = False

    # <summary>
    # Is Client Active?
    # </summary>
    active = False

    client_socket = None

    cThread = None


    def __init__(self): 
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def append_cmd_handler(self, cmd_handler):
        HandleClient.__cmd_event_handlers.append(cmd_handler)

    def append_chg_handler(self, chg_handler):
        HandleClient.__chg_event_handlers.append(chg_handler)


    # <summary>
    # Connects socket to a url or ip address
    # </summary>
    # <param name="s">url or ip address</param>
    def connect(self, s):
    
        if not self.connected:
        
            server_address = (s, 8888)
            self.client_socket.connect(server_address)
            
            self.connected = True
            self.active = True
            self.KeepAlive()
            
            #self.cThread = Process(target=self.doLoop)  # instantiating without any argument
            self.cThread = threading.Thread(target=self.doLoop)  # instantiating without any argument)
            self.cThread.start()
    

    # <summary>
    # Disconnects socket
    # </summary>
    def disconnect(self):
    
        if self.connected:
            self.client_socket.close()
        
        self.KeepAlive()
        self.active = False
        self.connected = False


    # <summary>
    # Send a player forward command
    # </summary>
    def sendForward(self):
        self.sendMsg("w")


    # <summary>
    # Send a player backward command
    # </summary>
    def sendBackward(self):
        self.sendMsg("s")
    

    # <summary>
    # Send a player turn left command
    # </summary>
    def sendTurnLeft(self):
        self.sendMsg("a")

    # <summary>
    # Send a player turn right command
    # </summary>
    def sendTurnRight(self):
        self.sendMsg("d")

    # <summary>
    # Send a player get item command
    # </summary>
    def sendGetItem(self):
        self.sendMsg("t")

    # <summary>
    # Send a player fire command
    # </summary>
    def sendShoot(self):
        self.sendMsg("e")

    # <summary>
    # Request observation
    # </summary>
    def sendRequestObservation(self):
        self.sendMsg("o")

    # <summary>
    # Request game status
    # </summary>
    def sendRequestGameStatus(self):
        self.sendMsg("g")

    # <summary>
    # Request user status
    # </summary>
    def sendRequestUserStatus(self):
        self.sendMsg("q")

    # <summary>
    # Request player position
    # </summary>
    def sendRequestPosition(self):
        self.sendMsg("p")

    # <summary>
    # Request server scoreboard
    # </summary>
    def sendRequestScoreboard(self):
        self.sendMsg("u")
    
    # <summary>
    # Quit game
    # </summary>
    def sendGoodbye(self):
        self.sendMsg("quit")

    # <summary>
    # Change player name
    # </summary>
    # <param name="name">new name</param>
    def sendName(self, name):
        self.sendMsg("name;" + name)
    

    # <summary>
    # Send a message to all players
    # </summary>
    # <param name="msg">text of the message</param>
    def sendSay(self, msg):
        self.sendMsg("say;" + msg)

    # <summary>
    # Change player color (R, G, B)
    # </summary>
    # <param name="r">Red color 0-255</param>
    # <param name="g">Green color 0-255</param>
    # <param name="b">Blue color 0-255</param>
    def sendRGB(self, r, g, b):
        self.sendColor((r, g, b))

    # <summary>
    # Change player color (Color)
    # </summary>
    # <param name="color">Color object</param>
    def sendColor(self, color):
        self.sendMsg("color;" + str(color[0]) + ";" + str(color[1]) + ";" + str(color[2]));

    # <summary>
    # Send a raw command to the server
    # </summary>
    # <param name="serverResponse">raw command</param>
    def sendMsg(self, serverResponse):

        try:
        
            if self.connected:
                send_cmd = serverResponse + "\n"
                send_cmd = send_cmd.encode("utf-8")
                self.client_socket.send(send_cmd)

        except Exception as ex:
            print(ex)
            self.KeepAlive()

    # <summary>
    # Keep socket alive - verify current status
    # </summary>
    def KeepAlive(self):
    
        if self.active != self.connected:
            self.processSocketStatusEvent()
        
        if not self.active or not self.connected:
            self.active = False
            self.connected = False

    

    def processSocketStatusEvent(self):
    
        #EventHandler handler = ChangeStatusEvent;
        #if (handler != null)
        #    EventArgs e = new EventArgs();
        #    handler(this, e);
        for eventhandler in HandleClient.__chg_event_handlers: 
            eventhandler()

    
    def processCommand(self, command):

        command = command.strip('\0').strip('\r')
        if len(command) > 0:
        
            try:
            
                if command.find(';') > -1:

                    cmd = command.split(';')

                    #EventHandler handler = CommandEvent;
                    #if (handler != null)
                    #   CommandEventArgs e = new CommandEventArgs();
                    #    e.cmd = cmd;
                    #    handler(this, e);

                    # <summary>
                    # Command Event Arguments - helps sending received messages from socket to other classes
                    # </summary>
                    for eventhandler in HandleClient.__cmd_event_handlers: 
                        eventhandler(cmd)

            except Exception as ex: # (Exception ex)
                print(ex)
                self.KeepAlive()


    def ProcessBuffer(self, data):
        
        index = data.find('\n')
        length = len(data)

        while (index > -1 and index < length):
        
            command = data[:index]
            data = data[(index+1):]
            
            command = command.strip('\0').strip('\r').strip('\n')

            if command.find(chr(1)) == -1 or command.find(chr(3)) == -1:
                if len(command) > 0:
                    self.processCommand(command)

            index = data.find('\n')


        return data
    
    
    def doLoop(self):

        offset = ""
        self.processSocketStatusEvent()

        while (self.active):
        
            receiveBufferSize = 1024

            if self.connected:

                try:
                    recv_str = self.client_socket.recv(receiveBufferSize)
                    data = offset + recv_str.decode('utf-8')
                    offset = self.ProcessBuffer(data)

                except Exception as ex: # (Exception ex)
                    print(ex)
                    self.KeepAlive()

            else:
               time.sleep(0.500)
