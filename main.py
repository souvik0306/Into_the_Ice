import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters
length_of_cave = 100  # Total length of the cave in meters
num_points = 1000  # Number of points to simulate
theta_max = 20 * np.pi  # Max angle for spiraling (multiple rotations)
z_values = np.linspace(0, -length_of_cave, num_points)  # Depth (z-axis)

# Noise parameters
noise_amplitude = 0.05  # Magnitude of random noise

# PID controller parameters
Kp = 0.8  # Proportional gain
Ki = 0.05  # Integral gain
Kd = 0.4  # Derivative gain

# Initialize arrays to store positions, velocities, control values
x_damped = np.zeros(num_points)
y_damped = np.zeros(num_points)
vx_damped = 0  # Initial velocity for damped trajectory
vy_damped = 0

x_undamped = np.zeros(num_points)
y_undamped = np.zeros(num_points)
vx_undamped = 0  # Initial velocity for undamped trajectory
vy_undamped = 0

error_percentage = []  # To store error percentage over time
left_thickness = np.zeros(num_points)  # Random left boundary of the cave
right_thickness = np.zeros(num_points)  # Random right boundary of the cave

# Robot's position marker for the thickness plot
robot_position_x = []  # X position of the robot in the thickness plot

# Function to apply the PID controller
def apply_PID_control(t, theta, x, y, vx, vy, integral_x, integral_y, desired_radius):
    desired_x = desired_radius * np.cos(theta)
    desired_y = desired_radius * np.sin(theta)
    
    # Errors
    error_x = desired_x - x
    error_y = desired_y - y
    
    # Integral of errors
    integral_x += error_x
    integral_y += error_y
    
    # Derivative of errors (rate of change of error)
    d_error_x = -vx
    d_error_y = -vy
    
    # PID control to adjust velocity
    control_x = Kp * error_x + Ki * integral_x + Kd * d_error_x
    control_y = Kp * error_y + Ki * integral_y + Kd * d_error_y
    
    # Update velocities
    vx_new = vx + control_x
    vy_new = vy + control_y
    
    return vx_new, vy_new, integral_x, integral_y

# Generate random cave thickness (left and right boundaries) over time
np.random.seed(42)  # Fix the seed for reproducibility
left_thickness = -1.0 * (0.5 + np.random.randn(num_points) * 0.2)  # Random left boundary
right_thickness = 1.0 * (0.5 + np.random.randn(num_points) * 0.2)  # Random right boundary

# Simulate the robot's spiral movement with the variable thickness and PID control
theta_values = np.linspace(0, theta_max, num_points)
for i in range(1, num_points):
    # Determine the valid radius at the current depth based on the cave boundaries
    random_radius = min(abs(left_thickness[i]), abs(right_thickness[i]))

    # Introduce random noise into both trajectories
    noise_x = noise_amplitude * np.random.randn()
    noise_y = noise_amplitude * np.random.randn()
    
    # Undamped trajectory (no control system)
    x_undamped[i] = np.clip(x_undamped[i-1] + vx_undamped + noise_x, left_thickness[i], right_thickness[i])
    y_undamped[i] = np.clip(y_undamped[i-1] + vy_undamped + noise_y, left_thickness[i], right_thickness[i])
    vx_undamped += noise_x
    vy_undamped += noise_y

    # Damped trajectory with PID control
    x_damped[i] = np.clip(x_damped[i-1] + vx_damped + noise_x, left_thickness[i], right_thickness[i])
    y_damped[i] = np.clip(y_damped[i-1] + vy_damped + noise_y, left_thickness[i], right_thickness[i])
    vx_damped, vy_damped, integral_x, integral_y = apply_PID_control(
        i, theta_values[i], x_damped[i], y_damped[i], vx_damped, vy_damped, 0, 0, random_radius
    )

    # Track the robot's x position in the thickness plot
    robot_position_x.append((x_damped[i] + x_undamped[i]) / 2)  # Use an average for position marker

    # Calculate error as a percentage difference between damped and undamped
    error = np.sqrt((x_damped[i] - x_undamped[i])**2 + (y_damped[i] - y_undamped[i])**2)
    error_percentage.append(error / (np.sqrt(x_undamped[i]**2 + y_undamped[i]**2) + 1e-6) * 100)  # Avoid division by zero

# Plotting setup
fig = plt.figure(figsize=(16, 8))

# Create subplots for 3D trajectory, 2D trajectory, thickness graph, and error plot
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
ax4.set_ylim([0, max(error_percentage) * 1.1])
ax4.set_title('Error Percentage Over Time')
ax4.set_xlabel('Time Step')
ax4.set_ylabel('Error (%)')
ax4.legend()

# Animation function to update the plot with new data
def update(frame):
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

    # Update the error plot
    line_error.set_data(range(frame), error_percentage[:frame])

    return line_damped_3d, line_undamped_3d, line_damped_2d, line_undamped_2d, line_left_thickness, line_right_thickness, robot_marker, line_error

# Create an animation for the simulation
ani = FuncAnimation(fig, update, frames=len(x_damped), interval=50, blit=True)

plt.tight_layout()
plt.show()
