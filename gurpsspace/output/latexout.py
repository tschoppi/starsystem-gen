"""latexout.py

Module for saving all the information about a StarSystem to a LaTeX file for
processing towards a nicely formatted PDF file.
"""

# from ..starsystem import StarSystem
from ..tables import AtmCompAbbr


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

        # Write the overviews
        file.write(self.overviews())

        # Write the detailed planet system chapters
        for star in self.starsystem.stars:
            str = self.psdetails(star.planetsystem)
            file.write(str)

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
\\usepackage{multirow}
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
        age = self.starsystem.get_age()
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
            oecc = self.starsystem.get_orbits()
            orb = ''
            ecc = ''
            for o, e in oecc:
                orb += ' & {:8.2f}'.format(round(o, 2))
                ecc += ' & {:8.2f}'.format(round(e, 2))
            str += "Orbital Separation [AU] " + orb + ' \\\\ \n'
            str += "Orbital Eccentricity    " + ecc + ' \\\\ \n'
            str += "Orbital Period [d]      "
            for per in self.starsystem.get_period():
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
        for star in self.starsystem.stars:
            str += '& Star ' + star.get_letter() + ' '
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
            sequence += ' & ' + star.get_sequence()
            mass += ' & {:7.2f}'.format(star.get_mass())
            temp += ' & {:7.0f}'.format(star.get_temp())
            lum += ' & {:7.4f}'.format(star.get_luminosity())
            rad += ' & {:7.5f}'.format(star.get_radius())
            inner += ' & {:7.2f}'.format(star.get_orbit_limits()[0])
            outer += ' & {:6.1f} '.format(star.get_orbit_limits()[1])
            snowline += ' & {:7.2f}'.format(star.get_snowline())
            if numstar > 1:
                fzinner += ' & {:6.1f} '.format(star.get_forbidden_zone()[0])
                fzouter += ' & {:6.1f} '.format(star.get_forbidden_zone()[1])

        # for string in [sequence, mass, temp, lum, rad, inner, outer, snowline]:
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
        str += '\\bottomrule\n\end{tabular} \n\end{table} \n\\vfill\n\n'

        return str

    def overviews(self):
        # Gather number of planet systems
        # For each planet system:
        #  - List orbits and occupants
        #  - List terrestrial planet details
        #  - List Moons and Moonlets
        #  - List Asteroid Belts
        str = ''
        for star in self.starsystem.stars:
            lettr = star.get_letter()
            ps = star.planetsystem
            oc = ps.get_orbitcontents()
            types = [pl.type() for key, pl in oc.items()]

            title = 'Overview -- Planet System ' + lettr
            str += '\chapter{' + title + '}\n'
            str += '\section{Summary}\n% A small amount of short sentences describing the general feel of this planet system.\n\n'
            str += '\section{Description}\n% A more in-depth description of the planet system.\n\n'
            str += '\section{GM Notes}\n% Notes about the planet system and eventual adventures that can be undertaken.\n\n'
            str += '\\begin{landscape}\n\section{List of Orbits and their Occupants}\n\\begin{table}[H]\n\\begin{tabular}{llllrrrrrrrrr}\n'  # noqa
            str += '\\toprule\n'
            str += '\multirow{2}{*}{Name} & \multirow{2}{*}{Type} & \multirow{2}{*}{Size} & \multirow{2}{*}{World} & $R_\mathrm{orb}$ & $P_\mathrm{orb}$ & \multirow{2}{*}{Ecc.} & $R_\mathrm{min}$ & $R_\mathrm{max}$ & \multirow{2}{*}{Moons} & \multirow{2}{*}{Moonlets} & $T_\mathrm{BB}$ \\\\ \n'  # noqa
            str += '\cmidrule(lr){5-5} \cmidrule(lr){6-6} \cmidrule(lr){8-8} \cmidrule(lr){9-9} \cmidrule(lr){12-12}\n'
            str += '& & & & \multicolumn{1}{c}{AU} & \multicolumn{1}{c}{Year} & & \multicolumn{1}{c}{AU} & \multicolumn{1}{c}{AU} & & & \multicolumn{1}{c}{K} \\\\ \n'  # noqa
            str += '\midrule\n'
            for skey in sorted(oc):
                str += '{} & '.format(oc[skey].get_name())
                str += '{} & '.format(oc[skey].type())
                str += '{} & '.format(oc[skey].get_size())
                str += '{} & '.format(oc[skey].get_type())
                str += '{:.2f} & '.format(oc[skey].get_orbit())
                str += '{:.2f} & '.format(oc[skey].get_period())
                str += '{:.2f} & '.format(oc[skey].get_eccentricity())
                str += '{:.2f} & '.format(oc[skey].get_min_max()[0])
                str += '{:.2f} & '.format(oc[skey].get_min_max()[1])
                nmoon = oc[skey].num_moons()
                nmoonlts = oc[skey].num_moonlets()
                if nmoon is 0:
                    str += ' & '
                else:
                    str += '{} & '.format(oc[skey].num_moons())
                if nmoonlts is 0:
                    str += ' & '
                else:
                    str += '{} & '.format(oc[skey].num_moonlets())
                str += '{:.0f}'.format(oc[skey].get_blackbody_temp())
                str += '\\\\ \n'
            str += '\\bottomrule\n\end{tabular}\n\end{table}\n\\vfill\n\n'

            # Now gather all asteroid belts and print an overview table
            astable = '\section{List of Asteroid Belts}\n\n'
            astable += '\\begin{table}[H]\n\\begin{tabular}{lrlrrr}\n'
            astable += '\\toprule\n'
            astable += 'Name & $T_\mathrm{surf}$ [K] & Climate Type & RVM & Affinity \\\\ \n'
            astable += '\midrule\n'
            for skey in sorted(oc):
                if oc[skey].type() != 'Ast. Belt':
                    continue
                astable += '{} & '.format(oc[skey].get_name())
                astable += '{:.0f} & '.format(oc[skey].get_average_surface_temp())
                astable += '{} & '.format(oc[skey].get_climate())
                astable += '{:+.0f} & '.format(oc[skey].get_rvm())
                astable += '{:+.0f} '.format(oc[skey].get_affinity())
                astable += '\\\\ \n'
            astable += '\\bottomrule\n\end{tabular}\n\end{table}\n\n'

            if 'Ast. Belt' in types:
                str += astable
            else:
                str += '\pagebreak\n\n'

            # Make a detail table for all terrestrials
            tertable = '\section{List of Planets and their Properties}\n'
            tertable += '\\begin{table}[H]\n\\begin{tabular}{l ' + ('l' * types.count('Terrestrial')) + '}\n'
            tertable += '\\toprule\n'
            tertable += '\multirow{2}{*}{Property} & \multicolumn{' + '{}'.format(types.count('Terrestrial')) + '}{c}{Planet Name}\\\\ \n'  # noqa
            for skey in sorted(oc):
                if oc[skey].type() != 'Terrestrial':
                    continue
                tertable += ' & {}'.format(oc[skey].get_name())
            tertable += '\\\\ \n\midrule\n'
            wtype = '{:22}'.format('World Type')
            size = '{:22}'.format('World Size')
            atmass = '{:22}'.format('Atm. Mass')
            atcom = '{:22}'.format('Atm. Comp.$^1$')
            hydro = '{:22}'.format('Hydr. Cov. [\%]')
            tsurf = '{:22}'.format('$T_\mathrm{surf}$ [K]')
            climate = '{:22}'.format('Climate Type')
            dens = '{:22}'.format('Density')
            diam = '{:22}'.format('Diameter')
            grav = '{:22}'.format('Surface Gravity')
            mass = '{:22}'.format('Mass')
            press = '{:22}'.format('Pressure [atm]')
            presscat = '{:22}'.format('Pressure Cat.')
            tte = '{:22}'.format('TTE$^2$')
            volc = '{:22}'.format('Volcanics')
            tect = '{:22}'.format('Tectonics')
            rvm = '{:22}'.format('RVM$^3$')
            hab = '{:22}'.format('Habitability')
            aff = '{:22}'.format('Affinity')
            prot = '{:22}'.format('$P_\mathrm{rot}$ [d]')
            axtilt = '{:22}'.format('Axial Tilt [$^\circ$]')
            for skey in sorted(oc):
                if oc[skey].type() != 'Terrestrial':
                    continue
                wtype += ' & {:10}'.format(oc[skey].get_type())
                size += ' & {:10}'.format(oc[skey].get_size())
                if oc[skey].get_atmospheric_mass() == 0:
                    atmass += ' &           '
                    atcom += ' &           '
                    press += ' &           '
                else:
                    atmass += ' & {:10}'.format(oc[skey].get_atmospheric_mass())
                    # atcom += ' &           '
                    atcomp = oc[skey].atmcomp
                    atkeys = [key for key in atcomp.keys() if atcomp[key] is True]
                    abbr = ''
                    for k in atkeys:
                        abbr += AtmCompAbbr[k] + ', '
                    atcom += ' & {:10}'.format(abbr[:-2])
                    press += ' & {:10.3f}'.format(oc[skey].get_pressure())
                if oc[skey].get_hydrographic_cover() == 0:
                    hydro += ' &           '
                else:
                    hydro += ' & {:10}'.format(oc[skey].get_hydrographic_cover())
                tsurf += ' & {:10.0f}'.format(oc[skey].get_average_surface_temp())
                climate += ' & {:10}'.format(oc[skey].get_climate())
                axtilt += ' & {:10}'.format(oc[skey].get_axial_tilt())
                dens += ' & {:10}'.format(oc[skey].get_density())
                diam += ' & {:10.2f}'.format(oc[skey].get_diameter())
                grav += ' & {:10.2f}'.format(oc[skey].get_gravity())
                mass += ' & {:10.3f}'.format(oc[skey].get_mass())
                presscat += ' & {:10}'.format(oc[skey].get_pressure_category())
                tte += ' & {:10.0f}'.format(oc[skey].get_total_tidal_effect())
                volc += ' & {:10}'.format(oc[skey].get_volcanism())
                tect += ' & {:10}'.format(oc[skey].get_tectonics())
                rvm += ' & {:+10.0f}'.format(oc[skey].get_rvm())
                hab += ' & {:+10.0f}'.format(oc[skey].get_habitability())
                aff += ' & {:+10.0f}'.format(oc[skey].get_affinity())
                prot += ' & {:10.2f}'.format(oc[skey].get_rotation())
            lend = '\\\\ \n'
            tertable += size + lend
            tertable += wtype + lend
            tertable += atmass + lend
            tertable += atcom + lend
            tertable += hydro + lend
            tertable += tsurf + lend
            tertable += climate + lend
            tertable += axtilt + lend
            tertable += dens + lend
            tertable += diam + lend
            tertable += grav + lend
            tertable += mass + lend
            tertable += press + lend
            tertable += presscat + lend
            tertable += tte + lend
            tertable += volc + lend
            tertable += tect + lend
            tertable += rvm + lend + hab + lend + aff + lend
            tertable += prot + lend
            tertable += '\\bottomrule\n\end{tabular}\n\n'
            tertable += '\\footnotesize\n$^1$ '
            tertable += '\\textbf{C}: Corrosive, \\textbf{LT}: Lethally Toxic, \\textbf{HT}: Highly Toxic, \\textbf{MT}: Mildly Toxic, \\textbf{S}: Suffocating\\\\ \n'  # noqa
            tertable += '$^2$ Total Tidal Effect\\\\ \n'
            tertable += '$^3$ Resource Value Modifier \n'
            tertable += '\end{table}\n\n'
            if 'Terrestrial' in types:
                str += tertable
            del tertable
            str += '\end{landscape}\n\n'
        return str

    def psdetails(self, planetsystem):
        """Print details about the planet system

        Every new section is a new orbiting object, be it terrestrial planet,
        gas giant or major moon
        """
        letter = planetsystem.parentstar.get_letter()
        oc = planetsystem.get_orbitcontents()
        str = '\chapter{Planet System ' + letter + '}\n\n'
        # Call for each celestial body the function to print its details
        for key in sorted(oc):
            type = oc[key].type()
            if type == 'Terrestrial':
                str += self.planetdetails(oc[key])
            if type == 'Gas Giant':
                str += self.gasgiantdetails(oc[key])
        return str

    def planetdetails(self, planet):
        """Print details about terrestrial planets"""
        str = '\section{Planet ' + planet.get_name() + '}\n'
        str += '\subsection{Summary}\n\n'
        str += '\subsection{World Properties}\n'
        str += '\\begin{table}[H]\n\centering\n'
        str += '\\begin{tabular}{ll}\n'
        str += '\\toprule\n'
        str += 'Property & Value \\\\ \n\midrule\n'
        str += 'Type & {} ({})\\\\ \n'.format(planet.get_size(), planet.get_type())
        atkeys = [key for key in planet.atmcomp.keys() if planet.atmcomp[key] is True]
        abbr = ''
        for k in atkeys:
            abbr += AtmCompAbbr[k] + ', '
        if len(atkeys) > 0:
            str += 'Atm. Comp. & {} \\\\ \n'.format(abbr[:-2])
        if planet.get_pressure() == 0:
            str += 'Pressure & None \\\\ \n'
        else:
            str += 'Pressure & {:.2f} atm, {} \\\\ \n'.format(planet.get_pressure(), planet.get_pressure_category())
        str += 'Hydrographic Coverage & {:.0f} \% \\\\ \n'.format(planet.get_hydrographic_cover())
        str += 'Average $T_\mathrm{surf}$ & {temp:.1f} K \\\\ \n'.format(surf='{surf}', temp=planet.get_average_surface_temp())
        str += 'Climate Type & {} \\\\ \n'.format(planet.get_climate())
        str += 'Diameter & {:.3f} Earth Diameters\\\\ \n'.format(planet.get_diameter())
        str += 'Surface Gravity & {:.2f} G \\\\ \n'.format(planet.get_gravity())
        str += 'Affinity & {:+.0f} \\\\ \n'.format(planet.get_affinity())
        if planet.num_moons() > 0:
            str += 'Moons & {} \\\\ \n'.format(planet.num_moons())
        if planet.num_moonlets() > 0:
            str += 'Moonlets & {} \\\\ \n'.format(planet.num_moonlets())
        str += '\\bottomrule\n\end{tabular}\n\end{table}\n\\vfill\n\n'
        str += '%\subsection{Social Parameters}\n'
        str += '%\subsection{Installations}\n\n'

        if planet.num_moons() > 0:
            moons = planet.get_satellites()
            for m in moons:
                str += self.moondetails(m)
        return str

    def gasgiantdetails(self, gasgiant):
        """Print details about gas giants"""
        str = '\section{Gas Giant ' + gasgiant.get_name() + '}\n'
        str += '\subsection{Summary}\n'
        str += '\subsection{World Properties}\n'
        str += '\\begin{table}[H]\n\centering\n'
        str += '\\begin{tabular}{ll}\n'
        str += '\\toprule\n'
        str += 'Property & Value \\\\ \n'
        str += '\midrule\n'
        str += 'Mass & {} Earth Masses\\\\ \n'.format(gasgiant.get_mass())
        str += 'Density & {} Earth Densities \\\\ \n'.format(gasgiant.get_density())
        str += 'Diameter & {:.2f} Earth Diameters \\\\ \n'.format(gasgiant.get_diameter())
        str += 'Cloud-Top Gravity & {:.2f} G \\\\ \n'.format(gasgiant.get_gravity())
        str += 'Satellites $1^\mathrm{st}$ Family & {num} \\\\ \n'.format(st='{st}', num=len(gasgiant.get_first_family()))
        str += 'Satellites $2^\mathrm{nd}$ Family & {num} \\\\ \n'.format(nd='{nd}', num=len(gasgiant.get_moons()))
        str += 'Satellites $3^\mathrm{rd}$ Family & {num} \\\\ \n'.format(rd='{rd}', num=len(gasgiant.get_third_family()))
        str += '\\bottomrule\n'
        str += '\end{tabular}\n\end{table}\n\\vfill\n\n'

        moons = gasgiant.get_moons()
        for m in moons:
            str += self.moondetails(m)
        return str

    def moondetails(self, moon):
        """Print details about a major moon"""
        str = '\section{Moon ' + moon.get_name() + '}\n'
        str += '%\subsection{Summary}\n\n'
        str += '\subsection{World Properties}\n'
        str += '\\begin{table}[H]\n\centering\n'
        str += '\\begin{tabular}{ll}\n'
        str += '\\toprule\n'
        str += 'Property & Value \\\\ \n\midrule\n'
        str += 'Type & {} ({})\\\\ \n'.format(moon.get_size(), moon.get_type())
        atkeys = [key for key in moon.atmcomp.keys() if moon.atmcomp[key] is True]
        abbr = ''
        for k in atkeys:
            abbr += AtmCompAbbr[k] + ', '
        if len(atkeys) > 0:
            str += 'Atm. Comp. & {} \\\\ \n'.format(abbr[:-2])
        if moon.get_pressure() == 0:
            str += 'Pressure & None \\\\ \n'
        else:
            str += 'Pressure & {:.2f} atm, {} \\\\ \n'.format(moon.get_pressure(), moon.get_pressure_category())
        str += 'Hydrographic Coverage & {:.0f} \% \\\\ \n'.format(moon.get_hydrographic_cover())
        str += 'Average $T_\mathrm{surf}$ & {temp:.1f} K \\\\ \n'.format(surf='{surf}', temp=moon.get_average_surface_temp())
        str += 'Climate Type & {} \\\\ \n'.format(moon.get_climate())
        str += 'Diameter & {:.3f} Earth Diameters\\\\ \n'.format(moon.get_diameter())
        str += 'Surface Gravity & {:.2f} G \\\\ \n'.format(moon.get_gravity())
        str += 'Affinity & {:+.0f} \\\\ \n'.format(moon.get_affinity())
        str += '\\bottomrule\n\end{tabular}\n\end{table}\n\\vfill\n\n'
        str += '%\subsection{Social Parameters}\n'
        str += '%\subsection{Installations}\n\n'
        return str

    def end(self):
        return "\n\n\\end{document}"
