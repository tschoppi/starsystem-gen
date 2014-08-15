"""This is an example script for automated star system generation"""

import gurpsspace.starsystem as starsys

# Change from None to a value if you want to set an argument
args = {
    'opencluster': None, # True or False
    'numstars': 1, # 1, 2 or 3
    'age': None # Number > 0
}

mysys = starsys.StarSystem(**args)
