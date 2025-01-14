# -*- coding : utf-8 -*- #
# coding: utf-8
__author__ = 'ASUS'
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from os import walk
from datetime import datetime, timedelta
# import pandas.plotting as pdplt
# pdplt.register_matplotlib_converters()

# 构成x轴
date = []
start_s = datetime(2019, 5, 15)
date.append(start_s.strftime("%Y-%m-%d"))
for i in range(1, 187):
    start = start_s + timedelta(i)
    # print(start)
    date.append(start.strftime("%Y-%m-%d"))
# print(date)

# 构成y轴
dataframe_list = []
for f, _, i in walk("C:\\Users\\ASUS\\Desktop\\ThisSemester\\CXSJ\\CSV"):
    for j in i:
        dataframe_list.append(pd.read_csv(f + "\\" + j, encoding='gbk'))  # 读取文件
del_dl = dataframe_list[0:20]
# print(del_dl)
del dataframe_list[0:20]
dataframe_list.extend(del_dl)                                          # 理清顺序
# 重复值和缺失值的预处理
dl = []
for dataframe in dataframe_list:
    # print(dataframe)
    dataframe = dataframe[~dataframe['?标题'].isin(['标题'])]
    dl.append(dataframe)                                                # 删除重复无用值
for df in dl:
    df[['?标题', '优点']] = df[['?标题', '优点']].fillna('暂无')
# for df in dl:
#     df.dropna(axis=[0, 1], how='all')
    # axis 指轴，0是行，1是列
    # how 是删除条件：any 任意一个为na则删除整行/列,all 整行/列为na才删除
    # inplace 是否在原DataFrame 上进行删除，false为否                    # 删除缺失整行的值
# 判断归类
num = []


def get_average(l):  # 获取平均数
    s = 0
    for i in l:
        s += i
    return int(s / len(l))


for df in dl:
    # everyday[0]-学区房,everyday[1]-地铁房,everyday[2]-繁华地段,everyday[3]-景观房
    everyday = [0, 0, 0, 0]

    to_identify1 = ['?标题']
    to_identify2 = ['优点']
    school_residence1 = pd.DataFrame()
    school_residence2 = pd.DataFrame()
    subway_residence1 = pd.DataFrame()
    subway_residence2 = pd.DataFrame()
    downtown_residence1 = pd.DataFrame()
    downtown_residence2 = pd.DataFrame()
    landscape_residence1 = pd.DataFrame()
    landscape_residence2 = pd.DataFrame()
    for to_i in to_identify1:
        school_residence1 = school_residence1.append(df[df[to_i].str.contains('大学|学区|学校|校区')]).copy()
        subway_residence1 = subway_residence1.append(df[df[to_i].str.contains('地铁|号线|轻轨|站')]).copy()
        downtown_residence1 = downtown_residence1.append(df[df[to_i].str.contains('CBD|商业|繁华|配套成熟|中心|融杭|核心')]).copy()
        landscape_residence1= landscape_residence1.append(df[df[to_i].str.contains('江景房|洋房|环境优美|南北通透|远离马路|高品质')]).copy()
    for to_i in to_identify2:
        school_residence2 = school_residence2.append(df[df[to_i].str.contains('大学|学区|学校|校区')]).copy()
        subway_residence2 = subway_residence2.append(df[df[to_i].str.contains('地铁|号线|轻轨|站')]).copy()
        downtown_residence2 = downtown_residence2.append(df[df[to_i].str.contains('CBD|商业|繁华|配套成熟|中心|融杭|核心')]).copy()
        landscape_residence2= landscape_residence2.append(df[df[to_i].str.contains('江景房|洋房|环境优美|南北通透|远离马路|高品质')]).copy()
    school_residence = pd.concat([school_residence1,school_residence2], axis=0, ignore_index=True)
    subway_residence = pd.concat([subway_residence1,subway_residence2], axis=0, ignore_index=True)
    downtown_residence = pd.concat([downtown_residence1,downtown_residence2], axis=0, ignore_index=True)
    landscape_residence = pd.concat([landscape_residence1,landscape_residence2], axis=0, ignore_index=True)

    l1 = np.array(school_residence._series['均价'])
    l2 = np.array(subway_residence._series['均价'])
    l3 = np.array(downtown_residence._series['均价'])
    l4 = np.array(landscape_residence._series['均价'])
    list1 = []
    list2 = []
    list3 = []
    list4 = []

    # 学区房
    for a in l1:
        list1.append(re.findall(r'\d+(?=\D)', a))
    list1 = sum(list1,[])
    list1 = list(map(int, list1))
    # print(list1)
    # 地铁房
    for b in l2:
        list2.append(re.findall(r'\d+(?=\D)', b))
    list2 = sum(list2, [])
    list2 = list(map(int, list2))
    # 繁华地段
    for c in l3:
        list3.append(re.findall(r'\d+(?=\D)', c))
    list3 = sum(list3, [])
    list3 = list(map(int, list3))
    # 景观房
    for d in l4:
        list4.append(re.findall(r'\d+(?=\D)', d))
    list4 = sum(list4, [])
    list4 = list(map(int, list4))
    everyday[0] = get_average(list1)
    everyday[1] = get_average(list2)
    everyday[2] = get_average(list3)
    everyday[3] = get_average(list4)
    # print(everyday)
    num.append(everyday)
num = np.array(num)
# print(num)
XQ = num[:, 0].tolist()                           # 学区房
DT = num[:, 1].tolist()                           # 地铁房
FH = num[:, 2].tolist()                           # 繁华地段
JG = num[:, 3].tolist()                           # 景观房
# print(XQ)

# 绘图
plt.style.use('ggplot')  # 设置绘图风格
fig = plt.figure(figsize=(50, 40))  # 设置图框的大小
colors1 = '#6D6D6D'  # 标题颜色(灰色)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
# 绘制第一条折线图
plt.plot(date, XQ, color='#C42022', marker='o', markersize=5, label='学区房')
# 绘制第二条折线图
plt.plot(date, DT, color='#4191C0', marker='o', markersize=5, label='地铁房')
# 绘制第三条折线图
plt.plot(date, FH, color='#FFFF00', marker='o', markersize=5, label='繁华地段')
# 绘制第四条折线图
plt.plot(date, JG, color='#008000', marker='o', markersize=5, label='景观房')
# 设置标题及横纵坐标轴标题
plt.title('钱塘新区房价走势图', color=colors1, fontsize=24)
plt.xticks(date, rotation=90)
plt.xlabel('日期', fontsize=20)
plt.ylabel('房价(元)', fontsize=20)
plt.legend(loc='upper left', prop={'family': 'SimHei', 'size': 20})  # 显示图例
plt.savefig('trend_qtxq.png', bbox_inches='tight', dpi=300)
plt.show()
