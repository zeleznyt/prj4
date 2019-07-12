import os
import PRJ4_tools
import TRC_tools
import numpy as np
import matplotlib.pyplot as plt

def normalize(_data):
    """
    normalize per marker channel. Out interval 0.0 - 1.0, default reserve 10 %
    :param _data: [batch, frames, markers]
    :return:
    """
    markers_count = np.size(_data, 2)
    normed_data = _data.copy()
    minmax = np.zeros((markers_count, 2))  # min, max
    for i in range(markers_count):
        _min = np.min(_data[:, :, i])
        _max = np.max(_data[:, :, i])
        if _max - _min == 0:
            normed_data[:, :, i] = 0
        else:
            normed_data[:, :, i] = (_data[:, :, i] - _min)/(_max - _min)
        minmax[i] = _min, _max
    return normed_data, minmax

def denormalize(_data, _minmax):
    """
    :param _data:
    :param _minmax:
    :return:
    """
    markers_count = np.size(_minmax, 0)
    _den_data = _data.copy()
    for i in range(markers_count):
        _den_data[:, :, i] = _data[:, :, i] * (_minmax[i, 1] - _minmax[i, 0]) + _minmax[i, 0]
    return _den_data



if __name__ == '__main__':
    path_to_data = 'C:/Users/Tomas/Documents/Škola/FAV/PRJ/PRJ4/Data'
    # path_to_data = '/home/jedle/data/Sign-Language/TRC_files/dict_fingerless/'
    TRC_infile = os.path.join(path_to_data, 'projevy_pocasi_02.TRC')
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
    znak_1_annotation = 2969
    znak_1_history_length = 10
    znak_1 = znak_1_source_trajectory[znak_1_annotation-znak_1_history_length:znak_1_annotation+1, :]

    znak_2_source_trajectory = trajectory_matrix
    znak_2_annotation = 3009
    znak_2_future_length = 10
    znak_2 = znak_2_source_trajectory[znak_2_annotation:znak_2_annotation+znak_2_future_length, :]

    int_len = znak_2_annotation-znak_1_annotation
    res_traj = PRJ4_tools.sign_synthesis(znak_1, znak_2, int_len, 'kubic')
    # res_traj = PRJ4_tools.sign_synthesis(znak_1, znak_2, int_len, 'linear')
    print(res_traj[:,12])
    concatenated = np.concatenate((znak_1[:-1, :], res_traj, znak_2), axis=0)
    # print(np.shape(concatenated))
    #
    # x = np.arange(0, 6, 0.01)
    # y = np.zeros((np.size(x, 0), 3))
    # y[:, 0] = 2
    # y[:, 1] = np.cos(x)
    # y[:, 2] = np.sin(x)
    #
    # plt.plot(y)
    #
    # v, a = PRJ4_tools.sign_velocity_acceleration(y)
    # print(np.shape(v[:, 0]))
    # print(np.shape(a[:, 0]))
    # plt.figure()
    # plt.plot(v[:, 1])
    # plt.figure()
    # plt.plot(a[:, 1])
    # plt.show()

    concatenated = concatenated.reshape((-1, int(np.size(concatenated, 1)/3), 3))
    # print(np.shape(concatenated))
    concentrated = np.linalg.norm(concatenated, axis=2)
    # print(np.shape(concentrated))
    velocity = np.diff(concentrated, axis=0)
    # print(np.shape(velocity))
    accel = np.diff(velocity)

    normalised, minmax = normalize(np.expand_dims(res_traj, axis = 0))
    denormalised = denormalize(normalised, minmax)

    print(np.shape(normalised))
    print(np.shape(res_traj))
    plt.plot(normalised[0,4:18,37:40])
    plt.plot(normalize(np.expand_dims(concentrated, axis = 0))[0][0,4:18:,12])
    

    # _,axs = plt.subplots(4)
    # axs[0].plot(res_traj[4:18, 37])
    # axs[1].plot(res_traj[4:18, 38])
    # axs[2].plot(res_traj[4:18, 39])
    # axs[3].plot(concentrated[4:18:,12])
    # plt.plot(concatenated[:, 0, :])
    # plt.plot(concentrated[:, 0])
    
    print(np.shape(concentrated))
    # print(velocity[:,12])
    # print(concentrated[:,12])
    plt.figure()
    plt.plot(velocity[:])
    plt.figure()
    plt.plot(accel)
    plt.show()
    # _, axs = plt.subplots(3)
    # v, a = PRJ4_tools.sign_velocity_acceleration(concatenated)
    # axs[0].plot(a[:, 0])
    # axs[1].plot(v[:, 0])
    # axs[2].plot(concatenated[:, :3])
    # axs = plt.figure()
    #
    # _, axs = plt.subplots(3)
    # axs[0].plot(concatenated[:, 0])
    # axs[1].plot(concatenated[:, 1])
    # axs[2].plot(concatenated[:, 2])
    # plt.show()


    # print(np.shape(znak_1))
    # new_TRC = np.concatenate([znak_1_source_trajectory[znak_1_annotation-30:znak_1_annotation], res_traj, znak_2_source_trajectory[znak_2_annotation:znak_2_annotation+30]], axis = 0)
    #
    # plt.plot(new_TRC[:,:3])
    # plt.plot(znak_1_source_trajectory[znak_1_annotation-30:znak_2_annotation+30,:3])
    # # plt.show()
    #
    # # TRC_tools.show_pose_comparison(znak_1[-1,:], znak_2[0,:])
    # # plt.plot(res_traj[:, :3], 'b', label='orig')
    # # plt.plot(trajectory_matrix[znak_1_annotation:znak_2_annotation, :3], 'g', label='synth')
    # # plt.legend()
    # # plt.show()
