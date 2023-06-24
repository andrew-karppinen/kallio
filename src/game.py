import pygame

from src import *




def Move(gamedata:object,right:bool,left:bool,up:bool,down:bool):
    '''
    move local player
    '''

    collisions = gamedata.collision_objects_
    pushing = gamedata.pushing_objects_


    if right:
        if gamedata.local_player_position_x_ + 1 < gamedata.map_width_ and not type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ +1]) in collisions:  #if map not end and if no collision
            CollectPoints(gamedata, gamedata.local_player_position_y_, gamedata.local_player_position_x_+1) #try collect point
            gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_] = None
            gamedata.local_player_position_x_ += 1 #move player

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
                    gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ + 2] =  gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ + 1] #set stone new position
                    gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_] = None
                    gamedata.local_player_position_x_ += 1  # move player
                    gamedata.pushing_right_ = 0
                    if gamedata.local_player_.animated_ == True:  # if player is animated
                        gamedata.local_player_.AnimateToRight() #animate player image

            #if door
            elif type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ + 1]) == Door: #if door
                if gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ + 1].direction_ == 2: #if the direction of the door is to the right
                    gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_] = None
                    gamedata.local_player_position_x_ += 2 #move player


    if left:
        if gamedata.local_player_position_x_-1 >= 0 and not type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1]) in collisions:  #if map not end and if no collision
            CollectPoints(gamedata, gamedata.local_player_position_y_, gamedata.local_player_position_x_-1) #try collect point
            gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_] = None
            gamedata.local_player_position_x_ -= 1 #move player

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
                    gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_] = None
                    gamedata.local_player_position_x_ -= 1 #move player
                    gamedata.pushing_left_ = 0
                    if gamedata.local_player_.animated_ == True:  # if player is animated
                        gamedata.local_player_.AnimateToLeft() #animate player image

            #if door
            elif type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1]) == Door: #if door
                if gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1].direction_ == 4: #if the direction of the door is to the left
                    gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_] = None
                    gamedata.local_player_position_x_ -= 2 #move player


    if up:
        if gamedata.local_player_position_y_ - 1 >= 0 and not type(gamedata.current_map_[gamedata.local_player_position_y_ -1][gamedata.local_player_position_x_]) in collisions:  #if map not end and if no collision
            CollectPoints(gamedata, gamedata.local_player_position_y_ - 1, gamedata.local_player_position_x_) #try collect point
            gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_] = None
            gamedata.local_player_position_y_ -= 1 #move player

            if gamedata.local_player_.animated_ == True: #if player is animated
                gamedata.local_player_.AnimateToHorizontal() #animate player image

        #if door
        elif gamedata.local_player_position_y_ - 2 >= 0 and gamedata.current_map_[gamedata.local_player_position_y_-2][gamedata.local_player_position_x_] == None: #if map not end and if index is empty
            if type(gamedata.current_map_[gamedata.local_player_position_y_ -1][gamedata.local_player_position_x_]) == Door: #if door
                if gamedata.current_map_[gamedata.local_player_position_y_-1][gamedata.local_player_position_x_].direction_ == 1: #if the direction of the door is to the up
                    gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_] = None
                    gamedata.local_player_position_y_ -= 2 #move player


    if down:
        if gamedata.local_player_position_y_ +1 <gamedata.map_height_ and not type(gamedata.current_map_[gamedata.local_player_position_y_ +1][gamedata.local_player_position_x_ ]) in collisions:  #if map not end and if no collision
            CollectPoints(gamedata,gamedata.local_player_position_y_ +1,gamedata.local_player_position_x_) #try collect point
            gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_] = None
            gamedata.local_player_position_y_ += 1 #move player

            if gamedata.local_player_.animated_ == True:  # if player is animated
                gamedata.local_player_.AnimateToHorizontal() #animate player image
        #if door
        elif gamedata.local_player_position_y_ + 2 < gamedata.map_height_ and gamedata.current_map_[gamedata.local_player_position_y_+2][gamedata.local_player_position_x_] == None: #if map not end and if index is empty
            if type(gamedata.current_map_[gamedata.local_player_position_y_ +1][gamedata.local_player_position_x_]) == Door: #if door
                if gamedata.current_map_[gamedata.local_player_position_y_ +1][gamedata.local_player_position_x_].direction_ == 3:  # if the direction of the door is to the down
                    gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_] = None
                    gamedata.local_player_position_y_ += 2  # move player


    gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_] = gamedata.local_player_ #set player to map list

def CollectPoints(gamedata:object,y:int,x:int):
    #try collect point from given location
    if type(gamedata.current_map_[y][x]) == Diamond:
        gamedata.current_map_[y][x] = None
        gamedata.points_collected_ += 1

