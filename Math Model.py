import math
import collections
import numpy as np
import pandas as pd
from functools import reduce
import os, csv, sys, time, random
from pandas import Series, DataFrame


def Local_time(Unix_time):  # 将Unix时间转换成北京时间
    beijing_local = time.localtime(Unix_time)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", beijing_local)
    return dt


def Area(lng, lat):  # lat已知纬度，lng已知经度
    r = float(6371)  # 地球半径千米
    dis = float(0.2)  # km距离
    dlng = float(2 * math.asin(math.sin(dis / (2 * r)) / math.cos(lat * math.pi / 180)))
    dlng = dlng * 180 / math.pi  # 角度转为弧度
    dlat = float(dis / r)
    dlat = dlat * 180 / math.pi
    left = lng - dlng
    right = lng + dlng
    top = lat + dlat
    bottom = lat - dlat
    return left, right, top, bottom  # 东南西北四个方向的范围


def lower_bound(nums, target):  #返回nums中第一个>=target的值得位置，如果nums中都比target小，则返回len(nums)
    low, high = 0, len(nums) - 1
    pos = len(nums)
    while low < high:
        mid = (low + high) // 2
        if nums[mid] < target:
            low = mid + 1
        else:
            high = mid
    if nums[low] >= target:
        pos = low
    return pos


def upper_bound(nums, target):  #返回nums中第一个>target的值得位置，如果nums中都不比target大，则返回len(nums)
    low, high = 0, len(nums) - 1
    pos = len(nums)
    while low < high:
        mid = (low + high) // 2
        if nums[mid] <= target:
            low = mid + 1
        else:
            high = mid
            pos = high
    if nums[low] > target:
        pos = low
    return pos

time_index = []  #时间索引列表
loc_index = []  #地点索引列表

#读入FanzimsiRecord第二列，返回时间索引列表time_index
pwdl = pd.read_csv('FanzimsiRecord.csv', sep=',', names=['key1', 'key2', 'key3', 'key4', 'key5'])
test1 = list(pwdl.key2)
for index in test1:
    time_index.append(int(index))
#删除
del pwdl
del test1[:]
del test1

#读入FanzfaceRecord第二列，返回时间索引列表loc_index
pwdl = pd.read_csv('xiaoheshang.csv', sep=',', names=['key1'])
test2 = list(pwdl.key1)
for index in test2:
    loc_index.append(int(index))
#删除
del pwdl
del test2[:]
del test2

print("阶段1完成！")

poj = 1
flag = []
count = []
face_find = []
ans_imsi = []
printcsv = []
soul = []

with open('fanzimsiRecord.csv', 'r') as u:
    reader2 = list(csv.reader(u))
    print("阶段2完成！")

with open('huanjie.csv', 'r') as f:  #记录选择的faceID的全部信息
    reader1 = list(csv.reader(f))
    print("阶段3完成！")

with open('testfaceids.csv', 'r') as p:  #记录选择的faceID的全部信息
    reader3 = list(csv.reader(p))
    print("阶段4完成！")

with open('testfaceids.csv', 'r') as l:  #记录选择的faceID的全部信息
    cunzai = list(csv.reader(l))
    print("阶段5完成！")


for num in range(1, len(reader3)):
    face_find.clear()
    ans_imsi.clear()

    test_id = reader3[num][1]

    start_face = lower_bound(loc_index, int(test_id))
    end_face = lower_bound(loc_index, int(test_id) + 1)
    for i in range(start_face, end_face):
        face_find.append(reader1[i])

    for i in range(len(face_find)):
        ans_imsi.append([])

    flag = 0

    for i in range(len(face_find)):
        flag = face_find[i][1]
        start_time = int(face_find[i][1]) - 128
        end_time = int(face_find[i][1]) + 85
        start_index = lower_bound(time_index, start_time)
        end_index = lower_bound(time_index, end_time)
        #print("第" + str(i + 1) + "组的时间索引是：", start_index, end_index)
        if (end_index != 24402954):
            for j in range(start_index, end_index + 1):
                if (face_find[i][2] == reader2[j][2]):
                    if (reader2[j][0] not in ans_imsi[i]):
                        if(len(face_find) != 1):
                            ans_imsi[i].append(reader2[j][0])
                        else:
                            if (reader2[j][0] not in cunzai):
                                ans_imsi[i].append(reader2[j][0])
        else:
            for j in range(start_index, 24402954):
                if (face_find[i][2] == reader2[j][2]):
                    if (reader2[j][0] not in ans_imsi[i]):
                        if (len(face_find) != 1):
                            ans_imsi[i].append(reader2[j][0])
                        else:
                            if (reader2[j][0] not in cunzai):
                                ans_imsi[i].append(reader2[j][0])

    mg = 0
    fpx = reduce(lambda x, y: x.extend(y) or x, ans_imsi)
    pp = collections.Counter(fpx)

    if (len(pp.keys()) != len(fpx)):
        for t in pp.keys():
            if (pp[t] == max(pp.values())):
                mg = t
                break
    else:
        result = sorted(fpx)
        mg = result[0]


    print(poj, test_id, mg)
    printcsv.append(mg)
    poj += 1

print("阶段6完成！")

with open('benbenjiejie.csv', 'w', newline='') as n:
    www= []
    writer = csv.writer(n)
    headline = ['NO', 'IMSIID']
    writer.writerow(headline)
    for i in range(len(printcsv)):
        www.append(i + 1)
        www.append(printcsv[i])
        writer.writerow(www)
        www.clear()
    n.close()