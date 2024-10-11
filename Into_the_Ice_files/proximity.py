import numpy as np
from constants import NUM_POINTS, LENGTH_OF_CAVE, RANDOM_SEED

def generate_cave_thickness():
    """Generate random cave thickness (left and right boundaries) over time."""
    np.random.seed(RANDOM_SEED)
    z_values = np.linspace(0, -LENGTH_OF_CAVE, NUM_POINTS)  # Depth (z-axis)
    left_thickness = -1.0 * (0.5 + np.random.randn(NUM_POINTS) * 0.2)  # Random left boundary
    right_thickness = 1.0 * (0.5 + np.random.randn(NUM_POINTS) * 0.2)  # Random right boundary
    return z_values, left_thickness, right_thickness

def generate_elliptical_trajectory(theta_values):
    """Generate elliptical trajectory with noise."""
    from constants import A, B, NOISE_AMPLITUDE
    ellipse_x = A * np.cos(theta_values) + NOISE_AMPLITUDE * np.random.randn(len(theta_values))
    ellipse_y = B * np.sin(theta_values) + NOISE_AMPLITUDE * np.random.randn(len(theta_values))
    return ellipse_x, ellipse_y