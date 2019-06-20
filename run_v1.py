import PRJ4_tools
import TRC_tools
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    TRC_infile = 'projevy_pocasi_02.TRC'
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
    znak_1_history_length = 1
    znak_1 = znak_1_source_trajectory[znak_1_annotation-znak_1_history_length:znak_1_annotation, :]

    znak_2_source_trajectory = trajectory_matrix
    znak_2_annotation = 3059
    znak_2_future_length = 1
    znak_2 = znak_2_source_trajectory[znak_2_annotation:znak_2_annotation+znak_2_future_length, :]

    int_len = znak_2_annotation-znak_1_annotation
    res_traj = PRJ4_tools.sign_synthesis_linear(znak_1, znak_2, int_len)

    plt.plot(res_traj[:, :3], 'b', label='orig')
    plt.plot(trajectory_matrix[znak_1_annotation:znak_2_annotation, :3], 'g', label='synth')
    plt.legend()
    plt.show()
