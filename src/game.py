import pygame

from src import *



def Move(gamedata:object,connection:object,right:bool,left:bool,up:bool,down:bool):
    '''
    move local player

    if multiplayer, send action to another computer
    '''


    #can move only 1 direction:
    if right == True:
        left = False;up = False; down = False;
    elif left == True:
        up = False; down = False;right = False;
    elif down == True:
        up = False; left = False;right = False;
    elif up == True:
        down = False;left = False;right = False;



    door = False #if go throught the door
    push = False #if pushing
    move = False #normal move
    sand = False #sand


    #backup current location, if the move is cancelled:
    original_x = gamedata.local_player_position_x_
    original_y = gamedata.local_player_position_y_



    if right:
        if gamedata.local_player_position_x_ + 1 < gamedata.map_width_ and not type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ +1]) in gamedata.collision_objects_:  #if map not end and if no collision

            if type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ +1]) == DefaultTile: #if sand
                sand = True #play sand audio

            Collect(gamedata, gamedata.local_player_position_y_, gamedata.local_player_position_x_ + 1) #try collect point
            gamedata.local_player_position_x_ += 1 #move player
            move = True



            gamedata.local_player_.AnimateToRight() #change player image
            gamedata.local_player_.movement_going_right_ = True #animate movement


        #if no default tile or diamond
        #if pushing objects
        elif gamedata.local_player_position_x_+2 < gamedata.map_width_ and gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ + 2] == None: #if map not end and if index is empty
            if type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ + 1]) in gamedata.pushing_objects_: #if pushing objects
                if gamedata.pushing_right_ == 0: #the player moves slower if it pushes a rock
                    gamedata.pushing_right_ = 1
                elif gamedata.pushing_right_ == 1:
                    if type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ + 1]) == Stone: #if stone
                        gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_+1].Rotate(1) #rotate image
                    gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ + 2] =  gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ + 1] #place the pushing object new position
                    gamedata.local_player_position_x_ += 1  # move player
                    gamedata.pushing_right_ = 0

                    push = True
                    gamedata.audio_.PlayPushSound() #play audio
                    gamedata.local_player_.AnimateToRight() #change player image

            #if door
            elif type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ + 1]) == Door: #if door
                if gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ + 1].direction_ == 2: #if the direction of the door is to the right
                    gamedata.local_player_position_x_ += 2 #move player
                    gamedata.local_player_.AnimateToRight()  #change player image
                    door = True

            #if keydoor
            elif type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_+1]) == LockedDoor and gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ + 1].door_type_ == "green":
                if gamedata.local_player_have_green_key_ == True:
                    gamedata.local_player_position_x_ += 2  # move player
                    gamedata.local_player_.AnimateToRight()  # change player image
                    door = True
            elif type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_+1]) == LockedDoor and gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ + 1].door_type_ == "blue":
                if gamedata.local_player_have_blue_key_ == True:
                    gamedata.local_player_position_x_ += 2  # move player
                    gamedata.local_player_.AnimateToRight()  # change player image
                    door = True

    elif left:
        if gamedata.local_player_position_x_-1 >= 0 and not type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1]) in gamedata.collision_objects_:  #if map not end and if no collision

            if type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ -1]) == DefaultTile: #if sand
                sand = True #play sand audio

            Collect(gamedata, gamedata.local_player_position_y_, gamedata.local_player_position_x_ - 1) #try collect point
            gamedata.local_player_position_x_ -= 1 #move player
            move = True

            gamedata.local_player_.AnimateToLeft() #change player image
            gamedata.local_player_.movement_going_left_ = True #animate movement

        #if pushing objects
        elif gamedata.local_player_position_x_-2 >= 0 and gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 2] == None: #if map not end if index is empty
            if type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1]) in gamedata.pushing_objects_: #if pushing objects
                if gamedata.pushing_left_ == 0: #the player moves slower if it pushes a rock
                    gamedata.pushing_left_ = 1
                elif gamedata.pushing_left_ == 1:
                    if type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1]) == Stone: #if stone
                        gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1].Rotate(2) #rotate image
                    gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 2] =  gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1] #set stone new position
                    gamedata.local_player_position_x_ -= 1 #move player
                    gamedata.pushing_left_ = 0

                    push = True
                    gamedata.audio_.PlayPushSound() #play audio


                    gamedata.local_player_.AnimateToLeft() #change player image

            #if door
            elif type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1]) == Door: #if door
                if gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1].direction_ == 4: #if the direction of the door is to the left
                    gamedata.local_player_position_x_ -= 2 #move player
                    gamedata.local_player_.AnimateToLeft()  #change player image
                    door = True
            #if keydoor
            elif type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_-1]) == LockedDoor and gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1].door_type_ == "green":
                if gamedata.local_player_have_green_key_ == True:
                    gamedata.local_player_position_x_ -= 2  # move player
                    gamedata.local_player_.AnimateToLeft()  # change player image
                    door = True
            #if keydoor
            elif type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_-1]) == LockedDoor and gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1].door_type_ == "blue":
                if gamedata.local_player_have_blue_key_ == True:
                    gamedata.local_player_position_x_ -= 2  # move player
                    gamedata.local_player_.AnimateToLeft()  # change player image
                    door = True



    elif up:
        if gamedata.local_player_position_y_ - 1 >= 0 and not type(gamedata.current_map_[gamedata.local_player_position_y_ -1][gamedata.local_player_position_x_]) in gamedata.collision_objects_:  #if map not end and if no collision

            if type(gamedata.current_map_[gamedata.local_player_position_y_-1][gamedata.local_player_position_x_]) == DefaultTile: #if sand
                sand = True #play sand audio

            Collect(gamedata, gamedata.local_player_position_y_ - 1, gamedata.local_player_position_x_) #try collect point
            gamedata.local_player_position_y_ -= 1 #move player
            move = True

            gamedata.local_player_.AnimateToHorizontal() #change player image
            gamedata.local_player_.movement_going_up_ = True #animate movement

        #if door
        elif gamedata.local_player_position_y_ - 2 >= 0 and gamedata.current_map_[gamedata.local_player_position_y_-2][gamedata.local_player_position_x_] == None: #if map not end and if index is empty
            if type(gamedata.current_map_[gamedata.local_player_position_y_ -1][gamedata.local_player_position_x_]) == Door: #if door
                if gamedata.current_map_[gamedata.local_player_position_y_-1][gamedata.local_player_position_x_].direction_ == 1: #if the direction of the door is to the up
                    gamedata.local_player_position_y_ -= 2 #move player
                    gamedata.local_player_.AnimateToHorizontal()  #change player image

                    door = True
            #if keydoor
            if type(gamedata.current_map_[gamedata.local_player_position_y_ -1][gamedata.local_player_position_x_]) == LockedDoor and gamedata.current_map_[gamedata.local_player_position_y_ - 1][gamedata.local_player_position_x_].door_type_ == "green":
                    if gamedata.local_player_have_green_key_ == True:
                        gamedata.local_player_position_y_ -= 2  # move player
                        gamedata.local_player_.AnimateToHorizontal()  # change player image
                        door = True
            #if keydoor
            elif type(gamedata.current_map_[gamedata.local_player_position_y_ -1][gamedata.local_player_position_x_]) == LockedDoor and gamedata.current_map_[gamedata.local_player_position_y_ - 1][gamedata.local_player_position_x_].door_type_ == "blue":
                if gamedata.local_player_have_blue_key_ == True:
                    gamedata.local_player_position_y_ -= 2  # move player
                    gamedata.local_player_.AnimateToHorizontal()  # change player image
                    door = True


    elif down:
        if gamedata.local_player_position_y_ +1 <gamedata.map_height_ and not type(gamedata.current_map_[gamedata.local_player_position_y_ +1][gamedata.local_player_position_x_ ]) in gamedata.collision_objects_:  #if map not end and if no collision

            if type(gamedata.current_map_[gamedata.local_player_position_y_ +1][gamedata.local_player_position_x_ ]) == DefaultTile: #if sand
                sand = True #play sand audio

            Collect(gamedata, gamedata.local_player_position_y_ + 1, gamedata.local_player_position_x_) #try collect point
            gamedata.local_player_position_y_ += 1 #move player
            move = True

            gamedata.local_player_.AnimateToHorizontal() #change player image
            gamedata.local_player_.movement_going_down_ = True #animate movement

        elif gamedata.local_player_position_y_ + 2 < gamedata.map_height_ and gamedata.current_map_[gamedata.local_player_position_y_+2][gamedata.local_player_position_x_] == None: #if map not end and if index is empty
            if type(gamedata.current_map_[gamedata.local_player_position_y_ +1][gamedata.local_player_position_x_]) == Door: #if door
                if gamedata.current_map_[gamedata.local_player_position_y_ +1][gamedata.local_player_position_x_].direction_ == 3:  # if the direction of the door is to the down
                    gamedata.local_player_position_y_ += 2  # move player
                    gamedata.local_player_.AnimateToHorizontal()  #change player image

                    door = True

            #if key door
            if type(gamedata.current_map_[gamedata.local_player_position_y_ +1][gamedata.local_player_position_x_]) == LockedDoor and gamedata.current_map_[gamedata.local_player_position_y_ + 1][gamedata.local_player_position_x_].door_type_ == "green":
                if gamedata.local_player_have_green_key_ == True:
                    gamedata.local_player_position_y_ += 2  # move player
                    gamedata.local_player_.AnimateToHorizontal()  # change player image
                    door = True
            #if keydoor
            elif type(gamedata.current_map_[gamedata.local_player_position_y_ +1][gamedata.local_player_position_x_]) == LockedDoor and gamedata.current_map_[gamedata.local_player_position_y_ + 1][gamedata.local_player_position_x_].door_type_ == "blue":
                if gamedata.local_player_have_blue_key_ == True:
                    gamedata.local_player_position_y_ += 2  # move player
                    gamedata.local_player_.AnimateToHorizontal()  # change player image
                    door = True




    if type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_]) in gamedata.deadlys_objects_: #if a player hits a monster or explosion
        RestartLevel(gamedata,connection) #level failed
    elif type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_]) == Goal: #if player go to goal
        if gamedata.total_points_collected_ >= gamedata.required_score_: #if enough points collected
            #player in goal
            if gamedata.multiplayer_ == True: #if multiplayer
                connection.SendInGoal()


            gamedata.local_player_in_goal_ = True #local player in goal
            gamedata.local_player_position_x_ = original_x #cancel move
            gamedata.local_player_position_y_ = original_y #cancel move
            gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_] = None #delete player from map

            return #exit function
        else:
            gamedata.local_player_position_x_ = original_x #cancel move
            gamedata.local_player_position_y_ = original_y
            gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_] = gamedata.local_player_  # set player to map list

            gamedata.local_player_.StopMovementAnimation() #no movement animations if the player is not moved

    else: #no goal or level not failed
        gamedata.current_map_[original_y][original_x] = None
        gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_] = gamedata.local_player_ #set player to map list

        if sand == True:
            gamedata.audio_.PlayStepSound()

        if gamedata.multiplayer_ == True: #if multiplayer

            #send actions:
            if door == True: #if door
                connection.SendMove(right,left,up,down,True)
            elif push == True: #if pushing
                connection.SendPush(right,left)
            elif move == True: #if normal move
                connection.SendMove(right, left, up, down, False) #normal move




