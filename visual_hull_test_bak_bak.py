import numpy as np
import matplotlib.pyplot as plt

# 输入数据
camera_position = np.array([-0.88031566, 0.02475476, 0.46827745])
rotation_matrix = np.array([[-0.04155656, -0.9680216, 0.24740115],
                            [-0.96694523, -0.0233824, -0.25390983],
                            [0.25157502, -0.24977498, -0.9350521]])

# 给定的相机在世界坐标系中的前、左、右边界
front_point = np.array([-0.13811219, -0.73697484, -2.336879])
left_point = np.array([-0.19449759, 1.0081879, -2.2817247])
right_point = np.array([-0.33340102, -2.2238421, -1.4408312])

# 假定的相机坐标系中的前、左、右方向（假设前方沿着z轴，左方沿着x轴，右方沿着y轴）
front_in_camera = np.array([0, 0, -3])  # 前方向
left_in_camera = np.array([-3, 0, -3])  # 左方向
right_in_camera = np.array([3, 0, -3])  # 右方向


# 将相机坐标系中的点转换到世界坐标系
def rotate_point(point, rotation_matrix, camera_position):
    return camera_position + np.dot(rotation_matrix, point)


# 计算旋转后的前点、左点和右点
rotated_front = rotate_point(front_in_camera, rotation_matrix, camera_position)
rotated_left = rotate_point(left_in_camera, rotation_matrix, camera_position)
rotated_right = rotate_point(right_in_camera, rotation_matrix, camera_position)

# 创建3D图形
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制相机位置
ax.scatter(camera_position[0], camera_position[1], camera_position[2], color='g', label="Camera Position", s=50)

# 绘制旋转后的前点、左点和右点
ax.scatter(rotated_front[0], rotated_front[1], rotated_front[2], color='b', label="Rotated Front Point", s=50)
ax.scatter(rotated_left[0], rotated_left[1], rotated_left[2], color='r', label="Rotated Left Point", s=50)
ax.scatter(rotated_right[0], rotated_right[1], rotated_right[2], color='y', label="Rotated Right Point", s=50)

# 绘制前点、左点和右点（实际给定的世界坐标）
ax.scatter(front_point[0], front_point[1], front_point[2], color='purple', label="Front Point (world)", s=50)
ax.scatter(left_point[0], left_point[1], left_point[2], color='orange', label="Left Point (world)", s=50)
ax.scatter(right_point[0], right_point[1], right_point[2], color='brown', label="Right Point (world)", s=50)

# 绘制连接相机与前点、左右边界
ax.plot([camera_position[0], rotated_left[0]],
        [camera_position[1], rotated_left[1]],
        [camera_position[2], rotated_left[2]], 'r-', label="Camera to Left Point (rotated)")

ax.plot([camera_position[0], rotated_right[0]],
        [camera_position[1], rotated_right[1]],
        [camera_position[2], rotated_right[2]], 'b-', label="Camera to Right Point (rotated)")

ax.plot([camera_position[0], rotated_front[0]],
        [camera_position[1], rotated_front[1]],
        [camera_position[2], rotated_front[2]], 'g-', label="Camera to Front Point (rotated)")

# 绘制前点与左右边界的连接线
ax.plot([rotated_left[0], rotated_front[0]],
        [rotated_left[1], rotated_front[1]],
        [rotated_left[2], rotated_front[2]], 'g-', label="Left to Front Point (rotated)")

ax.plot([rotated_front[0], rotated_right[0]],
        [rotated_front[1], rotated_right[1]],
        [rotated_front[2], rotated_right[2]], 'm-', label="Front to Right Point (rotated)")

# 第二部分：绘制基于前点、左点和右点的视锥体
# 直接连接相机位置和前点、左点、右点
ax.plot([camera_position[0], front_point[0]],
        [camera_position[1], front_point[1]],
        [camera_position[2], front_point[2]], 'c--', label="Camera to Front Point (original)")

ax.plot([camera_position[0], left_point[0]],
        [camera_position[1], left_point[1]],
        [camera_position[2], left_point[2]], 'm--', label="Camera to Left Point (original)")

ax.plot([camera_position[0], right_point[0]],
        [camera_position[1], right_point[1]],
        [camera_position[2], right_point[2]], 'y--', label="Camera to Right Point (original)")

ax.plot([left_point[0], front_point[0]],
        [left_point[1], front_point[1]],
        [left_point[2], front_point[2]], 'r--', label="Left to Front Point (original)")

ax.plot([front_point[0], right_point[0]],
        [front_point[1], right_point[1]],
        [front_point[2], right_point[2]], 'b--', label="Front to Right Point (original)")

# 设置图形属性
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Camera View Frustum Projection')

# 添加图例
ax.legend()

# 显示图形
plt.show()
