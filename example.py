"""This is an example script for automated star system generation"""

import gurpsspace.starsystem as starsys

# Change from None to a value if you want to set an argument
args = {
    'opencluster': None, # True or False
    'numstars': None, # 1, 2 or 3
    'age': None # Number > 0
}

# Generate starsystems until one is made that contains a Garden world.
garden = False
cyclenum = 0
while garden is not True:
    cyclenum += 1
    mysys = starsys.StarSystem(**args)
    garden = mysys.hasgarden()

mysys.printinfo()
print('Total number of cycles: {}'.format(cyclenum))
mysys.writelatex()
