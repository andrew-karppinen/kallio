from src import *

import pygame
pygame.init()


#program test file



PROGRAM_VERSION = "0.0.21"



if 0:  # client
    gamedata = GameData(True, False) #create gamedata object

    connection = Client("localhost", 1234) #create client object

    if connection.connected_:
        connection.SendReadyToStart("55664",PROGRAM_VERSION)
        connection.Read()  # read messages
        print(connection.data_)
        if connection.data_type_ == "startinfo":  # if start info

            #set map size and required score
            gamedata.map_height_, gamedata.map_width_, gamedata.required_score_,gamedata.level_timelimit_ = connection.data_
            connection.BufferNext()  # delete first message from buffer

            connection.Read()  # read messages
            if connection.data_type_ == "map":  # if message is map
                SetMap(gamedata, connection.data_)  # set map
                connection.BufferNext()  # delete first message from buffer

                screen = pygame.display.set_mode((1600, 900))  # create screen

                gamedata.InitDisplay(screen)  # set window to gamedata object

                connection.compress_messages_ = False  # disable message compression

                level_completed,connection_lost  = Run(gamedata, connection)  # start game
                print(level_completed)



if 0:  # server
    gamedata = GameData(True,True)  # create gamedata

    mapstr, gamedata.map_height_, gamedata.map_width_,map_is_multiplayer, gamedata.required_score_, gamedata.level_timelimit_ = ReadMapFile("maps/multiplayer/multiplayer1") #read map file


    connection = Server(1234,10,True) #create server object

    if connection.connected_:
        connection.Read()  # read messages
        if connection.data_type_ == "readytostart":  # if client ready to start the game
            if connection.data_[0] == "55664":
                connection.BufferNext()  # delete first message from buffer
                connection.SendStartInfo(gamedata.map_height_, gamedata.map_width_,gamedata.required_score_,gamedata.level_timelimit_)  #send start info

                connection.SendMap(mapstr)  # and send map
                SetMap(gamedata, mapstr)  #set map(local)

                screen = pygame.display.set_mode((1600, 900))  # create screen

                gamedata.InitDisplay(screen)  # set window to gamedata object

                connection.compress_messages_ = False  # disable message compression

                level_completed,connection_lost = Run(gamedata, connection)
                print(level_completed)


if 1:  # if singleplayer
    gamedata = GameData(False, False)  # create gamedata




    mapstr, gamedata.map_height_, gamedata.map_width_,map_is_multiplayer, gamedata.required_score_, gamedata.level_timelimit_ = ReadMapFile("maps/singleplayer/deep in the mine") #read map file
    SetMap(gamedata, mapstr)  # convert str to map list

    screen = pygame.display.set_mode((1600, 900)) #create screen

    gamedata.InitDisplay(screen)  # set window to gamedata object

    level_completed,connection_lost  = Run(gamedata, None) #start game

    pygame.display.quit() #close screen

    print(level_completed)



