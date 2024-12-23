import numpy as np
import matplotlib.pyplot as plt


def projectile_path(x, x0, y0, vo, theta_deg, g=9.81):
    theta_rad = np.radians(theta_deg)
    y=
    y = -g * (x - x0) ** 2 / (2 * vo ** 2 * np.cos(theta_rad) ** 2) + (x - x0) * np.tan(theta_rad) + y0
    return y


def horizontal_range(vo, theta_deg, g=9.81):
    theta_rad = np.radians(theta_deg)
    R = (vo ** 2 * np.sin(2 * theta_rad)) / g
    return R


# Set up parameters
x0 = 0  # Initial x-coordinate
y0 = 50  # Initial y-coordinate
vo = 20  # Initial velocity
theta = 50  # Launch angle in degrees
g = 9.81  # Acceleration due to gravity

# Generate x values
x_values = np.linspace(0, 40, 1000)

# Calculate corresponding y values using the projectile_path function
y_values = projectile_path(x_values, x0, y0, vo, theta, g)

# Calculate horizontal range
R = horizontal_range(vo, theta, g)

# Plot the projectile path with grid
plt.plot(x_values, y_values, label='Projectile Path')
plt.axvline(x=R, color='r', linestyle=':', label='Horizontal Range')
plt.title('Projectile Motion with Horizontal Range')
plt.xlabel('X-coordinate')
plt.ylabel('Y-coordinate')
plt.legend()
plt.grid(True)
plt.show()

print(f"Horizontal Range (R): {R:.2f} meters")