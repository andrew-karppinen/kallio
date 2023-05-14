import pygame


class Player:
    def __init__(self, image,local_player:bool = True):
        self.image_ = image
        self.local_player_ = local_player




class DefaultTile:
    image = None

    def __init__(self):
        pass

    @property
    def image_(self):
        return (DefaultTile.image)


class Stone:
    image = None

    def __init__(self,drop:bool=False):
        self.drop_ = drop  # if currently dropping
        self.angle_ = 0

    @property
    def image_(self):

        return pygame.transform.rotate(Stone.image,self.angle_) #Rotate the image and return it



    def Rotate(self,direction:int):
        #direction = 1 or 2
        #1 = clockwise
        #2 = counterclockwise

        if direction == 1:
            self.angle_ -= 90
        if direction == 2:
            self.angle_ += 90




class Diamond:
    image = None

    def __init__(self,drop:bool=False):
        self.drop_ = drop  # if currently dropping
        self.angle_ = 0



    @property
    def image_(self):
        return pygame.transform.rotate(Diamond.image, self.angle_)  # Rotate the image and return it


    def Rotate(self,direction:int):
        #direction = 1 or 2
        #1 = clockwise
        #2 = counterclockwise

        if direction == 1:
            self.angle_ -= 90
        if direction == 2:
            self.angle_ += 90



class Tnt:
    image = None
    def __init__(self,drop:bool=False):
        self.drop_ = drop  # if currently dropping



    @property
    def image_(self):
        return (Tnt.image)



class Explosion:
    image = None

    def __init__(self,counter:int = 0):
        self.counter_ = counter #1,2

    @property
    def image_(self):
        return (Explosion.image)

class Bedrock:
    image = None

    def __init__(self):
        pass

    @property
    def image_(self):
        return (Bedrock.image)

class Brick:
    image = None



    def __init__(self):
        pass

    @property
    def image_(self):
        return (Brick.image)


class Goal:
    image = None

    def __init__(self):
        pass

    @property
    def image_(self):
        return (Goal.image)





class Monster:
    image = None

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


    def Setimage(image:pygame.surface):
        #rotate images
        Door.image_right = image
        Door.image_up = pygame.transform.rotate(Door.image_right,90)
        Door.image_left = pygame.transform.rotate(Door.image_right,180)
        Door.image_down = pygame.transform.rotate(Door.image_right,270)

    def __init__(self, direction):
        self.direction_ = direction  # 1 = up, 2 = right, 3 = down, 4 = left


    @property
    def image_(self):
        if self.direction_ == 2:
            return(Door.image_right)
        elif self.direction_ == 3:
            return (Door.image_down)
        elif self.direction_ == 4:
            return(Door.image_left)
        elif self.direction_ == 1:
            return(Door.image_up)