from src import *

import pygame

import time
from pygame.locals import *
pygame.init()



#initialize

#load images
hiekkakuva = pygame.image.load("media/sand.png")
ukkeli = pygame.image.load("media/player.png")
kivikuva = pygame.image.load("media/stone.png")
tntkuva = pygame.image.load("media/tnt.png")
rajahdyskuva = pygame.image.load("media/explosion.png")
pisetekuva = pygame.image.load("media/diamond.png")
maalikuva = pygame.image.load("media/goal.png")

# set images
Goal.image = maalikuva
Diamond.image = pisetekuva
Explosion.image = rajahdyskuva
Tnt.image = tntkuva
DefaultTile.image = hiekkakuva
Stone.image = kivikuva

# create players
local_player = Player(ukkeli)
remote_player = Player(ukkeli, False)

if 0:  # client
    gamedata = GameData(local_player, True, remote_player, screen=None)

    connection = Client("localhost", 1234)  # tähän ip osoite!!!

    if connection.connected_:
        connection.SendReadyToStart("05664")
        connection.Read()  # read messages
        print("tässä1", connection.data_)
        if connection.data_type_ == "startinfo":  # if start info
            # set map size

            gamedata.map_height_, gamedata.map_width_ = connection.data_

            connection.Read()  # read messages
            print("tässä2", connection.data_)
            if connection.data_type_ == "map":  # if message is map
                SetMap(gamedata, connection.data_)  # set map
                gamedata.SetScreenSize((1920,1080))  # set screen size
                Run(gamedata, True, connection)  # start game
                print("tässä3", connection.data_)



if 0:  # server
    gamedata = GameData(local_player, True, remote_player)  # create gamedata
    gamedata.server_ = True
    connection = Server(1234)

    mapstr, gamedata.map_height_, gamedata.map_width_ = ReadMapFile("testmap.txt")
    SetMap(gamedata, mapstr)  # convert str to map list

    if connection.connected_:
        connection.Read()  # read messages
        if connection.data_type_ == "readytostart":  # if client ready to start the game
            if connection.data_ == "05664":
                connection.SendStartInfo(gamedata.map_height_, gamedata.map_width_)  # send start info

                connection.SendMap(gamedata.current_map_, 0)  # and send map
                gamedata.SetScreenSize((1920,1080))  # set screen size
                Run(gamedata, True, connection)

if 1:  # if singleplayer

    gamedata = GameData(local_player, False, remote_player)  # create gamedata

    gamedata.SetScreenSize((1920,1080)) #set screen size

    mapstr, gamedata.map_height_, gamedata.map_width_ = ReadMapFile("testmap.txt")
    SetMap(gamedata, mapstr)  # convert str to map list

    Run(gamedata, False)
