import sangfroid
import os

def get_animation(name):
    filename = os.path.join(
            os.path.dirname(__file__),
            name,
            )

    return sangfroid.Animation(filename)
