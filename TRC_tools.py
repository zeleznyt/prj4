import os
import numpy as np
import json
import matplotlib.pyplot as plt
import h5py
import decimal
from mpl_toolkits.mplot3d import Axes3D


def TRC_load(_file, raw=False):
    """
    loads TRC file (known issues: metadata read - \n \t removal issues
    :param _file: path
    :param raw: returns raw header
    :return: np.array data, list header
    """
    with open(_file, 'r') as f:
        content = f.readlines()

    _raw_header = content[:5]

    path_info = _raw_header[0][:-1]
    meta_items = _raw_header[1][:-1].split('\t')
    meta_data = _raw_header[2].strip().split('\t')
    column_names = _raw_header[3][:-2].split('\t')
    marker_info = _raw_header[4][:-1].split('\t')

    _raw_data = content[5:]
    data_list = []
    for i, _line in enumerate(_raw_data):
        clear_line = _line.split('\t')
        clear_line[-1] = clear_line[-1][:-2]
        np_line = np.zeros((len(clear_line[2:]), ))
        for j, number in enumerate(clear_line[2:]):
            if number is '':
                # print('all markers are not present file: {}, (frame: {})'.format(_file, i))
                number = float('inf')
            else:
                number = float(number)
            np_line[j] = number
        data_list.append(np_line)

    _header = {'path_info': path_info, 'meta_items': meta_items, 'meta_data': meta_data, 'column_names': column_names, 'marker_info': marker_info}
    if raw:
        return np.asarray(data_list), _raw_header
    else:
        return np.asarray(data_list), _header


def TRC_write(data_array, _header, outfile):
    """
    writes TRC file.
    :param data_array: numpy array (frames, markers)
    :param header: header (from TRC_load)
    :param outfile: path to output file
    """

    new_file = []
    data_length = np.size(data_array, 0)
    _header['meta_data'][2] = str(data_length)

    new_file.append(_header['path_info'] + '\n')
    new_file.append(line_maker(_header['meta_items']))
    new_file.append(line_maker(_header['meta_data']))
    new_file.append(line_maker(_header['column_names']))
    new_file.append(line_maker(_header['marker_info']))

    # print(_header['meta_items'])
    third_timestamp = float(0.015)
    time_step = 1/float(_header['meta_data'][0])
    zero_time = third_timestamp - 2*time_step
    for i in range(np.size(data_array, 0)):
        ts = float(zero_time) + i*time_step
        line = str(i) + '\t' + float_to_str(ts) + '\t'

        for j in range(np.size(data_array, 1)):
            line += float_to_str(data_array[i, j]) + '\t'
        line = line[:-1] + '\n'
        new_file.append(line)

    with open(outfile, 'w') as f:
        f.writelines(new_file)


def TRC_finger_remove(input_file):
    """
    Removes finger markers from TRC data !
    :param input_file: TRC file
    :return: trajectory data, new header
    """
    data, header = TRC_load(input_file)

    basic = []
    for i in range(int(np.size(data, 1)/3)):
        tmp = get_marker_name_obs(i*3, header, remove_before_char=':', axis_detail=False)
        if not (('0' in tmp or '1' in tmp or '2' in tmp or '3' in tmp) and len(tmp) == 5):
            basic.append(tmp)

    indexes = get_marker_id(basic, header)
    shft_indexes = [x+2 for x in indexes]
    shft_indexes = [0, 1] + shft_indexes

    sel_column_names = [s for i, s in enumerate(header['column_names']) if i in shft_indexes]
    sel_marker_info = [s for i, s in enumerate(header['marker_info']) if i in shft_indexes]

    sel_data = np.zeros((np.size(data, 0), len(indexes)))
    for i in range(len(indexes)):
        sel_data[:, i] = data[:, indexes[i]]

    new_header = {'path_info': header['path_info'], 'meta_data': header['meta_data'], 'meta_items': header['meta_items'], 'column_names': sel_column_names, 'marker_info':sel_marker_info}
    return sel_data, new_header


