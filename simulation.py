import numpy as np
from constants import *
from pid_controller import apply_PID_control

def run_simulation():
    # Initialize arrays to store positions, velocities, control values
    x_damped = np.zeros(num_points)
    y_damped = np.zeros(num_points)
    vx_damped = 0  # Initial velocity for damped trajectory
    vy_damped = 0
    integral_x = 0
    integral_y = 0

    x_undamped = np.zeros(num_points)
    y_undamped = np.zeros(num_points)
    vx_undamped = 0  # Initial velocity for undamped trajectory
    vy_undamped = 0

    error_percentage = []  # To store error percentage over time
    left_thickness = np.zeros(num_points)  # Random left boundary of the cave
    right_thickness = np.zeros(num_points)  # Random right boundary of the cave

    # Robot's position marker for the thickness plot
    robot_position_x = []  # X position of the robot in the thickness plot

    # Generate random cave thickness (left and right boundaries) over time
    left_thickness = -1.5 * (0.5 + np.random.rand(num_points) * 0.5)  # Random left boundary
    right_thickness = 1.5 * (0.5 + np.random.rand(num_points) * 0.5)  # Random right boundary

    # Simulate the robot's spiral movement with the variable thickness and PID control
    theta_values = np.linspace(0, theta_max, num_points)

    for i in range(1, num_points):
        theta = theta_values[i]
        # Determine the valid radius at the current depth based on the cave boundaries
        max_radius = min(abs(left_thickness[i]), abs(right_thickness[i]))
        desired_radius = max_radius * 0.8  # Stay within 80% of the maximum possible radius

        # Introduce random noise into both trajectories
        noise_x = noise_amplitude * np.random.randn()
        noise_y = noise_amplitude * np.random.randn()
        
        # Undamped trajectory (no control system), moves randomly within cave boundaries
        x_undamped[i] = np.clip(x_undamped[i-1] + vx_undamped + noise_x, left_thickness[i], right_thickness[i])
        y_undamped[i] = np.clip(y_undamped[i-1] + vy_undamped + noise_y, left_thickness[i], right_thickness[i])
        vx_undamped += noise_x
        vy_undamped += noise_y

        # Damped trajectory with PID control
        vx_damped, vy_damped, integral_x, integral_y = apply_PID_control(
            theta, x_damped[i-1], y_damped[i-1], vx_damped, vy_damped, integral_x, integral_y, desired_radius, Kp, Ki, Kd
        )
        x_damped[i] = np.clip(x_damped[i-1] + vx_damped, left_thickness[i], right_thickness[i])
        y_damped[i] = np.clip(y_damped[i-1] + vy_damped, left_thickness[i], right_thickness[i])

        # Track the robot's x position in the thickness plot
        robot_position_x.append(x_damped[i])

        # Calculate error as a percentage difference between damped and desired position
        desired_x = desired_radius * np.cos(theta)
        desired_y = desired_radius * np.sin(theta)
        error = np.sqrt((x_damped[i] - desired_x)**2 + (y_damped[i] - desired_y)**2)
        error_percentage.append(error / (desired_radius + 1e-6) * 100)  # Avoid division by zero

    return {
        'x_damped': x_damped,
        'y_damped': y_damped,
        'x_undamped': x_undamped,
        'y_undamped': y_undamped,
        'z_values': z_values,
        'left_thickness': left_thickness,
        'right_thickness': right_thickness,
        'robot_position_x': robot_position_x,
        'error_percentage': error_percentage,
        'theta_values': theta_values
    }
