from pyglet import app
from pyglet import clock
from pyglet.window import Window, FPSDisplay
from pyglet import gl
import puzzle

game = puzzle.Puzzle()

main_window = Window(576, 576)
main_window.set_caption('Puzzle')
fps_display = FPSDisplay(main_window)

gl.glClearColor(89 / 255, 106 / 255, 108 / 255, 1)


def update(dt):
    game.update(dt)


@main_window.event
def on_key_press(symbol, modifiers):
    game.on_key_press(symbol)


@main_window.event
def on_key_release(symbol, modifiers):
    pass


@main_window.event
def on_draw():
    main_window.clear()
    game.draw()
    fps_display.draw()


if __name__ == '__main__':
    clock.schedule_interval(update, 1 / 120.0)
    app.run()
