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

        # Write star system properties
        file.write(self.starsystemprop())


        # Write the end of document
        file.write(self.end())
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

    def starsystemprop(self):
        str = """\chapter{The Star System}
\section{Star System Properties}
"""
        numstar = len(self.starsystem.stars)
        str += "Number of stars: {}\\\\ \n".format(numstar)
        age = self.starsystem.getAge()
        str += "Stellar age: {} billion years \n\n".format(age)

        # Only put table (about the properties of the stellar system) if
        # necessary (i.e. more than one star)
        if numstar > 1:
            str += """\\begin{table}[H]
\centering
\\begin{tabular}{"""
            str += 'l' * numstar
            str += "}\n\\toprule \n"
            if numstar == 2:
                header = "Pair A--B \\\\ \n"
            else:
                header = "Pair A--B & Pair A--C \\\\ \n"
            str += "Property & " + header
            str += "\midrule\n"
            # Extract orbit and eccentricities
            oecc = self.starsystem.getOrbits()
            orb = ''
            ecc = ''
            for o, e in oecc:
                orb += ' & {:8.2f}'.format(round(o, 2))
                ecc += ' & {:8.2f}'.format(round(e, 2))
            str += "Orbital Separation [AU] " + orb + ' \\\\ \n'
            str += "Orbital Eccentricity    " + ecc + ' \\\\ \n'
            str += "Orbital Period [d]      "
            for per in self.starsystem.getPeriod():
                str += ' & {:7.1f} '.format(round(per, 1))
            str += " \\\\ \n"
            str += "\\bottomrule\n\end{tabular} \n\end{table}\n\n"
        return str


    def end(self):
        return "\n\n\\end{document}"
