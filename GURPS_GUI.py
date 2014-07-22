from Tkinter import *
import ttk
import GURPS_Dice as GD

roller = GD.DiceRoller()

def rollAndUpdate(dicenum, modifier):
	diceResult.set(roller.roll(dicenum, modifier))

root = Tk()
root.title("GURPS Starsystem Generator")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

diceResult = StringVar()
label1 = ttk.Label(mainframe, text="Roll some dice:").grid(column=1, row=1, sticky=(W,E))
ttk.Button(root, text="Roll!", command= lambda: rollAndUpdate(1,0)).grid(column=2, row=1, sticky=(W,E))
label2 = ttk.Label(mainframe,  textvariable=diceResult).grid(column=3, row=1, sticky=(W,E))

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.mainloop()