from 坐标转换算法.run import Solution
import time
import random
import math
from math import *
import copy
from PIL import Image
from tqdm import tqdm
import json


def time_wrapper(fun):
    def inner(*args, **kwargs):
        start = time.time()
        fun(*args, **kwargs)
        print(f'{fun.__name__}: {time.time() - start}')

    return inner


def real_count(fun):
    def inner(*args, **kwargs):
        fun(*args, **kwargs)
        with open('txt', mode='a', encoding='utf-8') as f:
            f.write(f'{fun.__name__}\n')

    return inner


class Sphere_V:
    def __init__(self, n, seed):
        self.n = n
        self.seed = seed
        self.size = 2 ** n + 1
        self.R = 6371  # 地球半径 6371km
        self.s = Solution(self.n, self.seed)  # 调用run文件中的Solution类
        self.table = [[0] * (self.size - 1) for _ in range(self.size - 1)]  # 二维数组
        self.color = self.colors()  # 种子点颜色生成
        self.test_co = self.test_colors()
        self.pane_colors = self.pane_color()
        self.counts = 0  # 总的格网数目
        self.visited = [[False] * (self.size - 1) for _ in range(self.size - 1)]  # 访问数组
        self.coordinate_table = self.coordinate_table()  # 其中坐标为四坐标中心
        self.seed_list = self.creat_seed()
        self.deal()

    def pane_color(self):
        res = [[0, 0, 0]]  # 第一个颜色是种子点的颜色
        for _ in range(self.seed):
            res.append([random.randrange(99, 198) for _ in range(3)])
        return res

    @classmethod
    def degree_to_pi(cls, degree):
        return (degree / 180) * math.pi

    def arc_distance(self, coord1, coord2):
        # coordinate 为经纬度坐标 根据公式得出地球表面的大弧距离, coordinate[0]:经度； coordinate[1]纬度；
        coord1 = [self.degree_to_pi(coord1[0]), self.degree_to_pi(coord1[1])]
        coord2 = [self.degree_to_pi(coord2[0]), self.degree_to_pi(coord2[1])]
        return self.R * acos(
            self.degree_to_pi(
                cos(coord1[1]) * cos(coord2[1]) * cos(coord1[0] - coord2[0]) + sin(coord1[1]) * sin(coord2[1])))

    def attribution(self, coord):
        # 参数为经纬度坐标
        dic = float('inf')
        res = []
        for i in range(self.seed):
            tmp = self.arc_distance(coord, self.seed_list[i])
            if tmp < dic:
                res.append(i)
                dic = tmp
        return res[-1] + 1

    def deal(self):
        # top deal
        for j in range(self.size - 1):
            self.counts += 1
            self.table[0][j] = self.attribution(self.s.get_la([0, j]))
            self.visited[0][j] = True
        # bottom deal
        for j in range(self.size - 1):
            self.counts += 1
            self.table[self.size - 2][j] = self.attribution(self.s.get_la([self.size - 2, j]))
            self.visited[self.size - 2][j] = True
        # left deal
        for i in range(self.size - 1):
            self.counts += 1
            self.table[i][0] = self.attribution(self.s.get_la([i, 0]))
            self.visited[i][0] = True
        # right deal
        for i in range(self.size - 1):
            self.counts += 1
            self.table[i][self.size - 2] = self.attribution(self.s.get_la([i, self.size - 2]))
            self.visited[i][self.size - 2] = True

    def positive_search(self):
        copy_table = copy.deepcopy(self.table)
        for i in range(1, self.size - 2):
            for j in range(1, self.size - 2):
                if self.s.get_la([i, j]) not in self.seed_list:
                    if copy_table[i][j - 1] == copy_table[i - 1][j - 1] == copy_table[i - 1][j] == copy_table[i - 1][
                        j + 1]:
                        copy_table[i][j] = copy_table[i][j - 1]
                    else:
                        self.visited[i][j] = True
                        self.counts += 1
                        copy_table[i][j] = self.attribution(self.get_center_coord([i, j]))
        return copy_table

    def positive_reverse(self):
        # 正向扫描
        copy_table = self.positive_search()
        # 逆向纠错
        for i in range(self.size - 3, 0, -1):
            for j in range(self.size - 3, 0, -1):
                if self.s.get_la([i, j]) not in self.seed_list:
                    if copy_table[i][j - 1] == copy_table[i - 1][j - 1] == copy_table[i - 1][j] == copy_table[i - 1][
                        j + 1] == copy_table[i][j + 1] == copy_table[i + 1][j + 1] == copy_table[i + 1][j] == \
                            copy_table[i + 1][j - 1]:
                        pass
                    else:
                        if not self.visited[i][j]:
                            copy_table[i][j] = self.attribution(self.get_center_coord([i, j]))
                            self.visited[i][j] = True
                            self.counts += 1
        return copy_table

    def attribution_algorithm(self):
        copy_table = copy.deepcopy(self.table)
        for i in range(1, self.size - 2):
            for j in range(1, self.size - 2):
                if self.s.get_la([i, j]) not in self.seed_list:
                    copy_table[i][j] = self.attribution(self.s.get_la([i, j]))
        return copy_table

    def coordinate_table(self):
        res = [[[]] * (self.size - 1) for _ in range(self.size - 1)]
        for i in range(self.size - 1):
            for j in range(self.size - 1):
                res[i][j] = self.get_center_coord([i, j])
        return res

    def colors(self):
        res = ['0, 0, 0']  # 第一个颜色是种子点的颜色
        for _ in range(self.seed):
            res.append(','.join([str(random.randrange(100, 200)) for _ in range(3)]))
        return res

    def test_colors(self):
        res = [[0, 0, 0]]  # 第一个颜色是种子点的颜色
        for _ in range(self.seed):
            res.append([random.randrange(0, 255) for _ in range(3)])
        return res

    def creat_seed(self):
        res = []
        for _ in range(self.seed):
            res.append(self.get_center_coord([random.randrange(self.size - 1), random.randrange(self.size - 1)]))
        return res

    def coord_trans(self, coord):
        return [coord[0] - self.size // 2, coord[1] - self.size // 2]

    def get_center_coord(self, coord):
        """
        coord: 坐标漂移前的原始索引坐标
        """
        left_top = self.s.get_la_long(self.coord_trans(coord))
        right_top = self.s.get_la_long(self.coord_trans([coord[0], coord[1] + 1]))
        left_bottom = self.s.get_la_long(self.coord_trans([coord[0] + 1, coord[1]]))
        right_bottom = self.s.get_la_long(self.coord_trans([coord[0] + 1, coord[1] + 1]))

        center_long, center_lat = 0, 0  # 提前定义

        if (left_top[0] >= 0 and right_top[0] >= 0 and left_bottom[0] >= 0 and right_bottom[0] >= 0) or (
                left_top[0] < 0 and right_top[0] < 0 and left_bottom[0] < 0 and right_bottom[0] < 0):
            center_long = (left_top[0] + right_top[0] + left_bottom[0] + right_bottom[0]) / 4  # 经度
        else:
            if abs(abs(left_top[0]) - 180) < abs(left_top[0]):
                tmp = (left_top[0] + right_top[0] + left_bottom[0] + right_bottom[0]) / 4
                if tmp <= 0:
                    center_long = 180.0 + tmp
                else:
                    center_long = -180.0 + tmp
            else:
                center_long = (left_top[0] + right_top[0] + left_bottom[0] + right_bottom[0]) / 4

        center_lat = (left_top[1] + right_top[1] + left_bottom[1] + right_bottom[1]) / 4  # 纬度
        return [center_long, center_lat]

    def final(self):
        color = self.positive_reverse()
        # res = [[[]] * (self.size - 1) for _ in range(self.size - 1)]
        res = []
        for i in range(self.size - 1):
            for j in range(self.size - 1):
                left_top = self.s.get_la_long(self.coord_trans([i, j]))
                right_top = self.s.get_la_long(self.coord_trans([i, j + 1]))
                left_bottom = self.s.get_la_long(self.coord_trans([i + 1, j]))
                right_bottom = self.s.get_la_long(self.coord_trans([i + 1, j + 1]))
                res.append([left_top + right_top + right_bottom + left_bottom, self.color[color[i][j]]])
        return res

    def positive_final(self):
        color = self.positive_search()
        # res = [[[]] * (self.size - 1) for _ in range(self.size - 1)]
        res = []
        for i in range(self.size - 1):
            for j in range(self.size - 1):
                left_top = self.s.get_la_long(self.coord_trans([i, j]))
                right_top = self.s.get_la_long(self.coord_trans([i, j + 1]))
                left_bottom = self.s.get_la_long(self.coord_trans([i + 1, j]))
                right_bottom = self.s.get_la_long(self.coord_trans([i + 1, j + 1]))
                res.append([left_top + right_top + right_bottom + left_bottom, self.color[color[i][j]]])
        return res

    def visited_final(self):
        res = []
        for i in range(self.size - 1):
            for j in range(self.size - 1):
                left_top = self.s.get_la_long(self.coord_trans([i, j]))
                right_top = self.s.get_la_long(self.coord_trans([i, j + 1]))
                left_bottom = self.s.get_la_long(self.coord_trans([i + 1, j]))
                right_bottom = self.s.get_la_long(self.coord_trans([i + 1, j + 1]))
                if self.visited[i][j]:
                    res.append([left_top + right_top + right_bottom + left_bottom, '255, 0, 0'])
                else:
                    res.append([left_top + right_top + right_bottom + left_bottom, '255, 255, 255'])
        return res

    @classmethod
    def paint(cls, data, name, colors):
        image = Image.new('RGB', (len(data), len(data[0])))
        put_pixel = image.putpixel
        for i in tqdm(range(len(data))):
            for j in range(len(data[0])):
                color = colors[data[i][j]]
                put_pixel((i, j), (color[0], color[1], color[2]))
        image.save(f'img/{name}.jpg')

    @classmethod
    def paint_check(cls, data1, data2, colors, name='错误'):
        image = Image.new('RGB', (len(data1), len(data1[0])))
        put_pixel = image.putpixel
        for i in tqdm(range(len(data1))):
            for j in range(len(data1[0])):
                if data1[i][j] == data2[i][j]:
                    color = colors[data1[i][j]]
                else:
                    color = [255, 0, 0]
                put_pixel((i, j), (color[0], color[1], color[2]))
        image.save(f'img/{name}.jpg')

    @classmethod
    def paint_visited(cls, data, name):
        image = Image.new('RGB', (len(data), len(data[0])))
        put_pixel = image.putpixel
        for i in tqdm(range(len(data))):
            for j in range(len(data[0])):
                if data[i][j]:
                    put_pixel((i, j), (255, 0, 0))
                else:
                    put_pixel((i, j), (255, 255, 255))
        image.save(f'img/{name}.jpg')


if __name__ == '__main__':
    v = Sphere_V(7, 5)
    # cesium展示
    data_ = json.dumps(v.final())
    with open('../htmls/8-5.json', mode='w', encoding='utf-8') as f:
        f.write(data_)
