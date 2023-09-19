import pygame

from src.objects import *
from src.config.tile_commands_config import mapsymbols #import mapsymbols

def SetMap(gamedata:object,mapstr:str)->None:
    '''
    set full map
    Convert mapstr to map list
    set maplist to gamedata object

    "initial" parameter must be true, If the level is started from the beginning

    data:
    src/config/tile commands_config.py

    '''



    #check mapstr correctness #Todo update this
    if mapstr.count(",") != gamedata.map_width_ * gamedata.map_height_ -1:
        raise Exception('incorrect mapstr')


    gamedata.original_mapstr_ = mapstr #save mapstr to gamedata object

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

            if number == "1":  # if local player
                gamedata.local_player_position_y_ = y
                gamedata.local_player_position_x_ = x

            elif number == "2":  # if remote player
                gamedata.remote_player_position_y_ = y
                gamedata.remote_player_position_x_ = x


            command = mapsymbols[number]['command'] #convert numbers to objects
            exec(f"maplist2d[y][x] = {command}") #convert numbers to objects

            #if command2 exist
            if mapsymbols[number]['command2'] != None:
                exec(mapsymbols[number]['command2'])




        if mapstr[i] == ",": #if ","


            if number == "1": #if local player
                gamedata.local_player_position_y_ = y
                gamedata.local_player_position_x_ = x

            elif number == "2": #if remote player
                gamedata.remote_player_position_y_ = y
                gamedata.remote_player_position_x_ = x




            command = mapsymbols[number]['command']  # convert numbers to objects
            exec(f"maplist2d[y][x] = {command}") #convert numbers to objects

            #if command2 exist
            if mapsymbols[number]['command2'] != None:
                exec(str(mapsymbols[number]['command2']))



            number = ""
            x += 1





    gamedata.current_map_ = maplist2d #set maplist to gamedata object



def ReadMapFile(file_path:str):
    '''
    read txt file

    return: map:str, height:int, width:int, multiplayer:bool, required_score:int, timelimit:int
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