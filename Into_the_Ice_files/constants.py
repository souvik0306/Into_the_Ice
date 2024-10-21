import numpy as np

# Parameters
length_of_cave = 1000  # Total length of the cave in meters
num_points = 100  # Number of points to simulate
theta_max = 20 * np.pi  # Max angle for spiraling (multiple rotations)
z_values = np.linspace(0, -length_of_cave, num_points)  # Depth (z-axis)

# Noise parameters
noise_amplitude = 0.05  # Magnitude of random noise

# PID controller parameters
Kp = 0.8  # Proportional gain
Ki = 0.05  # Integral gain
Kd = 0.4  # Derivative gain

# Set the random seed for reproducibility
np.random.seed(42)
