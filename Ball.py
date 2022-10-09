import tkinter as tk
from random import randint as rand

WIDTH = 300
HEIGHT = 200

def canvas_click_handler(event):
    print('canvas_click_handler( x=', event.x, 'y=', event.y, ')')

def tick():
    global x, y, dx, dy
    x += dx
    y += dy
    if x + radius > WIDTH or x - radius <= 0:
        dx = -dx
    if y + radius > HEIGHT or y - radius <= 0:
        dy = -dy
    canvas.move(ball_id, dx, dy)
    root.after(10, tick)

def main():
    global root, canvas
    global ball_id, radius, x, y, z, dx, dy
    root = tk.Tk()
    root.geometry(str(WIDTH) + 'x' + str(HEIGHT))
    canvas = tk.Canvas(root)
    canvas.pack()
    canvas.bind('<Button-1>', canvas_click_handler)

    radius = rand(20, 50)
    x = rand(radius, WIDTH - radius)
    y = rand(radius, HEIGHT - radius)
    dx, dy = (+1, +1)
    ball_id = canvas.create_oval(x - radius, y - radius,
                                x + radius, y + radius,
                                fill='green')

    tick()
    root.mainloop()

if __name__ == "__main__":
    main()