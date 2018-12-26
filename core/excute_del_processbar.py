__author__ = 'lulu614'

import threading, queue,time,os
from bin.stiffness import stiffness
from bin.load_paramenter import *
from progressbar import *
from multiprocessing import Process, Pipe,Manager, Pool,freeze_support



def run(q,count,res):
    num = q.get()
    stiff = stiffness(num, para, pile_dict_all, soil_list)
    res[num] = stiff
    # print('进程号', os.getpid())

# def bar(count):
#     pbar.update(10 * count + 1)
#     count += 1

def write_stiffness(num,stiff):
    for cell in ws.iter_rows(min_row=2):
        if cell[0].value < num:
            continue
        elif cell[0].value == num:
            cell[7].value = stiff
        else:
            break
    # print('%s is done...' %num)


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


time_start = time.time()

'''
    检索文件是否存在且齐全并进入文件所在目录
'''
if __name__ == '__main__':
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

'''
    导入参数
'''
para = load_para()
pile_dict_all = load_pile_dict()
soil_list = load_soil_list()
num_list = list(pile_dict_all.pile_dict.keys())
total = len(num_list)           # 节点总个数，总计数
progress_num = 5               #程序并行运行进程数，用户自定义

#打开表格
wb = load_workbook('pile.xlsx')
ws = wb.active

# #添加progressbar——进度条
# widgets = ['Progress: ', Percentage(), ' ', Bar('#'), ' ', Timer(),' ', ETA()]
# pbar = ProgressBar(widgets=widgets, maxval=10 * total).start()


if __name__ == '__main__':
    freeze_support()

    manager = Manager()
    res = manager.dict()  # num:stiff结果列表
    count = 0  # 进度计数

    # 添加num_list加入队列q
    q = manager.Queue()
    for num in num_list:
        q.put(num)


    pool = Pool(processes=progress_num)         #允许进程池同时放入progress_num个进程
    for i in range(total):
        pool.apply_async(func=run, args=(q,count,res,))    #callback=回调     callback=bar(count)
    pool.close()
    pool.join()             #进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。.join()

    # pbar.finish()
    for num in res.keys():
        write_stiffness(num, res[num])

    wb.save('pile.xlsx')
    wb.close()

    time_end = time.time()
    print('程序运行完毕，总共运行时间为：',time_end-time_start,'秒')
    print('程序将在10s后自动退出')

    def main():
        input('输入任何内容退出：',)
    def minor():
        time.sleep(10)
    t_main = threading.Thread(target=main)
    t_main.start()
    t_minor = threading.Thread(target=minor)
    t_minor.setDaemon(True)
    t_minor.start()



