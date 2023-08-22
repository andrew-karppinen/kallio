from src import *

import pygame
pygame.init()



#initialize



if 0:  # client
    gamedata = GameData(True, False) #create gamedata object

    connection = Client("localhost", 1234,True) #create client object

    if connection.connected_:
        connection.SendReadyToStart("55664")
        connection.Read()  # read messages
        print("tässä1", connection.data_)
        if connection.data_type_ == "startinfo":  # if start info

            #set map size and required score
            gamedata.map_height_, gamedata.map_width_, gamedata.required_score_,gamedata.level_timelimit_ = connection.data_
            connection.BufferNext()  # delete first message from buffer

            connection.Read()  # read messages
            print("tässä2", connection.data_)
            if connection.data_type_ == "map":  # if message is map
                SetMap(gamedata, connection.data_,True)  # set map
                connection.BufferNext()  # delete first message from buffer

                screen = pygame.display.set_mode((1600, 900))  # create screen

                gamedata.InitDisplay(screen)  # set window to gamedata object

                connection.SetTimeout(0.001)  # set new timeout
                connection.compress_messages_ = False  # disable message compression

                level_completed,connection_lost  = Run(gamedata, connection)  # start game
                print("tässä3", level_completed)



if 0:  # server
    gamedata = GameData(True,True)  # create gamedata

    mapstr, gamedata.map_height_, gamedata.map_width_,map_is_multiplayer, gamedata.required_score_, gamedata.level_timelimit_ = ReadMapFile("maps/multiplayer/multiplayer1.txt") #read map file


    connection = Server(1234,10,True) #create server object

    if connection.connected_:
        connection.Read()  # read messages
        if connection.data_type_ == "readytostart":  # if client ready to start the game
            if connection.data_ == "55664":
                connection.BufferNext()  # delete first message from buffer
                connection.SendStartInfo(gamedata.map_height_, gamedata.map_width_,gamedata.required_score_,gamedata.level_timelimit_)  #send start info

                connection.SendMap(mapstr)  # and send map
                SetMap(gamedata, mapstr, True)  #set map(local)

                screen = pygame.display.set_mode((1600, 900))  # create screen

                gamedata.InitDisplay(screen)  # set window to gamedata object

                connection.SetTimeout(0.001)  # set new timeout
                connection.compress_messages_ = False  # disable message compression

                level_completed,connection_lost = Run(gamedata, connection)
                print(level_completed)


if 0:  # if singleplayer
    gamedata = GameData(False, False)  # create gamedata




    mapstr, gamedata.map_height_, gamedata.map_width_,map_is_multiplayer, gamedata.required_score_, gamedata.level_timelimit_ = ReadMapFile(
        "maps/singleplayer/singleplayer1.txt") #read map file
    SetMap(gamedata, mapstr,True)  # convert str to map list

    screen = pygame.display.set_mode((1600, 900)) #create screen

    gamedata.InitDisplay(screen)  # set window to gamedata object

    level_completed,connection_lost  = Run(gamedata, None) #start game

    pygame.display.quit() #close screen

    print(level_completed)

