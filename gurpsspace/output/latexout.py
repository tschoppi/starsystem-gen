"""latexout.py

Module for saving all the information about a StarSystem to a LaTeX file for
processing towards a nicely formatted PDF file.
"""

#from ..starsystem import StarSystem

class LatexWriter:
    def __init__(self, starsystem, filename):
        self.starsystem = starsystem
        self.filename = filename

    def write(self):
        # First check for existing file
        pass
