# FIXME 这个项目的import有点奇怪，似乎存在循环依赖的问题，加入以下的import刚好能够运行这份代码
from scene.vastgs.appearance_network import AppearanceNetwork

import os
import copy
import sys
from argparse import ArgumentParser, Namespace
from arguments import ModelParams
from utils.manhattan_utils import get_man_trans
from utils.partition_utils import data_partition


def prepare_output_and_logger(args):
    if not args.model_path:
        model_path = os.path.join("./output/", args.exp_name)
        # 如果这个文件存在，就在这个文件名的基础上创建新的文件夹，文件名后面跟上1,2,3
        if os.path.exists(model_path):
            base_name = os.path.basename(model_path)
            dir_name = os.path.dirname(model_path)
            file_name, file_ext = os.path.splitext(base_name)
            counter = 1
            while os.path.exists(os.path.join(dir_name, f"{file_name}_{counter}{file_ext}")):
                counter += 1
            new_folder_name = f"{file_name}_{counter}{file_ext}"
            model_path = os.path.join(dir_name, new_folder_name)
        args.model_path = model_path

    # Set up output folder
    print("Output folder: {}".format(args.model_path))
    os.makedirs(args.model_path, exist_ok=True)
    with open(os.path.join(args.model_path, "cfg_args"), 'w') as cfg_log_f:
        var_dict = copy.deepcopy(vars(args))
        del_var_list = ["manhattan", "man_trans", "pos", "rot",
                        "m_region", "n_region", "extend_rate", "visible_rate",
                        "num_gpus", "partition_id", "partition_model_path", "platform",
                        "llffhold"]  # 删除多余的变量，防止无法使用SIBR可视化
        for key in vars(args).keys():
            if key in del_var_list:
                del var_dict[key]
        cfg_log_f.write(str(Namespace(**var_dict)))


if __name__ == "__main__":
    # Set up command line argument parser
    parser = ArgumentParser(description="Training script parameters")
    lp = ModelParams(parser)
    args = parser.parse_args(sys.argv[1:])

    lp = lp.extract(args)

    # Manhattan Alignment
    if args.manhattan:
        # 如果使用了--manhattan参数，执行相应的操作
        lp.man_trans = get_man_trans(lp)
        print("Manhattan alignment enabled")
    else:
        print("Manhattan alignment not enabled")

    # lp.extend_rate = 0.001
    prepare_output_and_logger(lp)

    # data partition
    partition_num, partition_id_list = data_partition(lp)

    # 感觉在这里加一个后处理是最实际的解决思路
    # readColmapSceneInfoVast这个函数可以好好利用！