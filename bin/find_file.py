__author__ = 'lulu614'

import os


def find_file():
    def is_file_exit(dir):
        count =0
        res = False
        path = os.path.join(work_dir, dir)
        if os.path.isdir(path):
            os.chdir(path)
            for data in data_list:
                if os.path.isfile(data):
                    count += 1
            if count == 3:
                res = True
        return res


    '''
        检索文件是否存在且齐全并进入文件所在目录
    '''

    # 所需文件
    data_list = ['pile.xlsx','soil.xlsx','para.xlsx']
    # 检索目录
    dir_list = ['',r'data',r'..\data']

    work_dir = os.getcwd()
    dir_count = 0
    for dir in dir_list:
        if is_file_exit(dir):
            break
        else:dir_count += 1
    if dir_count == len(dir_list):
        print('所需文件不存在，请重新确认')
        input('输入任何内容退出：', )
        os.exit()
__author__ = 'lulu614'