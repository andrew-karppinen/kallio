import pygame
from src.objects import *
from copy import deepcopy
import json


def ObjectToStr(gameobject):

    '''
    convert one objects to map symbols
    '''

    if gameobject == None:  # if none
        mapsymbol = ("0")

    elif type(gameobject) == Player:  # if player
        if gameobject.local_player_:  # if local player, change to remoteplayer
            if gameobject.image_number_ == 0:
                mapsymbol = ("2 1")
            elif gameobject.image_number_ == 1:
                mapsymbol = ("2 2")
            elif gameobject.image_number_ == 2:
                mapsymbol = ("2 3")
            elif gameobject.image_number_ == 3:
                mapsymbol = ("2 4")
            elif gameobject.image_number_ == 4:
                mapsymbol = ("2 5")
        else:  # if remoteplayer
            mapsymbol = ("1")  # change to local player

    elif type(gameobject) == DefaultTile:  # if default tile
        mapsymbol = ("3")
    elif type(gameobject) == Brick:  # can explode tile
        mapsymbol = ("4")
    elif type(gameobject) == Bedrock:  # cannot explode tile
        mapsymbol = ("5")
    elif type(gameobject) == Goal:
        mapsymbol = ("7")

    elif type(gameobject) == Tnt:  # if tnt
        if gameobject.drop_:  # if currently dropping
            mapsymbol = ("9")
        else:  # no currently dropping
            mapsymbol = ("8")

    elif type(gameobject) == Stone:  # if stone
        if gameobject.drop_:  # if currently dropping
            if gameobject.direction_ == 1:
                mapsymbol = ("11 1")
            elif gameobject.direction_ == 2:
                mapsymbol = ("11 2")
            elif gameobject.direction_ == 3:
                mapsymbol = ("11 3")
            elif gameobject.direction_ == 4:
                mapsymbol = ("11 4")

        else:  # no currently dropping
            if gameobject.direction_ == 1:
                mapsymbol = ("10 1")
            elif gameobject.direction_ == 2:
                mapsymbol = ("10 2")
            elif gameobject.direction_ == 3:
                mapsymbol = ("10 3")
            elif gameobject.direction_ == 4:
                mapsymbol = ("10 4")

    elif type(gameobject) == Explosion:  # if explosion
        pass
        # Todo delete this?


    elif type(gameobject) == Monster:  # if monster
        if gameobject.direction_ == 1:  # right
            mapsymbol = ("14")
        elif gameobject.direction_ == 2:  # down
            mapsymbol = ("15")
        elif gameobject.direction_ == 3:  # left
            mapsymbol = ("16")
        elif gameobject.direction_ == 4:  # up
            mapsymbol = ("17")

    elif type(gameobject) == Diamond:  # if diamond
        if gameobject.drop_:  # if currently dropping
            if gameobject.direction_ == 1:
                mapsymbol = ("19 1")
            elif gameobject.direction_ == 2:
                mapsymbol = ("19 2")
            elif gameobject.direction_ == 3:
                mapsymbol = ("19 3")
            elif gameobject.direction_ == 4:
                mapsymbol = ("19 4")
        else:  # no currently dropping
            print(gameobject.direction_)
            if gameobject.direction_ == 1:
                mapsymbol = ("18 1")
            elif gameobject.direction_ == 2:
                mapsymbol = ("18 2")
            elif gameobject.direction_ == 3:
                mapsymbol = ("18 3")
            elif gameobject.direction_ == 4:
                mapsymbol = ("18 4")

    elif type(gameobject) == Door:  # if door
        if gameobject.direction_ == 1:  # up
            mapsymbol = ("20")
        elif gameobject.direction_ == 2:  # right
            mapsymbol = ("21")
        elif gameobject.direction_ == 3:  # down
            mapsymbol = ("22")
        elif gameobject.direction_ == 4:  # left
            mapsymbol = ("23")


    return(mapsymbol)



def MapListToStr(maplist: list):
    '''
    convert full maplist to mapstr

    '''

    sendlist = []


    for i in range(len(maplist)):
        for j in range(len(maplist[i])):
            # i = y j = x

            sendlist.append(ObjectToStr(maplist[i][j])) #convert obejcts to mapsymbol


    sendstr = ",".join(sendlist) #convert list to string

    return (sendstr)






def SetMap(gamedata:object,mapstr:str,initial:bool = False):
    '''
    set full map
    Convert mapstr to map list
    set maplist to gamedata object

    "initial" parameter must be true, If the level is started from the beginning

    data:
    src/config/tile commands config.json

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

            if number == "1":  # if local player
                gamedata.local_player_position_y_ = y
                gamedata.local_player_position_x_ = x

            elif number == "2":  # if remote player
                gamedata.remote_player_position_y_ = y
                gamedata.remote_player_position_x_ = x


            command = gamedata.mapsymbols_[number]['command'] #convert numbers to objects
            exec(f"maplist2d[y][x] = {command}") #convert numbers to objects

            #if command2 exist
            if gamedata.mapsymbols_[number]['command2'] != None:
                exec(str(gamedata.mapsymbols_[number]['command2']))




        if mapstr[i] == ",": #if ","


            if number == "1": #if local player
                gamedata.local_player_position_y_ = y
                gamedata.local_player_position_x_ = x

            elif number == "2": #if remote player
                gamedata.remote_player_position_y_ = y
                gamedata.remote_player_position_x_ = x





            command = gamedata.mapsymbols_[number]['command']  # convert numbers to objects
            exec(f"maplist2d[y][x] = {command}") #convert numbers to objects

            #if command2 exist
            if gamedata.mapsymbols_[number]['command2'] != None:
                exec(str(gamedata.mapsymbols_[number]['command2']))



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