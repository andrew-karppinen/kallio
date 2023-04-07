import pygame
from src.objects import *



def SetMap(gamedata:object,mapstr:str):
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


    maplist = []
    maplist2d = [['' for i in range(gamedata.map_width_)] for j in range(gamedata.map_height_)] #create 2d array

    number = ""

    #numbers to objects
    mapsymbols = {"0":None,"1":gamedata.local_player_,"2":gamedata.remote_player_,"3":DefaultTile(),"4":Brick(),"5":Bedrock(),"6":Diamond(),"7":Goal(),"8":Tnt(False),"9":Tnt(True),"10":Stone(False),"11":Stone(True),"12":Monster(1),"13":Monster(2),"14":Monster(3),"15":Monster(4)}
    for i in range(len(mapstr)):



        if mapstr[i] != ",":

            number += mapstr[i]

        if i + 1 == len(mapstr):  # if map end
            maplist.append(mapsymbols[number])  # convert numbers to objects


        if mapstr[i] == ",": #if ","
            maplist.append(mapsymbols[number]) #convert numbers to objects

            number = ""



    #1d array to 2d array
    counter = 0
    for y in range(gamedata.map_height_):
        for x in range(gamedata.map_width_):
            maplist2d[y][x] = maplist[counter]
            counter += 1

    return(maplist2d)



def ReadMapFile(file_path:str):
    '''
    read txt file

    the first line specifies map size
    returns the end of the file as a string

    return height:int,width:int,map:str
    '''



    #Avataan tiedosto, josta rivit luetaan
    tiedosto = open(file_path, 'r')
    #rivi-muuttuja lukee tiedoston rivit
    rivit = tiedosto.readlines()
    #Suljetaan tiedosto
    tiedosto.close()


    mjono = rivit[0] #first line

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