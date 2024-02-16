import pygame
import json


class Music:
    def __init__(self,volume:float): #constructor
        self.music_is_on_ = False


        #read music file paths from json file:
        f = open("media/audio/audio config.json", "r")  #read json file
        self.audio_files_ = json.load(f)["audio files"]  #read audio file paths
        f.close()  #close file


        #load music files:
        try:
            self.music_ = pygame.mixer.Sound(self.audio_files_["music1"])  #collect sound
            self.music_channel_ = pygame.mixer.Channel(0)

        except: #file not found:
            self.music_ = None


        self.SetVolume(volume)



    def SetVolume(self, volume:float):
        if self.music_ != None:  # if audio file download was succesful

            self.music_.set_volume(volume)

    def PlayMusic(self):
        if self.music_ != None:  # if audio file download was succesful
            if self.music_is_on_ == False: #make sure that the music is not already on
                self.music_.play(loops=-1)
                self.music_is_on_ = True

    def StopMusic(self):
        if self.music_ != None:  # if audio file download was succesful
            self.music_.stop()
        self.music_is_on_ = False


class Sfx:

    def __init__(self,sfx_is_on:bool= True,volume:float=0.5):

        self.sfx_is_on_ = sfx_is_on

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
        except: #file not found
            self.push_ = None

        try:
            self.drop_ = pygame.mixer.Sound(self.audio_files_["drop"]) #push sound
        except: #file not found
            self.drop_ = None

        try:
            self.step_ = pygame.mixer.Sound(self.audio_files_["step"]) #push sound
        except: #file not found
            self.step_ = None


        self.volume_ = volume
        self.__CreateChannels()


    def __CreateChannels(self):
        #create channels:
        self.channel_collect_ = pygame.mixer.Channel(1)
        self.channel_explosion_ = pygame.mixer.Channel(2)
        self.channel_push_ = pygame.mixer.Channel(3)
        self.channel_drop_ = pygame.mixer.Channel(4)
        self.channel_step_ = pygame.mixer.Channel(5)

        self.channel_collect_.set_volume(self.volume_)
        self.channel_explosion_.set_volume(self.volume_)
        self.channel_push_.set_volume(self.volume_)
        self.channel_drop_.set_volume(self.volume_)
        self.channel_step_.set_volume(self.volume_)


    def SetVolume(self,volume):
        self.volume_ = volume #set new volume
        self.__CreateChannels() #update channels

    def PlayExplosionSound(self):
        if self.sfx_is_on_ == True and self.explosion_ != None: #if sounds is on and audio file download was succesful
            self.channel_explosion_.play(self.explosion_)


    def PlayCollectSound(self):
        if self.sfx_is_on_ == True and self.collect_ != None:  #if sounds is on and audio file download was succesful
            self.channel_collect_.play(self.collect_)

    def PlayPushSound(self):

        if self.sfx_is_on_ == True and self.push_ != None: #if sounds is on and audio file download was succesful
            self.channel_push_.play(self.push_)

    def PlayDropSound(self):
        if self.sfx_is_on_ == True and self.drop_ != None:  # if sounds is on and audio file download was succesful
            if  self.channel_drop_.get_busy() == False: #if the sound is already play
                self.channel_drop_.play(self.drop_)


    def PlayStepSound(self):
        if self.sfx_is_on_ == True and self.step_ != None:  # if sound is on and audio file download was succesful

            if self.channel_step_.get_busy() == False: #if the sound is already play
                    self.channel_step_.play(self.step_)
