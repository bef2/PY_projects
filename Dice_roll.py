import tkinter as tk
import random

def dice_roll():
    lbl["text"] = str(random.randint(1,6))

window = tk.Tk()
window.title("Игральная кость")
window.rowconfigure([0,1], minsize=80, weight=1)
window.columnconfigure(0, minsize=300, weight=1)

btn = tk.Button(text="Бросить", command=dice_roll, borderwidth=5)
btn.grid(row=0, column=0, sticky="nsew")

lbl = tk.Label(text="---")
lbl.grid(row=1, column=0)


window.mainloop()