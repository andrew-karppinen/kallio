import pygame

from src import *




def Move(gamedata:object,right:bool,left:bool,up:bool,down:bool):
    '''
    move local player
    '''

    collisions = gamedata.collision_objects_
    pushing = gamedata.pushing_objects_


    if right:
        if gamedata.local_player_.position_x_ + 1 < gamedata.map_width_ and not type(gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ +1]) in collisions:  #if map not end and if no collision
            CollectPoints(gamedata, gamedata.local_player_.position_y_, gamedata.local_player_.position_x_+1) #try collect point
            gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_] = None
            gamedata.local_player_.position_x_ += 1 #move player

        #if no default tile or diamond
        elif gamedata.local_player_.position_x_+2 < gamedata.map_width_ and gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ + 2] == None: #if map not end and if index is empty
            if type(gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ + 1]) in pushing: #if pushing objects
                if gamedata.pushing_right_ == 0: #the player moves slower if it pushes a rock
                    gamedata.pushing_right_ = 1
                elif gamedata.pushing_right_ == 1:
                    if type(gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ + 1]) == Stone: #if stone
                        gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_+1].Rotate(1) #rotate image
                    gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ + 2] =  gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ + 1] #set stone new position
                    gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_] = None
                    gamedata.local_player_.position_x_ += 1  # move player
                    gamedata.pushing_right_ = 0

            #if door
            elif type(gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ + 1]) == Door: #if door
                if gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ + 1].direction_ == 2: #if the direction of the door is to the right
                    gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_] = None
                    gamedata.local_player_.position_x_ += 2 #move player


    if left:
        if gamedata.local_player_.position_x_-1 >= 0 and not type(gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ - 1]) in collisions:  #if map not end and if no collision
            CollectPoints(gamedata, gamedata.local_player_.position_y_, gamedata.local_player_.position_x_-1) #try collect point
            gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_] = None
            gamedata.local_player_.position_x_ -= 1 #move player

        #if pushing objects
        elif gamedata.local_player_.position_x_-2 >= 0 and gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ - 2] == None: #if map not end if index is empty
            if type(gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ - 1]) in pushing: #if pushing objects
                if gamedata.pushing_left_ == 0: #the player moves slower if it pushes a rock
                    gamedata.pushing_left_ = 1
                elif gamedata.pushing_left_ == 1:
                    if type(gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ - 1]) == Stone: #if stone
                        gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ - 1].Rotate(2) #rotate image
                    gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ - 2] =  gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ - 1] #set stone new position
                    gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_] = None
                    gamedata.local_player_.position_x_ -= 1 #move player
                    gamedata.pushing_left_ = 0

            #if door
            elif type(gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ - 1]) == Door: #if door
                if gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ - 1].direction_ == 4: #if the direction of the door is to the left
                    gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_] = None
                    gamedata.local_player_.position_x_ -= 2 #move player


    if up:
        if gamedata.local_player_.position_y_ - 1 >= 0 and not type(gamedata.current_map_[gamedata.local_player_.position_y_ -1][gamedata.local_player_.position_x_]) in collisions:  #if map not end and if no collision
            CollectPoints(gamedata, gamedata.local_player_.position_y_ - 1, gamedata.local_player_.position_x_) #try collect point
            gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_] = None
            gamedata.local_player_.position_y_ -= 1

        #if door
        elif gamedata.local_player_.position_y_ - 2 >= 0 and gamedata.current_map_[gamedata.local_player_.position_y_-2][gamedata.local_player_.position_x_] == None: #if map not end and if index is empty
            if type(gamedata.current_map_[gamedata.local_player_.position_y_ -1][gamedata.local_player_.position_x_]) == Door: #if door
                if gamedata.current_map_[gamedata.local_player_.position_y_-1][gamedata.local_player_.position_x_].direction_ == 1: #if the direction of the door is to the up
                    gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_] = None
                    gamedata.local_player_.position_y_ -= 2 #move player


    if down:
        if gamedata.local_player_.position_y_ +1 <gamedata.map_height_ and not type(gamedata.current_map_[gamedata.local_player_.position_y_ +1][gamedata.local_player_.position_x_ ]) in collisions:  #if map not end and if no collision
            CollectPoints(gamedata,gamedata.local_player_.position_y_ +1,gamedata.local_player_.position_x_) #try collect point
            gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_] = None
            gamedata.local_player_.position_y_ += 1
        #if door
        elif gamedata.local_player_.position_y_ + 2 < gamedata.map_height_ and gamedata.current_map_[gamedata.local_player_.position_y_+2][gamedata.local_player_.position_x_] == None: #if map not end and if index is empty
            if type(gamedata.current_map_[gamedata.local_player_.position_y_ +1][gamedata.local_player_.position_x_]) == Door: #if door
                if gamedata.current_map_[gamedata.local_player_.position_y_ +1][gamedata.local_player_.position_x_].direction_ == 3:  # if the direction of the door is to the down
                    gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_] = None
                    gamedata.local_player_.position_y_ += 2  # move player


    gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_] = gamedata.local_player_ #set player to map list