def Collect(gamedata:object, y:int, x:int):
    #try collect point/key from given location
    if type(gamedata.current_map_[y][x]) == Diamond:
        gamedata.current_map_[y][x] = None
        gamedata.points_collected_ += 1
        gamedata.total_points_collected_ += 1
        gamedata.audio_.PlayCollectSound()  # play sound
        return True

    elif type(gamedata.current_map_[y][x]) == Key:
        if gamedata.current_map_[y][x].key_type_ == "green":
            gamedata.local_player_have_green_key_ = True
            gamedata.current_map_[y][x] = None
            gamedata.audio_.PlayCollectSound()  # play sound
            return  True

        elif gamedata.current_map_[y][x].key_type_ == "blue":
            gamedata.local_player_have_blue_key_ = True
            gamedata.current_map_[y][x] = None
            gamedata.audio_.PlayCollectSound()  # play sound
            return  True
    return  False
def RemoveTile(gamedata:object,connection, right:bool, left:bool, up:bool, down:bool):
    '''
    remove tile next to player
    '''

    if right:
        if gamedata.local_player_position_x_ +1 < gamedata.map_width_: #if map not end
            if type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_+1]) == DefaultTile:
                gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ + 1] = None
                gamedata.audio_.PlayStepSound()
            elif Collect(gamedata, gamedata.local_player_position_y_, gamedata.local_player_position_x_ + 1): #try collect
                pass
            else:
                return #exit function

    elif left:
        if gamedata.local_player_position_x_ -1 >= 0:  # if map not end
            if type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1]) == DefaultTile:
                gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1] = None
                gamedata.audio_.PlayStepSound()
            elif Collect(gamedata, gamedata.local_player_position_y_, gamedata.local_player_position_x_ - 1): #try collect
                pass
            else:
                return #exit function

    elif up:
        if gamedata.local_player_position_y_ - 1 >= 0:  # if map not end
            if type(gamedata.current_map_[gamedata.local_player_position_y_-1][gamedata.local_player_position_x_]) == DefaultTile:
                gamedata.current_map_[gamedata.local_player_position_y_-1][gamedata.local_player_position_x_] = None
                gamedata.audio_.PlayStepSound()
            elif Collect(gamedata, gamedata.local_player_position_y_ - 1, gamedata.local_player_position_x_): #try  #try collect
                pass
            else:
                return #exit function

    elif down:
        if gamedata.local_player_position_y_ + 1 < gamedata.map_height_:  # if map not end
            if type(gamedata.current_map_[gamedata.local_player_position_y_+1][gamedata.local_player_position_x_]) == DefaultTile:
                gamedata.current_map_[gamedata.local_player_position_y_+1][gamedata.local_player_position_x_] = None
                gamedata.audio_.PlayStepSound()
            elif Collect(gamedata, gamedata.local_player_position_y_ + 1, gamedata.local_player_position_x_): #try collect
                pass
            else:
                return #exit function


    #if tile removed
    if gamedata.multiplayer_ == True: #if multiplayer
        connection.SendRemove(right,left,up,down) #send remove action



