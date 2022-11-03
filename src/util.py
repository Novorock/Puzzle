from pyglet.image import ImageData, load
from pyglet.sprite import Sprite
from pyglet import font
import sys
import os

window_width, window_height = 576, 576
offset_x, offset_y = 64, 64

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)
else:
    application_path = ""

working_dir = os.path.join(application_path, 'assets\\')

print(working_dir)

font.add_file(working_dir + 'small_pixel.ttf')
SMALL_PIXEL = font.load('Small Pixel')


def set_center(img: ImageData):
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2


def rescale_sprite_64(sprite: Sprite, width, height):
    sprite.scale_x = 64 / width
    sprite.scale_y = 64 / height


def load_sprite(path: str, rescale=False):
    img = load(path)
    sprite = Sprite(img=img)

    if rescale:
        rescale_sprite_64(sprite, img.width, img.height)

    return sprite


GROUND = []
for i in range(8):
    GROUND.append(load(working_dir + 'ground_0%s.png' % i))

BLOCK = load(working_dir + 'block_02.png')
RED_PIECE = load(working_dir + 'pieces/red_piece.png')
GREEN_PIECE = load(working_dir + 'pieces/green_piece.png')
BLUE_PIECE = load(working_dir + 'pieces/blue_piece.png')
SELECTION = load(working_dir + 'selection.png')
RED_PIECE_SELECTED = load(working_dir + 'pieces/red_piece_selected.png')
GREEN_PIECE_SELECTED = load(working_dir + 'pieces/green_piece_selected.png')
BLUE_PIECE_SELECTED = load(working_dir + 'pieces/blue_piece_selected.png')

MOVEMENT_SPEED = 180
BLOCKED = [1, 2]
EMPTY, FIRST_KIND, SECOND_KIND, THIRD_KIND = 0, 21, 22, 23


def get_py_y_value(my_y_value):
    return window_height - 64 - my_y_value


def get_my_y_value(py_y_value):
    return window_height - 64 - py_y_value


def get_col(x_value):
    return (x_value - offset_x) // 64


def get_row(y_value):
    return (y_value - offset_y) // 64
