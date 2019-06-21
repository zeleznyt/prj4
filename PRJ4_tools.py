import numpy as np


def sign_synthesis_linear(_sign_1, _sign_2, _gap_length):
    """
    Synthesizes linear interpolation of movement
    :param _sign_1: trajectory frames1 X markers
    :param _sign_2: trajectory frames2 X markers
    :param _gap_length: number of frames (int)
    :return: resulting_trajectory framesR X markers (dim = frames1+frames2+_gap_length X markers)
    """
    inter = np.zeros((_gap_length, np.size(_sign_1, 1)))
    for traj in range(np.size(_sign_1, 1)):
        for frame in range(_gap_length):
            inter[frame, traj] = -1*(_sign_1[0,traj]-_sign_2[0,traj])/_gap_length*frame+_sign_1[0,traj]
    res = np.concatenate((_sign_1, inter, _sign_2), axis=0)
    return res