def Gravity(gamedata,connection):
    moved_left = False
    for y in range(gamedata.map_height_-1,-1,-1):
        for x in range(gamedata.map_width_-1,-1,-1):
            if type((gamedata.current_map_[y][x])) in gamedata.gravity_objects_: #if gravity objects

                if moved_left == True: #if the stone is moved to the left, the left square is skipped.
                    moved_left = False
                    continue

                if gamedata.current_map_[y][x].drop_: #if currently drop
                    if y + 1 < gamedata.map_height_: #if map not end


                        if gamedata.current_map_[y+1][x] != None: #falls on some tile
                            gamedata.audio_.PlayDropSound() #play audio

                        if type(gamedata.current_map_[y+1][x]) in gamedata.explosive2_: #if something falls on this tile
                            CreateExplosion(gamedata,connection,y+1,x) #create explosion
                            return

                        if gamedata.current_map_[y+1][x] != None:
                            if type(gamedata.current_map_[y][x]) == Tnt: #if tnt falls on something
                                CreateExplosion(gamedata,connection,y,x) #create explosion
                                return


                        if gamedata.current_map_[y+1][x] != None: #player dead
                            if type(gamedata.current_map_[y+1][x]) == Player:
                                RestartLevel(gamedata,connection)
                                return



                    else: #if map end
                        gamedata.audio_.PlayDropSound()  # play audio

                        if type(gamedata.current_map_[y][x]) == Tnt:
                            CreateExplosion(gamedata,connection, y, x)


                if y + 1 < gamedata.map_height_:  # if map not end
                    if gamedata.current_map_[y+1][x] == None: #if below is empty
                        #move downwards:
                        gamedata.current_map_[y][x].drop_ = True

                        gamedata.current_map_[y][x].movement_going_down_ = True #animate movement

                        #set object to new location
                        gamedata.current_map_[y+1][x] = gamedata.current_map_[y][x]
                        gamedata.current_map_[y][x] = None
                    else:

                        if type(gamedata.current_map_[y][x]) in [Stone,Diamond]: #if stone or diamond
                            if type(gamedata.current_map_[y+1][x]) in gamedata.gravity_objects_2_: #if below is stone or diamond

                                if x-1 >= 0: #if map not end
                                    if gamedata.current_map_[y][x-1] == None and gamedata.current_map_[y+1][x-1] == None: #if empty on the left
                                        gamedata.current_map_[y][x].movement_going_left_ = True #animate movement
                                        gamedata.current_map_[y][x].Rotate(2) #rotate image

                                        moved_left = True
                                        #set object to new location:
                                        gamedata.current_map_[y][x-1] = gamedata.current_map_[y][x] #move object to left
                                        gamedata.current_map_[y][x] = None

                                        continue


                                if x +1 < gamedata.map_width_: #if map not end
                                    if gamedata.current_map_[y][x+1] == None and gamedata.current_map_[y+1][x+1] == None: #if empty on the right

                                        gamedata.current_map_[y][x].movement_going_right_ = True #animate movement
                                        gamedata.current_map_[y][x].Rotate(1) #rotate image

                                        #set object to new location:
                                        gamedata.current_map_[y][x+1] = gamedata.current_map_[y][x] #move object to right
                                        gamedata.current_map_[y][x] = None

                                        continue




                        gamedata.current_map_[y][x].drop_ = False #drop stopping


                else:
                    gamedata.current_map_[y][x].drop_ = False #drop stopping


