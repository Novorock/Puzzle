from pyglet.window import key
from pyglet.text import Label
from util import GROUND_TILE, BLOCK_TILE
from util import RED_SIGN, GREEN_SIGN, BLUE_SIGN, BLOCK, BLOCK_RED, BLOCK_GREEN, BLOCK_BLUE
from util import KIND_1, KIND_2, KIND_3
from puzzle_objects import PieceFactory, Selection
from util import get_py_y_value, offset_x, offset_y
from field import Field, Canvas


class PuzzleFactory:
    def __init__(self, field: Field, canvas: Canvas):
        self._field = field
        self._canvas = canvas
        self._field_size = field.get_size()

    def create_pieces(self) -> list:
        pieces = []
        for i in range(self._field_size):
            for j in range(self._field_size):
                kind = self._field.get_tile_kind(j, i)

                if kind not in [KIND_1, KIND_2, KIND_3]:
                    continue

                pieces.append(
                    PieceFactory.new_instance(self._field.get_tile_kind(j, i), j, i, self._field, self._canvas))

        return pieces


class Puzzle:
    def __init__(self):
        self._field = Field({'kind1': KIND_1, 'kind2': KIND_2, 'kind3': KIND_3})
        self._canvas = Canvas()
        self._pieces = PuzzleFactory(self._field, self._canvas).create_pieces()

    def update(self, dt):
        for piece in self._pieces:
            piece.update(dt)

    def on_key_press(self, symbol):
        pass

    def draw(self):
        self._canvas.draw()
