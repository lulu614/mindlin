__author__ = 'lulu614'

from math import *

class Para(object):
    '''
        导入参数：
            empirical_coefficient = 经验系数
            alph = 桩端阻力比
            bata = 沿桩身均匀分布的桩侧摩阻力比
            sphere_influence = 群桩影响范围
            layer_thickness = 土层分层厚度
            depth = 桩顶深度
    '''

    def __init__(self,empirical_coefficient,alph,bata,sphere_influence,layer_thickness,depth):
        self.empirical_coefficient = empirical_coefficient
        self.alph = alph
        self.bata = bata
        self.sphere_influence = sphere_influence
        self.layer_thickness = layer_thickness
        self.depth = depth


class Pile_dict(object):
    '''
        桩字典：
            note = 备注
            pile_dict = {num:Pile_obj}
            字典 = {编号：桩对象}
    '''
    def __init__(self,note='empty',pile_dict=None):
        self.note = note
        if pile_dict == None:
            self.pile_dict = {}
        else:
            self.pile_dict = pile_dict

    def __str__(self):
        return '<备注:%s>' %self.note

    def __getitem__(self, key):
        return self.pile_dict.get(key)

    def __setitem__(self, key, value):
        self.pile_dict[key] = value

    def __delitem__(self, key):
        del self.pile_dict[key]

    def add(self,pile_obj):
        self[pile_obj.num] = pile_obj

class Pile(object):
    '''
        桩参数：
            mun = 节点号
            x = x坐标（mm）
            y = y坐标（mm）
            Q = 桩上所受集中力（KN）
            l = 桩长（m）
            d = 桩径（m）
            E = 压缩模量（MPa）
    '''

    def __init__(self,num,x,y,Q,l,d,E):
        self.num = num
        self.x = x
        self.y = y
        self.Q = Q
        self.l = l
        self.d = d
        self.E = E

    def __str__(self):
        return "<pile_num:%s>" % self.num

    def destance(self,obj):
        if self == obj:
            r = self.d/2
        else:
            r = sqrt((self.x-obj.x)**2 + (self.y-obj.y)**2)
        return r

    def choosen(self,pile_dict,sphere_influence):
        choosen_pile_dict = {}
        for pile in pile_dict.pile_dict.values():
            if self.destance(pile) < sphere_influence:
                choosen_pile_dict[pile.num] = pile
        return choosen_pile_dict


class Soil_list(object):
    '''
        土层列表：
        note = 备注
        soil_list = [Soil_obj]
        土层列表 = [土层对象]
    '''
    def __init__(self,note='empty',soil_list=None):
        self.note = note
        if soil_list == None:
            self.soil_list = []
        else:
            self.soil_list = soil_list

    def add(self,soil_obj):
        self.soil_list.append(soil_obj)

    def copy(self):
        soil_list_copied = Soil_list()
        for soil in self.soil_list:
            soil_list_copied.add(Soil(soil.num,soil.name,soil.h,soil.Es,soil.v))
        return soil_list_copied

    '''
        去除桩底以上部分
    '''
    def del_pile(self,length):
        temp = self.soil_list.copy()
        for i in temp:
            length -= i.h
            if length >= 0:
                self.soil_list.remove(i)
            else:
                self.soil_list[0].h -= length
                break

class Soil(object):
    '''
        土层参数：
            num = 层序
            name = 岩土名称
            h = 厚度（m）
            Es = 土层压缩模量（MPa）
            v = 泊松比
    '''
    def __init__(self,num,name,h,Es,v):
        self.num = num
        self.name = name
        self.h = h
        self.Es = Es
        self.v = v

    def __str__(self):
        return "<soil_num:%s,soil_name:%s>" % (self.num,self.name)

    '''
        建立h_list ——分层列表
    '''
    def divide(self,layer_thickness):
        h = self.h
        if isinstance(h / layer_thickness, int):
            soil_list_i_size = h // layer_thickness  # 分层数
            h_list = soil_list_i_size * [layer_thickness]
        else:
            soil_list_i_size = int(h // layer_thickness + 1)
            h_last = h - (layer_thickness * soil_list_i_size - 1)  # 最后一层厚度
            h_list = soil_list_i_size * [layer_thickness] + [h_last]
        return h_list
