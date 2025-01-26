import os
import sys
from argparse import ArgumentParser
from scene import sceneLoadTypeCallbacks
from utils.manhattan_utils import get_man_trans
import glob


def ensure_directory_exists(directory):
    """Ensure that the given directory exists. Create it if it does not."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created output directory: {directory}")


if __name__ == "__main__":
    parser = ArgumentParser(description="Training script parameters")
    # 添加命令行参数配置
    parser.add_argument('--source_path', required=True, help='Path to source data')
    parser.add_argument('--partition_model_path', required=True, help='Path to partition model')
    parser.add_argument('--output_dir', required=True, help='Path to output')
    parser.add_argument('--manhattan', action='store_true', help='Enable Manhattan alignment')
    parser.add_argument('--pos', type=str, help='Position as a space-separated string (x y z)')
    parser.add_argument('--rot', type=str, help='Rotation as a space-separated string (row1 col1 row1 col2...)')

    args = parser.parse_args(sys.argv[1:])

    # Ensure output directory exists
    ensure_directory_exists(args.output_dir)

    # Manhattan Alignment
    man_trans = None
    if args.manhattan:
        # 如果使用了--manhattan参数，执行相应的操作
        man_trans = get_man_trans(args)
        print("Manhattan alignment enabled")
    else:
        print("Manhattan alignment not enabled")

    # 获取所有的 .txt 文件
    txt_files = glob.glob(os.path.join(args.partition_model_path, "*_camera.txt"))

    if not txt_files:
        print("No partition files found in the partition model path.")
        sys.exit(1)

    print(f"Found {len(txt_files)} partition files.")

    for txt_file in txt_files:
        partition_id = os.path.splitext(os.path.basename(txt_file))[0].replace("_camera", "")  # 根据文件名提取 partition_id
        print(f"Processing partition_id: {partition_id}")

        partition_output_dir = os.path.join(args.output_dir, partition_id)
        ensure_directory_exists(partition_output_dir)

        scene_info = sceneLoadTypeCallbacks["ColmapToScannet"](
            args.source_path,
            args.partition_model_path,
            partition_id,
            man_trans=man_trans,
            output_dir=partition_output_dir
        )

        print(f"Finished processing partition_id: {partition_id}")
