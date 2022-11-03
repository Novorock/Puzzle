from pyglet.graphics import Batch, OrderedGroup
from pyglet.sprite import Sprite
from pyglet.image import ImageData
from util import BLOCKED


class Field:
    def __init__(self, scheme: dict):
        self._background = [
            [0, 4, 7, 5, 7, 6, 0, 0],
            [0, 1, 2, 2, 2, 2, 2, 0],
            [0, 3, 0, 0, 0, 0, 0, 0],
            [0, 3, 0, 0, 0, 0, 0, 0],
            [0, 3, 0, 0, 0, 0, 0, 0],
            [0, 3, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]

        self._matrix = [
            [10, 10, 10, 10, 10, 10, 10],
            [10, 21, 10, 22, 10, 23, 10],
            [10, 21, 21, 22, 22, 23, 10],
            [10, 0, 10, 22, 10, 23, 10],
            [10, 21, 0, 22, 0, 23, 10],
            [10, 21, 10, 0, 10, 23, 10],
            [10, 10, 10, 10, 10, 10, 10]
        ]

        self._scheme = scheme

    def check_vertical_lines(self):
        first_line, second_line, third_line = True, True, True

        for i in range(1, 6):
            if self._matrix[i][1] != self._scheme['first_line']:
                first_line = False
                break

        for i in range(1, 6):
            if self._matrix[i][3] != self._scheme['second_line']:
                second_line = False
                break

        for i in range(1, 6):
            if self._matrix[i][5] != self._scheme['third_line']:
                third_line = False
                break

        return first_line and second_line and third_line

    def get_size(self):
        return len(self._matrix)

    def update_field(self, col: int, row: int, tile: int):
        if not (0 <= row < len(self._matrix) or 0 <= col < len(self._matrix[0])):
            raise AttributeError("Tile<%s> outside matrix: col='%s', row='%s'" % (tile, col, row))

        self._matrix[row][col] = tile

    def is_blocked(self, col: int, row: int):
        return (self._matrix[row][col] // 10) in BLOCKED

    def get_tile(self, col: int, row: int):
        return self._matrix[row][col]

    def get_background_tile(self, col: int, row: int):
        return self._background[row][col]


class Canvas:
    def __init__(self):
        self._drawable_objects = []
        self._batch = Batch()
        self._background = OrderedGroup(0)
        self._foreground = OrderedGroup(1)
        self._curtain = OrderedGroup(2)
        self._text_layout = OrderedGroup(3)

    def get_sprite(self, img: ImageData, *, x=0, y=0, background=False):
        if background:
            sprite = Sprite(img=img, batch=self._batch, group=self._background, x=x, y=y)
        else:
            sprite = Sprite(img=img, batch=self._batch, group=self._foreground, x=x, y=y)

        self._drawable_objects.append(sprite)

        return sprite

    def delete_sprite(self, sprite: Sprite):
        if sprite is not None:
            sprite.delete()
            self._drawable_objects.remove(sprite)

    def get_batch(self):
        return self._batch

    def get_curtain(self):
        return self._curtain

    def get_text_layout(self):
        return self._text_layout

    def delete_drawable(self, objects):
        for drawable in objects:
            self._drawable_objects.remove(drawable)

    def track(self, drawable):
        self._drawable_objects.append(drawable)

    def draw(self):
        self._batch.draw()
