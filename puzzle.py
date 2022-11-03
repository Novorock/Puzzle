from pyglet import app
from pyglet import clock
from pyglet.window import Window, FPSDisplay
from pyglet import gl
from src.environment import Canvas
import src.states as states

main_window = Window(576, 576)
main_window.set_caption('Puzzle')
fps_display = FPSDisplay(main_window)

canvas = Canvas()
gsm = states.GameStateManager(canvas)
gsm.set_state(gsm.intro_state)

gl.glClearColor(89 / 255, 106 / 255, 108 / 255, 1)


def update(dt):
    gsm.update(dt)


@main_window.event
def on_key_press(symbol, modifiers):
    gsm.on_key_press(symbol)


@main_window.event
def on_draw():
    main_window.clear()
    gsm.draw()
    fps_display.draw()


if __name__ == '__main__':
    clock.schedule_interval(update, 1 / 120.0)
    app.run()
