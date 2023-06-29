import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # Create Figure
        self.fig = Figure(figsize=(10, 6))

        self.x = np.linspace(0, 2*np.pi, 400)
        self.y1 = np.sin(self.x**2)
        self.y2 = np.cos(self.x**2)
        self.y3 = np.tan(self.x)
        self.y4 = np.sinh(self.x)

        # Create subplots
        self.ax1 = self.fig.add_subplot(111)
        self.ax2 = self.ax1.twinx()
        self.ax3 = self.ax1.twinx()
        self.ax4 = self.ax1.twinx()

        # Adjust subplot for multiple y-axes
        self.fig.subplots_adjust(right=0.6)

        # Move y-axes to avoid overlap
        self.ax2.spines['right'].set_position(('axes', 1.1))
        self.ax3.spines['right'].set_position(('axes', 1.3))
        self.ax4.spines['right'].set_position(('axes', 1.5))

        # Enable visibility of y-axes frames
        self.ax2.set_frame_on(True)
        self.ax3.set_frame_on(True)
        self.ax4.set_frame_on(True)

        # Set the color of each axes
        self.ax2.spines['right'].set_color('green')
        self.ax3.spines['right'].set_color('blue')
        self.ax4.spines['right'].set_color('magenta')

        # Plotting data
        self.ax1.plot(self.x, self.y1, 'r')
        self.ax2.plot(self.x, self.y2, 'g')
        self.ax3.plot(self.x, self.y3, 'b')
        self.ax4.plot(self.x, self.y4, 'm')

        # Set labels
        self.ax1.set_ylabel('y1', color='r')
        self.ax2.set_ylabel('y2', color='g')
        self.ax3.set_ylabel('y3', color='b')
        self.ax4.set_ylabel('y4', color='m')

        # Create canvas and place in application
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
