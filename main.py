from tkinter import *
from tkinter import ttk
import tkinter
import gurpsspace.dice as GD
import gurpsspace
from gui.generator_main import StarSystemOverview
import gurpsspace.starsystem as starsys

class MainWindow(tkinter.Frame):
	roller = GD.DiceRoller()

	def __init__(self, parent):		
		width = parent.winfo_screenwidth() / 4 
		height = parent.winfo_screenheight() / 4
		offset_x = (parent.winfo_screenwidth() / 2) - (width / 2)
		offset_y = (parent.winfo_screenheight() / 2) - (height / 2)
		# Geometry is a string of the format 'WxH+offset_x+offset_y' where the offsets are calculated on Linux from the top right corner
		#parent.geometry('-' + str(offset_x) + '+' + str(offset_y))	

		mainframe = ttk.Frame(root, padding="3 3 12 12")

		ttk.Button(mainframe, text="Generate a completely random star system", command= lambda: self.openGenerator(parent)).pack(fill="x", expand=True, pady=5)
		ttk.Button(mainframe, text="Generate a star system", command= lambda: tkMessageBox.showinfo("Placeholder", "A series of dialogs will guide you through the generation of your star system")).pack(fill="x", expand=True, pady=5)
		ttk.Button(mainframe, text="Open a dice roller", command= lambda: self.openDiceWindow(parent)).pack(fill="x", expand=True, pady=5)
		mainframe.pack()

	def openDiceWindow(self, parent):
		window = Toplevel()
		DiceWindow(window)

	def openGenerator(self, parent):
		window = Toplevel()
		StarSystemOverview(window)



class DiceWindow(tkinter.Frame): 

	roller = GD.DiceRoller()
	

	def rollAndUpdate(self, dicenum, modifier, diceResult):
		# IntVars cannot directly be used as ints, for some reason. .get() returns their value, which is an int, getting around this problem.
		diceResult.set(self.roller.roll(dicenum, modifier))

	def __init__(self, parent):

		
		# For now, 1/16th of the screen, centered so that the center of the window is the center of the screen. 
		# Perhaps make it bigger later 
		width = parent.winfo_screenwidth() / 4 
		height = parent.winfo_screenheight() / 4
		offset_x = (parent.winfo_screenwidth() / 2) - (width / 4)
		offset_y = (parent.winfo_screenheight() / 2) - (height / 4)
		# Geometry is a string of the format 'WxH+offset_x+offset_y' where the offsets are calculated on Linux from the top right corner
		#parent.geometry(str(width) + 'x' + str(height) + '-' + str(offset_x) + '+' + str(offset_y))

		mainframe = ttk.Frame(parent, padding="3 3 12 12")
		mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
		mainframe.columnconfigure(3, weight=1)
		mainframe.rowconfigure(3, weight=1)

		diceResult = StringVar()
		dicenum    = IntVar()
		modifier   = IntVar()
		ttk.Label(mainframe, text="Roll some dice:").grid(column=1, row=1, sticky=(W,E))

		ttk.Entry(mainframe, textvariable=dicenum).grid(column=2, row=1, sticky=(W,E))
		ttk.Entry(mainframe, textvariable=modifier).grid(column=3, row=1, sticky=(W,E))
		ttk.Button(mainframe, text="Roll!", command= lambda: self.rollAndUpdate(dicenum.get(), modifier.get(), diceResult)).grid(column=2, row=2, sticky=(W,E))
		ttk.Label(mainframe,  text="Result of your roll:").grid(column=1, row=3, sticky=(W,E))
		ttk.Label(mainframe,  textvariable=diceResult).grid(column=2, row=3, sticky=(W,E))

		for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root = Tk()
root.title("GURPS Starsystem Generator")
startWindow = MainWindow(root)
root.mainloop()
