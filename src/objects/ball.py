from random import randrange

import numpy as np

from utils import config
from objects.gameObject import MovingObject


class Ball(MovingObject):

    def __init__(self, id, position, direction=config.BALL_DIRECTION, release=False, sp_factor=1):
        """
        sp_factor : Integer -> {1,2} : the multiplying factor for direction to increase the velocity of ball (for fast ball)
        release: Boolean : tells us whether the ball is released or not
        thru: Boolean: True if Thru Ball Power up is activated
        """
        self.__id = id
        self.__sp_factor = sp_factor
        self.__release = release
        self.__thru = False
        emoji = config.BALLS[randrange(len(config.BALLS))]
        shape = (1, 2)
        super().__init__(position=position, emoji=emoji, shape=shape, direction=direction)

    def get_sp_factor(self):
        return self.__sp_factor

    def set_sp_factor(self, sp_factor):
        self.__sp_factor = sp_factor

    def is_released(self):
        return self.__release

    def set_release(self, release):
        self.__release = release

    def is_thru(self):
        return self.__thru

    def set_thru(self, thru=True):
        self.__thru = thru

    def move(self, **kwargs):
        self._handle_wall_reflection()
        self.add_position(self._direction * self.__sp_factor)
