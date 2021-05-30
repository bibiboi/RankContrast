#!/usr/bin/env python
# -*- coding:utf-8 -*-

from numpy import *
import copy
from matplotlib import pyplot as plt
from pandas import *

#-------想法错误：递归至初始节点才入栈导致遇到分岔路无法记录前一条路的完整路径
# OnePath = []
# def FindGlobalPath(i,j,path,OnePath):
#
#     if i == 0 and j == 0:
#         OnePath = []
#         OnePath.append((i,j))
#     else:
#         passed = False
#         for k in range(3):
#             if k == 0:
#                 if path[i][j][k] != 0:
#                     FindGlobalPath(i,j-1,path,OnePath)
#                     OnePath.append(i,j)
#                     passed = True
#             elif  k == 1:
#                 if path[i][j][k] != 0:
#                     if passed:
#                         OnePath.append(i,j)
#                         LastGlobalPath.append(OnePath)
#                         passed = False
#                     FindGlobalPath(i-1,j,path,OnePath)
#                     OnePath.append(i,j)
#                     passed = True
#             else:
#                 if path[i][j][k] != 0:
#                     if passed:
#                         OnePath.append(i,j)
#                         LastGlobalPath.append(OnePath)
#                         passed = False
#                     FindGlobalPath(i-1,j-1,path,OnePath)
#                     OnePath.append(i, j)
#                     passed = True

#创建全局比对得分矩阵
def GlobalScoreMatrix(m,n,w,replace,s,path,senquence1,senquence2,gap):
    for i in range(m):
        for j in range(n):
            #判断s（0,0）这一特殊情况
            if i == 0 and j == 0:
                s[i][j] = 0
            elif i-1 < 0:#判断第一行的特殊情况
                s[i][j] = s[i][j - 1] + gap
                path[i,j,0] = 1
            elif j-1 < 0:#判断第一列的特殊情况
                s[i][j] = s[i - 1][j] + gap
                path[i,j,1] = 1
            else:
                #获取最大值
                s[i][j] = max(s[i - 1][j - 1] + w[replace[senquence2[i - 1]]][replace[senquence1[j - 1]]],
                              s[i - 1][j] + gap, s[i][j - 1] + gap)
                #记录最大值来的方向
                if s[i - 1][j - 1] + w[replace[senquence2[i - 1]]][replace[senquence1[j - 1]]] == s[i][j]:
                    path[i,j,2] = 1
                if s[i - 1][j] + gap == s[i][j]:
                    path[i,j,1] = 1
                if s[i][j - 1] + gap == s[i][j]:
                    path[i,j,0] = 1

#创建局部比对得分矩阵
def LocalScoreMatrix(m,n,w,replace,s,path,senquence1,senquence2,gap):
    for i in range(1,m):
        #局部矩阵第一行及第一列均为0，不需要再初始化
        for j in range(1,n):
            #获取最大值,与全局比对不同之处在于选取最大值时将0加入选择
            s[i][j] = max(0,s[i - 1][j - 1] + w[replace[senquence2[i - 1]]][replace[senquence1[j - 1]]],
                          s[i - 1][j] + gap, s[i][j - 1] + gap)
            #记录最大值来的方向，若最大值为0则不必记录
            if s[i - 1][j - 1] + w[replace[senquence2[i - 1]]][replace[senquence1[j - 1]]] == s[i][j]:
                path[i,j,2] = 1
            if s[i - 1][j] + gap == s[i][j]:
                path[i,j,1] = 1
            if s[i][j - 1] + gap == s[i][j]:
                path[i,j,0] = 1

#寻找全局序列比对路径
def FindGlobalPath(i,j,path,OnePath,LastGlobalPath):
    #递归终止条件：回到原点（0，0）
    if i == 0 and j == 0:
        OnePath.append((i, j))
        #将OnePath进行深拷贝再加入至最终路径列表LastGlobalPath中
        # 涉及问题：list的赋值、浅拷贝、深拷贝
        LastGlobalPath.append(copy.deepcopy(OnePath))
        #将该点出栈
        OnePath.pop()
    else:
        for k in range(3):
            #判断每个点来的方向
            if path[i,j,k] == 1:
                #下标0处记录从左来的方向
                if k == 0:
                    #将该点入栈
                    OnePath.append((i,j))
                    #进行递归记录下一个点
                    FindGlobalPath(i,j - 1,path,OnePath,LastGlobalPath)
                    #递归返回后将该点出栈，记录另一方向
                    OnePath.pop()
                #下标1处记录从上来的方向
                elif k == 1:
                    OnePath.append((i, j))
                    FindGlobalPath(i - 1, j, path,OnePath,LastGlobalPath)
                    OnePath.pop()
                #下标2处记录从左上来的方向
                else:
                    OnePath.append((i, j))
                    FindGlobalPath(i - 1, j - 1, path,OnePath,LastGlobalPath)
                    OnePath.pop()

