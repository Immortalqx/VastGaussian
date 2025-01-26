import os
import cv2
import numpy as np
import open3d as o3d

# 相机内参
fx = 715.1706353164301
fy = 715.1706353164301
cx = 482.28605682869267
cy = 362.1031007223982
# fx = 5.850000000000000000e+02
# fy = 5.850000000000000000e+02
# cx = 3.200000000000000000e+02
# cy = 2.400000000000000000e+02

# 定义路径
# path = "/media/immortalqx/Dataset/KiriSceneDepth/couplet"
# image_path = os.path.join(path, "images", "181905.645631.png")
# depth_path = os.path.join(path, "depth", "181905.645631.tiff")
path = "/media/immortalqx/Dataset/KiriSceneDepth/corridor"
image_path = os.path.join(path, "images", "178972.469109.png")
depth_path = os.path.join(path, "depth", "178972.469109.tiff")
# path = "/home/immortalqx/Projects/tsdf-fusion-python/data"
# image_path = os.path.join(path, "frame-000000.color.jpg")
# depth_path = os.path.join(path, "frame-000000.depth.png")

# 读取彩色图像和深度图
image = cv2.imread(image_path)
depth = cv2.imread(depth_path, cv2.IMREAD_UNCHANGED)
depth = np.power(depth, 2.2)
# depth = cv2.imread(depth_path, cv2.IMREAD_UNCHANGED).astype(float)
# depth = depth/1000.

# 检查数据是否成功加载
if image is None:
    raise FileNotFoundError(f"彩色图像未找到：{image_path}")
if depth is None:
    raise FileNotFoundError(f"深度图未找到：{depth_path}")

# 检查深度图格式
# if depth.dtype != np.float32:
#     raise ValueError("深度图格式应为32位浮点数 (cv2.IMREAD_UNCHANGED 读取)")

rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
cv2.imshow("Rotated Image", rotated_image)
cv2.waitKey(0)

# 确保图像尺寸与深度图一致
if image.shape[:2] != depth.shape:
    original_height, original_width = image.shape[:2]  # 原始图像尺寸
    new_height, new_width = depth.shape[:2]  # 调整后的尺寸
    # 调整图像尺寸
    image = cv2.resize(image, (new_width, new_height))
    # 按比例调整相机内参
    fx = fx * (new_width / original_width)
    fy = fy * (new_height / original_height)
    cx = cx * (new_width / original_width)
    cy = cy * (new_height / original_height)

# 对depth做resize，就不用调整相机内参了！
# if image.shape[:2] != depth.shape:
#     depth = cv2.resize(depth, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)

# 将BGR转换为RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 获取图像尺寸
height, width = depth.shape

# 将深度图像转换为点云
points = []
colors = []

# 点到相机光心的深度
for v in range(height):
    for u in range(width):
        z = depth[v, u]  # 深度值
        if 0.0 < z < 100.0 and np.isfinite(z):  # 过滤无效深度值（可根据场景调整范围）
            x = (u - cx) * z / fx
            y = (v - cy) * z / fy
            points.append((x, y, z))
            colors.append(image[v, u] / 255.0)  # 颜色归一化到[0,1]

# 创建 Open3D 点云
points = np.array(points)
colors = np.array(colors)
point_cloud = o3d.geometry.PointCloud()
point_cloud.points = o3d.utility.Vector3dVector(points)
point_cloud.colors = o3d.utility.Vector3dVector(colors)

# 可视化点云
o3d.visualization.draw_geometries([point_cloud], window_name="Point Cloud")
