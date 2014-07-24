from Tkinter import *
import ttk
import GURPS_Dice as GD

class diceWindow: 

	roller = GD.DiceRoller()
	

	def rollAndUpdate(self, dicenum, modifier, diceResult):
		# IntVars cannot directly be used as ints, for some reason. .get() returns their value, which is an int, getting around this problem.
		diceResult.set(self.roller.roll(dicenum, modifier))

	def __init__(self, parent):

		parent.title("GURPS Starsystem Generator")
		# For now, 1/16th of the screen, centered so that the center of the window is the center of the screen. 
		# Perhaps make it bigger later 
		width = parent.winfo_screenwidth() / 4 
		height = parent.winfo_screenheight() / 4
		offset_x = (parent.winfo_screenwidth() / 2) - (width / 2)
		offset_y = (parent.winfo_screenheight() / 2) - (height / 2)
		# Geometry is a string of the format 'WxH+offset_x+offset_y' where the offsets are calculated on Linux from the top right corner
		parent.geometry(str(width) + 'x' + str(height) + '-' + str(offset_x) + '+' + str(offset_y))

		mainframe = ttk.Frame(root, padding="3 3 12 12")
		mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
		mainframe.columnconfigure(4, weight=1)
		mainframe.rowconfigure(4, weight=1)

		diceResult = StringVar()
		dicenum    = IntVar()
		modifier   = IntVar()
		ttk.Label(mainframe, text="Roll some dice:").grid(column=1, row=1, sticky=(W,E))

		ttk.Entry(mainframe, textvariable=dicenum).grid(column=2, row=1, sticky=(W,E))
		ttk.Entry(mainframe, textvariable=modifier).grid(column=3, row=1, sticky=(W,E))
		ttk.Button(mainframe, text="Roll!", command= lambda: self.rollAndUpdate(dicenum.get(), modifier.get(), diceResult)).grid(column=2, row=2, sticky=(W,E))
		ttk.Label(mainframe,  textvariable=diceResult).grid(column=2, row=3, sticky=(W,E))

		for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root = Tk()
guiDiceWindow = diceWindow(root)
root.mainloop()