def MoveMonsters(gamedata:object,connection:object):

    def TryGoRight(gamedata,y,x):
        if x +1 < gamedata.map_width_: #if map not end
            if gamedata.current_map_[y][x+1] == None or type(gamedata.current_map_[y][x+1]) == Player:
                return True
        return False
    def TryGoDown(gamedata,y,x):
        if y + 1 < gamedata.map_height_: #if map not end
            if gamedata.current_map_[y+1][x] == None or type(gamedata.current_map_[y+1][x]) == Player:
                return True
        return False


    def TryGoLeft(gamedata,y,x):
        if x-1 >= 0: #if map not end
            if gamedata.current_map_[y][x-1] == None or  type(gamedata.current_map_[y][x-1]) == Player:
                return True
        return False

    def TryGoUp(gamedata, y, x):
        if y-1 >= 0: #if map not end
            if gamedata.current_map_[y - 1][x] == None or type(gamedata.current_map_[y - 1][x]) == Player:
                return True
        return False


    for y in range(gamedata.map_height_): #iterated map
        for x in range(gamedata.map_width_):
            if type(gamedata.current_map_[y][x]) == Monster: #if monster

                move_up = False #move up
                move_down = False #move down
                move_right = False #move right
                move_left = False #move left

                ##############
                if gamedata.current_map_[y][x].direction_ == 1: #right
                    if TryGoRight(gamedata,y,x) == False:
                        if TryGoDown(gamedata,y,x) == False:
                            if TryGoUp(gamedata,y,x) == False:
                                if TryGoLeft(gamedata, y, x) == False:
                                    pass
                                else:
                                    gamedata.current_map_[y][x].direction_ = 3  # set direction to left
                                    move_left = True
                            else:
                                gamedata.current_map_[y][x].direction_ = 4  # set direction to up
                                move_up = True
                        else:
                            gamedata.current_map_[y][x].direction_ = 2 #set direction to down
                            move_down = True
                    else:
                        move_right = True

                ##############
                elif gamedata.current_map_[y][x].direction_ == 2: #down
                    if TryGoDown(gamedata,y,x) == False:
                        if TryGoLeft(gamedata,y,x) == False:
                            if TryGoRight(gamedata,y,x) == False:
                                if TryGoUp(gamedata,y,x) == False:
                                    pass
                                else:
                                    gamedata.current_map_[y][x].direction_ = 4 #set direction to up
                                    move_up = True
                            else:
                                gamedata.current_map_[y][x].direction_ = 1 #set direction to right
                                move_right = True
                        else:
                            gamedata.current_map_[y][x].direction_ = 3 #set direction to left
                    else:
                        move_down = True

                ##############
                elif gamedata.current_map_[y][x].direction_ == 3: #left
                    if TryGoLeft(gamedata,y,x) == False:
                        if TryGoUp(gamedata,y,x) == False:
                            if TryGoDown(gamedata,y,x) == False:
                                if TryGoRight(gamedata,y,x) == False:
                                    pass
                                else:
                                    gamedata.current_map_[y][x].direction_ = 1 #set direction to right
                                    move_right = True
                            else:
                                gamedata.current_map_[y][x].direction_ = 2 #set direction to down
                        else:
                            gamedata.current_map_[y][x].direction_ = 4 #set direction to up
                    else:
                        move_left = True

                ################
                elif gamedata.current_map_[y][x].direction_ == 4: #up
                    if TryGoUp(gamedata,y,x) == False:
                        if TryGoRight(gamedata,y,x) == False:
                            if TryGoLeft(gamedata,y,x) == False:
                                if TryGoDown(gamedata,y,x) == False:
                                    pass
                                else:
                                    gamedata.current_map_[y][x].direction_ = 2 #set direcion to down
                                    move_down = True

                            else:
                                gamedata.current_map_[y][x].direction_ = 3 #set direction to left
                                move_left = True
                        else:
                            gamedata.current_map_[y][x].direction_ = 1 #set direction to right
                            move_right = True
                    else:
                        move_up = True



                #move monster:
                if any([move_right, move_left, move_up, move_down]):

                    if gamedata.current_map_[y][x].moved_during_this_function_call_ == False: #the monster is moved only once in function call

                        if move_up:
                            move_y = y - 1
                            move_x = x
                            gamedata.current_map_[y][x].movement_going_up_ = True #animate movement
                        elif move_down:
                            move_y = y + 1
                            move_x = x
                            gamedata.current_map_[y][x].movement_going_down_ = True #animate movement
                        elif move_right:
                            move_x = x + 1
                            move_y = y
                            gamedata.current_map_[y][x].movement_going_right_ = True #animate movement
                        elif move_left:
                            move_x = x - 1
                            move_y = y
                            gamedata.current_map_[y][x].movement_going_left_ = True #animate movement

                        if type(gamedata.current_map_[move_y][move_x]) == Player: #a monster hits a player
                            RestartLevel(gamedata,connection) #level failed
                            return #exit function



                        #set monster to new location:
                        gamedata.current_map_[move_y][move_x] = gamedata.current_map_[y][x]
                        gamedata.current_map_[y][x] = None
                        gamedata.current_map_[move_y][move_x].moved_during_this_function_call_ = True






    #moved_during_this_function_call_ variable to false
    #and change monster image
    for y in range(gamedata.map_height_): #iterated map
        for x in range(gamedata.map_width_):
            if type(gamedata.current_map_[y][x]) == Monster: #if monster
                gamedata.current_map_[y][x].moved_during_this_function_call_ = False

                # change monster image
                if gamedata.current_map_[y][x].image_number_ == 1:
                    gamedata.current_map_[y][x].image_number_ = 2
                else:
                    gamedata.current_map_[y][x].image_number_ = 1




