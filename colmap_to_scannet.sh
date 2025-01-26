#!/bin/bash

# 定义场景数组
scenes=("chrismas-tree" "corridor" "couplet" "entrance" "grove" "rv")

# 遍历每个场景并执行 Python 程序
for scene in "${scenes[@]}"; do
    source_path="/media/immortalqx/Dataset/KiriSceneDepth/$scene"
    partition_model_path="/media/immortalqx/Result/VastGaussian/output/$scene/partition_point_cloud/ori"
    output_dir="/media/immortalqx/Result/VastGaussian/output/$scene/scannet_dataset"

    # 执行 Python 程序
    echo "Processing scene: $scene"
    python splited_colmap_to_scannet.py --source_path "$source_path" \
    --partition_model_path "$partition_model_path" \
    --output_dir "$output_dir"

    echo "Finished processing scene: $scene"
done