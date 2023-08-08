import pygame

from src import *




def Move(gamedata:object,connection:object,right:bool,left:bool,up:bool,down:bool):
    '''
    move local player

    if multiplayer, send action
    '''

    collisions = gamedata.collision_objects_
    pushing = gamedata.pushing_objects_

    original_x = gamedata.local_player_position_x_
    original_y = gamedata.local_player_position_y_
    if right:
        if gamedata.local_player_position_x_ + 1 < gamedata.map_width_ and not type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ +1]) in collisions:  #if map not end and if no collision
            CollectPoints(gamedata, gamedata.local_player_position_y_, gamedata.local_player_position_x_+1) #try collect point
            gamedata.local_player_position_x_ += 1 #move player

            if gamedata.multiplayer_ == True: #if multiplayer
                connection.SendMove(right,left,up,down) #send action

            if gamedata.local_player_.animated_ == True: #if player is animated
                gamedata.local_player_.AnimateToRight() #animate player image

        #if no default tile or diamond
        #if pushing objects
        elif gamedata.local_player_position_x_+2 < gamedata.map_width_ and gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ + 2] == None: #if map not end and if index is empty
            if type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ + 1]) in pushing: #if pushing objects
                if gamedata.pushing_right_ == 0: #the player moves slower if it pushes a rock
                    gamedata.pushing_right_ = 1
                elif gamedata.pushing_right_ == 1:
                    if type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ + 1]) == Stone: #if stone
                        gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_+1].Rotate(1) #rotate image
                    gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ + 2] =  gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ + 1] #place the pushing object new position
                    gamedata.local_player_position_x_ += 1  # move player
                    gamedata.pushing_right_ = 0

                    if gamedata.multiplayer_ == True: #if multiplayer
                        connection.SendPush(right,left) #send push action

                    if gamedata.local_player_.animated_ == True:  # if player is animated
                        gamedata.local_player_.AnimateToRight() #animate player image

            #if door
            elif type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ + 1]) == Door: #if door
                if gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ + 1].direction_ == 2: #if the direction of the door is to the right
                    gamedata.local_player_position_x_ += 2 #move player
                    if gamedata.multiplayer_ == True:  # if multiplayer
                        connection.SendMove(right, left, up, down,True)  # send action


    if left:
        if gamedata.local_player_position_x_-1 >= 0 and not type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1]) in collisions:  #if map not end and if no collision
            CollectPoints(gamedata, gamedata.local_player_position_y_, gamedata.local_player_position_x_-1) #try collect point
            gamedata.local_player_position_x_ -= 1 #move player
            
            if gamedata.multiplayer_ == True: #if multiplayer
                connection.SendMove(right,left,up,down) #send action

            if gamedata.local_player_.animated_ == True: #if player is animated
                gamedata.local_player_.AnimateToLeft() #animate player image

        #if pushing objects
        elif gamedata.local_player_position_x_-2 >= 0 and gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 2] == None: #if map not end if index is empty
            if type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1]) in pushing: #if pushing objects
                if gamedata.pushing_left_ == 0: #the player moves slower if it pushes a rock
                    gamedata.pushing_left_ = 1
                elif gamedata.pushing_left_ == 1:
                    if type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1]) == Stone: #if stone
                        gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1].Rotate(2) #rotate image
                    gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 2] =  gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1] #set stone new position
                    gamedata.local_player_position_x_ -= 1 #move player
                    gamedata.pushing_left_ = 0

                    if gamedata.multiplayer_ == True: #if multiplayer
                        connection.SendPush(right,left) #send push action

                    if gamedata.local_player_.animated_ == True:  # if player is animated
                        gamedata.local_player_.AnimateToLeft() #animate player image

            #if door
            elif type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1]) == Door: #if door
                if gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1].direction_ == 4: #if the direction of the door is to the left
                    gamedata.local_player_position_x_ -= 2 #move player
                    if gamedata.multiplayer_ == True:  # if multiplayer
                        connection.SendMove(right, left, up, down,True)  # send action


    if up:
        if gamedata.local_player_position_y_ - 1 >= 0 and not type(gamedata.current_map_[gamedata.local_player_position_y_ -1][gamedata.local_player_position_x_]) in collisions:  #if map not end and if no collision
            CollectPoints(gamedata, gamedata.local_player_position_y_ - 1, gamedata.local_player_position_x_) #try collect point
            gamedata.local_player_position_y_ -= 1 #move player

            if gamedata.multiplayer_ == True: #if multiplayer
                connection.SendMove(right,left,up,down) #send action

            if gamedata.local_player_.animated_ == True: #if player is animated
                gamedata.local_player_.AnimateToHorizontal() #animate player image

        #if door
        elif gamedata.local_player_position_y_ - 2 >= 0 and gamedata.current_map_[gamedata.local_player_position_y_-2][gamedata.local_player_position_x_] == None: #if map not end and if index is empty
            if type(gamedata.current_map_[gamedata.local_player_position_y_ -1][gamedata.local_player_position_x_]) == Door: #if door
                if gamedata.current_map_[gamedata.local_player_position_y_-1][gamedata.local_player_position_x_].direction_ == 1: #if the direction of the door is to the up
                    gamedata.local_player_position_y_ -= 2 #move player
                    if gamedata.multiplayer_ == True:  # if multiplayer
                        connection.SendMove(right, left, up, down,True)  # send action


    if down:
        if gamedata.local_player_position_y_ +1 <gamedata.map_height_ and not type(gamedata.current_map_[gamedata.local_player_position_y_ +1][gamedata.local_player_position_x_ ]) in collisions:  #if map not end and if no collision
            CollectPoints(gamedata,gamedata.local_player_position_y_ +1,gamedata.local_player_position_x_) #try collect point
            gamedata.local_player_position_y_ += 1 #move player

            if gamedata.multiplayer_ == True: #if multiplayer
                connection.SendMove(right,left,up,down) #send action

            if gamedata.local_player_.animated_ == True:  # if player is animated
                gamedata.local_player_.AnimateToHorizontal() #animate player image
        #if door
        elif gamedata.local_player_position_y_ + 2 < gamedata.map_height_ and gamedata.current_map_[gamedata.local_player_position_y_+2][gamedata.local_player_position_x_] == None: #if map not end and if index is empty
            if type(gamedata.current_map_[gamedata.local_player_position_y_ +1][gamedata.local_player_position_x_]) == Door: #if door
                if gamedata.current_map_[gamedata.local_player_position_y_ +1][gamedata.local_player_position_x_].direction_ == 3:  # if the direction of the door is to the down
                    gamedata.local_player_position_y_ += 2  # move player
                    if gamedata.multiplayer_ == True:  # if multiplayer
                        connection.SendMove(right, left, up, down,True)  # send action



    if type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_]) in gamedata.deadlys_objects_: #if a player hits a monster or explosion
        RestartLevel(gamedata,connection) #level failed
    elif type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_]) == Goal: #if player go to goal
        if gamedata.total_points_collected_ >= gamedata.required_score_: #if enough points collected
            gamedata.level_complete_ = True #level complete
        else:
            gamedata.local_player_position_x_ = original_x #cancel move
            gamedata.local_player_position_y_ = original_y
            gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_] = gamedata.local_player_  # set player to map list

    else:
        gamedata.current_map_[original_y][original_x] = None
        gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_] = gamedata.local_player_ #set player to map list


