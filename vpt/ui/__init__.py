import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib
matplotlib.use('TkAgg')


class mclass:
    N = 50

    def __init__(self, window):
        fig, self.axs = plt.subplots(
            2, sharex=True, sharey=True, figsize=(5, 5))
        self.canvas = FigureCanvasTkAgg(fig, master=window)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()

        tk.Button(window, text="add point", command=self.add_point).pack()

        self.points = np.random.randint(0, 2, (self.N, 2))
        self.add_point()

    def draw(self, i, title):
        axs = self.axs[i]
        axs.cla()
        axs.set_title(title, fontsize=10)
        axs.axis('off')
        axs.bar(list(range(self.N)), self.points[-self.N:, i], 1)

    def add_point(self):
        self.points = np.append(self.points, [np.random.randint(0, 2, 2)], 0)
        self.draw(0, "Mouse & Keyboard input")
        self.draw(1, "Engagement estimation")
        self.canvas.draw()


window = tk.Tk()
start = mclass(window)
window.mainloop()
