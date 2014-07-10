# This file contains all the tables that will be used in this project.

# StEvoTable is the Stellar Evolution Table as per GURPS Space p. 103
StEvoTable = {
    # The mass in solar masses
    'mass': [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55,
             0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.05,
             1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 1.6,
             1.7, 1.8, 1.9, 2.0],

    # Most likely spectral type during main sequence
    # Note that the temperature is the best estimate for which spectral
    # type the star belongs to
    'type': ['M7', 'M6', 'M5', 'M4', 'M4', 'M3', 'M2', 'M1', 'M0',
             'K8', 'K6', 'K5', 'K4', 'K2', 'K0',
             'G8', 'G6', 'G4', 'G2', 'G1', 'G0',
             'F9', 'F8', 'F7', 'F6', 'F5', 'F4', 'F3', 'F2', 'F0',
             'A9', 'A7', 'A6', 'A5'],

    # The internal type is used to distinguish pure main sequencers
    # with no Lmax value (0), those with an Mspan (1) and sub- to
    # giant-type stars (2)
    'internaltype': [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                     2, 2, 2, 2],

    # Temperature of the star in K
    'temp': [3100, 3200, 3200, 3300, 3300, 3400, 3500, 3600, 3800,
             4000, 4200, 4400, 4600, 4900, 5200, 5400, 5500, 5700,
             5800, 5900, 6000, 6100, 6300, 6400, 6500, 6600, 6700,
             6900, 7000, 7300, 7500, 7800, 8000, 8200],

    # Minimum luminosity of the star in solar units
    'Lmin': [0.0012, 0.0036, 0.0079, 0.015, 0.024, 0.037, 0.054, 0.07,
             0.09, 0.11, 0.13, 0.15, 0.19, 0.23, 0.28, 0.36, 0.45,
             0.56, 0.68, 0.87, 1.1, 1.4, 1.7, 2.1, 2.5, 3.1, 3.7, 4.3,
             5.1, 6.7, 8.6, 11, 13, 16],

    # Maximum luminosity of the star in solar units
    'Lmax': [0, 0, 0, 0, 0, 0, 0, 0.08, 0.11, 0.15, 0.20, 0.25, 0.35,
             0.48, 0.65, 0.84, 1.0, 1.3, 1.6, 1.9, 2.2, 2.6, 3.0, 3.5,
             3.9, 4.5, 5.1, 5.7, 6.5, 8.2, 10, 13, 16, 20],

    # Span of the main sequence in billions of years
    'Mspan': [0, 0, 0, 0, 0, 0, 0, 70, 59, 50, 42, 37, 30, 24, 20, 17,
              14, 12, 10, 8.8, 7.7, 6.7, 5.9, 5.2, 4.6, 4.1, 3.7, 3.3,
              3.0, 2.5, 2.1, 1.8, 1.5, 1.3],

    # Span of the subgiant sequence in billions of years
    'Sspan': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.8,
              1.6, 1.4, 1.2, 1.0, 0.9, 0.8, 0.7, 0.6, 0.6, 0.5, 0.5,
              0.4, 0.3, 0.3, 0.2, 0.2],

    # Span of the giant sequence in billions of years
    'Gspan': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.1,
              1.0, 0.8, 0.7, 0.6, 0.6, 0.5, 0.4, 0.4, 0.4, 0.3, 0.3,
              0.2, 0.2, 0.2, 0.1, 0.1]
}

# The purpose of IndexTable is to facilitate lookups in StEvoTable.
# The contents of IndexTable are the indices of the respective entries in
# StEvoTable.
# It works as follows. After two 3d rolls the index is found as
#  IndexTable[firstroll][secondroll]
# very much like the star mass generation system. (Since most of the Star
# properties are closely linked to its mass, as evidenced by the stellar evo-
# lution table).
IndexTable = [
    None, None, None, # Indices 0, 1, and 2 are never used
    # Index 3
    [None, None, None, 33, 33, 33, 33, 33, 33, 33, 33, 32, 32, 32, 32, 32,
     32, 32, 32],
    # Index 4
    [None, None, None, 31, 31, 31, 31, 31, 31, 30, 30, 30, 29, 29, 29, 29,
     29, 29, 29],
    # Index 5
    [None, None, None, 28, 28, 28, 28, 28, 27, 27, 27, 26, 26, 25, 25, 25,
     25, 25, 25],
    # Index 6
    [None, None, None, 24, 24, 24, 24, 24, 23, 23, 22, 21, 21, 20, 20, 20,
     20, 20, 20],
    # Index 7
    [None, None, None, 19, 19, 19, 19, 19, 18, 18, 17, 16, 16, 15, 15, 15,
     15, 15, 15],
    # Index 8
    [None, None, None, 14, 14, 14, 14, 14, 13, 13, 12, 11, 11, 10, 10, 10,
     10, 10, 10],
    # Index 9
    [None, None, None,  9,  9,  9,  9,  9,  9,  8,  8,  8,  7,  7,  7,  7,
      7,  7,  7],
    # Index 10
    [None, None, None,  6,  6,  6,  6,  6,  6,  5,  5,  5,  4,  4,  4,  4,
      4,  4,  4],
    # Index 11
    [3] * 19,
    # Index 12
    [2] * 19,
    # Index 13
    [1] * 19,
    # Indices 14-18
    [0] * 19, [0] * 19, [0] * 19, [0] * 19, [0] * 19
]

# SequenceTable is used to look up the name of the sequence on which the star is
SequenceTable = {
    0: 'Main',
    1: 'Subgiant',
    2: 'Giant',
    3: 'White Dwarf'
}