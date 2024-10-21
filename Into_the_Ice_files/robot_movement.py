import numpy as np

def apply_PID_control(t, theta, x, y, vx, vy, integral_x, integral_y, desired_radius, Kp, Ki, Kd):
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
