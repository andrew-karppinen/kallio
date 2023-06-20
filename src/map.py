import pygame
from src.objects import *

from copy import deepcopy


def SetMap(gamedata:object,mapstr:str,initial:bool = False):
    '''
    Convert mapstr to map list
    set maplist to gamedata object

    "initial" parameter must be true, If the level is started from the beginning

    0 = empty
    1 = local player
    2 = remote player
    3 = default tile
    4 = tile that can be destroyed
    5 = tile that cannot be destroyed
    7 = goal
    8 not a falling tnt
    9 = falling tnt
    10 = not a falling stone
    11 = falling stone
    12 = Explosion
    14 = monster which looking to right
    15 = monster which looking to down
    16 = monster which looking to left
    17 = monster which looking to up
    18 = not a falling diamond
    19 = falling diamond

    20 Door up
    21 Door right
    22 door down
    23 door left
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


        if x == gamedata.map_width_:
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

    the first line specifies map size
    returns the end of the file as a string

    return map:str height:int,width:int,required_score:int,multiplayer:bool
    '''



    #Avataan tiedosto, josta rivit luetaan
    tiedosto = open(file_path, 'r')
    #rivi-muuttuja lukee tiedoston rivit
    rivit = tiedosto.readlines()
    #Suljetaan tiedosto
    tiedosto.close()

    multiplayer = rivit[0] #eka riv
    vaaditut_pisteet = rivit[1] #toka rivi
    mjono = rivit[2] #kolmas rivi

    #Luodaan y_ja_x-lista-muuttuja joka katkaisee merkkijonon siihen syötetyn pilkun kohdalta
    y_ja_x = mjono.split(',')

    #Muutetaan lista-muuttujan alkiot kokonaisluvuiksi
    y = int(y_ja_x[0])
    x = int(y_ja_x[1])

    #muunnetaan lista merkkijonoksi alkaen riviltä 4
    kartta = ''
    for i in rivit[3:]:
        kartta += i

    kartta = kartta.replace('\n', ',') #korvaa rivinvaihto merkit pilkuilla


    return kartta,y, x,vaaditut_pisteet,multiplayer