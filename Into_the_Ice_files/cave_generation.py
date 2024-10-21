import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from constants import *
import numpy as np

def setup_plots():
    # Plotting setup
    fig = plt.figure(figsize=(16, 8))
    
    # Create subplots for 3D trajectory, 2D trajectory, thickness graph
    ax1 = fig.add_subplot(131, projection='3d')
    ax2 = fig.add_subplot(132)
    ax3 = fig.add_subplot(133)
    
    # Set up 3D plot of the spiral
    line_damped_3d, = ax1.plot([], [], [], label="Damped (PID) Trajectory", lw=2, color='blue')
    line_undamped_3d, = ax1.plot([], [], [], label="Undamped Trajectory", lw=2, color='red')
    
    # Set up 2D plot of the trajectory
    line_damped_2d, = ax2.plot([], [], label="Damped (PID) Trajectory", lw=2, color='blue')
    line_undamped_2d, = ax2.plot([], [], label="Undamped Trajectory", lw=2, color='red')
    
    # Plotting the thickness of the moulin over time and adding the red dot for the robot's position
    line_left_thickness, = ax3.plot([], [], lw=2, color='orange', label="Left Cave Boundary")
    line_right_thickness, = ax3.plot([], [], lw=2, color='orange', label="Right Cave Boundary")
    robot_marker, = ax3.plot([], [], 'ro', label="Robot Position")
    
    # Plotting the error percentage over time
    fig2, ax4 = plt.subplots()
    line_error, = ax4.plot([], [], lw=2, color='green', label="Error Percentage")
    
    # Initialize plot limits and labels
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
    
    ax4.set_xlim([0, num_points])
    ax4.set_ylim([0, None])  # Will set y-limits after data is known
    ax4.set_title('Error Percentage Over Time')
    ax4.set_xlabel('Time Step')
    ax4.set_ylabel('Error (%)')
    ax4.legend()
    
    plt.tight_layout()
    
    lines_main = {
        'line_damped_3d': line_damped_3d,
        'line_undamped_3d': line_undamped_3d,
        'line_damped_2d': line_damped_2d,
        'line_undamped_2d': line_undamped_2d,
        'line_left_thickness': line_left_thickness,
        'line_right_thickness': line_right_thickness,
        'robot_marker': robot_marker
    }
    
    lines_error = {
        'line_error': line_error
    }
    
    figures = {
        'fig': fig,
        'fig2': fig2
    }
    
    axes = {
        'ax4': ax4
    }
    
    return figures, axes, lines_main, lines_error

def update_main_plot(frame, data, lines):
    x_damped = data['x_damped']
    y_damped = data['y_damped']
    x_undamped = data['x_undamped']
    y_undamped = data['y_undamped']
    z_values = data['z_values']
    left_thickness = data['left_thickness']
    right_thickness = data['right_thickness']
    robot_position_x = data['robot_position_x']

    line_damped_3d = lines['line_damped_3d']
    line_undamped_3d = lines['line_undamped_3d']
    line_damped_2d = lines['line_damped_2d']
    line_undamped_2d = lines['line_undamped_2d']
    line_left_thickness = lines['line_left_thickness']
    line_right_thickness = lines['line_right_thickness']
    robot_marker = lines['robot_marker']

    # Update the 3D and 2D plots for damped and undamped trajectories
    line_damped_3d.set_data(x_damped[:frame], y_damped[:frame])
    line_damped_3d.set_3d_properties(z_values[:frame])
    
    line_undamped_3d.set_data(x_undamped[:frame], y_undamped[:frame])
    line_undamped_3d.set_3d_properties(z_values[:frame])
    
    line_damped_2d.set_data(x_damped[:frame], y_damped[:frame])
    line_undamped_2d.set_data(x_undamped[:frame], y_undamped[:frame])

    # Update the thickness plot and robot's position marker
    line_left_thickness.set_data(left_thickness[:frame], z_values[:frame])
    line_right_thickness.set_data(right_thickness[:frame], z_values[:frame])
    robot_marker.set_data(robot_position_x[:frame], z_values[:frame])

    return line_damped_3d, line_undamped_3d, line_damped_2d, line_undamped_2d, line_left_thickness, line_right_thickness, robot_marker

def update_error_plot(frame, data, lines):
    error_percentage = data['error_percentage']
    line_error = lines['line_error']

    # Update the error plot
    line_error.set_data(range(frame), error_percentage[:frame])

    return line_error,
