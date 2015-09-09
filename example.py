"""This is an example script for automated star system generation"""

import gurpsspace.starsystem as starsys

# Change from None to a value if you want to set an argument
args = {
    'open_cluster': None,  # True or False
    'num_stars': None,  # 1, 2 or 3
    'age': None  # Number > 0
}

# Generate starsystems until one is made that contains a Garden world.
garden = False
cycle_num = 0
while garden is not True:
    cycle_num += 1
    mysys = starsys.StarSystem(**args)
    garden = mysys.has_garden()

mysys.printinfo()
print('Total number of cycles: {}'.format(cycle_num))
mysys.write_latex()
