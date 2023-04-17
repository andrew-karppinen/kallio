
from src import *

import pygame

import time




naytto = pygame.display.set_mode((1250, 850)) #create window


#initialize

#load images
hiekkakuva = pygame.image.load("media/hiekka.png")
ukkeli = pygame.image.load("media/ukkeli.png")
kivikuva = pygame.image.load("media/kivi.png")
tntkuva = pygame.image.load("media/tnt.png")
rajahdyskuva = pygame.image.load("media/räjähdys.png")
pisetekuva = pygame.image.load("media/piste.png")
maalikuva = pygame.image.load("media/maali.png")

#set images
Goal.image = maalikuva
Diamond.image = pisetekuva
Explosion.image = rajahdyskuva
Tnt.image = tntkuva
DefaultTile.image = hiekkakuva
Stone.image = kivikuva

#create players
local_player = Player(ukkeli)
remote_player = Player(ukkeli,False)






if 0: #client
    pygame.display.set_caption('client')
    gamedata = GameData(local_player, True, remote_player, screen=naytto)

    connection = Client("localhost", 1234) #tähän ip osoite!!!


    if connection.connected_:
        connection.SendReadyToStart("05664")
        connection.Read() #read messages
        print("tässä1",connection.data_)
        if connection.data_type_ == "startinfo": #if start info
            #set map size

            gamedata.map_height_,gamedata.map_width_ =  connection.data_

            connection.Read()  # read messages
            print("tässä2",connection.data_)
            if connection.data_type_ == "map":  #if message is map
                SetMap(gamedata,connection.data_) #set map
                Run(gamedata,True,connection) #start game
                print("tässä3",connection.data_)






if 0: #server
    pygame.display.set_caption('server')
    gamedata = GameData(local_player, True,remote_player, screen=naytto)  # create gamedata
    gamedata.server_ = True
    connection = Server(1234)

    mapstr,gamedata.map_height_,gamedata.map_width_ =ReadMapFile("testmap.txt")
    SetMap(gamedata,mapstr) #convert str to map list

    if connection.connected_:
        connection.Read()  #read messages

        if connection.data_type_ == "readytostart": #if client ready to start the game

            if connection.data_ == "05664":

                connection.SendStartInfo(gamedata.map_height_,gamedata.map_width_) #send start info

                connection.SendMap(gamedata.current_map_,0) #and send map
                Run(gamedata,True,connection)



if 1: #if singleplayer
    gamedata = GameData(local_player, False, remote_player, screen=naytto)  # create gamedata

    mapstr,gamedata.map_height_,gamedata.map_width_ =ReadMapFile("testmap.txt")
    SetMap(gamedata,mapstr) #convert str to map list


    Run(gamedata,False)


