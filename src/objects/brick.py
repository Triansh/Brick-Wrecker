import numpy as np

from objects.gameObject import GameObject


class Brick(GameObject):

    def __init__(self, id, position, level, shape=(1, 2), rainbow=False):
        """
        Level: Integer : denotes the strength of brick (max level is 4)
        """
        self.__id = id
        self.__level = level
        self.__isRainbow = rainbow
        super().__init__(position=position, emoji="🚫", shape=shape)

    def get_id(self):
        return self.__id

    def get_level(self):
        return self.__level

    def set_level(self, level):
        self.__level = level
        self.set_emoji()

    def get_coords(self):
        """
        This gives all the four coordinates of the brick
        """
        _x, _y = self._position
        _h, _w = self.get_shape()
        return [(_x, _y), (_x, _y + _h), (_x + _w, _y), (_x + _w, _y + _h)]

    def set_emoji(self, emoji="🚫"):

        if self.__class__.__name__ != "Brick":
            super().set_emoji(emoji=emoji)
            return

        if self.__level == 3:
            self._emoji = "🟦"
        elif self.__level == 4:
            self._emoji = '🟪'
        elif self.__level == 2:
            self._emoji = "🟩"
        elif self.__level == 1:
            self._emoji = "🟨"
        super().set_emoji(self._emoji)

    def reflect_obj(self, pos, direction):
        """
        This accounts for the reflection made when any object collides with brick
        """
        _x, _y = pos
        _dx, _dy = direction

        _bx, _by = self._position
        _h, _w = self.get_shape()

        if _by <= _y <= _by + _h and (_x <= _bx or _x >= _bx + _w):
            _dx *= -1
        elif _bx <= _x <= _bx + _w and (_y <= _by or _y >= _by + _h):
            _dy *= -1
        else:
            _dx *= -1
            _dy *= -1

        return np.array([_dx, _dy], dtype=float)

    def set_rainbow(self):
        self.__isRainbow = False

    def fluctuate(self):
        if not self.__isRainbow:
            return
        self.set_level((self.__level % 4) + 1)


class ExplosiveBrick(Brick):  # TODO

    def __init__(self, id, position, shape):
        super().__init__(id=id, position=position, level=1, shape=shape)

    def set_emoji(self, emoji="🚫"):
        super().set_emoji('🟥')


class UnBreakableBrick(Brick):

    def __init__(self, id, position, shape):
        super().__init__(id=id, position=position, level=100000, shape=shape)

    def set_emoji(self, emoji="🚫"):
        super().set_emoji(emoji='🟫')

    def set_level(self, level):
        return


class UFOBrick(Brick):
    def __init__(self, id, position, shape, emoji):
        super(UFOBrick, self).__init__(id=id, position=position, shape=shape, level=1000000)
        self.set_emoji(emoji)

    def set_emoji(self, emoji="🚫"):
        self._emoji = emoji
        self._make_rep()

    def set_level(self, level):
        return
