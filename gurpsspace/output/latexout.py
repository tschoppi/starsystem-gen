"""latexout.py

Module for saving all the information about a StarSystem to a LaTeX file for
processing towards a nicely formatted PDF file.
"""

#from ..starsystem import StarSystem

class LatexWriter:
    def __init__(self, starsystem, filename='starsystem.tex'):
        self.starsystem = starsystem
        self.filename = filename

    def write(self):
        # Open the file
        file = open(self.filename, 'w')

        # Write the preamble
        file.write(self.preamble())

        # Write the title page, ToC and first chapter
        file.write(self.title())


        # Close the file
        file.close()

    def preamble(self):
        preambulum = """\documentclass[a4paper,12pt,twoside]{scrreprt}

\\usepackage[T1]{fontenc}
\\usepackage[latin1]{inputenc}
\\usepackage[inner=35mm,outer=25mm,top=30mm,bottom=30mm]{geometry}
\\usepackage{float}
\\usepackage[hidelinks]{hyperref}
\\usepackage{booktabs}
\\usepackage[figuresright]{rotating} % For sideways tables
\\usepackage{pdflscape} % For rotation in the PDF
\setkomafont{sectioning}{\\bfseries}

% Activate the following two for nicer fonts
%\\usepackage{charter}
%\\usepackage[bitstream-charter]{mathdesign}

\\usepackage{scrlayer-scrpage}
\pagestyle{scrheadings}

\setcounter{tocdepth}{1}

"""
        return preambulum

    def title(self):
        titelus = """
\\begin{document}
\\title{CAS: Computer-Assisted Starsystem}
\subtitle{A GURPS Star System}
\\author{The Guy in Front of The Computer}
\date{\\today}
\maketitle

\\tableofcontents
\clearpage

\chapter{Summary}
\section{General Description}
% Give a general description, such as the one you could hand out to your players

\section{GM Notes}
% Enter here the GM Notes

"""
        return titelus
