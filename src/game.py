from threading import Thread
import pygame

from src.objects import *
from src.network import *
from src.map import *

import time



def Move(gamedata:object,right:bool,left:bool,up:bool,down:bool):
    '''
    move local player
    '''


    collisions = [Player,Stone]




    if right:
        if gamedata.local_player_.position_x_+1 < gamedata.map_width_: #if map not end

            if not type(gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ +1]) in collisions:   #collision check

                gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_] = None
                gamedata.local_player_.position_x_ += 1



    elif left:
        if gamedata.local_player_.position_x_-1 >= 0: #if map not end
            if not type(gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ - 1]) in collisions:  # collision check
                gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_] = None
                gamedata.local_player_.position_x_ -= 1



    elif up:
        if gamedata.local_player_.position_y_ - 1 >= 0:
            if not type(gamedata.current_map_[gamedata.local_player_.position_y_ -1][gamedata.local_player_.position_x_]) in collisions:  # collision check
                gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_] = None
                gamedata.local_player_.position_y_ -= 1



    elif down:
        if gamedata.local_player_.position_y_ +1 <gamedata.map_height_:
            if not type(gamedata.current_map_[gamedata.local_player_.position_y_ +1][gamedata.local_player_.position_x_ ]) in collisions:  # collision check
                gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_] = None
                gamedata.local_player_.position_y_ += 1


    gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_] = gamedata.local_player_ #set player new position





def Run(gamedata:object,multiplayer:bool,connection:object = None):


    clock = pygame.time.Clock()
    right = False
    left = False
    up = False
    down = False




    while True:

        if multiplayer:

            connection.Read() #read socket



            if connection.data_type_ == "map": #if message is map


                mapstr = connection.data_
                SetMap(gamedata,mapstr) #set map



        for event in pygame.event.get(): #pygame event loop
            #read keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left = True
                if event.key == pygame.K_RIGHT:
                    right = True

                if event.key == pygame.K_UP:
                    up = True

                if event.key == pygame.K_DOWN:
                    down = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_UP:
                    up = False
                if event.key == pygame.K_DOWN:
                    down = False




            if event.type == pygame.QUIT:  #exit program
                if multiplayer:
                    connection.CloseSocket() #close socket

                exit()

        if [right, left, up, down].count(True) == 1:  # can only move in one direction at a time
            Move(gamedata,right,left,up,down)
            if multiplayer:
                connection.SendMap(gamedata.current_map_,0)  # send map

        gamedata.DrawMap()  #draw map



        clock.tick(15)