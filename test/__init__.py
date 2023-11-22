import sangfroid
import os

def get_sif(name):
    filename = os.path.join(
            os.path.dirname(__file__),
            name,
            )

    return sangfroid.Sif(filename)
