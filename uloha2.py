import os
import numpy as np


def addChild(idx):
        # print('new child: ---------------------------')
        output = {}
        line = data_pro_tebe[idx].strip()
        while(line != '}') and idx < len(data_pro_tebe)-1:
            # print(line)
            if line.split(' ')[0] == 'End':
                output['End Site'] = {data_pro_tebe[idx+2].strip().split(' ')[0]: data_pro_tebe[idx+2].strip()[len(data_pro_tebe[idx+2].strip().split(' ')[0])+1:]}
                return output, idx+4
            if line.split(' ')[0] == 'JOINT':
                output[line], idx = addChild(idx+2)
            else:
                output[line.split(' ')[0]] = line[len(line.split(' ')[0])+1:]
            idx += 1
            line = data_pro_tebe[idx].strip()
            # print(output)
        # print('End child----------------------------------------------------------------------')
        return output, idx


if __name__ == '__main__':
    path_to_data = '/home/jedle/data/SL/data_prep/dict_solved' # Pavel
    # path_to_data = 'C:/Users/Tomas/Documents/Škola/FAV/PRJ/PRJ4/Data' # Tomáš notebook
    # path_to_data = 'D:\Škola\FAV\PRJ\PRJ4\Data' # Tomáš PC
    bvh_file = os.path.join(path_to_data, 'projevy_pocasi_02_solved_body.bvh') #'data2.bvh')#


    with open(bvh_file, 'r') as f:
        content = f.readlines()

    index = ([x for x, con in enumerate(content) if 'MOTION' in con])
    
    data_pro_tebe = content[:index[0]]

    slovnik = {}
    idx = 0
    while idx < len(data_pro_tebe):
        line = data_pro_tebe[idx].strip()
        if line == '{':
            slovnik[data_pro_tebe[idx-1].strip()], idx = addChild(idx+1)
        idx += 1
    print(slovnik)
    print(slovnik.keys())
    print(slovnik['ROOT Hips']['JOINT Spine'].keys())

