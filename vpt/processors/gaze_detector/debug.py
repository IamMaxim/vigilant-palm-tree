'''A visualization for the gaze detector used for debugging.'''
import matplotlib.pyplot as plt
import numpy as np


def draw_rotation_values(data: np.ndarray):
    '''Draw the entire cached rotation data as a plot.
       Call this from the PnP solve to get real-time data.'''
    # Clear the figure
    plt.clf()

    # Draw rotation vector values
    plt.plot(np.linspace(0, 1, len(data)), data[:, 0])
    plt.plot(np.linspace(0, 1, len(data)), data[:, 1])
    plt.plot(np.linspace(0, 1, len(data)), data[:, 2])
    plt.legend(['x', 'y', 'z'])

    # Show the updated vector values
    plt.ion()
    plt.show()
    plt.pause(0.001)
