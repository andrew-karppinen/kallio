import pygame


class Player:
    def __init__(self,local_player:bool = True):
        self.images_ = []
        self.local_player_ = local_player
        self.animated_ = False
        self.image_number_ = 0
        #0 = no move,1 left1, 2 = left2, 3 = right1, 4 = right2

    def SetImage(self,nomove,move1 = None,move2 = None):
        '''
        in the pictures the character is moving to the right!

        automatically create a mirror images

        images must be pygame surface object!
        '''

        if move1 != None and move2 != None:
            move3 = pygame.transform.flip(move1,True,False)
            move4 = pygame.transform.flip(move2,True,False)
            self.images_ = [nomove,move1,move2,move3,move4]
            self.animated_ = True
        else:
            self.images_ = [nomove, move1, move2]
            self.animated_ = False
    def ScaleImages(self,tile_size=50):
        self.images_[0] = pygame.transform.scale(self.images_[0],(tile_size,tile_size))

        if self.images_[1] != None:
            self.images_[1] = pygame.transform.scale(self.images_[1], (tile_size, tile_size))
            self.images_[3] = pygame.transform.scale(self.images_[3], (tile_size, tile_size))
        if self.images_[2] != None:
            self.images_[2] = pygame.transform.scale(self.images_[2], (tile_size, tile_size))
            self.images_[4] = pygame.transform.scale(self.images_[4], (tile_size, tile_size))


    def AnimateToRight(self):
        if self.image_number_ == 1:
            self.image_number_ = 2
        else:
            self.image_number_ = 1

    def AnimateToLeft(self):
        if self.image_number_ == 3:
            self.image_number_ = 4
        else:
            self.image_number_ = 3

    def AnimateToHorizontal(self):

        if self.image_number_ == 0 or self.image_number_ == 1 or self.image_number_ == 2:
            self.AnimateToRight()
        else:
            self.AnimateToLeft()


    @property
    def image_(self):

        if self.images_[self.image_number_] != None:
            return(self.images_[self.image_number_])

        else:
            return self.images_[0] #if no animation




class DefaultTile:
    #class variables:
    image = None

    def SetImage(image:pygame.surface):
        DefaultTile.image = image
    def __init__(self):
        pass

    @property
    def image_(self):
        return (DefaultTile.image)


class Stone:
    #class variables:
    image_left = None
    image_right = None
    image_up = None
    image_down = None
    image = None

    def SetImage(image:pygame.surface):
        Stone.image = image
        #rotate images
        Stone.image_right = image
        Stone.image_up = pygame.transform.rotate(Stone.image_right,90)
        Stone.image_left = pygame.transform.rotate(Stone.image_right,180)
        Stone.image_down = pygame.transform.rotate(Stone.image_right,270)


    def __init__(self, drop:bool,direction:int = 1):
        self.drop_ = drop
        self.direction_ = direction  # 1 = up, 2 = right, 3 = down, 4 = left


    def Rotate(self,direction:int):
        #direction = 1 or 2
        #1 = clockwise
        #2 = counterclockwise

        if direction == 1:
            if self.direction_ == 4:
                self.direction_ = 1
            else:
                self.direction_ += 1

        elif direction == 2:
            if self.direction_ == 1:
                self.direction_ = 4
            else:
                self.direction_ -= 1


    @property
    def image_(self):
        if self.direction_ == 1:
            return(Stone.image_up)
        elif self.direction_ == 2:
            return(Stone.image_right)
        elif self.direction_ == 3:
            return (Stone.image_down)
        elif self.direction_ == 4:
            return(Stone.image_left)



class Diamond:
    #class variables:
    image_left = None
    image_right = None
    image_up = None
    image_down = None
    image = None

    def SetImage(image:pygame.surface):
        Diamond.image = image
        #rotate images
        Diamond.image_right = image
        Diamond.image_up = pygame.transform.rotate(Diamond.image_right,90)
        Diamond.image_left = pygame.transform.rotate(Diamond.image_right,180)
        Diamond.image_down = pygame.transform.rotate(Diamond.image_right,270)


    def __init__(self, drop:bool,direction:int = 1):
        self.drop_ = drop
        self.direction_ = direction  # 1 = up, 2 = right, 3 = down, 4 = left


    def Rotate(self,direction:int):
        #direction = 1 or 2
        #1 = clockwise
        #2 = counterclockwise

        if direction == 1:
            if self.direction_ == 4:
                self.direction_ = 1
            else:
                self.direction_ += 1

        if direction == 2:
            if self.direction_ == 1:
                self.direction_ = 4
            else:
                self.direction_ -= 1


    @property
    def image_(self):
        if self.direction_ == 1:
            return(Diamond.image_up)
        elif self.direction_ == 2:
            return(Diamond.image_right)
        elif self.direction_ == 3:
            return (Diamond.image_down)
        elif self.direction_ == 4:
            return(Diamond.image_left)



class Tnt:
    #class variables:
    image = None

    def SetImage(image:pygame.surface):
        Tnt.image = image
    def __init__(self,drop:bool=False):
        self.drop_ = drop  # if currently dropping



    @property
    def image_(self):
        return (Tnt.image)



class Explosion:
    #class variables:
    image = None

    def SetImage(image:pygame.surface):
        Explosion.image = image

    def __init__(self,counter:int = 0):
        self.counter_ = counter #1,2

    @property
    def image_(self):
        return (Explosion.image)

class Bedrock:
    #class variables:
    image = None

    def SetImage(image:pygame.surface):
        Bedrock.image = image
    def __init__(self):
        pass

    @property
    def image_(self):
        return (Bedrock.image)

class Brick:
    #class variables:
    image = None

    def SetImage(image:pygame.surface):
        Brick.image = image

    def __init__(self):
        pass

    @property
    def image_(self):
        return (Brick.image)


class Goal:
    #class variables:
    image = None

    def SetImage(image:pygame.surface):
        Goal.image = image

    def __init__(self):
        pass

    @property
    def image_(self):
        return (Goal.image)





class Monster:
    #class variables:
    image = None

    def SetImage(image:pygame.surface):
        Monster.image = image

    def __init__(self,direction):
        self.direction_ = direction


    @property
    def image_(self):
        return (Monster.image)



class Door:
    image_left = None
    image_right = None
    image_up = None
    image_down = None
    image = None

    def SetImage(image:pygame.surface):
        Door.image = image
        #rotate images
        Door.image_right = image
        Door.image_up = pygame.transform.rotate(Door.image_right,90)
        Door.image_left = pygame.transform.rotate(Door.image_right,180)
        Door.image_down = pygame.transform.rotate(Door.image_right,270)

    def __init__(self, direction):
        self.direction_ = direction  # 1 = up, 2 = right, 3 = down, 4 = left


    @property
    def image_(self):
        if self.direction_ == 1:
            return(Door.image_up)
        elif self.direction_ == 2:
            return(Door.image_right)
        elif self.direction_ == 3:
            return (Door.image_down)
        elif self.direction_ == 4:
            return(Door.image_left)
