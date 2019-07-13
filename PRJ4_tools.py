import numpy as np
import matplotlib.pyplot as plt

def sign_synthesis(_sign_1, _sign_2, _gap_length, _type):
    """
    Synthesizes linear interpolation of movement
    :param _sign_1: trajectory frames1 X markers
    :param _sign_2: trajectory frames2 X markers
    :param _gap_length: number of frames (int)
    :param _type: type of interpolation: 'linear', 'kubic'
    :return: resulting_trajectory framesR X markers (dim = frames1+frames2+_gap_length X markers)
    """
    if _type == 'linear':
        _sign_1_t = _sign_1[-1:, :]
        _sign_2_t = _sign_2[0:1, :]
        inter = np.zeros((_gap_length, np.size(_sign_1_t, 1)))
        for traj in range(np.size(_sign_1_t, 1)):
            for frame in range(_gap_length):
                inter[frame, traj] = -1*(_sign_1_t[0, traj]-_sign_2_t[0, traj])/_gap_length*frame+_sign_1_t[0, traj]
        res = inter
    elif _type == 'kubic':
        if np.size(_sign_1, 0) < 2:
            res = -1
        else:
            _sign_1_t = _sign_1[-2:, :]
            _sign_2_t = _sign_2[0:2, :]
            inter = np.zeros((_gap_length, np.size(_sign_1_t, 1)))

            for traj in range(np.size(_sign_1_t, 1)):
                y1 = _sign_1_t[1, traj]
                y2 = _sign_2_t[0, traj]
                k1 = _sign_1_t[1, traj]-_sign_1_t[0, traj]
                k2 = _sign_2_t[1, traj]-_sign_2_t[0, traj]

                for frame in range(_gap_length):
                    t = frame/_gap_length
                    a = k1*_gap_length - (y2-y1)
                    b = -k2*_gap_length + (y2-y1)
                    inter[frame, traj] = (1-t)*y1 + t*y2 + t*(1-t)*((1-t)*a + t*b)
            res = inter
    else:
        res = -1
    return res[1:,:]

def sign_velocity_acceleration(_sign):
    """
    Calculates max velocity and acceleration in the sign
    :param _sign: trajectory frames X markers
    :return: max_velocity, max_acceleration, arg_max_vel, arg_max_acc (type = float, float, int, int)
    Uses the right difference: v(t) = x(t) - x(t+1)
    """

    if np.size(_sign, 0) < 3:
        return -1
    velocity = np.zeros((np.size(_sign, 0)-1, int(np.size(_sign, 1)/3)))
    acceleration = np.zeros((np.size(_sign, 0)-2, int(np.size(_sign, 1)/3)))

    for v in range(np.size(velocity, 0)):
        for traj in range(int(np.size(velocity, 1))):
            velocity[v, traj] = np.sqrt(np.power(_sign[v, 3*traj]-_sign[v+1, 3*traj], 2)+np.power(_sign[v, 3*traj+1]-_sign[v+1, 3*traj+1], 2)+np.power(_sign[v, 3*traj+2]-_sign[v+1, 3*traj+2], 2))

    for a in range(np.size(acceleration, 0)):
        for traj in range(np.size(acceleration, 1)):
            acceleration[a, traj] = (velocity[a, traj]-velocity[a+1, traj])

    plt.figure()
    plt.plot(velocity)
    plt.title('Velocity')
    print(np.shape(velocity))
    plt.figure()
    plt.plot(acceleration)
    plt.title('Acceleration')
    print(np.shape(acceleration))

    max_velocity = np.amax(abs(velocity))
    max_acceleration = np.amax(abs(acceleration))
    arg_max_vel = np.argmax(np.amax(abs(velocity), axis=0))
    arg_max_acc = np.argmax(np.amax(abs(acceleration), axis=0))

    return max_velocity, max_acceleration, arg_max_vel, arg_max_acc
