import pygame
import json

class Audio:

    def __init__(self):

        self.sounds_is_on_ = True

        #read audio file paths from json file:
        f = open("media/audio/audio config.json", "r")  #read json file
        self.audio_files_ = json.load(f)["audio files"]  #read audio file paths
        f.close()  #close file


        #load audio files:
        try:
            self.collect_ = pygame.mixer.Sound(self.audio_files_["collect"])  #collect sound
        except: #file not found:
            self.collect_ = None

        try:
            self.explosion_ = pygame.mixer.Sound(self.audio_files_["explosion"]) #explosion sound
        except: #file not found:
            self.explosion_ = None

        try:
            self.push_ = pygame.mixer.Sound(self.audio_files_["push"]) #push sound
        except: #file not found:d
            self.push_ = None

        try:
            self.drop_ = pygame.mixer.Sound(self.audio_files_["drop"]) #push sound
        except: #file not found
            self.drop_ = None

        try:
            self.step_ = pygame.mixer.Sound(self.audio_files_["step"]) #push sound
        except: #file not found
            self.step_ = None


        #create channels:
        self.channel_collect_ = pygame.mixer.Channel(0)
        self.channel_explosion_ = pygame.mixer.Channel(1)
        self.channel_push_ = pygame.mixer.Channel(2)
        self.channel_drop_ = pygame.mixer.Channel(3)
        self.channel_step_ = pygame.mixer.Channel(3)

    def PlayExplosionSound(self):
        if self.sounds_is_on_ == True and self.explosion_ != None: #if sounds is on and audio file download was succesful
            self.channel_explosion_.play(self.explosion_)


    def PlayCollectDiamond(self):
        if self.sounds_is_on_ == True and self.collect_ != None:  #if sounds is on and audio file download was succesful
            self.channel_collect_.play(self.collect_)

    def PlayPushSound(self):

        if self.sounds_is_on_ == True and self.push_ != None: #if sounds is on and audio file download was succesful
            self.channel_push_.play(self.push_)

    def PlayDropSound(self):
        if self.sounds_is_on_ == True and self.drop_ != None:  # if sounds is on and audio file download was succesful
            if  self.channel_drop_.get_busy() == False: #if the sound is already play
                self.channel_drop_.play(self.drop_)


    def PlayStepSound(self):
        if self.sounds_is_on_ == True and self.step_ != None:  # if sound is on and audio file download was succesful

            if self.channel_step_.get_busy() == False: #if the sound is already play
                    self.channel_step_.play(self.step_)