def float_to_str(f, precision=10):
    """
    Convert the given float to a string,
    without resorting to scientific notation
    """
    ctx = decimal.Context()
    ctx.prec = precision
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')


def line_maker(_list):
    """
    function used by TRC_write (list to line with tabs and newline)
    :param _list: item list (strings)
    :return: string line of items (tabs, newline)
    """
    _line = ''
    for part in _list:
        _line += part + '\t'
    _line = _line[:-1] + '\n'
    return _line


def dict_read(dict_file):
    """
    json load file tool
    :param dict_file:
    :return:
    """
    with open(dict_file, 'r') as f:
        tmp_dict = json.load(f)
    return tmp_dict


def get_marker_id(_marker_name, _header):
    """
    TODO: remake / check functionality  (does not work correctly)
    :param _marker_name:
    :param _header:
    :return:
    """
    print('function: get_marker_id, should be revised (does not work correctly)')
    column_info = _header['column_names'][2:]
    valid_idxs = []
    for mark in _marker_name:
        full_name = ([s for i, s in enumerate(column_info) if mark in s][0])
        idx = ([i for i, s in enumerate(column_info) if mark in s][0])
        valid_idxs.append(idx)
        for i in range(1, 3):
            if column_info[idx+i] is '':
                valid_idxs.append(idx+i)
            else:
                break
    return valid_idxs


def get_marker_name(_meta, _id):
    """
    TRC file tool: returns marker name (and axis)
    :param _meta: TRC_load meta
    :param _id: number of marker (0 based)
    :return: name, axis
    """
    pointer = (int(_id/3) * 3) + 2  # shift size 2 : first two columns are not markers (frame number, time)
    IoU = _meta['column_names'][pointer] if _meta['column_names'][pointer] != '' else '-1'
    IoU_axis = _meta['marker_info'][_id + 2]
    return IoU, IoU_axis


def get_marker_name_obs(_idx, _header, remove_before_char=None, axis_detail=True):
    """
    obsolete, new version is available
    :param _idx:
    :param _header:
    :param remove_before_char:
    :param axis_detail:
    :return:
    """
    print('get_marker_name_obs: obsolete, new function available in this lib')
    if _header['column_names'][_idx+2] is not '':
        IoU = _header['column_names'][_idx+2]
    else:
        for i in range(1, 5):
            if _header['column_names'][_idx+2-i] is not '':
                IoU = _header['column_names'][_idx+2-i]
                break

    if remove_before_char is not None:
        IoU = IoU.split(remove_before_char)[1]

    if not axis_detail:
        return IoU
    else:
        return IoU, _header['marker_info'][_idx+2]


def shift_trajectory(_raw_data, _coord_list):
    """
    Shift all trajectories based on selected marker
    :param _raw_data: trajectory (3D numpay array: [take, frame, marker])
    :param _coord_list: [X, Y, Z] coords of marker used for zeroing (selected manually)
    :return: shifted trajectory
    """
    takes_count, frames_count, markers_count = np.shape(_raw_data)
    _new_data = _raw_data.copy()
    for take in range(takes_count):
        for frame in range(frames_count):
            _zero = _raw_data[take, frame, _coord_list]
            _frame_res = np.reshape(_raw_data[take, frame, :], (-1, 3))
            _new_frame_res = _frame_res - _zero
            _new_data[take, frame, :] = np.reshape(_new_frame_res, (markers_count,))
    return _new_data


