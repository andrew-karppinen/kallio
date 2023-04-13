from threading import Thread
import pygame


from src import *

import time



def Move(gamedata:object,right:bool,left:bool,up:bool,down:bool):
    '''
    move local player
    '''


    collisions = gamedata.collision_objects_
    pushing = gamedata.pushing_objects_


    if right:
        #pushing objects
        if gamedata.local_player_.position_x_+2 < gamedata.map_width_: #if map not end
            if type(gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ + 1]) in pushing:
                if gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ + 2] == None:
                    gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ + 2] =  gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ + 1]
                    gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ + 1] = None

        #collision check
        if gamedata.local_player_.position_x_ + 1 < gamedata.map_width_:  # if map not end
            if not type(gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ +1]) in collisions:   #collision check
                gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_] = None
                gamedata.local_player_.position_x_ += 1



    elif left:
        #pushing objects
        if gamedata.local_player_.position_x_-2 >= 0: #if map not end
            if type(gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ - 1]) in pushing:
                if gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ - 2] == None:
                    gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ - 2] =  gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ - 1]
                    gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ - 1] = None


        #collision check
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


def Gravity(gamedata):

    for y in range(gamedata.map_height_-1,0,-1):
        for x in range(gamedata.map_width_-1,0,-1):
            if type((gamedata.current_map_[y][x])) in gamedata.gravity_objects_: #if gravity objects
                if gamedata.current_map_[y][x].drop_: #if stone currently drop
                    if y + 1 < gamedata.map_height_: #if map not end
                        if type(gamedata.current_map_[y+1][x]) == Player:
                            print("pööö")

                if y + 1 < gamedata.map_height_:  # if map not end
                    if gamedata.current_map_[y+1][x] == None:
                        # move stone downwards
                        gamedata.current_map_[y][x].drop_ = True
                        gamedata.current_map_[y+1][x] = gamedata.current_map_[y][x]
                        gamedata.current_map_[y][x] = None
                    else:
                        gamedata.current_map_[y][x].drop_ = False
                else:
                    gamedata.current_map_[y][x].drop_ = False




def Run(gamedata:object,multiplayer:bool,connection:object = None):


    clock = pygame.time.Clock()
    right = False
    left = False
    up = False
    down = False

    movelimit = 0


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


        if pygame.time.get_ticks() > movelimit + 140:
            movelimit = pygame.time.get_ticks()
            Gravity(gamedata)

        if [right, left, up, down].count(True) == 1:  # can only move in one direction at a time
            Move(gamedata,right,left,up,down)
            if multiplayer:
                connection.SendMap(gamedata.current_map_,0)  #send map

        gamedata.DrawMap()  #draw map



        clock.tick(15)