# 寻找局部序列比对路径
def FindLocalPath(i, j, path, OnePath, LastLocalPath):
    #递归终止条件：某个没有记录方向的点
    if all(path[i][j] == [0, 0, 0]):  # 涉及问题：列表比较 any() all()
        OnePath.append((i, j))
        # 将OnePath进行深拷贝再加入至最终路径列表LastLocalPath中
        LastLocalPath.append(copy.deepcopy(OnePath))
        # 将该点出栈
        OnePath.pop()
    else:
        for k in range(3):
            # 判断每个点来的方向
            if path[i, j, k] == 1:
                # 下标0处记录从左来的方向
                if k == 0:
                    # 将该点入栈
                    OnePath.append((i, j))
                    # 进行递归记录下一个点
                    FindLocalPath(i, j - 1, path, OnePath, LastLocalPath)
                    # 递归返回后将该点出栈，记录另一方向
                    OnePath.pop()
                # 下标1处记录从上来的方向
                elif k == 1:
                    OnePath.append((i, j))
                    FindLocalPath(i - 1, j, path, OnePath, LastLocalPath)
                    OnePath.pop()
                # 下标2处记录从左上来的方向
                else:
                    OnePath.append((i, j))
                    FindLocalPath(i - 1, j - 1, path, OnePath, LastLocalPath)
                    OnePath.pop()

#输出比对后的序列
def ShowContrastResult(LastPath,senquence1,senquence2):
    #依次输出每条路径
    for k,aPath in enumerate(LastPath):
        rowS = ''
        colS = ''
        #每条路径倒序遍历
        for i in range(len(aPath) -1,0,-1):
            #方向从左边来
            if aPath[i][0] == aPath[i - 1][0]:
                rowS += senquence1[aPath[i - 1][1] - 1]
                colS += '-'
            #方向从上面来
            elif aPath[i][1] == aPath[i - 1][1]:
                colS += senquence2[aPath[i - 1][0] -1]
                rowS += '-'
            #方向从左上来
            else:
                rowS += senquence1[aPath[i - 1][1] - 1]
                colS += senquence2[aPath[i - 1][0] - 1]
        #依次输出每条路的序列比对结果
        print("======比对结果",k+1,"======")
        print("序列1:",rowS)
        print("序列2:",colS)

# 判断是否为最终路径中的点
def judgePath(point, LastPath):
    for aPath in LastPath:
        if point in aPath:
            return True
    return False

