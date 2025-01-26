import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 输入数据：定义相机坐标系下的视锥体顶点
front_left_bottom_point = np.array([1.3967892, 0.34633094, -4.696389])
front_left_top_point = np.array([-1.2780788, 0.32894534, -5.03922])
front_right_bottom_point = np.array([1.3097558, -2.8871453, -3.8533525])
front_right_top_point = np.array([-1.3651122, -2.9045308, -4.196183])
camera_position = np.array([-0.62847555, 0.03159476, 0.51437616])  # 相机位置

# 将这些点组合成视锥体的顶点集合
cone_vertices = np.array([
    front_left_bottom_point,
    front_left_top_point,
    front_right_bottom_point,
    front_right_top_point,
    camera_position
])

# 输入数据：旋转矩阵
rotation_matrix = np.array([
    [-0.02603686, -0.99186575, 0.1245968],
    [-0.9673242, -0.00644676, -0.2534608],
    [0.25220233, -0.12712482, -0.9592879]
])

# 将点旋转到世界坐标系
def rotate_points(points, rotation_matrix):
    return np.dot(points, rotation_matrix.T)

# 旋转视锥体顶点（从相机坐标系转换到世界坐标系）
# rotated_cone_vertices = rotate_points(cone_vertices, rotation_matrix)
rotated_cone_vertices = cone_vertices

# 创建3D图形
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制视锥体的顶点（旋转后的点）
for i in range(len(rotated_cone_vertices)):
    ax.scatter(rotated_cone_vertices[i][0], rotated_cone_vertices[i][1], rotated_cone_vertices[i][2], s=50, label=f"Point {i+1}")

# 绘制视锥体的边界（连接各个顶点）
# Camera to front left bottom, front left top, front right bottom, front right top
ax.plot([rotated_cone_vertices[4][0], rotated_cone_vertices[0][0]],
        [rotated_cone_vertices[4][1], rotated_cone_vertices[0][1]],
        [rotated_cone_vertices[4][2], rotated_cone_vertices[0][2]], 'g-', label="Camera to Front Left Bottom")

ax.plot([rotated_cone_vertices[4][0], rotated_cone_vertices[1][0]],
        [rotated_cone_vertices[4][1], rotated_cone_vertices[1][1]],
        [rotated_cone_vertices[4][2], rotated_cone_vertices[1][2]], 'r-', label="Camera to Front Left Top")

ax.plot([rotated_cone_vertices[4][0], rotated_cone_vertices[2][0]],
        [rotated_cone_vertices[4][1], rotated_cone_vertices[2][1]],
        [rotated_cone_vertices[4][2], rotated_cone_vertices[2][2]], 'b-', label="Camera to Front Right Bottom")

ax.plot([rotated_cone_vertices[4][0], rotated_cone_vertices[3][0]],
        [rotated_cone_vertices[4][1], rotated_cone_vertices[3][1]],
        [rotated_cone_vertices[4][2], rotated_cone_vertices[3][2]], 'y-', label="Camera to Front Right Top")

# 绘制前左、前右边界点之间的连接线（形成视锥体边界）
ax.plot([rotated_cone_vertices[0][0], rotated_cone_vertices[1][0]],
        [rotated_cone_vertices[0][1], rotated_cone_vertices[1][1]],
        [rotated_cone_vertices[0][2], rotated_cone_vertices[1][2]], 'g--', label="Front Left Points")

ax.plot([rotated_cone_vertices[2][0], rotated_cone_vertices[3][0]],
        [rotated_cone_vertices[2][1], rotated_cone_vertices[3][1]],
        [rotated_cone_vertices[2][2], rotated_cone_vertices[3][2]], 'b--', label="Front Right Points")

# 设置坐标轴等间距
# 获取数据的最小值和最大值
x_min, y_min, z_min = np.min(rotated_cone_vertices, axis=0)
x_max, y_max, z_max = np.max(rotated_cone_vertices, axis=0)

# 计算轴的范围
max_range = np.max([x_max - x_min, y_max - y_min, z_max - z_min])

# 设置坐标轴范围，使其等间距
ax.set_xlim([x_min - 0.1 * max_range, x_max + 0.1 * max_range])
ax.set_ylim([y_min - 0.1 * max_range, y_max + 0.1 * max_range])
ax.set_zlim([z_min - 0.1 * max_range, z_max + 0.1 * max_range])

# 设置图形的等比例显示
ax.set_box_aspect([1, 1, 1])

# 设置图形属性
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Camera View Frustum')

# 添加图例
ax.legend()

# 显示图形
plt.show()
