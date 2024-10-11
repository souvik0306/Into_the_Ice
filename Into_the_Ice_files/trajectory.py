import numpy as np
from constants import num_points, noise_amplitude, left_thickness, right_thickness, collision_margin, a, b

def generate_elliptical_trajectory(theta_values):
    """Generates elliptical trajectory with added noise."""
    ellipse_x = a * np.cos(theta_values) + noise_amplitude * np.random.randn(num_points)
    ellipse_y = b * np.sin(theta_values) + noise_amplitude * np.random.randn(num_points)
    return ellipse_x, ellipse_y

def update_trajectory(x_prev, y_prev, vx, vy, noise_x, noise_y, left_bound, right_bound):
    """Updates the robot's position in the cave while avoiding collisions."""
    x_new = np.clip(x_prev + vx + noise_x, left_bound + collision_margin, right_bound - collision_margin)
    y_new = np.clip(y_prev + vy + noise_y, left_bound + collision_margin, right_bound - collision_margin)
    return x_new, y_new

def add_noise():
    """Generates random noise for x and y axes."""
    noise_x = noise_amplitude * np.random.randn()
    noise_y = noise_amplitude * np.random.randn()
    return noise_x, noise_y
