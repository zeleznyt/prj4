import os
import PRJ4_tools
import TRC_tools
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    path_to_data = 'D:/Škola/FAV/PRJ/PRJ4/Data'
    TRC_infile = os.path.join(path_to_data, 'projevy_pocasi_02_fullfingers.TRC')
    # slovnik_infile = 'pocasi_slovnik9.txt'
    trajectory_matrix, metadata = TRC_tools.TRC_load(TRC_infile)
    # slovnik = TRC_tools.dict_read(slovnik_infile)

    # print(TRC_tools.get_marker_name(metadata, 0))
    # for tmp_item in slovnik:
    #     file_name_pattern = TRC_infile.split('.')[0]
    #     if file_name_pattern in tmp_item['bvh_source']:
    #         print(tmp_item)
    #

    znak_1_source_trajectory = trajectory_matrix
    znak_1_annotation = 2959
    znak_1_history_length = 2
    znak_1 = znak_1_source_trajectory[znak_1_annotation-znak_1_history_length+1:znak_1_annotation+1, :]

    znak_2_source_trajectory = trajectory_matrix
    znak_2_annotation = 3009
    znak_2_future_length = 2
    znak_2 = znak_2_source_trajectory[znak_2_annotation:znak_2_annotation+znak_2_future_length, :]

    int_len = znak_2_annotation-znak_1_annotation
    res_traj = PRJ4_tools.sign_synthesis(znak_1, znak_2, int_len, 'kubic')
    orig_traj = trajectory_matrix[znak_1_annotation+1:znak_2_annotation]

    print(PRJ4_tools.compare_velocity(orig_traj, res_traj))

    error = PRJ4_tools.sign_error(orig_traj, res_traj, 'mse')
    print(np.shape(error))
    print(error)
    plt.figure()
    plt.plot(error)

    new_TRC = np.concatenate([znak_1_source_trajectory[znak_1_annotation-30:znak_1_annotation], res_traj, znak_2_source_trajectory[znak_2_annotation:znak_2_annotation+30]], axis = 0)

    # max_vel, max_acc, argmax_vel, argmax_acc = PRJ4_tools.sign_velocity_acceleration(res_traj)
    # print(max_vel)
    # print(argmax_vel)
    # print(max_acc)
    # print(argmax_acc)

    plt.figure()
    plt.plot(new_TRC[:,:3])
    plt.plot(znak_1_source_trajectory[znak_1_annotation-30:znak_2_annotation+30,:3])
    plt.show()
    # TRC_tools.show_pose_comparison(znak_1[-1,:], znak_2[0,:])
    # plt.plot(res_traj[:, :3], 'b', label='orig')
    # plt.plot(trajectory_matrix[znak_1_annotation:znak_2_annotation, :3], 'g', label='synth')
    # plt.legend()
    # plt.show()
