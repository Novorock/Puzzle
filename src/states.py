from pyglet.shapes import Rectangle
from pyglet.window import key
from pyglet.text import Label
from util import window_width, window_height, offset_x, offset_y, get_py_y_value
from util import GROUND, BLOCK, FIRST_KIND, SECOND_KIND, THIRD_KIND
from foundation import PieceFactory, Selection
from environment import Field, Canvas


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


class GameStateManager:
    def __init__(self, canvas: Canvas):
        self.intro_state = 0
        self.play_state = 1
        self.end_state = 2
        self._canvas = canvas
        self._current_state = None

    def set_state(self, state):
        if state == self.intro_state:
            self._current_state = IntroState(self, self._canvas)
        elif state == self.play_state:
            self._current_state = PlayState(self, self._canvas)
        elif state == self.end_state:
            self._current_state = None

    def on_key_press(self, symbol):
        self._current_state.on_key_press(symbol)

    def update(self, dt):
        self._current_state.update(dt)

    def draw(self):
        self._canvas.draw()


class State:
    def __init__(self, gsm: GameStateManager, canvas: Canvas):
        self._canvas = canvas
        self._gsm = gsm

    def update(self, dt):
        pass

    def on_key_press(self, symbol):
        pass


class IntroState(State):
    def __init__(self, gsm: GameStateManager, canvas: Canvas):
        super().__init__(gsm, canvas)
        self._background = Rectangle(0, 0, width=window_width, height=window_height, batch=canvas.get_batch(),
                                     color=(0, 0, 0))
        canvas.track(self._background)
        self._help_label = Label('Hello, world',
                                 batch=canvas.get_batch(),
                                 font_name='',
                                 font_size=36,
                                 x=window_width // 2, y=window_height // 2,
                                 anchor_x='center', anchor_y='center')

    def on_key_press(self, symbol):
        if symbol == key.ENTER:
            self._gsm.set_state(self._gsm.play_state)
            self._help_label.delete()
            del self._help_label
            self._background.delete()
            del self._background


class PlayState(State):
    def __init__(self, gsm: GameStateManager, canvas: Canvas):
        super().__init__(gsm, canvas)
        self._event_tick = 0
        self._start_event = True
        self._rectangles = []

        for i in range(9):
            self._rectangles.append(
                Rectangle(0, i * 64, width=window_width, height=64, batch=canvas.get_batch(),
                          group=canvas.get_curtain(), color=(0, 0, 0)))
            canvas.track(self._rectangles[-1])

        self._field = Field({'first_line': FIRST_KIND, 'second_line': SECOND_KIND, 'third': THIRD_KIND})
        self._factory = PuzzleFactory(self._field, self._canvas)
        self._pieces = self._factory.create_pieces()
        self._factory.build_environment()
        self._selection = Selection(1, 4, self._canvas)

    def update(self, dt):
        if self._start_event:
            self.start_event()

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

    def start_event(self):
        self._event_tick += 1

        for i in range(0, 9, 2):
            self._rectangles[i].x -= 12

        for i in range(1, 9, 2):
            self._rectangles[i].x += 12

        if self._rectangles[0].x < -window_width:
            self._start_event = False
            self._canvas.delete_drawable(self._rectangles)
            self._rectangles.clear()
