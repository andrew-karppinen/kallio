import pygame
from src.objects import *



def SetMap(gamedata:object,mapstr:str,map_height:int,map_width:int):
    '''
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
    14 = vihollinen joka katsoo oikealle
    15 = vihollinen joka katsoo alas
    16 = vihollinen joka katsoo vasemmalle
    17 = vihollinen joka katsoo ylös
    '''


    number = ""


    maplist = [[None] * map_width] * map_height

    y = 0
    x = 0


    mapsymbols = {"0":None,"1":gamedata.local_player_,"2":gamedata.remote_player_,"3":DefaultTile(),"4":Brick(),"5":Bedrock,"6":Diamond(),"7":Goal(),"8":Tnt(False),"9":Tnt(True),"10":Stone(False),"11":Stone(True),"12":Monster(1),"13":Monster(2),"14":Monster(3),"15":Monster(4)}

    for i in range(len(mapstr)):

        if x == map_width: #if next row
            y += 1
            x = 0
        else:
            x += 0

        if mapstr[i] != ",":
            maplist[y][x] = mapsymbols[mapstr[i]] #convert numbers to objects

    return(maplist)



def ReadMapFile(gamedata:object,filepath:str):
    '''
    read map in txt file
    return map list
    using SetMap function
    '''


    file = open(filepath,"r")
    mapstr = file.read()
    file.close()

    mapstr = mapstr.replace("\n","")
    print(mapstr)
    exit()

    number = ""
    for i in range(len(mapstr)): #map height
        if mapstr[i] != ",":
            number += mapstr[i]
        else:
            break

    map_height = int(number) #str to int
    number = ""


    for j in range(i+1,len(mapstr)):
        if mapstr[j] != ",":
            number += mapstr[j]
        else:
            break

    map_width = int(number) #str to int

    maplist = SetMap(gamedata,mapstr[j+1:],map_height,map_width)

    return(maplist,map_height,map_width)