def CollectPoints(gamedata:object,y:int,x:int):
    #try collect point from given location
    #return True/False
    if type(gamedata.current_map_[y][x]) == Diamond:
        gamedata.current_map_[y][x] = None
        gamedata.points_collected_ += 1
        gamedata.total_points_collected_ += 1
        return True

    return False

def RemoveTile(gamedata:object,connection, right:bool, left:bool, up:bool, down:bool):
    '''
    remove tile next to player
    '''

    if right:
        if gamedata.local_player_position_x_ +1 < gamedata.map_width_: #if map not end
            if type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_+1]) == DefaultTile:
                gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ + 1] = None
            elif CollectPoints(gamedata,gamedata.local_player_position_y_,gamedata.local_player_position_x_+1): #try collect points
                pass
            else:
                return #exit function

    elif left:
        if gamedata.local_player_position_x_ -1 >= 0:  # if map not end
            if type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1]) == DefaultTile:
                gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1] = None
            elif CollectPoints(gamedata,gamedata.local_player_position_y_,gamedata.local_player_position_x_-1): #try collect points
                pass
            else:
                return #exit function

    elif up:
        if gamedata.local_player_position_y_ - 1 >= 0:  # if map not end
            if type(gamedata.current_map_[gamedata.local_player_position_y_-1][gamedata.local_player_position_x_]) == DefaultTile:
                gamedata.current_map_[gamedata.local_player_position_y_-1][gamedata.local_player_position_x_] = None
            elif CollectPoints(gamedata,gamedata.local_player_position_y_-1,gamedata.local_player_position_x_): #try  #try collect pointscollect points
                pass
            else:
                return #exit function

    elif down:
        if gamedata.local_player_position_y_ + 1 < gamedata.map_height_:  # if map not end
            if type(gamedata.current_map_[gamedata.local_player_position_y_+1][gamedata.local_player_position_x_]) == DefaultTile:
                gamedata.current_map_[gamedata.local_player_position_y_+1][gamedata.local_player_position_x_] = None

            elif CollectPoints(gamedata,gamedata.local_player_position_y_+1,gamedata.local_player_position_x_): #try collect points
                pass
            else:
                return #exit function


    #if tile removed
    if gamedata.multiplayer_ == True: #if multiplayer
        connection.SendRemove(right,left,up,down) #send remove action


