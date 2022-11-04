from pyglet.shapes import Rectangle
from pyglet.window import key
from pyglet.text import Label
from src.util import window_width, window_height, offset_x, offset_y, get_py_y_value
from src.util import GROUND, BLOCK, FIRST_KIND, SECOND_KIND, THIRD_KIND
from src.foundation import PieceFactory, Selection
from src.environment import Field, Canvas


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
            self._current_state = EndState(self, self._canvas)

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
        self._title = Label(text='PUZZLE', font_name='Small Pixel', font_size=30,
                            x=window_width // 2, y=window_height // 2 + 64,
                            anchor_x='center', anchor_y='center',
                            batch=canvas.get_batch(), group=canvas.get_text_layout())
        self._movement_info_1 = Label(text='<ENTER> or <SPACE> to select pieces', font_name='Small Pixel', font_size=16,
                                      x=window_width // 2, y=window_height // 2,
                                      anchor_x='center', anchor_y='center',
                                      batch=canvas.get_batch(), group=canvas.get_text_layout())
        self._movement_info_2 = Label(text='<ARROWS> to move piece', font_name='Small Pixel', font_size=16,
                                      x=window_width // 2, y=window_height // 2 - 32,
                                      anchor_x='center', anchor_y='center',
                                      batch=canvas.get_batch(), group=canvas.get_text_layout())
        self._continue_info = Label(text='Press <ENTER> to continue', font_name='Small Pixel', font_size=16,
                                    x=window_width // 2, y=window_height // 2 - 128,
                                    anchor_x='center', anchor_y='center',
                                    batch=canvas.get_batch(), group=canvas.get_text_layout())
        self._background = Rectangle(0, 0, width=window_width, height=window_height, batch=canvas.get_batch(),
                                     group=canvas.get_curtain(), color=(0, 0, 0))
        canvas.track(self._title)
        canvas.track(self._movement_info_1)
        canvas.track(self._movement_info_2)
        canvas.track(self._continue_info)
        canvas.track(self._background)

        self._ticks = 0
        self._forward_animation = True

    def update(self, dt):
        if self._continue_info is None:
            return

        if self._forward_animation:
            self._ticks += 1
        else:
            self._ticks -= 1

        self._continue_info.color = (255, 255, 255, 255 - 255 * self._ticks // 80)

        if self._ticks == 80:
            self._forward_animation = False
        elif self._ticks == 0:
            self._forward_animation = True

    def on_key_press(self, symbol):
        if symbol == key.ENTER:
            self._gsm.set_state(self._gsm.play_state)
            self._canvas.delete_drawable(
                [self._movement_info_1, self._movement_info_2, self._title, self._continue_info])
            self._background.delete()
            self._title.delete()
            self._movement_info_1.delete()
            self._movement_info_2.delete()
            self._continue_info.delete()


class PlayState(State):
    def __init__(self, gsm: GameStateManager, canvas: Canvas):
        super().__init__(gsm, canvas)
        self._event_tick = 0
        self._start_event, self._end_event = True, False
        self._rectangles = []

        for i in range(9):
            self._rectangles.append(
                Rectangle(0, i * 64, width=window_width, height=64, batch=canvas.get_batch(),
                          group=canvas.get_curtain(), color=(0, 0, 0)))
            canvas.track(self._rectangles[-1])

        self._field = Field({'first_line': FIRST_KIND, 'second_line': SECOND_KIND, 'third_line': THIRD_KIND})
        self._factory = PuzzleFactory(self._field, self._canvas)
        self._pieces = self._factory.create_pieces()
        self._factory.build_environment()
        self._selection = Selection(1, 4, self._canvas)

    def update(self, dt):
        if self._start_event:
            self.start_event()

        if self._end_event:
            self.end_event()

        self._selection.update(dt)

        if self._field.check_vertical_lines():
            self._end_event = True

    def on_key_press(self, symbol):
        if symbol == key.RIGHT:
            self._selection.move_right()
        elif symbol == key.LEFT:
            self._selection.move_left()
        elif symbol == key.DOWN:
            self._selection.move_down()
        elif symbol == key.UP:
            self._selection.move_up()

        if symbol == key.SPACE or symbol == key.ENTER:
            if self._selection.is_active() and not self._selection.is_moving():
                self._selection.drop()
            else:
                col, row = self._selection.get_col(), self._selection.get_row()
                result = list(filter(lambda piece: piece.get_col() == col and piece.get_row() == row, self._pieces))
                if len(result) > 0:
                    self._selection.select(result[0])

    def start_event(self):
        for i in range(0, 9, 2):
            self._rectangles[i].x -= 12

        for i in range(1, 9, 2):
            self._rectangles[i].x += 12

        if self._rectangles[0].x < -window_width:
            self._start_event = False

    def end_event(self):
        if self._event_tick > 60:
            for i in range(0, 9, 2):
                self._rectangles[i].x += 12

            for i in range(1, 9, 2):
                self._rectangles[i].x -= 12

            if self._rectangles[0].x > 0:
                self._end_event = False

            if self._rectangles[0].x > 0:
                self._gsm.set_state(self._gsm.end_state)
        else:
            self._event_tick += 1


class EndState(State):
    def __init__(self, gsm: GameStateManager, canvas: Canvas):
        super().__init__(gsm, canvas)
        self._background = Rectangle(0, 0, width=window_width, height=window_height, batch=canvas.get_batch(),
                                     group=canvas.get_curtain(), color=(0, 0, 0))
        self._title = Label(text='THE END', font_name='Small Pixel', font_size=30,
                            x=window_width // 2, y=window_height // 2 + 64,
                            anchor_x='center', anchor_y='center',
                            batch=canvas.get_batch(), group=canvas.get_text_layout())
