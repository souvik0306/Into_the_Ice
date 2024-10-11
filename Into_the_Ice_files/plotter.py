import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def setup_plots():
    """Set up the plot layout and axes."""
    fig = plt.figure(figsize=(16, 8))
    ax1 = fig.add_subplot(131, projection='3d')
    ax2 = fig.add_subplot(132)
    ax3 = fig.add_subplot(133)

    fig2, ax4 = plt.subplots()

    return fig, ax1, ax2, ax3, fig2, ax4

def initialize_plot_elements(ax1, ax2, ax3, ax4):
    """Initialize plot elements for animation."""
    line_damped_3d, = ax1.plot([], [], [], label="Damped (PID) Trajectory", lw=2, color='blue')
    line_undamped_3d, = ax1.plot([], [], [], label="Undamped Trajectory", lw=2, color='red')
    line_damped_2d, = ax2.plot([], [], label="Damped (PID) Trajectory", lw=2, color='blue')
    line_undamped_2d, = ax2.plot([], [], label="Undamped Trajectory", lw=2, color='red')
    line_left_thickness, = ax3.plot([], [], lw=2, color='orange', label="Left Cave Boundary")
    line_right_thickness, = ax3.plot([], [], lw=2, color='orange', label="Right Cave Boundary")
    robot_marker, = ax3.plot([], [], 'ro', label="Robot Position")
    line_error, = ax4.plot([], [], lw=2, color='green', label="Error Percentage")
    line_proximity, = ax4.plot([], [], lw=2, color='blue', label="Proximity to Walls")

    return (line_damped_3d, line_undamped_3d, line_damped_2d, line_undamped_2d, 
            line_left_thickness, line_right_thickness, robot_marker, line_error, line_proximity)

def set_plot_properties(ax1, ax2, ax3, ax4, z_values):
    """Set plot limits, labels, and titles."""
    ax1.set_xlim([-2, 2])
    ax1.set_ylim([-2, 2])
    ax1.set_zlim([z_values.min(), z_values.max()])
    ax1.set_title('3D Trajectories: Damped (Blue) vs Undamped (Red)')
    ax1.set_xlabel('X Position (m)')
    ax1.set_ylabel('Y Position (m)')
    ax1.set_zlabel('Z Position (Depth in meters)')
    ax1.legend()

    ax2.set_xlim([-2, 2])
    ax2.set_ylim([-2, 2])
    ax2.set_title('2D Trajectories: Damped (Blue) vs Undamped (Red)')
    ax2.set_xlabel('X Position (m)')
    ax2.set_ylabel('Y Position (m)')
    ax2.legend()

    ax3.set_xlim([-2, 2])
    ax3.set_ylim([z_values.min(), z_values.max()])
    ax3.set_title('Thickness of the Moulin and Robot Position')
    ax3.set_xlabel('Thickness (m)')
    ax3.set_ylabel('Depth (m)')
    ax3.legend()

    ax4.set_xlim([0, len(z_values)])
    ax4.set_ylim([0, 100])  # Assume max error percentage is 100%
    ax4.set_title('Error Percentage and Proximity to Walls Over Time')
    ax4.set_xlabel('Time Step')
    ax4.set_ylabel('Error (%) / Proximity (m)')
    ax4.legend()

def create_animation(fig, update_func, frames):
    """Create and return the animation object."""
    return FuncAnimation(fig, update_func, frames=frames, interval=50, blit=True)

def show_plots():
    """Display the plots."""
    plt.tight_layout()
    plt.show()