def Gravity(gamedata,connection):

    for y in range(gamedata.map_height_-1,-1,-1):
        for x in range(gamedata.map_width_-1,-1,-1):
            if type((gamedata.current_map_[y][x])) in gamedata.gravity_objects_: #if gravity objects
                if gamedata.current_map_[y][x].drop_: #if currently drop
                    if y + 1 < gamedata.map_height_: #if map not end
                        if type(gamedata.current_map_[y+1][x]) in gamedata.explosive2_: #if something falls on this tile
                            CreateExplosion(gamedata,connection,y+1,x) #create explosion
                            return

                        if gamedata.current_map_[y+1][x] != None:
                            if type(gamedata.current_map_[y][x]) == Tnt: #if tnt falls on something
                                CreateExplosion(gamedata,connection,y,x) #create explosion
                                return
                    else: #if map end
                        if type(gamedata.current_map_[y][x]) == Tnt:
                            CreateExplosion(gamedata,connection, y, x)


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
                                        gamedata.current_map_[y][x].Rotate(1)
                                        gamedata.current_map_[y][x] = None
                                        continue

                                if x-1 >= 0: #if map not end
                                    if gamedata.current_map_[y][x-1] == None and gamedata.current_map_[y+1][x-1] == None: #if empty on the left
                                        gamedata.current_map_[y][x-1] = gamedata.current_map_[y][x] #move stone to left
                                        gamedata.current_map_[y][x].Rotate(2)
                                        gamedata.current_map_[y][x] = None
                                        continue


                        gamedata.current_map_[y][x].drop_ = False
                else:
                    gamedata.current_map_[y][x].drop_ = False



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

    for y in range(gamedata.map_height_):
        for x in range(gamedata.map_width_):
            if type(gamedata.current_map_[y][x]) == Monster:
                move_x = x
                move_y = y

                ##############
                if gamedata.current_map_[y][x].direction_ == 1: #right
                    if TryGoRight(gamedata,y,x) == False:
                        if TryGoDown(gamedata,y,x) == False:
                            if TryGoUp(gamedata,y,x) == False:
                                if TryGoLeft(gamedata, y, x) == False:
                                    pass
                                else:
                                    gamedata.current_map_[y][x].direction_ = 3  # set direction to left
                                    move_x -= 1
                            else:
                                gamedata.current_map_[y][x].direction_ = 4  # set direction to up
                                move_y -= 1
                        else:
                            gamedata.current_map_[y][x].direction_ = 2 #set direction to down
                            move_y += 1
                    else:
                        move_x += 1

                ##############
                elif gamedata.current_map_[y][x].direction_ == 2: #down
                    if TryGoDown(gamedata,y,x) == False:
                        if TryGoLeft(gamedata,y,x) == False:
                            if TryGoRight(gamedata,y,x) == False:
                                if TryGoUp(gamedata,y,x) == False:
                                    pass
                                else:
                                    gamedata.current_map_[y][x].direction_ = 4 #set direction to up
                                    move_y -= 1
                            else:
                                gamedata.current_map_[y][x].direction_ = 1 #set direction to right
                                move_x += 1
                        else:
                            gamedata.current_map_[y][x].direction_ = 3 #set direction to left
                    else:
                        move_y += 1

                ##############
                elif gamedata.current_map_[y][x].direction_ == 3: #left
                    if TryGoLeft(gamedata,y,x) == False:
                        if TryGoUp(gamedata,y,x) == False:
                            if TryGoDown(gamedata,y,x) == False:
                                if TryGoRight(gamedata,y,x) == False:
                                    pass
                                else:
                                    gamedata.current_map_[y][x].direction_ = 1 #set direction to right
                                    move_x += 1
                            else:
                                gamedata.current_map_[y][x].direction_ = 2 #set direction to down
                        else:
                            gamedata.current_map_[y][x].direction_ = 4 #set direction to up
                    else:
                        move_x -= 1

                ################
                elif gamedata.current_map_[y][x].direction_ == 4: #up
                    if TryGoUp(gamedata,y,x) == False:
                        if TryGoRight(gamedata,y,x) == False:
                            if TryGoLeft(gamedata,y,x) == False:
                                if TryGoDown(gamedata,y,x) == False:
                                    pass
                                else:
                                    gamedata.current_map_[y][x].direction_ = 2 #set direcion to down
                                    move_y += 1

                            else:
                                gamedata.current_map_[y][x].direction_ = 3 #set direction to left
                                move_x -= 1
                        else:
                            gamedata.current_map_[y][x].direction_ = 1 #set direction to right
                            move_x += 1
                    else:
                        move_y -= 1


                if x != move_x or y != move_y:
                    if gamedata.current_map_[y][x].moved_during_this_function_call_ == False: #the monster is moved only once in function call
                        if type(gamedata.current_map_[move_y][move_x]) == Player: #a monster hits a player
                            RestartLevel(gamedata,connection) #level failed
                            return #exit function


                        #move monster:
                        gamedata.current_map_[move_y][move_x] = gamedata.current_map_[y][x]
                        gamedata.current_map_[y][x] = None
                        gamedata.current_map_[move_y][move_x].moved_during_this_function_call_ = True




    #moved_during_this_function_call_ variable to false
    #and change monster image
    for y in range(gamedata.map_height_):
        for x in range(gamedata.map_width_):
            if type(gamedata.current_map_[y][x]) == Monster:
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
        text1 = font.render('Back', True, (0, 0, 0))
    else:
        text1 = font.render('Back', True, (255, 255, 255))
    if pausemenu_number == 2:
        text2 = font.render('restart level', True, (0, 0, 0))
    else:
        text2 = font.render('restart level', True, (255, 255, 255))
    if pausemenu_number == 3:
        text3 = font.render('exit level', True, (0, 0, 0))
    else:
        text3 = font.render('exit level', True, (255, 255, 255))

    x, y = gamedata.screen_.get_size() #get screen size

    pygame.draw.rect(gamedata.screen_, (50, 50, 50), pygame.Rect(x // 2 - 200, y // 2 - 200, 400, 400))  #draw a box in the center of the screen

    #centering the text position
    text1_x = x // 2
    text1_x -= text1.get_width() // 2
    text1_y = y // 2

    text2_x = x // 2
    text2_x -= text2.get_width() // 2
    text2_y = y // 2

    text3_x = x // 2
    text3_x -= text3.get_width() // 2
    text3_y = y // 2

    head_x = x // 2
    head_x -= head_text.get_width() // 2
    head_y = y // 2 - 190

    # draw the texts:
    gamedata.screen_.blit(head_text, (head_x, head_y))  # draw title
    gamedata.screen_.blit(text1, (text1_x, text1_y))
    gamedata.screen_.blit(text2, (text2_x, text2_y - 50))
    gamedata.screen_.blit(text3, (text3_x, text3_y - 100))


def RestartLevel(gamedata:object,connection:object=None,sendrestartlevel:bool = True):

    SetMap(gamedata, gamedata.original_mapstr_, True)  #set original map to current map
    gamedata.points_collected_ = 0
    gamedata.total_points_collected_ = 0
    gamedata.InitTimer() #init timer

    if connection != None and sendrestartlevel == True:
            connection.SendRestartLevel()


def ExecuteAction(gamedata:object,connection:object,action:str):

    #execute a other player actions
    action = action.split(":") #split str to list
    position_x = gamedata.remote_player_position_x_ #temp variables
    position_y = gamedata.remote_player_position_y_

    if action[0] ==  "moveright":
        if action[1] == "0": #no door
            gamedata.remote_player_position_x_ += 1 #move player
            gamedata.current_map_[position_y][position_x+1] = gamedata.remote_player_ #place the player to new location
            gamedata.current_map_[position_y][position_x] = None #remote player from current position

        elif action[1] == "1": #door
            gamedata.remote_player_position_x_ += 2 #move player
            gamedata.current_map_[position_y][position_x+2] = gamedata.remote_player_ #place the player to new location
            gamedata.current_map_[position_y][position_x] = None #remote player from current position

        gamedata.remote_player_.AnimateToRight()

    elif action[0] ==  "moveleft":
        if action[1] == "0": #no door
            gamedata.remote_player_position_x_ -= 1 #move player
            gamedata.current_map_[position_y][position_x-1] = gamedata.remote_player_ #place the player to new location
            gamedata.current_map_[position_y][position_x] = None #remote player from current position

        elif action[1] == "1": #door
            gamedata.remote_player_position_x_ -= 2 #move player
            gamedata.current_map_[position_y][position_x-2] = gamedata.remote_player_ #place the player to new location
            gamedata.current_map_[position_y][position_x] = None #remote player from current position

        gamedata.remote_player_.AnimateToLeft()

    elif action[0] == "movedown":
        if action[1] == "0": #no door
            gamedata.remote_player_position_y_ += 1 #move player
            gamedata.current_map_[position_y+1][position_x] = gamedata.remote_player_ #place the player to new location
            gamedata.current_map_[position_y][position_x] = None #remote player from current position

        elif action[1] == "1": #door
            gamedata.remote_player_position_y_ += 2 #move player
            gamedata.current_map_[position_y+2][position_x] = gamedata.remote_player_ #place the player to new location
            gamedata.current_map_[position_y][position_x] = None #remote player from current position

        gamedata.remote_player_.AnimateToHorizontal()

    elif action[0] == "moveup":
        if action[1] == "0": #no door
            gamedata.remote_player_position_y_ -= 1 #move player
            gamedata.current_map_[position_y-1][position_x] = gamedata.remote_player_ #place the player to new location
            gamedata.current_map_[position_y][position_x] = None #remote player from current position

        elif action[1] == "1": #door
            gamedata.remote_player_position_y_ -= 2 #move player
            gamedata.current_map_[position_y-2][position_x] = gamedata.remote_player_ #place the player to new location
            gamedata.current_map_[position_y][position_x] = None #remote player from current position

        gamedata.remote_player_.AnimateToHorizontal()

    elif action[0] == "pushright":

        if type(gamedata.current_map_[position_y][position_x + 1]) == Stone: #if the player pushes a stone
            gamedata.current_map_[position_y][position_x + 1].Rotate(1) #rotae stone image

        gamedata.remote_player_position_x_ += 1  # move player
        gamedata.current_map_[position_y][position_x+2] = gamedata.current_map_[position_y][position_x+1] #place the pushing object to new location
        gamedata.current_map_[position_y][position_x + 1] = gamedata.remote_player_ #place the player to new location
        gamedata.current_map_[position_y][position_x] = None  # remote player from current position
        gamedata.remote_player_.AnimateToRight()



    elif action[0] == "pushleft":

        if type(gamedata.current_map_[position_y][position_x - 1]) == Stone: #if the player pushes a stone
            gamedata.current_map_[position_y][position_x - 1].Rotate(2) #rotate stone image

        gamedata.remote_player_position_x_ -= 1  # move player
        gamedata.current_map_[position_y][position_x-2] = gamedata.current_map_[position_y][position_x-1] #place the pushing object to new location
        gamedata.current_map_[position_y][position_x - 1] = gamedata.remote_player_ #place the player to new location
        gamedata.current_map_[position_y][position_x] = None  # remote player from current position
        gamedata.remote_player_.AnimateToLeft()


    if action[0] == "removeright":
        gamedata.current_map_[position_y][position_x+1] = None #remove tile next to remoteplayer

    elif action[0] == "removedown":
        gamedata.current_map_[position_y+1][position_x] = None  # remove tile next to remoteplayer

    elif action[0] == "removeleft":
        gamedata.current_map_[position_y][position_x - 1] = None  # remove tile next to remoteplayer

    elif action[0] == "removeup":
        gamedata.current_map_[position_y-1][position_x] = None  # remove tile next to remoteplayer



def Run(gamedata:object,connection:object = None)->bool:
    '''
    game main function

    return True if level complete
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

    movelimit = 0 #gravity and monster
    movelimit2 = 0 #player move

    timelimit = 0 #send collected points every 2 seconds
    timelimit2 = 0 #sets player image to default image if no move

    gamedata.InitTimer() #init timer

    while True: #game main loop



        if gamedata.level_complete_: #if level complete
            if gamedata.multiplayer_: #if multiplayer
                connection.SendGameExit(True)
                connection.CloseSocket()  # close socket
            return True # back to menu

        #timer:
        if gamedata.level_timelimit_ != 0: #if level has timelimit
            if gamedata.Timer() >= gamedata.level_timelimit_: #time out
                RestartLevel(gamedata,connection) #restart level



        #read socket
        if gamedata.multiplayer_:
            if connection.connected_ == True:

                try: #check connection
                    connection.Read()  # read socket
                except:
                    print("connection problem")

                try: # read the content of the message

                    if connection.data_type_ == "action": #if message is action
                        ExecuteAction(gamedata,connection,connection.data_) #execute a other player actions
                        timelimit2 = pygame.time.get_ticks()

                    else: #if remoteplayer no move
                        #set player image to default image:
                        if pygame.time.get_ticks() > timelimit2 +150: #timelimit
                            timelimit2 = pygame.time.get_ticks()
                            gamedata.remote_player_.image_number_ = 0



                    if connection.data_type_ == "points": #if message is collected points
                        gamedata.total_points_collected_ = gamedata.points_collected_ + connection.data_


                    elif connection.data_type_ == "restartlevel":
                        RestartLevel(gamedata)

                    elif connection.data_type_ == "map": #if message is map
                        #this feature is not used!!!
                        mapstr = connection.data_
                        SetMap(gamedata,mapstr) #set map

                    elif connection.data_type_ == "gameexit":
                        connection.CloseSocket()  # close socket
                        return connection.data_ #back to menu



                    connection.BufferNext() #delete first message from buffer


                except Exception as error_message: #if error
                    print(error_message) #print error message





        for event in pygame.event.get(): #pygame event loop
            #read keyboard
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE: #if esc is pressed
                    pausemenu_is_active = True


                if event.key == pygame.K_RETURN:
                    enter = True

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
                if event.key == pygame.K_RETURN:
                    enter = False
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
                if gamedata.multiplayer_:
                    connection.SendGameExit(False)
                    connection.CloseSocket()  #close socket
                return False #back to menu

        if enter == True:
            if pausemenu_is_active == True: #if pausemenu is active
                if pausemenu_number == 1: #exit pause menu
                    pausemenu_is_active = False
                elif pausemenu_number == 2: #restart level
                    RestartLevel(gamedata,connection)

                    pausemenu_is_active = False
                elif pausemenu_number == 3: #exit level
                    if gamedata.multiplayer_: #if multiplayer
                        connection.SendGameExit(False)
                        connection.CloseSocket()  # close socket
                    return False  # back to menu



        if pygame.time.get_ticks() > movelimit + 140: #gravity and monster moving
            movelimit = pygame.time.get_ticks()
            Gravity(gamedata,connection)
            MoveMonsters(gamedata,connection)


        if [right, left, up, down].count(True) == 1:  #can only move in one direction at a time
            if pygame.time.get_ticks() > movelimit2 + 100: #speed limit
                movelimit2 = pygame.time.get_ticks()
                if pausemenu_is_active == False:
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
            if pygame.time.get_ticks() > movelimit2 + 150: #speed limit
                #set player image to defaultimage
                if gamedata.local_player_.animated_ == True:
                    if gamedata.local_player_.image_number_ != 0:
                        gamedata.local_player_.image_number_ = 0



        if gamedata.multiplayer_ == True: #if multiplayer
            if pygame.time.get_ticks() > timelimit + 2000:  #send collected points every 2 seconds
                timelimit = pygame.time.get_ticks()
                connection.SendCollectedPoints(gamedata.points_collected_)

        DeleteExplosion(gamedata) #delete exlplosions


        gamedata.screen_.fill((0, 0, 0))  # set backcolor
        gamedata.DrawMap()  #draw map
        gamedata.DrawInfoPanel() #draw infopanel

        if pausemenu_is_active == True: #if pausemenu is active
            DrawPauseMenu(gamedata,pausemenu_number) #draw pausemenu
        pygame.display.flip()  #update screen
        clock.tick(30) #fps limit


