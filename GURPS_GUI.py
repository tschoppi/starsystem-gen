from Tkinter import *
import ttk
import GURPS_Dice as GD

roller = GD.DiceRoller()

def rollAndUpdate(dicenum, modifier):
	# IntVars cannot directly be used as ints, for some reason. .get() returns their value, which is an int, getting around this problem.
	dicenum = dicenum.get()
	modifier = modifier.get()
	diceResult.set(roller.roll(dicenum, modifier))

root = Tk()
root.title("GURPS Starsystem Generator")
# For now, 1/16th of the screen, centered so that the center of the window is the center of the screen. 
# Perhaps make it bigger later 
width = root.winfo_screenwidth() / 4 
height = root.winfo_screenheight() / 4
offset_x = (root.winfo_screenwidth() / 2) - (width / 2)
offset_y = (root.winfo_screenheight() / 2) - (height / 2)
# Geometry is a string of the format 'WxH+offset_x+offset_y' where the offsets are calculated on Linux from the top right corner
root.geometry(str(width) + 'x' + str(height) + '-' + str(offset_x) + '+' + str(offset_y))

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(4, weight=1)
mainframe.rowconfigure(4, weight=1)

diceResult = StringVar()
ttk.Label(mainframe, text="Roll some dice:").grid(column=1, row=1, sticky=(W,E))

dicenum = IntVar()
modifier = IntVar()
ttk.Entry(root, textvariable=dicenum).grid(column=2, row=1, sticky=(W,E))
ttk.Entry(root, textvariable=modifier).grid(column=3, row=1, sticky=(W,E))
ttk.Button(root, text="Roll!", command= lambda: rollAndUpdate(dicenum, modifier)).grid(column=2, row=2, sticky=(W,E))
ttk.Label(mainframe,  textvariable=diceResult).grid(column=2, row=3, sticky=(W,E))

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.mainloop()