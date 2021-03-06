__author__ = 'lulu614'

import threading, queue
from bin.stiffness import stiffness
from bin.load_paramenter import *
from progressbar import *



def run():
    global count
    stiff = stiffness(q.get(), para, pile_dict_all, soil_list)
    res[num] = stiff
    lock.acquire()
    pbar.update(10 * count + 1)
    count += 1
    lock.release()

def write_stiffness(num,stiff):
    for cell in ws.iter_rows(min_row=2):
        if cell[0].value < num:
            continue
        elif cell[0].value == num:
            cell[7].value = stiff
        else:
            break
    # print('%s is done...' %num)


time_start = time.time()
#导入参数
para = load_para()
pile_dict_all = load_pile_dict()
soil_list = load_soil_list()
num_list = list(pile_dict_all.pile_dict.keys())
line_num = 10        #程序并行运行进程数，用户自定义

#打开表格
wb = load_workbook('pile.xlsx')
ws = wb.active

res = {}                    #num:stiff结果列表
total = len(num_list)       #节点总个数，总计数
count = 0                   #进度计数
lock = threading.Lock()     #添加线程锁

#添加progressbar
widgets = ['Progress: ', Percentage(), ' ', Bar('#'), ' ', Timer(),' ', ETA()]
pbar = ProgressBar(widgets=widgets, maxval=10 * total).start()

#添加num_list加入队列q
q = queue.Queue()
for num in num_list:
    q.put(num)

if __name__ == '__main__':
    semaphore = threading.BoundedSemaphore(line_num)  # 最多允许5个线程同时运行
    # 建立line_num个线程，从队列q中取num值
    for i in range(total):
        t = threading.Thread(target=run)
        t.start()
while threading.active_count() != 1:
    pass
else:
    pbar.finish()

    for num in res.keys():
        write_stiffness(num, res[num])

    wb.save('pile.xlsx')
    wb.close()

    time_end = time.time()
    print('程序运行完毕，总共运行时间为：',time_end-time_start,'s')
    print('程序将在10s后自动退出')
    time.sleep(10)
