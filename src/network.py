import socket
from objects import *


class Network:
    def __init__(self,server:bool,ip:str,port:int = 12345):


        if server: #

            self.s_ = socket.socket() #create socket object
            self.s_.settimeout(2)
            self.port_ = port

            self.s_.settimeout(5) #timeout 5 second

            self.s_.bind(('', port))
            print("socket binded to %s" % (self.port_)) #set port

            self.s_.listen(1)
            print("socket is listening")

            c, addr = self.s_.accept()  #waiting for someone to connect





        #self.connection_.connect((ip, port))

        #c, addr = s.accept()  # odottaa että joku yhdistää



    def SendStartInfo(self):
        pass

    def SendGameExit(self,win = False): #if game exit
        pass



    def SendMap(self,maplist:list):

        '''
        send map data

        0 = tyhjä
        1 = paikallinen pelaaja
        2 = toisen tietokoneen pelaaja
        3 = perustile
        4 = tile joka voidaan räjäyttää
        5 = tile jota ei voida räjäyttää
        6 = piste
        7 = maali
        8 = tnt joka ei putoamassa
        9 = tnt joka putoamassa
        10 = kivi joka ei putoamassa
        11 = kivi joka putoamassa
        14 =  vihollinen joka katsoo oikealle
        15 = vihollinen joka katsoo alas
        16 = vihollinen joka katsoo vasemmalle
        17 = vihollinen joka katsoo ylös
        '''

        sendlist = []

        sendlist.append(len(maplist)) #mapsize y
        sendlist.append(len(maplist[1]))  #mapsize x

        for i in range(len(maplist)):
            for j in range(len(maplist[i])):
                #i = y j = x

                if maplist[i][j] == None: #if none
                    sendlist.append(0)

                elif type(maplist[i][j]) == Player: #if player
                    if maplist[i][j].local_player_: #if local player
                        sendlist.append(2) #change to remoteplayer
                    else: #if remoteplayer
                        sendlist.append(1) #change to local player

                elif type(maplist[i][j]) == DefaultTile: #if default tile
                    sendlist.append(3)
                elif type(maplist[i][j]) == Brick: #can explode tile
                    sendlist.append(4)
                elif type(maplist[i][j]) == Bedrock: #cannot explode tile
                    sendlist.append(5)
                elif type(maplist[i][j]) == Diamond:
                    sendlist.append(6)
                elif type(maplist[i][j]) == Goal:
                    sendlist.append(7)

                elif type(maplist[i][j]) == Tnt: #if tnt
                    if maplist[i][j].drop_: #if currently dropping
                        sendlist.append(9)
                    else: #no currently dropping
                        sendlist.append(8)

                elif type(maplist[i][j]) == Stone: #if stone
                    if maplist[i][j].drop_: #if currently dropping
                        sendlist.append(11)

                    else: #no currently dropping
                       sendlist.append(10)

                elif type(maplist[i][j]) == Monster: #if monster

                    if maplist[i][j].direction_ == 1: #right
                        sendlist.append(14)
                    elif maplist[i][j].direction_ == 2: #down
                        sendlist.append(15)
                    elif maplist[i][j].direction_ == 3: #left
                        sendlist.append(16)
                    elif maplist[i][j].direction_ == 4: #up
                        sendlist.append(17)



        sendlist = str(sendlist) #list to string
        sendlist = sendlist.replace("[","")
        sendlist = sendlist.replace("]","")


    def Read(self):

        pass