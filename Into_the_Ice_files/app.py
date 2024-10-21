from constants import *
from visualization import run_simulation
from cave_generation import setup_plots, update_main_plot, update_error_plot
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def main():
    data = run_simulation()
    figures, axes, lines_main, lines_error = setup_plots()
    fig = figures['fig']
    fig2 = figures['fig2']
    ax4 = axes['ax4']

    # Now that we have the error_percentage data, we can set y-limits for ax4
    max_error = max(data['error_percentage']) * 1.1
    ax4.set_ylim([0, max_error])

    # Create animations for the simulation
    ani_main = FuncAnimation(fig, update_main_plot, frames=num_points, fargs=(data, lines_main), interval=50, blit=True)
    ani_error = FuncAnimation(fig2, update_error_plot, frames=num_points, fargs=(data, lines_error), interval=50, blit=True)

    plt.show()

if __name__ == "__main__":
    main()
