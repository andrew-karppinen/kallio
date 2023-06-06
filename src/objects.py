import pygame


class Player:
    def __init__(self, image,local_player:bool = True):
        self.image_ = image
        self.local_player_ = local_player




class DefaultTile:
    image = None

    def SetImage(image:pygame.surface):
        DefaultTile.image = image
    def __init__(self):
        pass

    @property
    def image_(self):
        return (DefaultTile.image)


class Stone:
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

    def __init__(self, drop:bool):
        self.drop_ = drop
        self.direction_ = 1  # 1 = up, 2 = right, 3 = down, 4 = left


    def Rotate(self,direction:int):
        #direction = 1 or 2
        #1 = clockwise
        #2 = counterclockwise

        if direction == 1:
            if self.direction_ == 1:
                self.direction_ = 4
            else:
                self.direction_ -= 1
        if direction == 2:
            if self.direction_ == 4:
                self.direction_ == 1
            else:
                self.direction_ += 1

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
    image = None

    def SetImage(image:pygame.surface):
        Diamond.image = image
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

    def SetImage(image:pygame.surface):
        Tnt.image = image
    def __init__(self,drop:bool=False):
        self.drop_ = drop  # if currently dropping



    @property
    def image_(self):
        return (Tnt.image)



class Explosion:
    image = None

    def SetImage(image:pygame.surface):
        Explosion.image = image

    def __init__(self,counter:int = 0):
        self.counter_ = counter #1,2

    @property
    def image_(self):
        return (Explosion.image)

class Bedrock:
    image = None

    def SetImage(image:pygame.surface):
        Bedrock.image = image
    def __init__(self):
        pass

    @property
    def image_(self):
        return (Bedrock.image)

class Brick:
    image = None

    def SetImage(image:pygame.surface):
        Brick.image = image

    def __init__(self):
        pass

    @property
    def image_(self):
        return (Brick.image)


class Goal:
    image = None

    def SetImage(image:pygame.surface):
        Goal.image = image

    def __init__(self):
        pass

    @property
    def image_(self):
        return (Goal.image)





class Monster:
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
