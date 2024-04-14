import pygame
import re

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




    multiplayer = None
    required_score = None
    time = None

    y = None
    x = None


    line_number = 0
    file = open(file_path,'r')
    lines = file.readlines()
    for line in lines:

        line_number += 1

        if line == "mapstart:\n":
            if None in [time,multiplayer,required_score,y,x]:
                print([time,multiplayer,required_score,y,x])
                raise Exception("invalid option")
            else:
                break



        multiplayer_find = re.search(r'\bmultiplayer=(\S+)\b',line) #find multiplayer
        if multiplayer_find:
            multiplayer = str(multiplayer_find.group(1))
            if multiplayer.lower() == "false":
                multiplayer = False
            elif multiplayer.lower() == "true":
                multiplayer = True
            else:
                raise Exception("invalid multiplayer option")



        required_score_find = re.search(r'required_score=(\d+)', line) #find required score
        if required_score_find:
            required_score = int(required_score_find.group(1))


        time_find = re.search(r'time=(\d+)',line) #find time
        if time_find:
            time = int(time_find.group(1))


        x_find = re.search(r'size_x=(\d+)',line) #find size y
        if x_find:
            x = int(x_find.group(1))

        y_find = re.search(r'size_y=(\d+)',line) #find size y
        if y_find:
            y = int(y_find.group(1))


    file.close() #close file


    #read the remaining lines of the file
    mapstr = ''

    for i in lines[line_number:]: #change the remaining lines of the file to str
        mapstr += i

    mapstr = mapstr.replace('\n', ',') #newline to ","


    return mapstr,y,x,multiplayer,required_score,time