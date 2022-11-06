from pyglet.image import ImageData
from src.util import get_py_y_value, offset_x, offset_y
from src.util import ANIMATION_RATE, RED_PIECE, GREEN_PIECE
from src.util import BLUE_PIECE, RED_PIECE_SELECTED, BLUE_PIECE_SELECTED, GREEN_PIECE_SELECTED, SELECTION
from src.util import EMPTY, FIRST_KIND, SECOND_KIND, THIRD_KIND
from src.environment import Field, Canvas


class MovementAnimation:
    def __init__(self, col, row):
        self._col, self._row = col, row
        self._x, self._y = offset_x + col * 64, offset_y + row * 64
        self._dx, self._dy = 0, 0
        self._is_moving = False

    def move_down(self):
        if self._is_moving:
            return

        self._dy = ANIMATION_RATE
        self._row += 1
        self._is_moving = True

    def move_up(self):
        if self._is_moving:
            return

        self._dy = -ANIMATION_RATE
        self._row -= 1
        self._is_moving = True

    def move_right(self):
        if self._is_moving:
            return

        self._dx = ANIMATION_RATE
        self._col += 1
        self._is_moving = True

    def move_left(self):
        if self._is_moving:
            return

        self._dx = -ANIMATION_RATE
        self._col -= 1
        self._is_moving = True

    def update(self, dt):
        if self._is_moving:
            self._x += self._dx * dt
            self._y += self._dy * dt

        if (offset_x + self._col * 64 - self._x) * self._dx < 0:
            self._x = offset_x + self._col * 64
            self._is_moving = False
        elif (offset_y + self._row * 64 - self._y) * self._dy < 0:
            self._y = offset_y + self._row * 64
            self._is_moving = False

        if not self._is_moving:
            self._dx = self._dy = 0

    def is_moving(self):
        return self._is_moving

    def get_col(self):
        return self._col

    def get_row(self):
        return self._row


class Piece(MovementAnimation):
    def __init__(self, dft_img: ImageData, slt_img: ImageData, canvas: Canvas, field: Field, kind: int, col, row):
        super(Piece, self).__init__(col, row)
        self._kind = kind
        self._field = field
        self._dft_img, self._slt_img = dft_img, slt_img
        self._current_sprite = canvas.get_sprite(dft_img)
        self._current_sprite.update(self._x, get_py_y_value(self._y))
        self._canvas = canvas

    def update(self, dt):
        if self._is_moving:
            if self._dx > 0:
                self._field.update_field(self._col - 1, self._row, EMPTY)
            elif self._dx < 0:
                self._field.update_field(self._col + 1, self._row, EMPTY)
            elif self._dy > 0:
                self._field.update_field(self._col, self._row - 1, EMPTY)
            elif self._dy < 0:
                self._field.update_field(self._col, self._row + 1, EMPTY)

        if self._field.is_blocked(self._col, self._row):
            if self._dx > 0:
                self._col -= 1
            elif self._dx < 0:
                self._col += 1
            elif self._dy > 0:
                self._row -= 1
            elif self._dy < 0:
                self._row += 1

        super(Piece, self).update(dt)

        if not self._is_moving:
            self._field.update_field(self._col, self._row, self._kind)

        self._current_sprite.update(self._x, get_py_y_value(self._y))

    def on_select(self):
        self._canvas.delete_sprite(self._current_sprite)
        self._current_sprite = self._canvas.get_sprite(self._slt_img)
        self._current_sprite.update(self._x, get_py_y_value(self._y))

    def on_drop(self):
        self._canvas.delete_sprite(self._current_sprite)
        self._current_sprite = self._canvas.get_sprite(self._dft_img)
        self._current_sprite.update(self._x, get_py_y_value(self._y))

    def get_current_sprite(self):
        return self._current_sprite


def __str__(self):
    return "<Piece col='%s' row='%s' x='%s' y='%s'>" % (self._col, self._row, self._x, self._y)


class RedPiece(Piece):
    def __init__(self, canvas: Canvas, field: Field, kind: int, col: int, row: int):
        super().__init__(RED_PIECE, RED_PIECE_SELECTED, canvas, field, kind, col, row)


class GreenPiece(Piece):
    def __init__(self, canvas: Canvas, field: Field, kind: int, col: int, row: int):
        super().__init__(GREEN_PIECE, GREEN_PIECE_SELECTED, canvas, field, kind, col, row)


class BluePiece(Piece):
    def __init__(self, canvas: Canvas, field: Field, kind: int, col: int, row: int):
        super().__init__(BLUE_PIECE, BLUE_PIECE_SELECTED, canvas, field, kind, col, row)


class PieceFactory:
    def __init__(self):
        pass

    @staticmethod
    def new_instance(field: Field, kind, col, row, canvas: Canvas):
        if kind == FIRST_KIND:
            return RedPiece(canvas, field, FIRST_KIND, col, row)
        elif kind == SECOND_KIND:
            return GreenPiece(canvas, field, SECOND_KIND, col, row)
        elif kind == THIRD_KIND:
            return BluePiece(canvas, field, THIRD_KIND, col, row)
        else:
            raise AttributeError("Invalid kind of piece")


class Selection(MovementAnimation):
    def __init__(self, col, row, canvas: Canvas):
        super().__init__(col, row)
        self._current_piece = None
        self._active = False
        self._canvas = canvas
        self._dft_img = SELECTION
        self._sprite = canvas.get_sprite(SELECTION, group=canvas.get_selection_layout())
        self._sprite.update(self._x, get_py_y_value(self._y))

    def move_down(self):
        if self._active:
            self._current_piece.move_down()

        if not self._active and self._row < 5:
            super().move_down()

    def move_up(self):
        if self._active:
            self._current_piece.move_up()

        if not self._active and self._row > 1:
            super().move_up()

    def move_right(self):
        if self._active:
            self._current_piece.move_right()

        if not self._active and self._col < 5:
            super().move_right()

    def move_left(self):
        if self._active:
            self._current_piece.move_left()

        if not self._active and self._col > 1:
            super().move_left()

    def update(self, dt):
        if self._active:
            self._current_piece.update(dt)

        if not self._active:
            super().update(dt)
            if self._sprite is not None:
                self._sprite.update(self._x, get_py_y_value(self._y))

    def select(self, piece: Piece):
        self._canvas.delete_sprite(self._sprite)
        self._current_piece = piece
        self._current_piece.on_select()
        self._active = True

    def drop(self):
        self._col = self._current_piece.get_col()
        self._row = self._current_piece.get_row()
        self._x = offset_x + self._col * 64
        self._y = offset_y + self._row * 64
        self._current_piece.on_drop()
        self._current_piece = None
        self._sprite = self._canvas.get_sprite(self._dft_img, group=self._canvas.get_selection_layout())
        self._active = False

    def get_sprite(self):
        return self._sprite

    def is_moving(self):
        if self._current_piece is not None:
            return self._current_piece.is_moving()

        return self._is_moving

    def is_active(self):
        return self._active
