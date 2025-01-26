# train building
#nohup python train_vast.py -s ../datasets/Mill19/building \
#--exp_name building \
#--manhattan \
#--eval \
#--llffhold 83 \
#--resolution 4 \
#--pos "-62.527942657471 0.000000000000 -15.786898612976" \
#--rot "0.932374119759 0.000000000000 0.361494839191 0.000000000000 1.000000000000 0.000000000000 -0.361494839191 0.000000000000 0.932374119759" \
#--m_region 3 \
#--n_region 3 \
#--iterations 60_000 \
#> log-6.23 2>&1 & echo $! > run.pid


# train rubble cc
#nohup python train_vast.py -s ../datasets/Mill19/rubble \
#--exp_name rubble \
#--manhattan \
#--eval \
#--llffhold 83 \
#--resolution 4 \
#--pos "25.607364654541 0.000000000000 -12.012700080872" \
#--rot "0.923032462597 0.000000000000 0.384722054005 0.000000000000 1.000000000000 0.000000000000 -0.384722054005 0.000000000000 0.923032462597" \
#--m_region 3 \
#--n_region 3 \
#--iterations 60_000 \
#> log-7.1-rubble 2>&1 & echo $! > run.pid

# train rubble tj
#nohup python train_vast.py -s ../datasets/Mill19/rubble \
#--exp_name rubble_tj \
#--manhattan \
#--platform "tj" \
#--eval \
#--llffhold 83 \
#--resolution 4 \
#--pos "0.0 0.0 0.0" \
#--rot "0.0 21 0.0" \
#--m_region 3 \
#--n_region 3 \
#--iterations 60_000 \
#> log-6.26 2>&1 & echo $! > run.pid

# train train
#python train_vast.py -s /media/immortalqx/Dataset/KiriScene/vastgaussian/tandt/train \
#--exp_name train \
#--manhattan \
#--pos "-7.70662571 4.45195873 0.51466437" \
#--rot "0.86119716 0.03436749 0.50710779 0.03316087 0.99414171 -0.1028718 -0.50768368 0.10611482 0.85498364" \
#--m_region 2 \
#--n_region 1 \
#--iterations 30_000
#> log-6.23 2>&1 & echo $! > run.pid


# =========================================================
# #########################################################
# *********************************************************

#python split_colmap.py -s /media/immortalqx/Dataset/KiriScene/corridor \
#--exp_name corridor \
#--m_region 4 \
#--n_region 2

#python split_colmap.py -s /media/immortalqx/Dataset/KiriScene/couplet \
#--exp_name couplet \
#--m_region 1 \
#--n_region 2

#python split_colmap.py -s /media/immortalqx/Dataset/KiriScene/gate \
#--exp_name gate \
#--m_region 2 \
#--n_region 2

#python split_colmap.py -s /media/immortalqx/Dataset/KiriScene/office \
#--exp_name office \
#--m_region 2 \
#--n_region 2

#python split_colmap.py -s /media/immortalqx/Dataset/KiriScene/room \
#--exp_name room \
#--m_region 2 \
#--n_region 2

#python train_vast.py -s /media/immortalqx/Dataset/KiriScene/room \
#--exp_name room \
#--manhattan \
#--pos "0.0 0.0 0.0" \
#--rot "1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0" \
#--m_region 2 \
#--n_region 1 \
#--iterations 30_000

# 使用cloudcompare得到的变换矩阵
# [21:07:03] 0.846814572811 0.000000000000 0.531888246536 -2.974608421326
  #0.000000000000 1.000000000000 0.000000000000 0.000000000000
  #-0.531888246536 0.000000000000 0.846814572811 -7.207013607025
  #0.000000000000 0.000000000000 0.000000000000 1.000000000000
#python split_colmap.py -s /media/immortalqx/Dataset/KiriScene/office \
#--exp_name office \
#--manhattan \
#--pos "-2.974608421326 0.000000000000 -7.207013607025" \
#--rot "0.846814572811 0.000000000000 0.531888246536 0.000000000000 1.000000000000 0.000000000000 -0.531888246536 0.000000000000 0.846814572811" \
#--m_region 2 \
#--n_region 2

# 跑得比较快的数据集，上面的office没有深度，而且跑得慢
#python split_colmap.py -s /media/immortalqx/Dataset/KiriSceneDepth/chrismas-tree \
#--exp_name chrismas-tree \
#--m_region 2 \
#--n_region 1
#
python split_colmap.py -s /media/immortalqx/Dataset/KiriSceneDepth/corridor \
--exp_name corridor \
--m_region 2 \
--n_region 2
#
#python split_colmap.py -s /media/immortalqx/Dataset/KiriSceneDepth/couplet \
#--exp_name couplet \
#--m_region 2 \
#--n_region 1
#
#python split_colmap.py -s /media/immortalqx/Dataset/KiriSceneDepth/entrance \
#--exp_name entrance \
#--m_region 2 \
#--n_region 1
#
#python split_colmap.py -s /media/immortalqx/Dataset/KiriSceneDepth/grove \
#--exp_name grove \
#--m_region 2 \
#--n_region 2
#
#python split_colmap.py -s /media/immortalqx/Dataset/KiriSceneDepth/rv \
#--exp_name rv \
#--m_region 3 \
#--n_region 1