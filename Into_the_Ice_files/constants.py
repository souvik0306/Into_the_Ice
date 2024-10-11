import numpy as np

# Cave parameters
LENGTH_OF_CAVE = 100  # Total length of the cave in meters
NUM_POINTS = 1000  # Number of points to simulate
THETA_MAX = 20 * np.pi  # Max angle for spiraling (multiple rotations)

# Noise parameters
NOISE_AMPLITUDE = 0.02  # Magnitude of random noise

# Elliptical trajectory parameters
A = 1.5  # Semi-major axis of the ellipse
B = 1.0  # Semi-minor axis of the ellipse

# PID controller parameters
KP = 0.8  # Proportional gain
KI = 0.05  # Integral gain
KD = 0.4  # Derivative gain

# Collision avoidance margin
COLLISION_MARGIN = 0.1  # Distance from walls to avoid collision

# Random seed for reproducibility
RANDOM_SEED = 42