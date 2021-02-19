from random import randrange
import numpy as np

import config
from objects.brick import Brick, ExplosiveBrick, UnBreakableBrick


class BrickWall:

    def __init__(self, position):
        """
        counter: Integer : Assigns id to each brick
        position: np.array -> [x, y] : Wall position
        bricks : list(Brick): All un-destroyed bricks
        next_explodes : list((Brick, frame)) : The brick must be destroyed in this frame
        leftover_bricks : Integer: Remaining bricks
        matrix : list(String) : Design of brick wall
        """
        self.__counter = 0
        self.__position = position
        self.__bricks = []
        self.__next_explodes = []
        self.__leftover_bricks = 0
        self.matrix = [
            '11111SSSSSSSSSSSSSSS11111',
            '1P100SSSSSSSSSSSSSSS00111',
            '1P100SSSSSSSSSSSSSSS00111',
            '1P100LLLLLLLELLLLLLL00111',
            '1P100LLLLLLLELLLLLLL001P1',
            '1P100LLLLLLELELLLLLL001P1',
            '1P100LLLLLLLELLLLLLL001P1',
            '11100LLLLLLLELLLLLLL001P1',
            '11100SSSSSSSSSSSSSSS001P1',
            '11100SSSSSSSSSSSSSSS001P1',
            '11111SSSSSSSSSSSSSSS11111',
        ]
        self.make_structure()

    def get_all_bricks(self):
        return self.__bricks + [x[0] for x in self.__next_explodes]

    def get_count_bricks(self):
        return self.__leftover_bricks

    @staticmethod
    def is_neighbour(center, shape, brick):
        """
        Check whether a Brick b  is neighbour of another Brick brick
        """
        _cx, _cy = center
        _ch, _cw = shape
        for i, j in brick.get_coords():
            if (((_cx - i) / _cw) ** 2) + (((_cy - j) / _ch) ** 2) <= 1:
                return True
        return False

    def destroy_brick(self, brick: Brick, frames):
        if brick.__class__.__name__ == "ExplosiveBrick":
            self.do_explosion(brick, frames)
        else:
            try:
                self.__bricks.remove(brick)
            except ValueError:
                pass
        self.__leftover_bricks = len(self.__bricks)
        return

    def do_explosion(self, brick, frames):
        to_remove = [brick]
        center, shape = brick.get_center(), brick.get_shape()
        for b in self.__bricks:
            if b != brick and self.is_neighbour(center, shape, b):
                if b.__class__.__name__ == "ExplosiveBrick":
                    self.__next_explodes.append((b, frames + 5))
                else:
                    to_remove.append(b)
        self.__bricks = [x for x in self.__bricks if x not in to_remove]
        self.__next_explodes = [x for x in self.__next_explodes if x[0] not in to_remove]
        self.__leftover_bricks = len(self.__bricks)

    def explode_bricks(self, frame):
        for brick, f in self.__next_explodes:
            if f == frame:
                self.do_explosion(brick, frame)

    def make_structure(self):
        """
        Function to construct the design of wall
        """
        _shape = (2, 4)
        y = 0
        for i in range(len(self.matrix)):
            x = 0
            for j in range(len(self.matrix[i])):
                x = self.set_character(self.matrix[i][j], x, y)
            y += _shape[0]
        self.__leftover_bricks = len(self.__bricks)

    def set_character(self, ch, x, y):
        """
        How the bricks are placed in layout
        """
        _shape = (2, 4)
        if ch == '0':
            x += 4
        elif ch == "S":
            x += 6
        else:
            if ch in ['L', 'E']:
                _shape = (2, 6)
            _pos = np.array([x, y]) + self.__position

            if ch in ['E', 'P']:
                new_brick = ExplosiveBrick(id=self.__counter, position=_pos, shape=_shape)
            else:
                if randrange(10) >= 2:
                    new_brick = Brick(id=self.__counter, position=_pos, shape=_shape,
                                      level=randrange(1, config.BRICK_TYPES + 1))
                else:
                    new_brick = UnBreakableBrick(id=self.__counter, position=_pos, shape=_shape)
            self.__bricks.append(new_brick)
            self.__counter += 1
            x += _shape[1]
        return x
