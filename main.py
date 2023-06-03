from src import *

import pygame

import time
from pygame.locals import *
pygame.init()



#initialize

#initialize

#load images
sandimage = pygame.image.load("media/sand.png")
playerimage = pygame.image.load("media/player.png")
playerimage2 = pygame.image.load("media/player2.png")
stoneimage = pygame.image.load("media/stone.png")
tntimage = pygame.image.load("media/tnt.png")
explosionimage = pygame.image.load("media/explosion.png")
diamondimage = pygame.image.load("media/diamond.png")
goalimage = pygame.image.load("media/goal.png")
bedrockimage = pygame.image.load("media/bedrock.png")
brickimage = pygame.image.load("media/brick.png")
doorimage = pygame.image.load("media/door.png")

#set images
Goal.image = goalimage
Diamond.image = diamondimage
Explosion.image = explosionimage
Tnt.image = tntimage
DefaultTile.image = sandimage
Stone.image = stoneimage
Bedrock.image = bedrockimage
Brick.image = brickimage
Door.Setimage(doorimage)

#create players
local_player = Player(playerimage)
remote_player = Player(playerimage2, False)

if 0:  # client
    gamedata = GameData(local_player, True, False,remote_player) #create gamedata object

    connection = Client("localhost", 1234)  # tähän ip osoite!!!

    if connection.connected_:
        connection.SendReadyToStart("05664")
        connection.Read()  # read messages
        print("tässä1", connection.data_)
        if connection.data_type_ == "startinfo":  # if start info

            #set map size and required score
            gamedata.map_height_, gamedata.map_width_,gamedata.required_score_ = connection.data_

            connection.Read()  # read messages
            print("tässä2", connection.data_)
            if connection.data_type_ == "map":  # if message is map
                SetMap(gamedata, connection.data_,True)  # set map
                gamedata.SetScreenSize((1920,1080))  # set screen size
                Run(gamedata, connection)  # start game
                print("tässä3", connection.data_)



if 0:  # server
    gamedata = GameData(local_player, True,True, remote_player)  # create gamedata


    connection = Server(1234) #create server object

    mapstr, gamedata.map_height_, gamedata.map_width_,gamedata.required_score_,map_is_multiplayer = ReadMapFile("maps/testmap.txt")
    SetMap(gamedata, mapstr,True)  # convert str to map list

    if connection.connected_:
        connection.Read()  # read messages
        if connection.data_type_ == "readytostart":  # if client ready to start the game
            if connection.data_ == "05664":
                connection.SendStartInfo(gamedata.map_height_, gamedata.map_width_,gamedata.required_score_)  #send start info

                connection.SendMap(gamedata.current_map_, 0)  # and send map
                gamedata.SetScreenSize((1920,1080))  # set screen size
                Run(gamedata, connection)

if 1:  # if singleplayer

    gamedata = GameData(local_player, False, False)  # create gamedata

    gamedata.SetScreenSize((1920,1080)) #set screen size
    mapstr, gamedata.map_height_, gamedata.map_width_,gamedata.required_score_,map_is_multiplayer = ReadMapFile("maps/testmap.txt")
    SetMap(gamedata, mapstr,True)  # convert str to map list

    Run(gamedata, False) #start game
