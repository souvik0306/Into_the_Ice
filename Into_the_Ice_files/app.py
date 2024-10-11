import numpy as np
from constants import NUM_POINTS, THETA_MAX
from proximity import generate_cave_thickness, generate_elliptical_trajectory
from control import simulate_robot_movement
from plotter import (setup_plots, initialize_plot_elements, set_plot_properties, 
                           create_animation, show_plots)

def main():
    # Generate cave geometry
    z_values, left_thickness, right_thickness = generate_cave_thickness()
    theta_values = np.linspace(0, THETA_MAX, NUM_POINTS)
    ellipse_x, ellipse_y = generate_elliptical_trajectory(theta_values)

    # Simulate robot movement
    x_damped, y_damped, x_undamped, y_undamped, error_percentage, robot_position_x, proximity_to_walls = (
        simulate_robot_movement(left_thickness, right_thickness, ellipse_x, ellipse_y)
    )

    # Set up visualization
    fig, ax1, ax2, ax3, fig2, ax4 = setup_plots()
    plot_elements = initialize_plot_elements(ax1, ax2, ax3, ax4)
    set_plot_properties(ax1, ax2, ax3, ax4, z_values)

    # Animation update function
    def update(frame):
        plot_elements[0].set_data(x_damped[:frame], y_damped[:frame])
        plot_elements[0].set_3d_properties(z_values[:frame])
        plot_elements[1].set_data(x_undamped[:frame], y_undamped[:frame])
        plot_elements[1].set_3d_properties(z_values[:frame])
        plot_elements[2].set_data(x_damped[:frame], y_damped[:frame])
        plot_elements[3].set_data(x_undamped[:frame], y_undamped[:frame])
        plot_elements[4].set_data(left_thickness[:frame], z_values[:frame])
        plot_elements[5].set_data(right_thickness[:frame], z_values[:frame])
        plot_elements[6].set_data(robot_position_x[:frame], z_values[:frame])
        plot_elements[7].set_data(range(frame), error_percentage[:frame])
        plot_elements[8].set_data(range(frame), proximity_to_walls[:frame])
        return plot_elements

    # Create and show animation
    ani = create_animation(fig, update, frames=len(x_damped))
    show_plots()

if __name__ == "__main__":
    main()