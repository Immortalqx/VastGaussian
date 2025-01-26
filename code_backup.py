def refine_ori_bbox_visualHull(self, partition_dict):
    """将连续的相机坐标作为无缝分块的边界，并在每个相机视角下扩展 3 米范围"""
    bbox_with_id = {}
    buffer_distance = 3  # 设置缓冲距离为 3 米

    for partition_idx, cameras in partition_dict.items():
        camera_list = cameras["camera_list"]

        # 初始化分区的最小和最大坐标
        min_x, max_x = float("inf"), float("-inf")
        min_z, max_z = float("inf"), float("-inf")

        for camera in camera_list:
            camera_position = camera.pose
            camera_rotation = camera.rotation

            # 通过相机的光心发出一条长度为 3 米的射线，并将其投影在 xz 平面上来计算
            # 获取相机的Z轴方向
            forward_vector = camera_rotation[:, 2]
            forward_vector = forward_vector / np.linalg.norm(forward_vector)  # 单位化

            # 计算缓冲区域边界点
            front_point = camera_position + buffer_distance * forward_vector

            # 是否考虑camera_position，否则如果是一个环视，那bbox就变成环视中心的小区域了，还是没拍到的。
            # 更新 bbox 的范围
            min_x = min(min_x, camera_position[0], front_point[0])
            max_x = max(max_x, camera_position[0], front_point[0])
            min_z = min(min_z, camera_position[2], front_point[2])
            max_z = max(max_z, camera_position[2], front_point[2])

        ori_camera_bbox = [min_x, max_x, min_z, max_z]
        bbox_with_id[partition_idx] = ori_camera_bbox

    # # 2.按照z轴对相机的边界进行修正
    # for m in range(1, self.m_region + 1):
    #     for n in range(1, self.n_region + 1):
    #         if n + 1 == self.n_region + 1:
    #             break
    #         partition_idx_1 = str(m) + '_' + str(n + 1)  # 上边块
    #         min_x_1, max_x_1, min_z_1, max_z_1 = bbox_with_id[partition_idx_1]
    #         partition_idx_2 = str(m) + '_' + str(n)  # 下边块
    #         min_x_2, max_x_2, min_z_2, max_z_2 = bbox_with_id[partition_idx_2]
    #         mid_x, mid_y, mid_z = partition_dict[partition_idx_2]["z_mid_camera"].pose
    #         bbox_with_id[partition_idx_1] = [min_x_1, max_x_1, mid_z, max_z_1]
    #         bbox_with_id[partition_idx_2] = [min_x_2, max_x_2, min_z_2, mid_z]
    #
    # # 3.按照x轴对相机的边界进行修正
    # for n in range(1, self.n_region + 1):
    #     for m in range(1, self.m_region + 1):
    #         if m + 1 == self.m_region + 1:
    #             break
    #         partition_idx_1 = str(m) + '_' + str(n)  # 左边块
    #         min_x_1, max_x_1, min_z_1, max_z_1 = bbox_with_id[partition_idx_1]
    #         partition_idx_2 = str(m + 1) + '_' + str(n)  # 右边块
    #         min_x_2, max_x_2, min_z_2, max_z_2 = bbox_with_id[partition_idx_2]
    #         mid_x, mid_y, mid_z = partition_dict[partition_idx_1]["x_mid_camera"].pose
    #         bbox_with_id[partition_idx_1] = [min_x_1, mid_x, min_z_1, max_z_1]
    #         bbox_with_id[partition_idx_2] = [mid_x, max_x_2, min_z_2, max_z_2]

    # 返回新的分区和边界字典

    new_partition_dict = {
        f"{partition_id}": cameras["camera_list"] for partition_id, cameras in partition_dict.items()
    }

    return new_partition_dict, bbox_with_id
    # #############################################################################
    # =============================================================================
    # partition_dict = new_partition_dict
    # refined_ori_bbox = bbox_with_id
    #
    # # 计算每个部分的拓展后的边界坐标，以及该部分对应的点云
    # pcd = self.pcd
    # partition_list = []
    # point_num = 0
    # point_extend_num = 0
    # for partition_idx, camera_list in partition_dict.items():
    #     min_x, max_x, min_z, max_z = refined_ori_bbox[partition_idx]
    #     ori_camera_bbox = [min_x, max_x, min_z, max_z]
    #     ori_camera_centers = []
    #     for camera_pose in camera_list:
    #         ori_camera_centers.append(camera_pose.pose)
    #     # 保存ori相机位置
    #     storePly(os.path.join(self.partition_ori_dir, f'{partition_idx}_camera_centers.ply'),
    #              np.array(ori_camera_centers),
    #              np.zeros_like(np.array(ori_camera_centers)))
    #
    #     # 获取该部分对应的点云
    #     points, colors, normals = self.extract_point_cloud(pcd, ori_camera_bbox)  # 分别提取原始边界内的点云，和拓展边界后的点云
    #
    #
    #     # 论文中说点云围成的边界框的高度选取为最高点到地平面的距离，但在本实现中，因为不确定地平面位置，(可视化中第平面不用坐标轴xz重合)
    #     # 因此使用整个点云围成的框作为空域感知的边界框
    #     partition_list.append(CameraPartition(partition_id=partition_idx, cameras=new_camera_list,
    #                                           point_cloud=BasicPointCloud(points_extend, colors_extend,
    #                                                                       normals_extend),
    #                                           ori_camera_bbox=ori_camera_bbox,
    #                                           extend_camera_bbox=extend_camera_bbox,
    #                                           extend_rate=self.extend_rate,
    #                                           ori_point_bbox=self.get_point_range(points),
    #                                           extend_point_bbox=self.get_point_range(points_extend),
    #                                           ))
    #
    #     point_num += points.shape[0]
    #     point_extend_num += points_extend.shape[0]
    #     storePly(os.path.join(self.partition_ori_dir, f"{partition_idx}.ply"), points,
    #              colors * 255)  # 分别保存未拓展前 和 拓展后的点云
    #     storePly(os.path.join(self.partition_extend_dir, f"{partition_idx}_extend.ply"), points_extend,
    #              colors_extend * 255)
    #
    # # 未拓展边界前：根据位置选择后的数据量会比初始的点云数量小很多，因为相机围成的边界会比实际的边界小一些，因此使用这些边界筛点云，点的数量会减少
    # # 拓展边界后：因为会有许多重合的点，因此点的数量会增多
    # print(f"Total ori point number: {pcd.points.shape[0]}\n", f"Total before extend point number: {point_num}\n",
    #       f"Total extend point number: {point_extend_num}\n")
    #
    # return partition_list