def Eat(gamedata:object,right:bool,left:bool,up:bool,down:bool):
    '''
    remove tile next to player
    '''

    if right:
        if gamedata.local_player_position_x_ +1 < gamedata.map_width_: #if map not end
            if type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_+1]) == DefaultTile:
                gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ + 1] = None
            CollectPoints(gamedata,gamedata.local_player_position_y_,gamedata.local_player_position_x_+1)


    elif left:
        if gamedata.local_player_position_x_ -1 >= 0:  # if map not end
            if type(gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1]) == DefaultTile:
                gamedata.current_map_[gamedata.local_player_position_y_][gamedata.local_player_position_x_ - 1] = None

            CollectPoints(gamedata,gamedata.local_player_position_y_,gamedata.local_player_position_x_-1)

    elif up:
        if gamedata.local_player_position_y_ - 1 >= 0:  # if map not end
            if type(gamedata.current_map_[gamedata.local_player_position_y_-1][gamedata.local_player_position_x_]) == DefaultTile:
                gamedata.current_map_[gamedata.local_player_position_y_-1][gamedata.local_player_position_x_] = None
            CollectPoints(gamedata,gamedata.local_player_position_y_-1,gamedata.local_player_position_x_)

    elif down:
        if gamedata.local_player_position_y_ + 1 < gamedata.map_height_:  # if map not end
            if type(gamedata.current_map_[gamedata.local_player_position_y_+1][gamedata.local_player_position_x_]) == DefaultTile:
                gamedata.current_map_[gamedata.local_player_position_y_+1][gamedata.local_player_position_x_] = None

            CollectPoints(gamedata,gamedata.local_player_position_y_+1,gamedata.local_player_position_x_)

def Gravity(gamedata):

    for y in range(gamedata.map_height_-1,-1,-1):
        for x in range(gamedata.map_width_-1,-1,-1):
            if type((gamedata.current_map_[y][x])) in gamedata.gravity_objects_: #if gravity objects
                if gamedata.current_map_[y][x].drop_: #if currently drop
                    if y + 1 < gamedata.map_height_: #if map not end
                        if type(gamedata.current_map_[y+1][x]) in gamedata.explosive2_: #if something falls on this tile
                            CreateExplosion(gamedata,y+1,x) #create explosion


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
                                        gamedata.current_map_[y][x].Rotate(1)
                                        gamedata.current_map_[y][x] = None
                                        return

                                if x-1 >= 0: #if map not end
                                    if gamedata.current_map_[y][x-1] == None and gamedata.current_map_[y+1][x-1] == None: #if empty on the left
                                        gamedata.current_map_[y][x-1] = gamedata.current_map_[y][x] #move stone to left
                                        gamedata.current_map_[y][x].Rotate(2)
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


def Run(gamedata:object,connection:object = None): #game main function


    right = False
    left = False
    up = False
    down = False
    space = False
    enter = False

    pausemenu_is_active = False
    pausemenu_number = 1  #1 = back to game, 2 = restart level, 3 = exit level


    clock = pygame.time.Clock()
    movelimit = 0 #gravity
    movelimit2 = 0 #player move

    while True: #game main loop

        if gamedata.multiplayer_:
            if connection.connected_ == True:

                try:
                    connection.Read()  # read socket
                except:
                    print("connection problem")


                try:
                    if connection.data_type_ == "map": #if message is map
                            mapstr = connection.data_
                            SetMap(gamedata,mapstr) #set map
                            gamedata.total_points_collected_ = connection.points_collected_ + gamedata.points_collected_

                    elif connection.data_type_ == "gameexit":
                        connection.CloseSocket()  # close socket
                        pygame.display.quit()  # close screen
                        return #back to menu

                    elif connection.data_type_ == "restartlevel":
                        SetMap(gamedata, gamedata.original_mapstr_, True)  # restart level

                except Exception as error_message:
                    print(error_message)



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
                pygame.display.quit()  #close screen
                return #back to menu

        if enter == True:
            if pausemenu_is_active == True:
                if pausemenu_number == 1: #exit pause menu
                    pausemenu_is_active = False
                elif pausemenu_number == 2: #restart level
                    SetMap(gamedata, gamedata.original_mapstr_, True) #restart level
                    if gamedata.multiplayer_: #if multiplayer
                        connection.SendRestartLevel()
                    pausemenu_is_active = False
                elif pausemenu_number == 3: #exit level
                    if gamedata.multiplayer_:
                        connection.SendGameExit(False)
                        connection.CloseSocket()  # close socket
                    pygame.display.quit()  # close screen
                    return  # back to menu


        if pygame.time.get_ticks() > movelimit + 140: #gravity
            movelimit = pygame.time.get_ticks()
            Gravity(gamedata)


        if pygame.time.get_ticks() > movelimit2 + 80:
            movelimit2 = pygame.time.get_ticks()
            if [right, left, up, down].count(True) == 1:  #can only move in one direction at a time
                if pausemenu_is_active == False:
                    if space: #if space pressed
                        Eat(gamedata,right,left,up,down) #remove tile in left,right,up or down
                    else:
                        Move(gamedata,right,left,up,down) #move player
                    if gamedata.multiplayer_:
                        connection.SendMap(gamedata.current_map_, gamedata.points_collected_)  #send map

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
                #set player image to defaultimage
                if gamedata.local_player_.animated_ == True:
                    if gamedata.local_player_.image_number_ != 0:
                        gamedata.local_player_.image_number_ = 0
                        if gamedata.multiplayer_ == True:
                            connection.SendMap(gamedata.current_map_, gamedata.points_collected_)  #send map


        if DeleteExplosion(gamedata): #delete exlplosions
            #if explosion removed
            if gamedata.multiplayer_: #if multiplayer
                connection.SendMap(gamedata.current_map_, gamedata.points_collected_)  #send map



        gamedata.screen_.fill((0, 0, 0))  # set backcolor
        gamedata.DrawMap()  #draw map
        if pausemenu_is_active == True: #if pausemenu is active
            DrawPauseMenu(gamedata,pausemenu_number) #draw pausemenu
        pygame.display.flip()  #update screen

        clock.tick(30) #fps limit