import numpy as np
import open3d as o3d
from noise import pnoise2
from constants import length_of_cave

# Set constants
radius = 5.0  # Cave radius
scale = 4.0
freq = 1.0
num_points = 1000

# Create a cylindrical mesh to represent the cave tunnel
cave_mesh = o3d.geometry.TriangleMesh.create_cylinder(radius=radius, height=length_of_cave, resolution=100, split=4)
cave_mesh.translate((0, 0, -length_of_cave / 2))  # Center the cylinder

# Apply Perlin noise to deform the cylinder walls
vertices = np.asarray(cave_mesh.vertices)
for i in range(len(vertices)):
    x, y, z = vertices[i]
    theta = np.arctan2(y, x)
    n = pnoise2(theta * freq, z * freq, octaves=4)
    displacement = n * scale
    r = np.sqrt(x**2 + y**2) + displacement
    vertices[i][0] = r * np.cos(theta)
    vertices[i][1] = r * np.sin(theta)

# Update the mesh and calculate normals
cave_mesh.vertices = o3d.utility.Vector3dVector(vertices)
cave_mesh.compute_vertex_normals()

# Invert normals for better visualization
cave_mesh.vertex_normals = o3d.utility.Vector3dVector(-np.asarray(cave_mesh.vertex_normals))

# Assign colors based on height
vertices = np.asarray(cave_mesh.vertices)
colors = np.zeros_like(vertices)
z_min = vertices[:, 2].min()
z_max = vertices[:, 2].max()
z_norm = (vertices[:, 2] - z_min) / (z_max - z_min)

# Set colors
colors[:, 0] = z_norm                # Red
colors[:, 1] = 1.0 - z_norm          # Green
colors[:, 2] = np.abs(np.sin(z_norm * np.pi))  # Blue
cave_mesh.vertex_colors = o3d.utility.Vector3dVector(colors)

# Convert to a point cloud
pcd_cave = cave_mesh.sample_points_poisson_disk(number_of_points=30000)

# Poisson surface reconstruction for a smoother mesh
pcd_clean, ind = pcd_cave.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
voxel_size = 0.1
pcd_down = pcd_clean.voxel_down_sample(voxel_size=voxel_size)
pcd_down.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.5, max_nn=30))

# Simulate the robot's path inside the cave
theta_values = np.linspace(0, 2 * np.pi * 5, num_points)  # 5 turns
z_values = np.linspace(-length_of_cave / 2, length_of_cave / 2, num_points)  # Depth of the cave

# Define robot's path (centered circular path with minimal noise)
robot_path = np.zeros((num_points, 3))
for i in range(num_points):
    radius_offset = 0.8 * radius + 0.1 * np.random.randn()  # Slight random radius deviation
    theta = theta_values[i]
    robot_path[i, 0] = radius_offset * np.cos(theta)
    robot_path[i, 1] = radius_offset * np.sin(theta)
    robot_path[i, 2] = z_values[i]  # Depth

# Convert robot path to an Open3D point cloud for visualization
robot_pcd = o3d.geometry.PointCloud()
robot_pcd.points = o3d.utility.Vector3dVector(robot_path)
robot_pcd.paint_uniform_color([1, 0, 0])  # Set robot color to red

# Visualize cave and robot position
o3d.visualization.draw_geometries([pcd_down, robot_pcd])
