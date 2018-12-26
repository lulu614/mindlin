__author__ = 'lulu614'

from bin.mindlin import mindlin
from bin.load_paramenter import *
from bin.find_file import find_file


def stiffness(num,para,pile_dict_all,soil_list):
    sphere_influence = para.sphere_influence     #群桩影响范围
    layer_thickness = para.layer_thickness
    depth = para.depth
    pile_num = pile_dict_all[num]
    pile_dict = pile_num.choosen(pile_dict_all,sphere_influence)

    '''
        导入土层参数并去除桩端以上部分
    '''
    l = pile_num.l            #桩长
    z = l                     #深度
    soil_list_copied = soil_list.copy()
    soil_list_copied.del_pile(l+depth)

    sum_s = 0   #沉降
    for soil in soil_list_copied.soil_list:      #分土层计算
        break_flag = False
        #建立h_list ——分层列表
        Es = soil.Es
        v = soil.v
        h_list = soil.divide(layer_thickness)
        for h in h_list:          #按layer_thickness分层计算
            stress = 0   #附加应力值
            for pile in pile_dict.values():

                #计算并累加附加应力值
                m = mindlin(para,pile_num,pile,v,z)
                stress += m[0] + m[1]
                print('m1,m2:',m[0] , m[1])
                # print(a, b, v, Q, l, r, z)
                # print(m[0] , m[1])
                # print(stress)

            z += h    #累计深度值
            print(stress)
            sum_s += stress*h/Es   #累计沉降值

            '''
                变形收敛——占比小于1%
            '''
            if stress*layer_thickness/Es/sum_s < 0.01:
                break_flag = True
                break
        if break_flag == True:
            break


    Q = pile_num.Q
    E = Q/sum_s
    return E,sum_s


if __name__ == '__main__':
    find_file()
    '''
        导入参数
    '''
    para = load_para()
    pile_dict_all = load_pile_dict()
    soil_list = load_soil_list()
    print(stiffness(194, para, pile_dict_all, soil_list))
