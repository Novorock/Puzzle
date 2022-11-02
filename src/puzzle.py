from pyglet.window import key
from pyglet.text import Label
from puzzle_objects import PieceFactory, Selection
from util import GROUND_TILE, BLOCK_TILE
from util import GROUND, RED_SIGN, GREEN_SIGN, BLUE_SIGN, BLOCK, BLOCK_RED, BLOCK_GREEN, BLOCK_BLUE
from util import KIND_1, KIND_2, KIND_3
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

    def build_environment(self):
        for i in range(self._field_size):
            for j in range(self._field_size):
                x, y = offset_x + j * 64, get_py_y_value(offset_y + i * 64)
                kind = self._field.get_tile_kind(j, i)

                self._canvas.get_sprite(GROUND_TILE, background=True, x=x, y=y)

                if kind == BLOCK:
                    self._canvas.get_sprite(BLOCK_TILE, x=x, y=y)
                elif kind == RED_SIGN:
                    self._canvas.get_sprite(BLOCK_RED, x=x, y=y)
                elif kind == GREEN_SIGN:
                    self._canvas.get_sprite(BLOCK_GREEN, x=x, y=y)
                elif kind == BLUE_SIGN:
                    self._canvas.get_sprite(BLOCK_BLUE, x=x, y=y)


class Puzzle:
    def __init__(self):
        self._field = Field({'kind1': KIND_1, 'kind2': KIND_2, 'kind3': KIND_3})
        self._canvas = Canvas()
        self._factory = PuzzleFactory(self._field, self._canvas)
        self._factory.build_environment()
        self._pieces = self._factory.create_pieces()
        self._selection = Selection(1, 4, self._canvas)

    def update(self, dt):
        self._selection.update(dt)

    def on_key_press(self, symbol):
        if symbol == key.RIGHT:
            self._selection.move_right()
        elif symbol == key.LEFT:
            self._selection.move_left()
        elif symbol == key.DOWN:
            self._selection.move_down()
        elif symbol == key.UP:
            self._selection.move_up()

        if symbol == key.ENTER:
            if self._selection.is_active() and not self._selection.is_moving():
                self._selection.drop()
            else:
                col, row = self._selection.get_col(), self._selection.get_row()
                result = list(filter(lambda piece: piece.get_col() == col and piece.get_row() == row, self._pieces))
                if len(result) > 0:
                    self._selection.select(result[0])

    def draw(self):
        self._canvas.draw()
