import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 输入数据
camera_position = np.array([-0.25801495, -0.01710191, -8.019467])
focus_point = np.array([-0.45803636, -0.88606215, -10.883886])
left_boundary = np.array([-0.44522738, 0.86229664, -10.881566])
right_boundary = np.array([-0.40290633, -2.339271, -9.913282])

# 创建3D图形
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制四个关键点
ax.scatter(camera_position[0], camera_position[1], camera_position[2], color='g', label="Camera Position", s=50)
ax.scatter(focus_point[0], focus_point[1], focus_point[2], color='b', label="Front Boundary", s=50)
ax.scatter(left_boundary[0], left_boundary[1], left_boundary[2], color='r', label="Left Boundary", s=50)
ax.scatter(right_boundary[0], right_boundary[1], right_boundary[2], color='y', label="Right Boundary", s=50)

# 绘制连接相机和左右边界
ax.plot([camera_position[0], left_boundary[0]],
        [camera_position[1], left_boundary[1]],
        [camera_position[2], left_boundary[2]], 'r-', label="Camera to Left Boundary")

ax.plot([camera_position[0], right_boundary[0]],
        [camera_position[1], right_boundary[1]],
        [camera_position[2], right_boundary[2]], 'b-', label="Camera to Right Boundary")

# 绘制左边界到光心和光心到右边界的连接线
ax.plot([left_boundary[0], focus_point[0]],
        [left_boundary[1], focus_point[1]],
        [left_boundary[2], focus_point[2]], 'g-', label="Left Boundary to Front Boundary")

ax.plot([focus_point[0], right_boundary[0]],
        [focus_point[1], right_boundary[1]],
        [focus_point[2], right_boundary[2]], 'm-', label="Front Boundary to Right Boundary")

# 设置图形属性
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D View Frustum Projection')

# 添加图例
ax.legend()

# 显示图形
plt.show()
