from pyglet.window import key
from puzzle_objects import PieceFactory, Selection
from util import GROUND, BLOCK, FIRST_KIND, SECOND_KIND, THIRD_KIND
from util import get_py_y_value, offset_x, offset_y
from field import Field, Canvas


class PuzzleFactory:
    def __init__(self, field: Field, canvas: Canvas):
        self._field = field
        self._canvas = canvas
        self._field_size = field.get_size()

    def create_pieces(self) -> list:
        pieces = []
        for i in range(1, self._field_size - 1):
            for j in range(1, self._field_size - 1):
                kind = self._field.get_tile(j, i)

                if kind not in [FIRST_KIND, SECOND_KIND, THIRD_KIND]:
                    continue

                pieces.append(
                    PieceFactory.new_instance(self._field.get_tile(j, i), j, i, self._field, self._canvas))

        return pieces

    def build_environment(self):
        for i in range(1, self._field_size - 1):
            for j in range(1, self._field_size - 1):
                x = offset_x + j * 64
                y = get_py_y_value(offset_y + i * 64)
                self._canvas.get_sprite(GROUND[self._field.get_background_tile(j, i)], background=True, x=x, y=y)

                if self._field.get_tile(j, i) == 10:
                    self._canvas.get_sprite(BLOCK, x=x, y=y)

        for i in range(1, self._field_size - 1):
            x = offset_x + i * 64
            y = get_py_y_value(offset_y)
            self._canvas.get_sprite(GROUND[self._field.get_background_tile(i, 0)], background=True, x=x, y=y)


class Puzzle:
    def __init__(self):
        self._field = Field({'first_line': FIRST_KIND, 'second_line': SECOND_KIND, 'third': THIRD_KIND})
        self._canvas = Canvas()
        self._factory = PuzzleFactory(self._field, self._canvas)
        self._pieces = self._factory.create_pieces()
        self._factory.build_environment()
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
