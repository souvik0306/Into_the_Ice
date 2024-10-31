import numpy as np
import open3d as o3d
from noise import pnoise2

# Constants for cave generation
LENGTH_OF_CAVE = 100.0  # Total length of the cave in meters
RADIUS = 10.0            # Average radius of the cave
SCALE = 4.0             # Scale for Perlin noise
FREQ = 1.0              # Frequency for Perlin noise
NUM_POINTS = 1000       # Number of points for robot trajectory

def create_cave_mesh():
    """Create and deform a cylindrical mesh to represent the cave."""
    # Create a cylindrical mesh representing the open-ended cave tunnel
    mesh = o3d.geometry.TriangleMesh.create_cylinder(
        radius=RADIUS,
        height=LENGTH_OF_CAVE,
        resolution=100,
        split=4
    )
    mesh.translate((0, 0, -LENGTH_OF_CAVE / 2))  # Center the cylinder at z=0

    # Apply Perlin noise to the vertices to deform the cylinder walls
    vertices = np.asarray(mesh.vertices)
    for i in range(len(vertices)):
        x, y, z = vertices[i]
        theta = np.arctan2(y, x)
        n = pnoise2(theta * FREQ, z * FREQ, octaves=4)
        displacement = n * SCALE
        r = np.sqrt(x**2 + y**2) + displacement
        vertices[i][0] = r * np.cos(theta)
        vertices[i][1] = r * np.sin(theta)

    # Update the mesh vertices with deformed coordinates and recalculate normals
    mesh.vertices = o3d.utility.Vector3dVector(vertices)
    mesh.compute_vertex_normals()
    return mesh

def assign_colors(mesh):
    """Assign colors to the mesh vertices based on their z-coordinate."""
    vertices = np.asarray(mesh.vertices)
    colors = np.zeros_like(vertices)
    z_min = vertices[:, 2].min()
    z_max = vertices[:, 2].max()
    z_norm = (vertices[:, 2] - z_min) / (z_max - z_min)
    # Assign colors based on normalized z values, using a gradient from blue to green
    colors[:, 0] = z_norm  # Red channel
    colors[:, 1] = z_norm  # Green channel
    colors[:, 2] = 1 - z_norm  # Blue channel
    mesh.vertex_colors = o3d.utility.Vector3dVector(colors)
    return mesh

def create_robot_path():
    """Simulate the robot's path inside the cave."""
    theta_values = np.linspace(0, 2 * np.pi * 5, NUM_POINTS)  # 5 turns in the cave
    z_values = np.linspace(0, -LENGTH_OF_CAVE, NUM_POINTS)  # Depth range matches the cave

    # Define robot's path as a slightly smaller, mostly circular trajectory with minor noise
    path = np.zeros((NUM_POINTS, 3))
    for i in range(NUM_POINTS):
        radius_offset = 0.8 * RADIUS + 0.1 * np.random.randn()
        theta = theta_values[i]
        path[i, 0] = radius_offset * np.cos(theta)
        path[i, 1] = radius_offset * np.sin(theta)
        path[i, 2] = z_values[i]  # Position the robot along the cave's depth
    return path

def main():
    # Create and deform the cave mesh
    cave_mesh = create_cave_mesh()
    
    cave_mesh = assign_colors(cave_mesh)

    # Convert the mesh to a point cloud for a more natural cave appearance
    pcd_cave = cave_mesh.sample_points_poisson_disk(number_of_points=30000)

    # Simulate the robot's path inside the cave
    robot_path = create_robot_path()

    # Convert the robot's path to an Open3D point cloud for visualization
    robot_pcd = o3d.geometry.PointCloud()
    robot_pcd.points = o3d.utility.Vector3dVector(robot_path)
    robot_pcd.paint_uniform_color([1, 0, 1])  # Set the robot's color to cyan for contrast

    # Visualize the open-ended cave and robot position
    o3d.visualization.draw_geometries([pcd_cave, robot_pcd])

if __name__ == "__main__":
    main()
