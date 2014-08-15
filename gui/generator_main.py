from Tkinter import *
import Tkinter
import ttk
import gurpsspace.dice as GD
import tkMessageBox
import gurpsspace.starsystem as starsys


class StarSystemOverview(Tkinter.Frame):
	# Change from None to a value if you want to set an argument
	def __init__(self, parent):

		width = parent.winfo_screenwidth() / 4 
		height = parent.winfo_screenheight() / 4
		offset_x = (parent.winfo_screenwidth() / 2) - (width / 2)
		offset_y = (parent.winfo_screenheight() / 2) - (height / 4)
		# Geometry is a string of the format 'WxH+offset_x+offset_y' where the offsets are calculated on Linux from the top right corner
		parent.geometry(str(width) + 'x' + str(height) + '-' + str(offset_x) + '+' + str(offset_y))

		mainframe = ttk.Frame(parent)
		#mainframe.pack(side="top", fill="both", expand=True)
		#mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
		#mainframe.columnconfigure(3, weight=1)
		#mainframe.rowconfigure(3, weight=1)

		args = {
		    'opencluster': None, # True or False
		    'numstars': None, # 1, 2 or 3
		    'age': None # Number > 0
		}
		mysys = starsys.StarSystem(**args)

		ttk.Label(parent, text="Star System Overview", anchor=CENTER).pack(side="top", fill="x", expand=False)

		labels = ttk.Frame(parent)
		labels.pack(side=LEFT)
		ttk.Label(labels, text="Age:", anchor=W).pack(side=TOP)
		ttk.Label(labels, text="# of Stars:", anchor=W).pack(side=TOP)
		ttk.Label(labels, text="Open Cluster:", anchor=W).pack(side=TOP)
		if mysys._StarSystem__numstars > 1:
			ttk.Label(labels, text="Stellar Orbits:", anchor=W).pack(side=TOP)
			ttk.Label(labels, text="Stellar Orbits Min/Max:", anchor=W).pack(side=TOP)
			ttk.Label(labels, text="Orbital Periods:", anchor=W).pack(side=TOP)

		values = ttk.Frame(parent)
		values.pack(side=RIGHT)
		ttk.Label(values, text=mysys._StarSystem__age).pack(side=TOP)
		ttk.Label(values, text=mysys._StarSystem__numstars).pack(side=TOP)
		ttk.Label(values, text=mysys._StarSystem__opencluster).pack(side=TOP)
		if mysys._StarSystem__numstars > 1:
			ttk.Label(values, text=mysys._StarSystem__orbits, anchor=E).pack(side=TOP)
			ttk.Label(values, text=mysys._StarSystem__minmaxorbits, anchor=E).pack(side=TOP)
			ttk.Label(values, text=mysys._StarSystem__periods, anchor=E).pack(side=TOP)

		mainframe.pack()