# 画出路径图
def ShowPaths(senquence1, senquence2, LastPath):
    s1 = "0" + senquence1
    s2 = "0" + senquence2
    # 列索引
    col = list(s1)
    # 行索引
    row = list(s2)
    # 设置画布大小
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, frameon=True, xticks=[], yticks=[], )
    # 画出路径矩阵表格 涉及问题：表格与画布大小不一致 解决方式：bbox参数
    the_table = plt.table(cellText=s, rowLabels=row, colLabels=col, rowLoc='right',
                          loc='center', cellLoc='bottom right', bbox=[0, 0, 1, 1])
    # 设置表格文本字体大小
    the_table.set_fontsize(8)
    # 画出每个点的路径图
    for i in range(m):
        for j in range(n):
            for k in range(3):
                if path[i, j, k] == 1:  # 画出记录的方向
                    # 下标0处记录从左来的方向
                    if k == 0:
                        if judgePath((i, j), LastPath):  # 若某点在在最终路径中
                            # 画出红色箭头
                            plt.annotate('', xy=(j / n, (2 * m - 2 * i - 1) / (2 * (m + 1))),
                                         xytext=((2 * j + 1) / (2 * n), (2 * m - 2 * i - 1) / (2 * (m + 1))),
                                         arrowprops=dict(arrowstyle="->", color='r', connectionstyle="arc3"))
                        else:
                            # 未在最终路径中则画出黑色箭头
                            plt.annotate('', xy=(j / n, (2 * m - 2 * i - 1) / (2 * (m + 1))),
                                         xytext=((2 * j + 1) / (2 * n), (2 * m - 2 * i - 1) / (2 * (m + 1))),
                                         arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
                    # 下标1处记录从上来的方向
                    elif k == 1:
                        if judgePath((i, j), LastPath):
                            plt.annotate('', xy=((2 * j + 1) / (2 * n), (2 * m - 2 * i - 1) / (2 * (m + 1))),
                                         xytext=((2 * j + 1) / (2 * n), (m - i) / (m + 1)),
                                         arrowprops=dict(arrowstyle="<-", color='r', connectionstyle="arc3"))
                        else:
                            plt.annotate('', xy=((2 * j + 1) / (2 * n), (2 * m - 2 * i - 1) / (2 * (m + 1))),
                                         xytext=((2 * j + 1) / (2 * n), (m - i) / (m + 1)),
                                         arrowprops=dict(arrowstyle="<-", connectionstyle="arc3"))
                    # 下标1处记录从上来的方向
                    elif k == 2:
                        if judgePath((i, j), LastPath):
                            plt.annotate('', xy=((2 * j + 1) / (2 * n), (2 * m - 2 * i - 1) / (2 * (m + 1))),
                                         xytext=(j / n, (m - i) / (m + 1)),
                                         arrowprops=dict(arrowstyle="<-", color='r', connectionstyle="arc3"))
                        else:
                            plt.annotate('', xy=((2 * j + 1) / (2 * n), (2 * m - 2 * i - 1) / (2 * (m + 1))),
                                         xytext=(j / n, (m - i) / (m + 1)),
                                         arrowprops=dict(arrowstyle="<-", connectionstyle="arc3"))
    plt.show()


#将碱基转换为集合下标
replace = {'A':0,'G':1,'C':2,'T':3}
#构造替换计分矩阵
w = [[10,-1,-3,-4],[-1,7,-5,-3],[-3,-5,9,0],[-4,-3,0,8]]
#定义需要比对的序列
senquence1 = input("请输入序列1：").upper()
senquence2 = input("请输入序列2：").upper()
#定义输入的gap
gap = int(input("请输入gap："))
choise = int(input("请选择要进行的序列比对(1-全局序列比对  2-局部序列比对) : "))
# 获取序列的长度
m = len(senquence2) + 1
n = len(senquence1) + 1
#构建m*n全0矩阵
s = zeros((m,n))
#记录每个点的方向，下标0处存储从左来的方向，下标1处存储从上来的方向，下标2处存储从左上来的方向
#初始值均为0，若存在从某方向上来则将其对应下标的值置为1
path = zeros((m,n,3))
#记录每条路径
OnePath = []
#记录所有全局序列比对路径
LastGlobalPath = []
#记录所有局部序列比对路径
LastLocalPath = []

if choise == 1:#进行全局序列比对
    #构建得分矩阵
    GlobalScoreMatrix(m,n,w,replace,s,path,senquence1,senquence2,gap)
    #寻找比对路径
    FindGlobalPath(m-1,n-1,path,OnePath,LastGlobalPath)
    #输出比对结果
    ShowContrastResult(LastGlobalPath,senquence1,senquence2)
    #画出路径
    ShowPaths(senquence1, senquence2, LastGlobalPath)
elif choise == 2:#进行局部序列比对
    #构建得分矩阵
    LocalScoreMatrix(m, n, w, replace, s, path, senquence1, senquence2, gap)
    # 获取得分矩阵中最大值的行索引 涉及问题：获取where结果的索引值 涉及numpy中array的存储方式 待学
    row = where(s == np.max(s))[0]
    # 获取得分矩阵中最大值的列索引
    col = where(s == np.max(s))[1]
    for i in range(len(row)):#依次寻找不同局部比对的比对路径并输出比对结果
        FindLocalPath(row[i], col[i], path, OnePath, LastLocalPath)
        # 输出比对结果
        ShowContrastResult(LastLocalPath, senquence1, senquence2)
        # 画出路径
        ShowPaths(senquence1, senquence2, LastLocalPath)
else:
    print("无效选择！")

