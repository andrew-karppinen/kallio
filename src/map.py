import pygame
from src.objects import *

from copy import deepcopy

def SetMap(gamedata:object,mapstr:str):
    '''
    Convert mapstr to map list
    set maplist to gamedata object


    0 = tyhjä
    1 = paikallinen pelaaja
    2 = toisen tietokoneen pelaaja
    3 = perustile
    4 = tile joka voidaan räjäyttää
    5 = tile jota ei voida räjäyttää
    6 = piste
    7 = maali
    8 = tnt joka ei putoamassa
    9 = tnt joka putoamassa
    10 = kivi joka ei putoamassa
    11 = kivi joka putoamassa
    12 = räjähdys
    14 = vihollinen joka katsoo oikealle
    15 = vihollinen joka katsoo alas
    16 = vihollinen joka katsoo vasemmalle
    17 = vihollinen joka katsoo ylös
    '''



    #check mapstr correctness #Todo update this
    if mapstr.count(",") != gamedata.map_width_ * gamedata.map_height_ -1:
        raise Exception('incorrect mapstr')

    number = ""

    maplist = []
    maplist2d = [['' for i in range(gamedata.map_width_)] for j in range(gamedata.map_height_)] #create 2d array

    number = ""

    y = 0
    x = 0


    #numbers to objects
    mapsymbols = {"0":None,"3":DefaultTile(),"4":Brick(),"5":Bedrock(),"6":Diamond(),"7":Goal(),"8":Tnt(False),"9":Tnt(True),"10":Stone(False),"11":Stone(True),"12":Explosion(),"14":Monster(1),"15":Monster(2),"16":Monster(3),"17":Monster(4)}
    for i in range(len(mapstr)):


        if x == gamedata.map_width_:
            y += 1
            x = 0


        if mapstr[i] != ",":

            number += mapstr[i]

        if i + 1 == len(mapstr):  # if map end
            if number != "1" and number != "2":  # if no player

                maplist2d[y][x] =  deepcopy(mapsymbols[number])  # convert numbers to objects

            if number == "1":  # if local player
                gamedata.local_player_.position_y_ = y  # set player position
                gamedata.local_player_.position_x_ = x
                maplist2d[y][x] = gamedata.local_player_

            elif number == "2":  # if remote player
                maplist2d[y][x] = gamedata.remote_player_


        if mapstr[i] == ",": #if ","

            if number != "1" and number != "2": #if no player

                maplist2d[y][x] = deepcopy(mapsymbols[number]) #convert numbers to objects


            if number == "1": #if local player
                gamedata.local_player_.position_y_ = y #set player position
                gamedata.local_player_.position_x_ = x
                maplist2d[y][x] = gamedata.local_player_

            elif number == "2": #if remote player
                maplist2d[y][x] = gamedata.remote_player_

            number = ""
            x += 1





    gamedata.current_map_ = maplist2d #set maplist to gamedata object



def ReadMapFile(file_path:str):
    '''
    read txt file

    the first line specifies map size
    returns the end of the file as a string

    return map:str height:int,width:int
    '''



    #Avataan tiedosto, josta rivit luetaan
    tiedosto = open(file_path, 'r')
    #rivi-muuttuja lukee tiedoston rivit
    rivit = tiedosto.readlines()
    #Suljetaan tiedosto
    tiedosto.close()


    mjono = rivit[0] #eka rivi

    #Luodaan y_ja_x-lista-muuttuja joka katkaisee merkkijonon siihen syötetyn pilkun kohdalta
    y_ja_x = mjono.split(',')

    #Muutetaan lista-muuttujan alkiot kokonaisluvuiksi
    y = int(y_ja_x[0])
    x = int(y_ja_x[1])

    #muunnetaan lista merkkijonoksi
    kartta = ''
    for i in rivit[1:]:
        kartta += i

    kartta = kartta.replace('\n', ',') #korvaa rivinvaihto merkit pilkuilla


    return kartta,y, x