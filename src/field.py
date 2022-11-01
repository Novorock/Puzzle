from pyglet.graphics import Batch, OrderedGroup


class Field:
    def __init__(self, scheme: dict):
        self._matrix = [
            [10, 11, 10, 12, 10, 13, 10],
            [10, 21, 10, 22, 10, 23, 10],
            [10, 21, 21, 22, 22, 23, 10],
            [10, 0, 10, 22, 10, 23, 10],
            [10, 21, 0, 22, 0, 23, 10],
            [10, 21, 10, 0, 10, 23, 10],
            [10, 10, 10, 10, 10, 10, 10]
        ]

        self._scheme = scheme

    def check_vertical_lines(self):
        kind_1_line, kind_2_line, kind_3_line = True, True, True

        for i in range(1, 6):
            if self._matrix[i][1] != self._scheme['kind1']:
                kind_1_line = False
                break

        for i in range(1, 6):
            if self._matrix[i][3] != self._scheme['kind2']:
                kind_2_line = False
                break

        for i in range(1, 6):
            if self._matrix[i][5] != self._scheme['kind3']:
                kind_3_line = False
                break

        return kind_1_line and kind_2_line and kind_3_line

    def get_size(self):
        return len(self._matrix)

    def update_field(self, col: int, row: int, tile: int):
        if not (0 <= row < len(self._matrix) or 0 <= col < len(self._matrix[0])):
            raise AttributeError("Tile<%s> outside matrix: col='%s', row='%s'" % (tile, col, row))

        self._matrix[row][col] = tile

    def is_blocked(self, col: int, row: int):
        return self._matrix[row][col] // 10 == 1 or self._matrix[row][col] // 10 == 2

    def get_tile_kind(self, col: int, row: int):
        return self._matrix[row][col]


class Canvas:
    def __init__(self):
        self._drawable_objects = []
        self._batch = Batch()
        self._background = OrderedGroup(0)
        self._foreground = OrderedGroup(1)

    def add_drawable(self, drawable, background=False):
        drawable.batch = self._batch

        if background:
            drawable.group = self._background
        else:
            drawable.group = self._foreground

        self._drawable_objects.append(drawable)

    def contains(self, drawable):
        return drawable in self._drawable_objects

    def draw(self):
        self._batch.draw()
