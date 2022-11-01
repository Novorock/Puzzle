from pyglet.sprite import Sprite
from util import get_py_y_value, load_sprite
from util import offset_x, offset_y
from field import Field

GROUND_TILE = load_sprite('ground_06.png')
BLOCK_TILE = load_sprite('block.png', rescale=True)
BLOCK_RED = load_sprite('block_red_signature.png')
BLOCK_GREEN = load_sprite('block_green_signature.png')
BLOCK_BLUE = load_sprite('block_blue_signature.png')
RED_PIECE = load_sprite('pieces/red_piece.png')
GREEN_PIECE = load_sprite('pieces/green_piece.png')
BLUE_PIECE = load_sprite('pieces/blue_piece.png')
SELECTION = load_sprite('selection.png')
RED_PIECE_SELECTED = load_sprite('pieces/red_piece_selected.png')
GREEN_PIECE_SELECTED = load_sprite('pieces/green_piece_selected.png')
BLUE_PIECE_SELECTED = load_sprite('pieces/blue_piece_selected.png')

MOVEMENT_SPEED = 200
GROUND, BLOCK, RED_SIGN, GREEN_SIGN, BLUE_SIGN = 0, 10, 11, 12, 13
KIND_1, KIND_2, KIND_3 = 21, 22, 23


class MovementAnimation:
    def __init__(self, col, row):
        self._col = col
        self._row = row
        self._x = offset_x + col * 64
        self._y = offset_y + row * 64
        self._dx, self._dy = 0, 0
        self._is_moving = False

    def move_down(self):
        self._row += 1
        self._dy = MOVEMENT_SPEED
        self._is_moving = True

    def move_up(self):
        self._row -= 1
        self._dy = -MOVEMENT_SPEED
        self._is_moving = True

    def move_right(self):
        self._col += 1
        self._dx = MOVEMENT_SPEED
        self._is_moving = True

    def move_left(self):
        self._col -= 1
        self._dx = -MOVEMENT_SPEED
        self._is_moving = True

    @classmethod
    def is_next_tile(cls, dx, x, col):
        if (dx > 0 and x > offset_x + col * 64) or (
                dx < 0 and x < offset_x + col * 64):
            return True

        return False

    def update(self, dt):
        if self._is_moving:
            self._x += self._dx * dt
            self._y += self._dy * dt

            if self.is_next_tile(self._dx, self._x, self._col):
                self._x = offset_x + self._col * 64
                self._dx = 0
            elif self.is_next_tile(self._dy, self._y, self._row):
                self._y = offset_y + self._row * 64
                self._dy = 0

        if self._dy == 0 and self._dx == 0:
            self._is_moving = False

    def is_moving(self):
        return self._is_moving

    def get_col(self):
        return self._col

    def get_row(self):
        return self._row


class Piece(MovementAnimation):
    def __init__(self, sprite: Sprite, on_selection_sprite: Sprite, kind: int, col, row, field: Field):
        self._sprite = sprite
        self._kind = kind
        self._on_selection = False
        self._on_selection_sprite = on_selection_sprite
        self._field = field
        super().__init__(col, row)

    def move_down(self):
        if not self._field.is_blocked(self._col, self._row + 1) and not self._is_moving:
            super().move_down()
            self._field.update_field(self._col, self._row - 1, GROUND)
            self._field.update_field(self._col, self._row, self._kind)

    def move_up(self):
        if not self._field.is_blocked(self._col, self._row - 1) and not self._is_moving:
            super().move_up()
            self._field.update_field(self._col, self._row + 1, GROUND)
            self._field.update_field(self._col, self._row, self._kind)

    def move_right(self):
        if not self._field.is_blocked(self._col + 1, self._row) and not self._is_moving:
            super().move_right()
            self._field.update_field(self._col - 1, self._row, GROUND)
            self._field.update_field(self._col, self._row, self._kind)

    def move_left(self):
        if not self._field.is_blocked(self._col - 1, self._row) and not self._is_moving:
            super().move_left()
            self._field.update_field(self._col + 1, self._row, GROUND)
            self._field.update_field(self._col, self._row, self._kind)

    def update(self, dt):
        super().update(dt)

    def set_selection(self, value: bool):
        self._on_selection = value

    def draw(self):
        if not self._on_selection:
            self._sprite.update(self._x, get_py_y_value(self._y))
            self._sprite.draw()
        else:
            self._on_selection_sprite.update(self._x, get_py_y_value(self._y))
            self._on_selection_sprite.draw()

    def __str__(self):
        return "<Piece col='%s' row='%s' x='%s' y='%s'>" % (self._col, self._row, self._x, self._y)


class RedPiece(Piece):
    def __init__(self, col, row, field):
        super().__init__(RED_PIECE, RED_PIECE_SELECTED, KIND_1, col, row, field)


class GreenPiece(Piece):
    def __init__(self, col, row, field):
        super().__init__(GREEN_PIECE, GREEN_PIECE_SELECTED, KIND_2, col, row, field)


class BluePiece(Piece):
    def __init__(self, col, row, field):
        super().__init__(BLUE_PIECE, BLUE_PIECE_SELECTED, KIND_3, col, row, field)


class PieceFactory:
    def __init__(self):
        pass

    @staticmethod
    def new_instance(kind, col, row, field: Field):
        if kind == KIND_1:
            return RedPiece(col, row, field)

        if kind == KIND_2:
            return GreenPiece(col, row, field)

        if kind == KIND_3:
            return BluePiece(col, row, field)


class Selection(MovementAnimation):
    def __init__(self, col, row):
        self._sprite = SELECTION
        self._current_piece = None
        self._active = False
        super().__init__(col, row)

    def move_down(self):
        if self._active:
            self._current_piece.move_down()

        if not self._active and not self._is_moving:
            super().move_down()

    def move_up(self):
        if self._active:
            self._current_piece.move_up()

        if not self._active and not self._is_moving:
            super().move_up()

    def move_right(self):
        if self._active:
            self._current_piece.move_right()

        if not self._active and not self._is_moving:
            super().move_right()

    def move_left(self):
        if self._active:
            self._current_piece.move_left()

        if not self._active and not self._is_moving:
            super().move_left()

    def update(self, dt):
        if self._active:
            self._current_piece.update(dt)

        if not self._active:
            super().update(dt)

    def select(self, piece: Piece):
        self._current_piece = piece
        self._current_piece.set_selection(True)
        self._active = True

    def drop(self):
        self._col = self._current_piece.get_col()
        self._row = self._current_piece.get_row()
        self._x = offset_x + self._col * 64
        self._y = offset_y + self._row * 64
        self._current_piece.set_selection(False)
        self._current_piece = None
        self._active = False

    def is_moving(self):
        if self._current_piece is not None:
            return self._current_piece.is_moving()

        return self._is_moving

    def is_active(self):
        return self._active

    def draw(self):
        if not self._active:
            self._sprite.update(self._x, get_py_y_value(self._y))
            self._sprite.draw()
