import numpy as np
from constants import NUM_POINTS, THETA_MAX, NOISE_AMPLITUDE, KP, KI, KD, COLLISION_MARGIN

def apply_PID_control(t, x, y, vx, vy, integral_x, integral_y, desired_x, desired_y):
    """Apply PID control to adjust velocity."""
    error_x = desired_x - x
    error_y = desired_y - y
    
    integral_x += error_x
    integral_y += error_y
    
    d_error_x = -vx
    d_error_y = -vy
    
    control_x = KP * error_x + KI * integral_x + KD * d_error_x
    control_y = KP * error_y + KI * integral_y + KD * d_error_y
    
    vx_new = vx + control_x
    vy_new = vy + control_y
    
    return vx_new, vy_new, integral_x, integral_y

def simulate_robot_movement(left_thickness, right_thickness, ellipse_x, ellipse_y):
    """Simulate the robot's movement with damped and undamped trajectories."""
    x_damped = np.zeros(NUM_POINTS)
    y_damped = np.zeros(NUM_POINTS)
    vx_damped = vy_damped = 0

    x_undamped = np.zeros(NUM_POINTS)
    y_undamped = np.zeros(NUM_POINTS)
    vx_undamped = vy_undamped = 0

    error_percentage = []
    robot_position_x = []
    proximity_to_walls = []

    for i in range(1, NUM_POINTS):
        noise_x = NOISE_AMPLITUDE * np.random.randn()
        noise_y = NOISE_AMPLITUDE * np.random.randn()
        
        # Undamped trajectory
        x_undamped[i] = np.clip(x_undamped[i-1] + vx_undamped + noise_x, left_thickness[i] + COLLISION_MARGIN, right_thickness[i] - COLLISION_MARGIN)
        y_undamped[i] = np.clip(y_undamped[i-1] + vy_undamped + noise_y, left_thickness[i] + COLLISION_MARGIN, right_thickness[i] - COLLISION_MARGIN)
        vx_undamped += noise_x
        vy_undamped += noise_y

        # Damped trajectory with PID control
        x_damped[i] = np.clip(x_damped[i-1] + vx_damped + noise_x, left_thickness[i] + COLLISION_MARGIN, right_thickness[i] - COLLISION_MARGIN)
        y_damped[i] = np.clip(y_damped[i-1] + vy_damped + noise_y, left_thickness[i] + COLLISION_MARGIN, right_thickness[i] - COLLISION_MARGIN)
        vx_damped, vy_damped, integral_x, integral_y = apply_PID_control(
            i, x_damped[i], y_damped[i], vx_damped, vy_damped, 0, 0, ellipse_x[i], ellipse_y[i]
        )

        # Calculate proximity to walls
        proximity_left = x_damped[i] - left_thickness[i]
        proximity_right = right_thickness[i] - x_damped[i]
        proximity_to_walls.append(min(proximity_left, proximity_right))

        # Track robot position and calculate error
        robot_position_x.append((x_damped[i] + x_undamped[i]) / 2)
        error = np.sqrt((x_damped[i] - x_undamped[i])**2 + (y_damped[i] - y_undamped[i])**2)
        error_percentage.append(error / (np.sqrt(x_undamped[i]**2 + y_undamped[i]**2) + 1e-6) * 100)

    return x_damped, y_damped, x_undamped, y_undamped, error_percentage, robot_position_x, proximity_to_walls