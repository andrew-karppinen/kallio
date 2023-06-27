import pygame
from src.objects import *


import json

def SetMap(gamedata:object,mapstr:str,initial:bool = False):
    '''
    Convert mapstr to map list
    set maplist to gamedata object

    "initial" parameter must be true, If the level is started from the beginning

    '''



    #check mapstr correctness #Todo update this
    if mapstr.count(",") != gamedata.map_width_ * gamedata.map_height_ -1:
        raise Exception('incorrect mapstr')

    if initial == True:
        gamedata.original_mapstr_ = mapstr

    maplist2d = [['' for i in range(gamedata.map_width_)] for j in range(gamedata.map_height_)] #create 2d array

    number = ""

    y = 0
    x = 0



    #numbers to objects
    for i in range(len(mapstr)):


        if x == gamedata.map_width_: #next row
            y += 1
            x = 0


        if mapstr[i] != ",":

            number += mapstr[i]

        if i + 1 == len(mapstr):  # if map end


            if number != "1":  # if no local player

                exec(gamedata.mapsymbols_[number]['command'])  #convert numbers to objects

            elif number == "1":  # if local player
                if initial == True:
                    #this scope run only in beginning the game

                    gamedata.local_player_position_y_ = y  #set player position
                    gamedata.local_player_position_x_ = x
                    maplist2d[y][x] = gamedata.local_player_
                else:
                    #the localplayer's location already exists
                    maplist2d[y][x] = None
                    maplist2d[gamedata.local_player_position_y_][gamedata.local_player_position_x_] = gamedata.local_player_




        if mapstr[i] == ",": #if ","

            if number != "1": #if no player

                exec(gamedata.mapsymbols_[number]['command']) #convert numbers to objects


            elif number == "1": #if local player
                if initial == True:
                    #this scope run only in beginning the game
                    gamedata.local_player_position_y_ = y  # set player position
                    gamedata.local_player_position_x_ = x
                    maplist2d[y][x] = gamedata.local_player_
                else:
                    #the localplayer's location already exists
                    maplist2d[y][x] = None
                    maplist2d[gamedata.local_player_position_y_][gamedata.local_player_position_x_] = gamedata.local_player_



            number = ""
            x += 1





    gamedata.current_map_ = maplist2d #set maplist to gamedata object



def ReadMapFile(file_path:str):
    '''
    read txt file

    return map:str height:int,width:int,required_score:int,time limit:int,multiplayer:bool
    '''



    #open file
    file = open(file_path, 'r')
    #read rows to list
    rows = file.readlines()
    #close file
    file.close()

    multiplayer = eval(rows[0]) #row 1, multiplayer
    required_score = int(rows[1]) #row 2, required score
    time = int(rows[2]) #row 3, time limit
    mjono = rows[3] # row 4, map size

    #read map size:
    y_and_x = mjono.split(',') #replace str
    y = int(y_and_x[0]) #str to int
    x = int(y_and_x[1])

    #read the remaining lines of the file
    mapstr = ''
    for i in rows[4:]: #change the remaining lines of the file to str
        mapstr += i

    mapstr = mapstr.replace('\n', ',') #newline to ","


    return mapstr,y,x,multiplayer,required_score,time