def CreateExplosion(gamedata:object,connection:object,y:int,x:int):

    '''
    create 3x3 explosion at the given location
    '''


    list1 = [0,0,0,1,1,1,-1,-1,-1] #y
    list2 = [1,-1,0,1,-1,0,1,-1,0] #x

    for i in range(len(list1)):

        if y + list1[i] >= 0 and y + list1[i] < gamedata.map_height_: #if map not end
            if x + list2[i] >= 0 and x + list2[i] < gamedata.map_width_:  # if map not end

                if type(gamedata.current_map_[y+list1[i]][x+list2[i]]) == Player: #if player explose
                    RestartLevel(gamedata,connection) #restart level
                    return "exit"

                if type(gamedata.current_map_[y+list1[i]][x+list2[i]]) != Bedrock: #if not Bedrock
                    if type(gamedata.current_map_[y+list1[i]][x+list2[i]]) in gamedata.explosive_: #if tnt, monster...
                        gamedata.current_map_[y + list1[i]][x + list2[i]] = Explosion()

                        # create new explosion:
                        if CreateExplosion(gamedata,connection,y+list1[i],x+list2[i]) == "exit": #if player explose
                            #player explose
                            #exit function
                            return "exit"


                    gamedata.current_map_[y+list1[i]][x+list2[i]] = Explosion()
                    gamedata.audio_.PlayExplosionSound() #play sound




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