def CollectPoints(gamedata:object,y:int,x:int):
    #try collect point from given location
    if type(gamedata.current_map_[y][x]) == Diamond:
        gamedata.current_map_[y][x] = None
        gamedata.points_collected_ += 1

def Eat(gamedata:object,right:bool,left:bool,up:bool,down:bool):
    '''
    remove tile in left,right,up or down
    '''

    if right:
        if gamedata.local_player_.position_x_ +1 < gamedata.map_width_: #if map not end
            if type(gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_+1]) == DefaultTile:
                gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ + 1] = None
            CollectPoints(gamedata,gamedata.local_player_.position_y_,gamedata.local_player_.position_x_+1)


    elif left:
        if gamedata.local_player_.position_x_ -1 >= 0:  # if map not end
            if type(gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ - 1]) == DefaultTile:
                gamedata.current_map_[gamedata.local_player_.position_y_][gamedata.local_player_.position_x_ - 1] = None

            CollectPoints(gamedata,gamedata.local_player_.position_y_,gamedata.local_player_.position_x_-1)

    elif up:
        if gamedata.local_player_.position_y_ - 1 >= 0:  # if map not end
            if type(gamedata.current_map_[gamedata.local_player_.position_y_-1][gamedata.local_player_.position_x_]) == DefaultTile:
                gamedata.current_map_[gamedata.local_player_.position_y_-1][gamedata.local_player_.position_x_] = None
            CollectPoints(gamedata,gamedata.local_player_.position_y_-1,gamedata.local_player_.position_x_)

    elif down:
        if gamedata.local_player_.position_y_ + 1 < gamedata.map_height_:  # if map not end
            if type(gamedata.current_map_[gamedata.local_player_.position_y_+1][gamedata.local_player_.position_x_]) == DefaultTile:
                gamedata.current_map_[gamedata.local_player_.position_y_+1][gamedata.local_player_.position_x_] = None

            CollectPoints(gamedata,gamedata.local_player_.position_y_+1,gamedata.local_player_.position_x_)

def Gravity(gamedata):

    for y in range(gamedata.map_height_-1,-1,-1):
        for x in range(gamedata.map_width_-1,-1,-1):
            if type((gamedata.current_map_[y][x])) in gamedata.gravity_objects_: #if gravity objects
                if gamedata.current_map_[y][x].drop_: #if currently drop
                    if y + 1 < gamedata.map_height_: #if map not end
                        if type(gamedata.current_map_[y+1][x]) == Player:
                            CreateExplosion(gamedata,y+1,x) #create explosion
                        elif type(gamedata.current_map_[y+1][x]) == Tnt: #if something falls on the tnt
                            CreateExplosion(gamedata, y+1, x) #create explosion

                        if gamedata.current_map_[y+1][x] != None:
                            if type(gamedata.current_map_[y][x]) == Tnt: #if tnt falls on something
                                CreateExplosion(gamedata,y,x) #create explosion

                    else: #if map end
                        if type(gamedata.current_map_[y][x]) == Tnt:
                            CreateExplosion(gamedata, y, x)


                if y + 1 < gamedata.map_height_:  # if map not end
                    if gamedata.current_map_[y+1][x] == None: #if below is empty
                        #move downwards
                        gamedata.current_map_[y][x].drop_ = True
                        gamedata.current_map_[y+1][x] = gamedata.current_map_[y][x]
                        gamedata.current_map_[y][x] = None
                    else:

                        if type(gamedata.current_map_[y][x]) in [Stone,Diamond]: #if stone or diamond
                            if type(gamedata.current_map_[y+1][x]) in gamedata.gravity_objects_2_: #if below is stone or diamond

                                if x +1 < gamedata.map_width_:
                                    if gamedata.current_map_[y][x+1] == None and gamedata.current_map_[y+1][x+1] == None: #if empty on the right
                                        gamedata.current_map_[y][x+1] = gamedata.current_map_[y][x] #move stone to right
                                        gamedata.current_map_[y][x].Rotate(2)
                                        gamedata.current_map_[y][x] = None
                                        return

                                if x-1 >= 0: #if map not end
                                    if gamedata.current_map_[y][x-1] == None and gamedata.current_map_[y+1][x-1] == None: #if empty on the left
                                        gamedata.current_map_[y][x-1] = gamedata.current_map_[y][x] #move stone to left
                                        gamedata.current_map_[y][x] = None
                                        return


                        gamedata.current_map_[y][x].drop_ = False
                else:
                    gamedata.current_map_[y][x].drop_ = False



