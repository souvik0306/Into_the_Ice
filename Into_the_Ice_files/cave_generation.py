import numpy as np
from constants import NUM_POINTS, LENGTH_OF_CAVE, RANDOM_SEED

def generate_cave_thickness():
    """Generate random cave thickness (left and right boundaries) over time."""
    np.random.seed(RANDOM_SEED)
    z_values = np.linspace(0, -LENGTH_OF_CAVE, NUM_POINTS)  # Depth (z-axis)
    left_thickness = -1.0 * (0.5 + np.random.randn(NUM_POINTS) * 0.2)  # Random left boundary
    right_thickness = 1.0 * (0.5 + np.random.randn(NUM_POINTS) * 0.2)  # Random right boundary
    return z_values, left_thickness, right_thickness

def generate_circular_lobed_trajectory(theta_values):
    """Generate circular trajectory with lobes."""
    from constants import NOISE_AMPLITUDE
    r = 1 + 0.3 * np.sin(3 * theta_values)  # Base circle with 3 lobes
    x = r * np.cos(theta_values) + NOISE_AMPLITUDE * np.random.randn(len(theta_values))
    y = r * np.sin(theta_values) + NOISE_AMPLITUDE * np.random.randn(len(theta_values))
    return x, y