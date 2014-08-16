from Tkinter import *
import Tkinter
import ttk
import gurpsspace.dice as GD
import tkMessageBox
import gurpsspace.starsystem as starsys


class StarSystemOverview(Tkinter.Frame):
	

	def __init__(self, parent, mysys = None):

		width = parent.winfo_screenwidth() / 4 
		height = parent.winfo_screenheight() / 4
		offset_x = (parent.winfo_screenwidth() / 2) - (width / 2)
		offset_y = (parent.winfo_screenheight() / 2) - (height / 4)
		# Geometry is a string of the format 'WxH+offset_x+offset_y' where the offsets are calculated on Linux from the top right corner
		parent.geometry(str(width) + 'x' + str(height) + '-' + str(offset_x) + '+' + str(offset_y))

		mainframe = ttk.Frame(parent)

		ttk.Label(parent, text="Star System Overview", anchor=CENTER).pack(side="top", fill="x", expand=False)

		if mysys == None:
			args = {
			    'opencluster': None, # True or False
			    'numstars': None, # 1, 2 or 3
			    'age': None # Number > 0
			}
			mysys = starsys.StarSystem(**args)

		labels = ttk.Frame(parent)
		labels.pack(side=LEFT)
		ttk.Label(labels, text="Age:", anchor=W).pack(side=TOP)
		ttk.Label(labels, text="# of Stars:", anchor=W).pack(side=TOP)
		ttk.Label(labels, text="Open Cluster:", anchor=W).pack(side=TOP)
		if mysys._StarSystem__numstars > 1:
			for i in range(len(mysys._StarSystem__orbits)):
				ttk.Label(labels, text="Companion Star " + str(i+1), anchor=W).pack(side=TOP)
				ttk.Label(labels, text="Stellar Orbit:", anchor=W).pack(side=TOP)
				ttk.Label(labels, text="Eccentricity:", anchor=W).pack(side=TOP)
				ttk.Label(labels, text="Minimum Stellar Orbit:", anchor=W).pack(side=TOP)
				ttk.Label(labels, text="Maximum Stellar Orbit:", anchor=W).pack(side=TOP)
				ttk.Label(labels, text="Orbital Period:", anchor=W).pack(side=TOP)

		values = ttk.Frame(parent)
		values.pack(side=RIGHT)
		ttk.Label(values, text=mysys._StarSystem__age).pack(side=TOP)
		ttk.Label(values, text=mysys._StarSystem__numstars).pack(side=TOP)
		ttk.Label(values, text=mysys._StarSystem__opencluster).pack(side=TOP)
		if mysys._StarSystem__numstars > 1:
			for i in range(len(mysys._StarSystem__orbits)):
				ttk.Label(values, text="--------------------").pack(side=TOP)
				ttk.Label(values, text=str(mysys._StarSystem__orbits[i][0]) + " AU", anchor=E).pack(side=TOP)
				ttk.Label(values, text=mysys._StarSystem__orbits[i][1], anchor=E).pack(side=TOP)
				ttk.Label(values, text=str(mysys._StarSystem__minmaxorbits[i][0]) + " AU", anchor=E).pack(side=TOP)
				ttk.Label(values, text=str(mysys._StarSystem__minmaxorbits[i][1]) + " AU", anchor=E).pack(side=TOP)
				ttk.Label(values, text=str(round(mysys._StarSystem__periods[i], 1)) + "d", anchor=E).pack(side=TOP)

		mainframe.pack()
