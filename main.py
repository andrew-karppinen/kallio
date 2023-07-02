from src import *

import pygame
pygame.init()



#initialize



if 0:  # client
    gamedata = GameData(True, False) #create gamedata object

    connection = Client("localhost", 1234)  # tähän ip osoite!!!

    if connection.connected_:
        connection.SendReadyToStart("05664")
        connection.Read()  # read messages
        print("tässä1", connection.data_)
        if connection.data_type_ == "startinfo":  # if start info

            #set map size and required score
            gamedata.map_height_, gamedata.map_width_, gamedata.required_score_ = connection.data_

            connection.Read()  # read messages
            print("tässä2", connection.data_)
            if connection.data_type_ == "map":  # if message is map
                SetMap(gamedata, connection.data_,True)  # set map
                gamedata.SetScreenSize((1920,1080))  # set screen size
                gamedata.SetDrawarea()
                a = Run(gamedata, connection)  # start game
                print("tässä3", a)



if 1:  # server
    gamedata = GameData(True,True)  # create gamedata

    mapstr, gamedata.map_height_, gamedata.map_width_,map_is_multiplayer, gamedata.required_score_, timelimit = ReadMapFile("maps/multiplayer/multiplayer0.txt")
    SetMap(gamedata, mapstr,True)  # convert str to map list

    connection = Server(1234,10) #create server object

    if connection.connected_:
        connection.Read()  # read messages
        if connection.data_type_ == "readytostart":  # if client ready to start the game
            if connection.data_ == "55664":
                connection.SendStartInfo(gamedata.map_height_, gamedata.map_width_,gamedata.required_score_)  #send start info

                connection.SendMap(gamedata.current_map_, 0)  # and send map
                gamedata.SetScreenSize((1280,720))  # set screen size
                gamedata.SetDrawarea()

                a = Run(gamedata, connection)
                print(a)

if 0:  # if singleplayer
    gamedata = GameData(False, False)  # create gamedata



    mapstr, gamedata.map_height_, gamedata.map_width_,map_is_multiplayer, gamedata.required_score_, timelimit = ReadMapFile("maps/singleplayer/down they fall.txt")
    SetMap(gamedata, mapstr,True)  # convert str to map list
    gamedata.SetScreenSize((1920,1080)) #set screen size
    gamedata.SetDrawarea()

    a = Run(gamedata, None) #start game
    print(a)
