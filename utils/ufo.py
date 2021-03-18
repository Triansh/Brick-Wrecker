import numpy as np

from objects.brick import UFOBrick
from objects.bullet import UFOBomb
from utils.brickwall import BrickWall
from utils import config


class UFO(BrickWall):

    def __init__(self):
        self.__bombs = []
        super().__init__(stage=config.STAGES)

    def _set_character(self, ch, x, y):
        _shape = (1, 2)
        if ch in ['A', 'F', 'C', 'G']:
            _pos = np.array([x, y]) + self._position
            emoji = '🛸'
            if ch == 'F':
                emoji = '🛸'
            elif ch == 'A':
                emoji = '👽'
            elif ch == 'C':
                emoji = '🔵'
            elif ch == 'G':
                emoji = '🟩'
            self._bricks.append(
                UFOBrick(id=self._counter, position=_pos, shape=_shape, emoji=emoji))
            self._counter += 1
            x += 2
            return x
        else:
            x += 2
            return x

    def _make_structure(self):
        self._bricks = []
        y = 0
        for i in range(len(self._matrix)):
            x = 0
            for j in range(len(self._matrix[i])):
                x = self._set_character(self._matrix[i][j], x, y)
            y += 1
        return

    def shift_wall(self, val=1):
        _pos = np.array([val, 0])
        self._position += _pos
        for brick in self._bricks:
            brick.add_position(_pos)

    def get_bombs(self):
        return self.__bombs

    def set_bombs(self, bombs):
        self.__bombs = bombs

    def set_time(self, value=0):
        self._time = value

    def drop_bomb(self):
        self._time += 1
        if self._time % config.UFO_DROP_TIME == 0:
            _pos = config.UFO_CENTER + self._position
            new_bomb = UFOBomb(position=_pos, id=self._time)
            self.__bombs.append(new_bomb)