def CreateExplosion(gamedata:object,y:int,x:int):


    list1 = [0,0,0,1,1,1,-1,-1,-1] #y
    list2 = [1,-1,0,1,-1,0,1,-1,0] #x

    for i in range(len(list1)):

        if y + list1[i] >= 0 and y + list1[i] < gamedata.map_height_: #if map not end
            if x + list2[i] >= 0 and x + list2[i] < gamedata.map_width_:  # if map not end

                if type(gamedata.current_map_[y+list1[i]][x+list2[i]]) != Bedrock: #if not Bedrock
                    if type(gamedata.current_map_[y+list1[i]][x+list2[i]]) in gamedata.explosive_: #if tnt,player, monster...
                        gamedata.current_map_[y + list1[i]][x + list2[i]] = Explosion()
                        CreateExplosion(gamedata,y+list1[i],x+list2[i]) #create new explosion

                    gamedata.current_map_[y+list1[i]][x+list2[i]] = Explosion()




def DeleteExplosion(gamedata:object):
    #return true if explosion removed, else false

    removed = False
    for y in range(gamedata.map_height_):
        for x in range(gamedata.map_width_):
            if type(gamedata.current_map_[y][x]) == Explosion:
                gamedata.current_map_[y][x].counter_ += 1
                if gamedata.current_map_[y][x].counter_ > 15: #duration of the explosion
                    gamedata.current_map_[y][x] = None
                    removed = True #if explosion removed

    return removed

def ExitProgram(connection):
    try: #if multiplayer
        connection.CloseSocket()  # close socket
    except:
        pass

    pygame.quit()
    exit()


def Run(gamedata:object,connection:object = None): #game main function

    clock = pygame.time.Clock()
    right = False
    left = False
    up = False
    down = False
    space = False

    movelimit = 0 #gravity
    movelimit2 = 0 #player move


    while True: #game main loop

        if gamedata.multiplayer_:

            connection.Read() #read socket


            if connection.data_type_ == "map": #if message is map
                try:
                    mapstr = connection.data_
                    SetMap(gamedata,mapstr) #set map
                    gamedata.total_points_collected_ = connection.points_collected_ + gamedata.points_collected_

                except: #if incorrect socket message
                    print(mapstr)
                    print("incorrect socket message")


        for event in pygame.event.get(): #pygame event loop
            #read keyboard
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE: #if esc is pressed
                    ExitProgram(connection)
                if event.key == pygame.K_LEFT:
                    left = True
                if event.key == pygame.K_RIGHT:
                    right = True

                if event.key == pygame.K_UP:
                    up = True

                if event.key == pygame.K_DOWN:
                    down = True
                if event.key == pygame.K_SPACE:
                    space = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_UP:
                    up = False
                if event.key == pygame.K_DOWN:
                    down = False
                if event.key == pygame.K_SPACE:
                    space = False




            if event.type == pygame.QUIT:  #exit program
                ExitProgram(connection)


        if pygame.time.get_ticks() > movelimit + 140:
            movelimit = pygame.time.get_ticks()
            Gravity(gamedata)


        if pygame.time.get_ticks() > movelimit2 + 80:
            movelimit2 = pygame.time.get_ticks()
            if [right, left, up, down].count(True) == 1:  #can only move in one direction at a time
                if space: #if space pressed
                    Eat(gamedata,right,left,up,down) #remove tile in left,right,up or down
                else:
                    Move(gamedata,right,left,up,down) #move player
                if gamedata.multiplayer_:
                    connection.SendMap(gamedata.current_map_, gamedata.points_collected_)  #send map


        gamedata.DrawMap()  #draw map

        if DeleteExplosion(gamedata): #delete exlplosions
            #if explosion removed
            if gamedata.multiplayer_: #if multiplayer
                connection.SendMap(gamedata.current_map_, gamedata.points_collected_)  #send map


        clock.tick(30) #fps limit