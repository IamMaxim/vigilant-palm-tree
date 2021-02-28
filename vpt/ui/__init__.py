import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib
matplotlib.use('TkAgg')


class mclass:
    N = 100

    def __init__(self, window):
        fig = Figure(figsize=(10, 1))

        fig, axs = plt.subplots(2, sharex=True, sharey=True,)
        axs[0].set_title("Mouse & Keyboard")
        axs[0].axis('off')
        axs[1].set_title("Engagement estimation")
        axs[1].axis('off')

        self.axs = axs
        self.canvas = FigureCanvasTkAgg(fig, master=window)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()

        tk.Button(window, text="add point", command=self.add_point).pack()

        self.points = np.random.randint(0, 2, (self.N, 2))
        self.add_point()

    def draw(self, i):
        self.axs[i].cla()
        self.axs[i].plot(self.points[-self.N:, i])

    def add_point(self):
        self.points = np.append(self.points, [np.random.randint(0, 2, 2)], 0)
        self.draw(0)
        self.draw(1)
        self.canvas.draw()


window = tk.Tk()
start = mclass(window)
window.mainloop()