def DrawPauseMenu(gamedata, pausemenu_number: int = 1):
    '''
    pausemenu_number
    1 = back to game, 2 = restart level, 3 = exit level
    '''

    font = gamedata.font_

    head_text = font.render('Pause Menu', True, (255, 255, 255))


    #the selected text is drawn in black
    if pausemenu_number == 1:
        text1 = font.render('Resume game', True, (0, 0, 0))
    else:
        text1 = font.render('Resume game', True, (255, 255, 255))
    if pausemenu_number == 2:
        text2 = font.render('Restart level', True, (0, 0, 0))
    else:
        text2 = font.render('Restart level', True, (255, 255, 255))
    if pausemenu_number == 3:
        text3 = font.render('Exit level', True, (0, 0, 0))
    else:
        text3 = font.render('Exit level', True, (255, 255, 255))

    x, y = gamedata.screen_.get_size() #get screen size

    pygame.draw.rect(gamedata.screen_, (50, 50, 50), pygame.Rect(x // 2 - 200, y // 2 - 200, 400, 400))  #draw a box in the center of the screen



    # draw the texts:
    gamedata.screen_.blit(head_text, (gamedata.head_text_position_x_, gamedata.head_text_position_y_))  # draw title
    gamedata.screen_.blit(text1, (gamedata.text1_position_x_, gamedata.text1_position_y_))
    gamedata.screen_.blit(text2, (gamedata.text2_position_x_, gamedata.text2_position_y_))
    gamedata.screen_.blit(text3, (gamedata.text3_position_x_, gamedata.text3_position_y_))


def RestartLevel(gamedata:object,connection:object=None,sendrestartlevel:bool = True):

    if connection != None and sendrestartlevel == True:
            connection.SendRestartLevel() #send restart level message

    SetMap(gamedata, gamedata.original_mapstr_)  #set original map to current map

    #init gamedata:
    gamedata.points_collected_ = 0
    gamedata.total_points_collected_ = 0
    gamedata.InitTimer() #init timer

    gamedata.local_player_in_goal_ = False
    gamedata.remote_player_in_goal_ = False
    gamedata.local_player_have_green_key_ = False
    gamedata.local_player_have_blue_key_ = False

    #draw map:
    gamedata.screen_.fill((0,0,0))
    gamedata.DrawMap()
    gamedata.DrawInfoPanel()


    #draw "GAME OVER" text:
    timesleep = pygame.time.get_ticks()
    text = gamedata.big_size_font_.render("GAME OVER", True,(153, 0, 0),(0,0,0)) #create text

    while pygame.time.get_ticks() < timesleep +700: #wait 0,7 seconds
        gamedata.screen_.blit(text,(gamedata.screen_width_//2 - text.get_width()//2,gamedata.screen_height_ //2- gamedata.infopanel_height_)) #draw text to screen
        pygame.display.flip()  #update screen




def ExecuteAction(gamedata:object,connection:object,action:str):

    #execute a other player actions
    action = action.split(":") #split str to list
    position_x = gamedata.remote_player_position_x_ #rename variable name to short in this function
    position_y = gamedata.remote_player_position_y_

    if action[0] == "moveright":
        if action[1] == "0": #no door
            gamedata.remote_player_.movement_going_right_ = True #animate movement

            #move player:
            gamedata.remote_player_position_x_ += 1 #move player

            if type(gamedata.current_map_[position_y][position_x+1]) == Diamond: #if diamond
                gamedata.total_points_collected_ += 1
                gamedata.audio_.PlayCollectSound() #play audio

            gamedata.current_map_[position_y][position_x+1] = gamedata.remote_player_ #place the player to new location
            gamedata.current_map_[position_y][position_x] = None #remote player from current position

        elif action[1] == "1": #door
            gamedata.remote_player_position_x_ += 2 #move player
            gamedata.current_map_[position_y][position_x+2] = gamedata.remote_player_ #place the player to new location
            gamedata.current_map_[position_y][position_x] = None #remote player from current position

        gamedata.remote_player_.AnimateToRight() #change player image

    elif action[0] ==  "moveleft":
        if action[1] == "0": #no door
            gamedata.remote_player_.movement_going_left_ = True #animate movement


            #move player:
            gamedata.remote_player_position_x_ -= 1

            if type(gamedata.current_map_[position_y][position_x-1]) == Diamond: #if diamond
                gamedata.total_points_collected_ += 1
                gamedata.audio_.PlayCollectSound() #play audio

            gamedata.current_map_[position_y][position_x-1] = gamedata.remote_player_ #place the player to new location
            gamedata.current_map_[position_y][position_x] = None #remote player from current position

        elif action[1] == "1": #door
            gamedata.remote_player_position_x_ -= 2 #move player
            gamedata.current_map_[position_y][position_x-2] = gamedata.remote_player_ #place the player to new location
            gamedata.current_map_[position_y][position_x] = None #remote player from current position

        gamedata.remote_player_.AnimateToLeft() #change player image

    elif action[0] == "movedown":
        if action[1] == "0": #no door
            gamedata.remote_player_.movement_going_down_ = True #animate movement


            gamedata.remote_player_position_y_ += 1 #move player
            if type(gamedata.current_map_[position_y + 1][position_x]) == Diamond: #if diamond
                gamedata.total_points_collected_ += 1
                gamedata.audio_.PlayCollectSound() #play audio

            gamedata.current_map_[position_y+1][position_x] = gamedata.remote_player_ #place the player to new location
            gamedata.current_map_[position_y][position_x] = None #remote player from current position

        elif action[1] == "1": #door
            gamedata.remote_player_position_y_ += 2 #move player
            gamedata.current_map_[position_y+2][position_x] = gamedata.remote_player_ #place the player to new location
            gamedata.current_map_[position_y][position_x] = None #remote player from current position

        gamedata.remote_player_.AnimateToHorizontal() #change player image

    elif action[0] == "moveup":
        if action[1] == "0": #no door
            gamedata.remote_player_.movement_going_up_ = True #animate movement

            gamedata.remote_player_position_y_ -= 1 #move player

            if type(gamedata.current_map_[position_y - 1][position_x]) == Diamond: #if diamond
                gamedata.total_points_collected_ += 1
                gamedata.audio_.PlayCollectSound() #play audio

            gamedata.current_map_[position_y-1][position_x] = gamedata.remote_player_ #place the player to new location
            gamedata.current_map_[position_y][position_x] = None #remote player from current position

        elif action[1] == "1": #door
            gamedata.remote_player_position_y_ -= 2 #move player
            gamedata.current_map_[position_y-2][position_x] = gamedata.remote_player_ #place the player to new location
            gamedata.current_map_[position_y][position_x] = None #remote player from current position

        gamedata.remote_player_.AnimateToHorizontal() #change player image

    elif action[0] == "pushright":

        if type(gamedata.current_map_[position_y][position_x + 1]) == Stone: #if the player pushes a stone
            gamedata.current_map_[position_y][position_x + 1].Rotate(1) #rotate stone image

        gamedata.remote_player_position_x_ += 1  # move player
        gamedata.current_map_[position_y][position_x+2] = gamedata.current_map_[position_y][position_x+1] #place the pushing object to new location
        gamedata.current_map_[position_y][position_x + 1] = gamedata.remote_player_ #place the player to new location
        gamedata.current_map_[position_y][position_x] = None  # remote player from current position
        gamedata.remote_player_.AnimateToRight() #change player image
        gamedata.audio_.PlayPushSound() #play audio


    elif action[0] == "pushleft":

        if type(gamedata.current_map_[position_y][position_x - 1]) == Stone: #if the player pushes a stone
            gamedata.current_map_[position_y][position_x - 1].Rotate(2) #rotate stone image

        gamedata.remote_player_position_x_ -= 1  # move player
        gamedata.current_map_[position_y][position_x-2] = gamedata.current_map_[position_y][position_x-1] #place the pushing object to new location
        gamedata.current_map_[position_y][position_x - 1] = gamedata.remote_player_ #place the player to new location
        gamedata.current_map_[position_y][position_x] = None  # remote player from current position
        gamedata.remote_player_.AnimateToLeft() #change player image
        gamedata.audio_.PlayPushSound() #play audio


    if action[0] == "removeright":
        if type(gamedata.current_map_[position_y][position_x+1]) == Diamond:  # if diamond
            gamedata.total_points_collected_ += 1
            gamedata.audio_.PlayCollectSound()  # play audio
        gamedata.current_map_[position_y][position_x+1] = None #remove tile next to remoteplayer

    elif action[0] == "removedown":
        if type(gamedata.current_map_[position_y+1][position_x]) == Diamond:  # if diamond
            gamedata.total_points_collected_ += 1
            gamedata.audio_.PlayCollectSound()  # play audio
        gamedata.current_map_[position_y+1][position_x] = None  # remove tile next to remoteplayer

    elif action[0] == "removeleft":
        if type(gamedata.current_map_[position_y][position_x-1]) == Diamond:  # if diamond
            gamedata.total_points_collected_ += 1
            gamedata.audio_.PlayCollectSound()  # play audio
        gamedata.current_map_[position_y][position_x - 1] = None  # remove tile next to remoteplayer

    elif action[0] == "removeup":
        if type(gamedata.current_map_[position_y-1][position_x]) == Diamond:  # if diamond
            gamedata.total_points_collected_ += 1
            gamedata.audio_.PlayCollectSound()  # play audio

        gamedata.current_map_[position_y-1][position_x] = None  # remove tile next to remoteplayer



def Run(gamedata:object,connection:object = None)->bool:
    '''
    game main function

    return: level_completed:bool,connection_fail:bool
    '''

    right = False
    left = False
    up = False
    down = False
    space = False
    enter = False

    pausemenu_is_active = False
    pausemenu_number = 1  #1 = back to game, 2 = restart level, 3 = exit level


    clock = pygame.time.Clock() #fps limit

    #set speed control variables:
    if gamedata.multiplayer_ == True: #if multiplayer
        gravity_counter,gravity_speed = 0,4  #execute gravity every 4 loops
        player_move_counter,player_speed = 0,3 #player speedlimit
        monstermove_counter,monster_speed = 0,5 #move monster every 5 loops

    else: #singelplayer
        gravity_counter,gravity_speed = 0,5  #execute gravity every 5 loops
        player_move_counter,player_speed = 0,3 #player speecd limit
        monstermove_counter,monster_speed = 0,6 #move monster every 6 loops


    image_switching_counter, image_switching_speed = 0,5 #set remoteplayer image to default image if not move


    gamedata.InitTimer() #init timer

    if connection != None and gamedata.server_ == False:  # if multiplayer and this is client
        #client send first message
        connection.SendPass()

    loopcount = 0 #Variable loopCount keeps track of how many times the main loop has been executed




    while True: #game main loop

        if connection != None: #if multiplayer
            # send some message every loop round
            connection.message_sended_this_loop_round_ = False

        #Todo update this?
        if gamedata.total_points_collected_ >= gamedata.required_score_: #if required score have been collected
            Goal.goal_is_open = True #change goal image
        else:
            Goal.goal_is_open = False #change goal image



        if gamedata.local_player_in_goal_: #if local player in goal

            if gamedata.multiplayer_: #if multiplayer
                if gamedata.remote_player_in_goal_ == True:
                    #level completed:
                    connection.CloseSocket()  # close socket
                    return True,False # back to menu, level completed

            else: #if singleplayer
                return True,False #back to menu


        #timer:
        if gamedata.level_timelimit_ != 0: #if level has timelimit
            if gamedata.Timer() >= gamedata.level_timelimit_: #time out
                RestartLevel(gamedata,connection) #restart level





        for event in pygame.event.get(): #pygame event loop
            #read keyboard
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE: #if esc is pressed
                    pausemenu_is_active = True


                if event.key == pygame.K_RETURN: #enter
                    enter = True
                if event.key == pygame.K_SPACE: #space
                    space = True


                #arrowkeys
                if event.key == pygame.K_LEFT:
                    left = True
                if event.key == pygame.K_RIGHT:
                    right = True

                if event.key == pygame.K_UP:
                    up = True

                if event.key == pygame.K_DOWN:
                    down = True


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN: #enter
                    enter = False
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_UP:
                    up = False
                if event.key == pygame.K_DOWN:
                    down = False
                if event.key == pygame.K_SPACE: #space
                    space = False



            if event.type == pygame.QUIT:  #exit program
                if gamedata.multiplayer_: #if multiplayer
                    connection.SendGameExit()
                    connection.CloseSocket()  #close socket
                return False,False #back to menu


            if event.type == pygame.MOUSEBUTTONUP: #if mouse button click
                if pausemenu_is_active == True:
                    mouse_position = pygame.mouse.get_pos() #get mouse position
                    number = gamedata.GetPauseMenuButtonNumber(mouse_position) #check is the mouse touches the button

                    if number != None:
                        if number == 1: #return game
                            pausemenu_is_active = False
                        elif number == 2: #restart level
                            RestartLevel(gamedata,connection)
                        elif number == 3: #exit level
                            if gamedata.multiplayer_: #if multiplayer
                                connection.SendGameExit()
                                connection.CloseSocket()  # close socket
                            return False, False  #back to menu
                        pausemenu_is_active = False #diasble the pause menu if menu button is pressed with the mouse.
        if enter == True: #if enter is pressed
            if pausemenu_is_active == True: #if pausemenu is active
                if pausemenu_number == 1: #exit pause menu
                    pausemenu_is_active = False
                elif pausemenu_number == 2: #restart level
                    RestartLevel(gamedata,connection)

                    pausemenu_is_active = False
                elif pausemenu_number == 3: #exit level
                    if gamedata.multiplayer_: #if multiplayer
                        connection.SendGameExit()
                        connection.CloseSocket()  #close socket
                    return False,False  # back to menu



        if loopcount > gravity_counter+gravity_speed: #gravity
            gravity_counter = loopcount
            Gravity(gamedata,connection) #gravity



        if loopcount > monstermove_counter+monster_speed: #move monster
            monstermove_counter = loopcount
            MoveMonsters(gamedata,connection) #move monsters



        if [right, left, up, down].count(True) > 0:  #if arrow key is pressed
            if loopcount > player_move_counter+player_speed: #speed limit
                player_move_counter = loopcount
                if pausemenu_is_active == False:

                    if gamedata.local_player_in_goal_ == False: #if player in goal, can't move
                        if space: #if space pressed
                            RemoveTile(gamedata,connection, right, left, up, down) #remove tile in left,right,up or down
                        else:
                            Move(gamedata,connection,right,left,up,down) #move player


                else: #pause menu is active
                    if up:
                        if pausemenu_number != 3:
                            pausemenu_number += 1
                        else:
                            pausemenu_number = 1
                    elif down:
                        if pausemenu_number != 1:
                            pausemenu_number -= 1
                        else:
                            pausemenu_number = 3

        else: #no move
            if loopcount > player_move_counter+player_speed: #speed limit
                #set player image to defaultimage
                if gamedata.local_player_.animated_ == True:
                    if gamedata.local_player_.image_number_ != 0:
                        gamedata.local_player_.image_number_ = 0


        DeleteExplosion(gamedata) #delete exlplosions

        gamedata.screen_.fill((0, 0, 0))  # set backcolor
        gamedata.DrawMap()  #draw map
        gamedata.DrawInfoPanel() #draw infopanel

        if pausemenu_is_active == True: #if pausemenu is active
            DrawPauseMenu(gamedata,pausemenu_number) #draw pausemenu
        pygame.display.flip()  #update screen




        if connection != None: #if multiplayer
            if connection.message_sended_this_loop_round_ == False:
                #send some message every loop round
                connection.SendPass() #send pass message




        '''
        read socket and execute another player actions
        '''
        if gamedata.multiplayer_: #if multiplayer
            if connection.connected_ == True:

                connection.Read()  # read socket

                try: # read the content of the message

                    if connection.data_type_ == "action": #if message is action
                        ExecuteAction(gamedata,connection,connection.data_) #execute a other player actions
                        image_switching_counter = loopcount
                    else: #if no action
                        if loopcount > image_switching_counter + image_switching_speed: #timelimit
                            image_switching_counter = loopcount
                            gamedata.remote_player_.image_number_ = 0 #set remote player image to default image

                    if connection.data_type_ == "restartlevel":
                        RestartLevel(gamedata)

                    elif connection.data_type_ == "ingoal":
                        gamedata.remote_player_in_goal_ = True
                        gamedata.current_map_[gamedata.remote_player_position_y_][gamedata.remote_player_position_x_] = None

                    elif connection.data_type_ == "gameexit":
                        connection.CloseSocket()  # close socket
                        return False,False #back to menu, level not completed

                    connection.BufferNext() #delete first message from buffer

                except Exception as error_message: #incorrect message
                    print("incorrect socket message")
                    print(error_message)
                    connection.CloseSocket()  # close socket
                    return False,True  # back to menu, level not completed

            else: #if connection lost
                connection.CloseSocket()  # close socket
                print(connection.error_message_)
                return False, True  # back to menu, level not completed



        clock.tick(30) #fps limit
        loopcount += 1