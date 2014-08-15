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

        # Write stellar system and star properties
        file.write(self.starsystemprop())

        file.write(self.starprop())

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

    def starprop(self):
        str = """\section{Star Properties}
% Number of data columns = Number of stars
\\begin{table}[H]
\centering
\\begin{tabular}{"""
        numstar = len(self.starsystem.stars)
        str += 'l' * (numstar + 1) + '}\n'
        str += '\\toprule\n'
        str += 'Property '
        letters = ['A', 'B', 'C']
        for nst in range(numstar):
            str += '& Star ' + letters[nst] + ' '
        str += '\\\\ \n\midrule\n'

        sequence = 'Sequence   '
        mass = 'Mass       '
        temp = 'Temperature'
        lum = 'Luminosity '
        rad = 'Radius     '
        inner = 'Inner Limit'
        outer = 'Outer Limit'
        snowline = 'Snow line  '
        if numstar > 1:
            fzinner = 'FZ Inner   '
            fzouter = 'FZ Outer   '
        for star in self.starsystem.stars:
            sequence += ' & ' + star.getSequence()
            mass += ' & {:7.2f}'.format(star.getMass())
            temp += ' & {:7.0f}'.format(star.getTemp())
            lum += ' & {:7.4f}'.format(star.getLuminosity())
            rad += ' & {:7.5f}'.format(star.getRadius())
            inner += ' & {:7.2f}'.format(star.getOrbitlimits()[0])
            outer += ' & {:6.1f} '.format(star.getOrbitlimits()[1])
            snowline += ' & {:7.2f}'.format(star.getSnowline())
            if numstar > 1:
                fzinner += ' & {:6.1f} '.format(star.getForbidden()[0])
                fzouter += ' & {:6.1f} '.format(star.getForbidden()[1])
        #for string in [sequence, mass, temp, lum, rad, inner, outer, snowline]:
        #    string += '\\\\ \n'
        eol = ' \\\\ \n'
        sequence += eol
        mass += eol
        temp += eol
        lum += eol
        rad += eol
        inner += eol
        outer += eol
        snowline += eol
        if numstar > 1:
            fzinner += eol
            fzouter += eol

        str += sequence + mass + temp + lum + rad + inner + outer + snowline
        if numstar > 1:
            str += fzinner + fzouter
        str += '\\bottomrule\n\end{tabular} \n\end{table} \n\n'

        return str

    def end(self):
        return "\n\n\\end{document}"
