import numpy as np
import open3d as o3d
from noise import pnoise2
from constants import length_of_cave

# Set constants for cave generation
radius = 5.0  # Average radius for the tunnel
scale = 4.0  # Scale for Perlin noise
freq = 1.0  # Frequency for Perlin noise
num_points = 1000  # Number of points for robot trajectory

# Create a cylindrical mesh representing the open-ended cave tunnel
cave_mesh = o3d.geometry.TriangleMesh.create_cylinder(radius=radius, height=length_of_cave, resolution=100, split=4)
cave_mesh.translate((0, 0, -length_of_cave / 2))  # Center the cylinder

# Apply Perlin noise to the vertices to deform the cylinder walls
vertices = np.asarray(cave_mesh.vertices)
for i in range(len(vertices)):
    x, y, z = vertices[i]
    theta = np.arctan2(y, x)
    n = pnoise2(theta * freq, z * freq, octaves=4)
    displacement = n * scale
    r = np.sqrt(x**2 + y**2) + displacement
    vertices[i][0] = r * np.cos(theta)
    vertices[i][1] = r * np.sin(theta)

# Update the mesh vertices with deformed coordinates and recalculate normals
cave_mesh.vertices = o3d.utility.Vector3dVector(vertices)
cave_mesh.compute_vertex_normals()

# Invert normals for better visualization (optional depending on visualization direction)
cave_mesh.vertex_normals = o3d.utility.Vector3dVector(-np.asarray(cave_mesh.vertex_normals))

# Assign colors based on the z-coordinate for a depth-based color gradient
vertices = np.asarray(cave_mesh.vertices)
colors = np.zeros_like(vertices)
z_min = vertices[:, 2].min()
z_max = vertices[:, 2].max()
z_norm = (vertices[:, 2] - z_min) / (z_max - z_min)

# Set colors (for example, a gradient from red to green based on depth)
colors[:, 0] = z_norm                # Red
colors[:, 1] = 1.0 - z_norm          # Green
colors[:, 2] = np.abs(np.sin(z_norm * np.pi))  # Blue
cave_mesh.vertex_colors = o3d.utility.Vector3dVector(colors)

# Convert the mesh to a point cloud for a more natural cave appearance
pcd_cave = cave_mesh.sample_points_poisson_disk(number_of_points=30000)

# Simulate the robot's path inside the cave
theta_values = np.linspace(0, 2 * np.pi * 5, num_points)  # 5 turns in the cave
z_values = np.linspace(-length_of_cave / 2, length_of_cave / 2, num_points)  # Match depth to cave length

# Define robot's path as a slightly smaller, mostly circular trajectory with minor noise
robot_path = np.zeros((num_points, 3))
for i in range(num_points):
    # Generate a circular path with minor random deviation for a natural effect
    radius_offset = 0.8 * radius + 0.1 * np.random.randn()
    theta = theta_values[i]
    robot_path[i, 0] = radius_offset * np.cos(theta)
    robot_path[i, 1] = radius_offset * np.sin(theta)
    robot_path[i, 2] = z_values[i]  # Position the robot along the cave's depth

# Convert the robot's path to an Open3D point cloud for visualization
robot_pcd = o3d.geometry.PointCloud()
robot_pcd.points = o3d.utility.Vector3dVector(robot_path)
robot_pcd.paint_uniform_color([1, 0, 0])  # Set the robot's color to red for contrast

# Visualize the open-ended cave and robot position
o3d.visualization.draw_geometries([pcd_cave, robot_pcd])
