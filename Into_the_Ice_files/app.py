from constants import *
from simulation import run_simulation
from plotting import setup_plots, update_main_plot, update_error_plot
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def main():
    data = run_simulation()
    figures, axes, lines_main, lines_error = setup_plots()
    fig = figures['fig']
    ax3 = axes['ax3']

    # Now that we have the error_percentage data, we can set y-limits for ax3
    max_error = max(data['error_percentage']) * 1.1
    ax3.set_ylim([0, max_error])

    # Create animations for the simulation
    ani_main = FuncAnimation(fig, update_main_plot, frames=num_points, fargs=(data, lines_main), interval=50, blit=True)
    ani_error = FuncAnimation(fig, update_error_plot, frames=num_points, fargs=(data, lines_error), interval=50, blit=True)

    plt.show()

if __name__ == "__main__":
    main()
