from random import randrange

from utils import config
from objects.powerup import BallMultiplier, ThruBall, FastBall, PaddleGrab, ExpandPaddle, \
    ShrinkPaddle, ShootingPaddle
from utils.powerUpActivity import PaddleSizeActivity, FastBallActivity, ThruBallActivity, \
    PaddleGrabActivity, ShootingActivity


class PowerUpHandler:

    def __init__(self):
        self.__counter = 0
        self.__power_ups_activity = [
            PaddleSizeActivity(),
            ThruBallActivity(),
            FastBallActivity(),
            PaddleGrabActivity(),
            ShootingActivity()
        ]

    @staticmethod
    def __map(name):

        if name in ["ExpandPaddle", "ShrinkPaddle"]:
            return 0
        elif name == "ThruBall":
            return 1
        elif name == "FastBall":
            return 2
        elif name == "PaddleGrab":
            return 3
        elif name == "ShootingPaddle":
            return 4
        return None

    def create_power_up(self, position, direction):

        prob = randrange(100)
        if prob > config.POWER_UP_CHANCE:
            return None

        _type = randrange(7)
        self.__counter += 1
        if _type == 6:
            return ShootingPaddle(self.__counter, position, direction)
        if _type == 5:
            return BallMultiplier(self.__counter, position, direction)
        elif _type == 3:
            return ThruBall(self.__counter, position, direction)
        elif _type == 2:
            return FastBall(self.__counter, position, direction)
        elif _type == 4:
            return PaddleGrab(self.__counter, position, direction)
        elif _type == 1:
            return ExpandPaddle(self.__counter, position, direction)
        elif _type == 0:
            return ShrinkPaddle(self.__counter, position, direction)
        else:
            return None

    def activate_power_ups(self, name, **kwargs):
        index = self.__map(name)
        self.__power_ups_activity[index].activate(**kwargs)

    def update_power_ups(self, **kwargs):
        for activity in self.__power_ups_activity:
            activity.update(**kwargs)

    def deactivate_power_ups(self, **kwargs):
        for activity in self.__power_ups_activity:
            activity.deactivate(**kwargs)

    def is_power_up_active(self, name):
        index = self.__map(name)
        return self.__power_ups_activity[index].is_active()

    def get_power_up_duration(self, name):
        index = self.__map(name)
        return self.__power_ups_activity[index].get_duration()
