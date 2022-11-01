from pyglet.window import key
from pyglet.text import Label
from puzzle_objects import GROUND_TILE, BLOCK, RED_SIGN, GREEN_SIGN, BLUE_SIGN, BLOCK_TILE, BLOCK_RED, BLOCK_GREEN, \
    BLOCK_BLUE, KIND_1, KIND_2, KIND_3, Selection
from puzzle_objects import PieceFactory
from util import get_py_y_value, offset_x, offset_y
from field import Field


class PuzzleFactory:
    def __init__(self, field: Field):
        self._field = field
        self._field_size = field.get_size()

    def create_pieces(self) -> list:
        pieces = []
        for i in range(self._field_size):
            for j in range(self._field_size):
                pieces.append(PieceFactory.new_instance(self._field.get_tile_kind(j, i), j, i, self._field))

        return pieces


class Puzzle:
    def __init__(self):
        self.field = Field({'kind1': KIND_1, 'kind2': KIND_2, 'kind3': KIND_3})
        self.field_size = self.field.get_size()
        self.selection = Selection(1, 4)
        self.pieces = PuzzleFactory(self.field).create_pieces()
        self.log = Label("Log", font_size=12, x=20, y=20)

    def update(self, dt):
        self.selection.update(dt)

    def on_key_press(self, symbol):
        if symbol == key.UP:
            self.selection.move_up()
        elif symbol == key.DOWN:
            self.selection.move_down()
        elif symbol == key.RIGHT:
            self.selection.move_right()
        elif symbol == key.LEFT:
            self.selection.move_left()
        elif symbol == key.ENTER:
            if self.selection.is_active() and not self.selection.is_moving():
                self.selection.drop()
            elif not self.selection.is_moving():
                for piece in self.pieces:
                    if piece is not None:
                        if piece.get_col() == self.selection.get_col() and piece.get_row() == self.selection.get_row():
                            self.selection.select(piece)

    def draw_background(self):
        for i in range(self.field_size):
            for j in range(self.field_size):
                GROUND_TILE.update(x=offset_x + j * 64, y=get_py_y_value(offset_y + i * 64))
                GROUND_TILE.draw()

    def draw_border(self):
        for i in range(self.field_size):
            for j in range(self.field_size):
                if self.field.get_tile_kind(j, i) == BLOCK:
                    BLOCK_TILE.update(x=offset_x + j * 64, y=get_py_y_value(offset_y + i * 64))
                    BLOCK_TILE.draw()
                elif self.field.get_tile_kind(j, i) == RED_SIGN:
                    BLOCK_RED.update(x=offset_x + j * 64, y=get_py_y_value(offset_y + i * 64))
                    BLOCK_RED.draw()
                elif self.field.get_tile_kind(j, i) == GREEN_SIGN:
                    BLOCK_GREEN.update(x=offset_x + j * 64, y=get_py_y_value(offset_y + i * 64))
                    BLOCK_GREEN.draw()
                elif self.field.get_tile_kind(j, i) == BLUE_SIGN:
                    BLOCK_BLUE.update(x=offset_x + j * 64, y=get_py_y_value(offset_y + i * 64))
                    BLOCK_BLUE.draw()

    def draw(self):
        self.draw_background()
        self.draw_border()

        for piece in self.pieces:
            if piece is not None:
                piece.draw()

        self.selection.draw()
        # self.log.draw()