def show_pose(frame, highlight_marker=None):
    """
    Create 3D plot of marker positions
    :param frame: trajectory (1d numpy array: [markers])
    :param highlight_marker: order number of marker to be highlighted
    :return: True
    """
    show_frame = frame.reshape(int(frame.shape[0]/3), 3)

    fig = plt.figure(figsize=(10, 10))

    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim3d(-1000, 1000)
    ax.set_ylim3d(-1000, 1000)
    ax.set_zlim3d(-1000, 1000)

    if highlight_marker is None:
        Axes3D.scatter(ax, xs=show_frame[:, 0], ys=show_frame[:, 1], zs=show_frame[:, 2], c='b', marker='o')
    else:
        Axes3D.scatter(ax, xs=show_frame[:highlight_marker, 0], ys=show_frame[:highlight_marker, 1], zs=show_frame[:highlight_marker, 2], c='b', marker='o')
        Axes3D.scatter(ax, xs=show_frame[highlight_marker+1:, 0], ys=show_frame[highlight_marker+1:, 1], zs=show_frame[highlight_marker+1:, 2], c='b', marker='o')
        Axes3D.scatter(ax, xs=show_frame[highlight_marker, 0], ys=show_frame[highlight_marker, 1], zs=show_frame[highlight_marker, 2], c='r', marker='o', label='marker #{}'.format(highlight_marker))
        ax.legend()
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')
    # Axes3D.plot(ax, xs=trajectory[:, 0], ys=trajectory[:, 1], zs=trajectory[:, 2], c='k', linestyle='dashed')
    ax.view_init(90, -90)
    plt.show()
    return True


def show_pose_comparison(frame, frame_comparison, highlight_marker=None):
    """
    Create 3D plot of marker positions
    :param frame: trajectory (1d numpy array: [markers])
    :param highlight_marker: order number of marker to be highlighted
    :return: True
    """
    show_frame = frame.reshape(int(frame.shape[0]/3), 3)
    show_frame_comp = frame_comparison.reshape(int(frame_comparison.shape[0]/3), 3)

    fig = plt.figure(figsize=(10, 10))

    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim3d(-1000, 1000)
    ax.set_ylim3d(-1000, 1000)
    ax.set_zlim3d(-1000, 1000)

    if highlight_marker is None:
        Axes3D.scatter(ax, xs=show_frame[:, 0], ys=show_frame[:, 1], zs=show_frame[:, 2], c='b', marker='o')
    else:
        Axes3D.scatter(ax, xs=show_frame[:highlight_marker, 0], ys=show_frame[:highlight_marker, 1], zs=show_frame[:highlight_marker, 2], c='b', marker='o')
        Axes3D.scatter(ax, xs=show_frame[highlight_marker+1:, 0], ys=show_frame[highlight_marker+1:, 1], zs=show_frame[highlight_marker+1:, 2], c='b', marker='o')
        Axes3D.scatter(ax, xs=show_frame[highlight_marker, 0], ys=show_frame[highlight_marker, 1], zs=show_frame[highlight_marker, 2], c='r', marker='o', label='marker #{}'.format(highlight_marker))
        ax.legend()

    if highlight_marker is None:
        Axes3D.scatter(ax, xs=show_frame_comp[:, 0], ys=show_frame_comp[:, 1], zs=show_frame_comp[:, 2], c='m', marker='o')
    else:
        Axes3D.scatter(ax, xs=show_frame_comp[:highlight_marker, 0], ys=show_frame_comp[:highlight_marker, 1], zs=show_frame_comp[:highlight_marker, 2], c='g', marker='o')
        Axes3D.scatter(ax, xs=show_frame_comp[highlight_marker+1:, 0], ys=show_frame_comp[highlight_marker+1:, 1], zs=show_frame_comp[highlight_marker+1:, 2], c='g', marker='o')
        Axes3D.scatter(ax, xs=show_frame_comp[highlight_marker, 0], ys=show_frame_comp[highlight_marker, 1], zs=show_frame_comp[highlight_marker, 2], c='g', marker='o', label='marker #{}'.format(highlight_marker))
        ax.legend()

    for i in range(np.size(show_frame, 0)):
        ax.plot((show_frame[i, 0], show_frame_comp[i, 0]),(show_frame[i, 1], show_frame_comp[i, 1]), (show_frame[i, 2], show_frame_comp[i, 2]), 'b-')

    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')
    ax.view_init(90, -90)
    plt.show()
    return True
