# -*- coding:utf-8 -*-
#author:jeremy

import networkx as nx
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import collections
from pandas import Series
import math
import os
from matplotlib.pyplot import MultipleLocator
import threading
from utils import create_dir
from config import Config
import json
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

def draw(jiedian_split_time_work,jiedian_split_time_nonwork):
    '''
    画非营运车辆的出行车数（分不同时）、状态（分不同时）
    :param jiedian_split_time_work:
    :param jiedian_split_time_nonwork:
    :return:
    '''

    create_dir('./picture')
    create_dir('./picture' + '/' + 'ronghe')
    create_dir('./picture' + '/' + 'ronghe' + '/' + 'splitBytime')

    draw_cheshu_time([1205],
                       [['-', 'dodgerblue'], ['-', 'darkorange']],
                       '1205_cheshu_time',jiedian_split_time_work,jiedian_split_time_nonwork,200000)

    draw_cheshu_time([1206],
                     [['-', 'dodgerblue'], ['-', 'darkorange']],
                     '1206_cheshu_time', jiedian_split_time_work, jiedian_split_time_nonwork, 200000)

    draw_cheshu_time([1207],
                     [['-', 'dodgerblue'], ['-', 'darkorange']],
                     '1207_cheshu_time', jiedian_split_time_work, jiedian_split_time_nonwork, 200000)

    draw_cheshu_time([1208],
                     [['-', 'dodgerblue'], ['-', 'darkorange']],
                     '1208_cheshu_time', jiedian_split_time_work, jiedian_split_time_nonwork, 200000)

    draw_cheshu_time([1209],
                     [['-', 'dodgerblue'], ['-', 'darkorange']],
                     '1209_cheshu_time', jiedian_split_time_work, jiedian_split_time_nonwork, 200000)

    draw_cheshu_time([1210],
                [['--', 'dodgerblue'], ['--', 'darkorange']],
                '1210_cheshu_time',jiedian_split_time_work,jiedian_split_time_nonwork,200000)

    draw_cheshu_time([1211],
                     [['-', 'dodgerblue'], ['-', 'darkorange']],
                     '1211_cheshu_time', jiedian_split_time_work, jiedian_split_time_nonwork, 200000)


    draw_cheshu_time_zaike_kongshi([1205],
                       [['-', 'dodgerblue'], ['-', 'darkorange']],
                       '1205_cheshu_time_zaike_kongshi',jiedian_split_time_work,jiedian_split_time_nonwork,200000)

    draw_cheshu_time_zaike_kongshi([1206],
                     [['-', 'dodgerblue'], ['-', 'darkorange']],
                     '1206_cheshu_time_zaike_kongshi', jiedian_split_time_work, jiedian_split_time_nonwork, 200000)

    draw_cheshu_time_zaike_kongshi([1207],
                     [['-', 'dodgerblue'], ['-', 'darkorange']],
                     '1207_cheshu_time_zaike_kongshi', jiedian_split_time_work, jiedian_split_time_nonwork, 200000)

    draw_cheshu_time_zaike_kongshi([1208],
                     [['-', 'dodgerblue'], ['-', 'darkorange']],
                     '1208_cheshu_time_zaike_kongshi', jiedian_split_time_work, jiedian_split_time_nonwork, 200000)

    draw_cheshu_time_zaike_kongshi([1209],
                     [['-', 'dodgerblue'], ['-', 'darkorange']],
                     '1209_cheshu_time_zaike_kongshi', jiedian_split_time_work, jiedian_split_time_nonwork, 200000)

    draw_cheshu_time_zaike_kongshi([1210],
                [['--', 'dodgerblue'], ['--', 'darkorange']],
                '1210_cheshu_time_zaike_kongshi',jiedian_split_time_work,jiedian_split_time_nonwork,200000)

    draw_cheshu_time_zaike_kongshi([1211],
                     [['-', 'dodgerblue'], ['-', 'darkorange']],
                     '1211_cheshu_time_zaike_kongshi', jiedian_split_time_work, jiedian_split_time_nonwork, 200000)




    draw_zhuangtai_time(1205,
                  '1205_zhuangtai_time',jiedian_split_time_work,jiedian_split_time_nonwork,150000)

    draw_zhuangtai_time(1206,
                  '1206_zhuangtai_time',jiedian_split_time_work,jiedian_split_time_nonwork,150000)

    draw_zhuangtai_time(1207,
                  '1207_zhuangtai_time',jiedian_split_time_work,jiedian_split_time_nonwork,150000)

    draw_zhuangtai_time(1208,
                  '1208_zhuangtai_time',jiedian_split_time_work,jiedian_split_time_nonwork,150000)

    draw_zhuangtai_time(1209,
                  '1209_zhuangtai_time',jiedian_split_time_work,jiedian_split_time_nonwork,150000)

    draw_zhuangtai_time(1210,
                   '1210_zhuangtai_time',jiedian_split_time_work,jiedian_split_time_nonwork,150000)

    draw_zhuangtai_time(1211,
                  '1211_zhuangtai_time',jiedian_split_time_work,jiedian_split_time_nonwork,150000)

    # draw_kongzhi_time([1205],
    #              [['-', 'dodgerblue'], ['-', 'darkorange']],
    #              '1205_kongzhi',jiedian_split_time_work,jiedian_split_time_nonwork,1)
    #
    # draw_kongzhi_time([1210],
    #              [['--', 'dodgerblue'], ['--', 'darkorange']],
    #              '1210_kongzhi',jiedian_split_time_work,jiedian_split_time_nonwork,1)

def draw_cheshu_time(dates,linestyle_color_list,save_path,jiedian_split_time_work,jiedian_split_time_nonwork,ylimit):
    '''
    按小时分布的优化前出行车数和优化后出行车数（分时，优化使用不同时间阈值）
    :param dates:
    :param linestyle_color_list:
    :param save_path:
    :param jiedian_split_time_work:
    :param jiedian_split_time_nonwork:
    :param ylimit:
    :return:
    '''
    fig = plt.figure(figsize=(18, 12), dpi=1000)
    for date_index in range(len(dates)):
        if '10' in str(dates[date_index]) or '11' in str(dates[date_index]):
            x = np.array(list(range(24))) + [0.5] * 24
            y = np.array([0] * len(x))
            x1 = np.array(list(range(24))) + [0.5] * 24
            y1 = np.array([0] * len(x))
            for t in range(len(jiedian_split_time_nonwork) - 1):
                feiyunyingche_jiedian = pd.read_csv(open('./data/节点/'+ str(dates[date_index]) + '_jiedian_'+str(jiedian_split_time_nonwork[t])+'_'+str(jiedian_split_time_nonwork[t+1])+'.csv'))
                feiyunyingche_jiedian['start_time'] = (feiyunyingche_jiedian['start_time'] // 3600).astype(int)
                feiyunyingche_jiedian['end_time'] = (feiyunyingche_jiedian['end_time'] // 3600).astype(int)

                paths = []
                filePathList = os.listdir('./data/PathList/' + 'ronghe' + '/splitBytime/' + str(dates[date_index]))
                for allDir in filePathList:
                    if '_'+str(jiedian_split_time_nonwork[t])+'_'+str(jiedian_split_time_nonwork[t+1])+'_'  in allDir:
                        child = os.path.join('%s/%s' % ('./data/PathList/' + 'ronghe' + '/splitBytime/' + str(dates[date_index]), allDir))
                        numpy_path = np.load(child, allow_pickle=True)
                        paths.append(numpy_path)

                endtime_ord = -1
                starttime_ord = -1
                for i in range(len(feiyunyingche_jiedian.columns)):
                    if feiyunyingche_jiedian.columns[i] == 'end_time':
                        endtime_ord = i
                    if feiyunyingche_jiedian.columns[i] == 'start_time':
                        starttime_ord = i

                for part in paths:
                    for i in part:
                        y[feiyunyingche_jiedian.iloc[i[0], starttime_ord]:feiyunyingche_jiedian.iloc[i[-1], endtime_ord] + 1] = y[feiyunyingche_jiedian.iloc[i[0], starttime_ord]:feiyunyingche_jiedian.iloc[i[-1], endtime_ord] + 1] + 1

                for i in range(len(feiyunyingche_jiedian)):
                    y1[feiyunyingche_jiedian.iloc[i, starttime_ord]:feiyunyingche_jiedian.iloc[i, endtime_ord] + 1] = y1[feiyunyingche_jiedian.iloc[i, starttime_ord]:feiyunyingche_jiedian.iloc[i, endtime_ord] + 1] + 1

            plt.plot(  # 画折线图y
                x, y, label='Minimized vehicle number' + '(' + str(dates[date_index]) + ')',
                lw=5,  # 折线图的线条宽度
                linestyle=linestyle_color_list[date_index * len(dates)][0],
                color=linestyle_color_list[date_index * len(dates)][1],
                marker='o',
                markerfacecolor='k'
            )

            plt.plot(  # 画折线图y
                x1, y1, label='Current on-road vehicle number' + '(' + str(dates[date_index]) + ')',
                lw=5,  # 折线图的线条宽度
                linestyle=linestyle_color_list[date_index * len(dates) + 1][0],
                color=linestyle_color_list[date_index * len(dates) + 1][1],
                marker='o',
                markerfacecolor='k'
            )
        else:
            x = np.array(list(range(24))) + [0.5] * 24
            y = np.array([0] * len(x))
            x1 = np.array(list(range(24))) + [0.5] * 24
            y1 = np.array([0] * len(x))
            for t in range(len(jiedian_split_time_work) - 1):
                feiyunyingche_jiedian = pd.read_csv(open('./data/节点/'+ str(dates[date_index]) + '_jiedian_'+str(jiedian_split_time_work[t])+'_'+str(jiedian_split_time_work[t+1])+'.csv'))
                feiyunyingche_jiedian['start_time'] = (feiyunyingche_jiedian['start_time'] // 3600).astype(int)
                feiyunyingche_jiedian['end_time'] = (feiyunyingche_jiedian['end_time'] // 3600).astype(int)

                paths = []
                filePathList = os.listdir('./data/PathList/' + 'ronghe' + '/splitBytime/' + str(dates[date_index]))
                for allDir in filePathList:
                    if '_'+str(jiedian_split_time_work[t])+'_'+str(jiedian_split_time_work[t+1])+'_' in allDir:
                        child = os.path.join('%s/%s' % ('./data/PathList/' + 'ronghe' + '/splitBytime/' + str(dates[date_index]), allDir))
                        numpy_path = np.load(child, allow_pickle=True)
                        paths.append(numpy_path)

                endtime_ord = -1
                starttime_ord = -1
                for i in range(len(feiyunyingche_jiedian.columns)):
                    if feiyunyingche_jiedian.columns[i] == 'end_time':
                        endtime_ord = i
                    if feiyunyingche_jiedian.columns[i] == 'start_time':
                        starttime_ord = i

                for part in paths:
                    for i in part:
                        y[feiyunyingche_jiedian.iloc[i[0], starttime_ord]:feiyunyingche_jiedian.iloc[i[-1], endtime_ord] + 1] = y[feiyunyingche_jiedian.iloc[i[0], starttime_ord]:feiyunyingche_jiedian.iloc[i[-1], endtime_ord] + 1] + 1

                for i in range(len(feiyunyingche_jiedian)):
                    y1[feiyunyingche_jiedian.iloc[i, starttime_ord]:feiyunyingche_jiedian.iloc[i, endtime_ord] + 1] = y1[feiyunyingche_jiedian.iloc[i, starttime_ord]:feiyunyingche_jiedian.iloc[i, endtime_ord] + 1] + 1

            plt.plot(  # 画折线图y
                x, y, label='Minimized vehicle number' + '(' + str(dates[date_index]) + ')',
                lw=5,  # 折线图的线条宽度
                linestyle=linestyle_color_list[date_index * len(dates)][0],
                color=linestyle_color_list[date_index * len(dates)][1],
                marker='o',
                markerfacecolor='k'
            )

            plt.plot(  # 画折线图y
                x1, y1, label='Current on-road vehicle number' + '(' + str(dates[date_index]) + ')',
                lw=5,  # 折线图的线条宽度
                linestyle=linestyle_color_list[date_index * len(dates) + 1][0],
                color=linestyle_color_list[date_index * len(dates) + 1][1],
                marker='o',
                markerfacecolor='k'
            )

    plt.xticks(fontsize=28)  # 数量多可以采用270度，数量少可以采用340度，得到更好的视图
    plt.yticks(fontsize=28)
    plt.xlabel('Time of a day', fontsize=35)
    # plt.ylabel('车量数',fontsize=35)
    plt.xlim(0, 24, 1)
    plt.ylim(0, ylimit)
    x_major_locator = MultipleLocator(1)
    # 把x轴的刻度间隔设置为1，并存在变量里
    ax = plt.gca()
    # ax为两条坐标轴的实例
    ax.xaxis.set_major_locator(x_major_locator)
    plt.legend(fontsize=30, bbox_to_anchor=(1.2, -0.1), ncol=1)
    plt.subplots_adjust(bottom=0.2)
    # plt.title('非工作日车辆时间分布',fontsize=38)
    plt.savefig('./picture/' + 'ronghe' + '/splitBytime/' + save_path)
    plt.close()

def draw_cheshu_time_zaike_kongshi(dates,linestyle_color_list,save_path,jiedian_split_time_work,jiedian_split_time_nonwork,ylimit):
    fig = plt.figure(figsize=(18, 12), dpi=1000)
    df_kakou_time = pd.read_csv(open('./data/kakou_time.csv'), dtype={'origin_kid': str, 'des_kid': str})

    for date_index in range(len(dates)):
        if '10' in str(dates[date_index]) or '11' in str(dates[date_index]):
            x = np.array(list(range(24))) + [0.5] * 24
            y = np.array([0] * len(x))
            x1 = np.array(list(range(24))) + [0.5] * 24
            y1 = np.array([0] * len(x))
            for t in range(len(jiedian_split_time_nonwork) - 1):
                feiyunyingche_jiedian = pd.read_csv(open('./data/节点/'+ str(dates[date_index]) + '_jiedian_'+str(jiedian_split_time_nonwork[t])+'_'+str(jiedian_split_time_nonwork[t+1])+'.csv'))

                paths = []
                filePathList = os.listdir('./data/PathList/' + 'ronghe' + '/splitBytime/' + str(dates[date_index]))
                for allDir in filePathList:
                    if '_'+str(jiedian_split_time_nonwork[t])+'_'+str(jiedian_split_time_nonwork[t+1])+'_'  in allDir:
                        child = os.path.join('%s/%s' % ('./data/PathList/' + 'ronghe' + '/splitBytime/' + str(dates[date_index]), allDir))
                        numpy_path = np.load(child, allow_pickle=True)
                        paths.append(numpy_path)

                endtime_ord = -1
                starttime_ord = -1
                end_kid_ord = -1
                start_kid_ord = -1
                for i in range(len(feiyunyingche_jiedian.columns)):
                    if feiyunyingche_jiedian.columns[i] == 'end_time':
                        endtime_ord = i
                    if feiyunyingche_jiedian.columns[i] == 'start_time':
                        starttime_ord = i
                    if feiyunyingche_jiedian.columns[i] == 'end_kid':
                        end_kid_ord = i
                    if feiyunyingche_jiedian.columns[i] == 'start_kid':
                        start_kid_ord = i

                for part in paths:
                    for i in part:
                        for j in range(len(i) - 1):
                            a = feiyunyingche_jiedian.iloc[i[j], starttime_ord]
                            c = feiyunyingche_jiedian.iloc[i[j], endtime_ord]
                            b = df_kakou_time[
                                (df_kakou_time['origin_kid'] == feiyunyingche_jiedian.iloc[i[j], end_kid_ord]) & (
                                        df_kakou_time['des_kid'] == feiyunyingche_jiedian.iloc[
                                    i[j + 1], start_kid_ord])].iloc[0]['time']
                            if (c + b) // 3600 == (feiyunyingche_jiedian.iloc[i[j + 1], starttime_ord]) // 3600:
                                y[a // 3600:(c + b) // 3600] = y[a // 3600:(c + b) // 3600] + 1
                            else:
                                y[a // 3600:(c + b) // 3600 + 1] = y[a // 3600:(c + b) // 3600 + 1] + 1
                        y[(feiyunyingche_jiedian.iloc[i[-1], starttime_ord]) // 3600:(feiyunyingche_jiedian.iloc[
                            i[-1], endtime_ord]) // 3600 + 1] = y[(feiyunyingche_jiedian.iloc[
                            i[-1], starttime_ord]) // 3600:(feiyunyingche_jiedian.iloc[
                            i[-1], endtime_ord]) // 3600 + 1] + 1

                for i in range(len(feiyunyingche_jiedian)):
                    y1[feiyunyingche_jiedian.iloc[i, starttime_ord] // 3600:feiyunyingche_jiedian.iloc[
                                                                                i, endtime_ord] // 3600 + 1] = y1[
                                                                                                               feiyunyingche_jiedian.iloc[
                                                                                                                   i, starttime_ord] // 3600:
                                                                                                               feiyunyingche_jiedian.iloc[
                                                                                                                   i, endtime_ord] // 3600 + 1] + 1
            print('城区fenshi当日峰值载客+空驶车辆数（我们车队下）：' + str(dates[date_index]) + '  ' + str(y.max()))

            plt.plot(  # 画折线图y
                x, y, label='zaike+kongshi' + '(' + str(dates[date_index]) + ')',
                lw=5,  # 折线图的线条宽度
                linestyle=linestyle_color_list[date_index * len(dates)][0],
                color=linestyle_color_list[date_index * len(dates)][1],
                marker='o',
                markerfacecolor='k'
            )

            plt.plot(  # 画折线图y
                x1, y1, label='Current on-road vehicle number' + '(' + str(dates[date_index]) + ')',
                lw=5,  # 折线图的线条宽度
                linestyle=linestyle_color_list[date_index * len(dates) + 1][0],
                color=linestyle_color_list[date_index * len(dates) + 1][1],
                marker='o',
                markerfacecolor='k'
            )
        else:
            x = np.array(list(range(24))) + [0.5] * 24
            y = np.array([0] * len(x))
            x1 = np.array(list(range(24))) + [0.5] * 24
            y1 = np.array([0] * len(x))
            for t in range(len(jiedian_split_time_work) - 1):
                feiyunyingche_jiedian = pd.read_csv(open('./data/节点/'+ str(dates[date_index]) + '_jiedian_'+str(jiedian_split_time_work[t])+'_'+str(jiedian_split_time_work[t+1])+'.csv'))

                paths = []
                filePathList = os.listdir('./data/PathList/' + 'ronghe' + '/splitBytime/' + str(dates[date_index]))
                for allDir in filePathList:
                    if '_'+str(jiedian_split_time_work[t])+'_'+str(jiedian_split_time_work[t+1])+'_' in allDir:
                        child = os.path.join('%s/%s' % ('./data/PathList/' + 'ronghe' + '/splitBytime/' + str(dates[date_index]), allDir))
                        numpy_path = np.load(child, allow_pickle=True)
                        paths.append(numpy_path)

                endtime_ord = -1
                starttime_ord = -1
                end_kid_ord = -1
                start_kid_ord = -1
                for i in range(len(feiyunyingche_jiedian.columns)):
                    if feiyunyingche_jiedian.columns[i] == 'end_time':
                        endtime_ord = i
                    if feiyunyingche_jiedian.columns[i] == 'start_time':
                        starttime_ord = i
                    if feiyunyingche_jiedian.columns[i] == 'end_kid':
                        end_kid_ord = i
                    if feiyunyingche_jiedian.columns[i] == 'start_kid':
                        start_kid_ord = i

                for part in paths:
                    for i in part:
                        for j in range(len(i) - 1):
                            a = feiyunyingche_jiedian.iloc[i[j], starttime_ord]
                            c = feiyunyingche_jiedian.iloc[i[j], endtime_ord]
                            b = df_kakou_time[
                                (df_kakou_time['origin_kid'] == feiyunyingche_jiedian.iloc[i[j], end_kid_ord]) & (
                                        df_kakou_time['des_kid'] == feiyunyingche_jiedian.iloc[
                                    i[j + 1], start_kid_ord])].iloc[0]['time']
                            if (c + b) // 3600 == (feiyunyingche_jiedian.iloc[i[j + 1], starttime_ord]) // 3600:
                                y[a // 3600:(c + b) // 3600] = y[a // 3600:(c + b) // 3600] + 1
                            else:
                                y[a // 3600:(c + b) // 3600 + 1] = y[a // 3600:(c + b) // 3600 + 1] + 1
                        y[(feiyunyingche_jiedian.iloc[i[-1], starttime_ord]) // 3600:(feiyunyingche_jiedian.iloc[
                            i[-1], endtime_ord]) // 3600 + 1] = y[(feiyunyingche_jiedian.iloc[
                            i[-1], starttime_ord]) // 3600:(feiyunyingche_jiedian.iloc[
                            i[-1], endtime_ord]) // 3600 + 1] + 1

                for i in range(len(feiyunyingche_jiedian)):
                    y1[feiyunyingche_jiedian.iloc[i, starttime_ord]//3600:feiyunyingche_jiedian.iloc[i, endtime_ord]//3600 + 1] = y1[feiyunyingche_jiedian.iloc[i, starttime_ord]//3600:feiyunyingche_jiedian.iloc[i, endtime_ord]//3600 + 1] + 1

            print('城区fenshi当日峰值载客+空驶车辆数（我们车队下）：' + str(dates[date_index]) + '  ' + str(y.max()))

            plt.plot(  # 画折线图y
                x, y, label='zaike+kongshi' + '(' + str(dates[date_index]) + ')',
                lw=5,  # 折线图的线条宽度
                linestyle=linestyle_color_list[date_index * len(dates)][0],
                color=linestyle_color_list[date_index * len(dates)][1],
                marker='o',
                markerfacecolor='k'
            )

            plt.plot(  # 画折线图y
                x1, y1, label='Current on-road vehicle number' + '(' + str(dates[date_index]) + ')',
                lw=5,  # 折线图的线条宽度
                linestyle=linestyle_color_list[date_index * len(dates) + 1][0],
                color=linestyle_color_list[date_index * len(dates) + 1][1],
                marker='o',
                markerfacecolor='k'
            )

    plt.xticks(fontsize=28)  # 数量多可以采用270度，数量少可以采用340度，得到更好的视图
    plt.yticks(fontsize=28)
    plt.xlabel('Time of a day', fontsize=35)
    # plt.ylabel('车量数',fontsize=35)
    plt.xlim(0, 24, 1)
    plt.ylim(0, ylimit)
    x_major_locator = MultipleLocator(1)
    # 把x轴的刻度间隔设置为1，并存在变量里
    ax = plt.gca()
    # ax为两条坐标轴的实例
    ax.xaxis.set_major_locator(x_major_locator)
    plt.legend(fontsize=30, bbox_to_anchor=(1.2, -0.1), ncol=1)
    plt.subplots_adjust(bottom=0.2)
    # plt.title('非工作日车辆时间分布',fontsize=38)
    plt.savefig('./picture/' + 'ronghe' + '/splitBytime/' + save_path)
    plt.close()

def draw_zhuangtai_time(date,save_path,jiedian_split_time_work,jiedian_split_time_nonwork,ylimit):
    '''
    按秒分布的优化后车辆状态（分时，，优化使用不同时间阈值）
    :param date:
    :param save_path:
    :param jiedian_split_time_work:
    :param jiedian_split_time_nonwork:
    :param ylimit:
    :return:
    '''
    fig = plt.figure(figsize=(18, 12), dpi=1000)
    df_kakou_time = pd.read_csv(open('./data/kakou_time.csv'), dtype={'origin_kid': str, 'des_kid': str})
    df_kakou_time = df_kakou_time[df_kakou_time['time'] <= 1200]  # 卡口时间限制900s
    if '10' in str(date) or '11' in str(date):
        x = np.array(list(range(24 * 60 * 60)))
        y = np.array([0] * len(x))  # 总共活跃时间
        y1 = np.array([0] * len(x))  # 载客状态
        y2 = np.array([0] * len(x))  # 路上行驶时间
        y3 = np.array([0] * len(x))  # 等待时间
        for t in range(len(jiedian_split_time_nonwork) - 1):
            feiyunyingche_jiedian = pd.read_csv(open('./data/节点/' + str(date) + '_jiedian_' + str(jiedian_split_time_nonwork[t]) + '_' + str(jiedian_split_time_nonwork[t + 1]) + '.csv'))
            feiyunyingche_jiedian['start_time'] = (feiyunyingche_jiedian['start_time']).astype(int)
            feiyunyingche_jiedian['end_time'] = (feiyunyingche_jiedian['end_time']).astype(int)
            feiyunyingche_jiedian['start_kid'] = (feiyunyingche_jiedian['start_kid']).astype(str)
            feiyunyingche_jiedian['end_kid'] = (feiyunyingche_jiedian['end_kid']).astype(str)

            paths = []
            filePathList = os.listdir('./data/PathList/'+'ronghe'+'/splitBytime/'+str(date))
            for allDir in filePathList:
                if '_'+str(jiedian_split_time_nonwork[t])+'_'+str(jiedian_split_time_nonwork[t+1])+'_'  in allDir:
                    child = os.path.join('%s/%s' % ('./data/PathList/'+'ronghe'+'/splitBytime/'+str(date), allDir))
                    numpy_path = np.load(child, allow_pickle=True)
                    paths.append(numpy_path)

            endtime_ord = -1
            starttime_ord = -1
            end_kid_ord = -1
            start_kid_ord = -1
            for i in range(len(feiyunyingche_jiedian.columns)):
                if feiyunyingche_jiedian.columns[i] == 'end_time':
                    endtime_ord = i
                if feiyunyingche_jiedian.columns[i] == 'start_time':
                    starttime_ord = i
                if feiyunyingche_jiedian.columns[i] == 'end_kid':
                    end_kid_ord = i
                if feiyunyingche_jiedian.columns[i] == 'start_kid':
                    start_kid_ord = i

            for part in paths:
                for i in part:
                    y[feiyunyingche_jiedian.iloc[i[0], starttime_ord]:feiyunyingche_jiedian.iloc[i[-1], endtime_ord]] = y[feiyunyingche_jiedian.iloc[i[0], starttime_ord]:feiyunyingche_jiedian.iloc[i[-1], endtime_ord]] + 1
                    for j in i:
                        y1[feiyunyingche_jiedian.iloc[j, starttime_ord]:feiyunyingche_jiedian.iloc[j, endtime_ord]] = y1[feiyunyingche_jiedian.iloc[j, starttime_ord]:feiyunyingche_jiedian.iloc[j, endtime_ord]] + 1

            for part in paths:
                for i in part:
                    for j in range(len(i) - 1):
                        a = feiyunyingche_jiedian.iloc[i[j], endtime_ord]
                        b = df_kakou_time[(df_kakou_time['origin_kid'] == feiyunyingche_jiedian.iloc[i[j], end_kid_ord]) & (df_kakou_time['des_kid'] == feiyunyingche_jiedian.iloc[i[j + 1], start_kid_ord])].iloc[0]['time']
                        c = feiyunyingche_jiedian.iloc[i[j + 1], starttime_ord]
                        y2[a:(a + b)] = y2[a:(a + b)] + 1
                        y3[(a + b):c] = y3[(a + b):c] + 1

        print('载客率：' + str(date) + '  ' + str(np.trapz(y1) / np.trapz(y)))
        print('空驶率：' + str(date) + '  ' + str(np.trapz(y2) / np.trapz(y)))
        print('等待率：' + str(date) + '  ' + str(np.trapz(y3) / np.trapz(y)))
        plt.plot(  # 画折线图y
            x, y,
            label='活跃状态',
            color='black', linestyle='-',
            lw=5  # 折线图的线条宽度
        )

        plt.plot(  # 画折线图y
            x, y1,
            label='载客状态',
            color='red', linestyle='--',
            lw=5  # 折线图的线条宽度
        )

        plt.plot(  # 画折线图y
            x, y2,
            label='空驶状态',
            color='dodgerblue', linestyle='-.',
            lw=5  # 折线图的线条宽度
        )

        plt.plot(  # 画折线图y
            x, y3,
            label='等待状态',
            color='darkorange', linestyle=':',
            lw=5  # 折线图的线条宽度
        )
    else:
        x = np.array(list(range(24 * 60 * 60)))
        y = np.array([0] * len(x))  # 总共活跃时间
        y1 = np.array([0] * len(x))  # 载客状态
        y2 = np.array([0] * len(x))  # 路上行驶时间
        y3 = np.array([0] * len(x))  # 等待时间
        for t in range(len(jiedian_split_time_work) - 1):
            feiyunyingche_jiedian = pd.read_csv(open(
                './data/节点/' + str(date) + '_jiedian_' + str(jiedian_split_time_work[t]) + '_' + str(
                    jiedian_split_time_work[t + 1]) + '.csv'))
            feiyunyingche_jiedian['start_time'] = (feiyunyingche_jiedian['start_time']).astype(int)
            feiyunyingche_jiedian['end_time'] = (feiyunyingche_jiedian['end_time']).astype(int)
            feiyunyingche_jiedian['start_kid'] = (feiyunyingche_jiedian['start_kid']).astype(str)
            feiyunyingche_jiedian['end_kid'] = (feiyunyingche_jiedian['end_kid']).astype(str)

            paths = []
            filePathList = os.listdir(
                './data/PathList/' + 'ronghe' + '/splitBytime/' + str(date))
            for allDir in filePathList:
                if '_'+str(jiedian_split_time_work[t])+'_'+str(jiedian_split_time_work[t+1])+'_'  in allDir:
                    child = os.path.join('%s/%s' % (
                    './data/PathList/' + 'ronghe' + '/splitBytime/' + str(date), allDir))
                    numpy_path = np.load(child, allow_pickle=True)
                    paths.append(numpy_path)

            endtime_ord = -1
            starttime_ord = -1
            end_kid_ord = -1
            start_kid_ord = -1
            for i in range(len(feiyunyingche_jiedian.columns)):
                if feiyunyingche_jiedian.columns[i] == 'end_time':
                    endtime_ord = i
                if feiyunyingche_jiedian.columns[i] == 'start_time':
                    starttime_ord = i
                if feiyunyingche_jiedian.columns[i] == 'end_kid':
                    end_kid_ord = i
                if feiyunyingche_jiedian.columns[i] == 'start_kid':
                    start_kid_ord = i

            for part in paths:
                for i in part:
                    y[
                    feiyunyingche_jiedian.iloc[i[0], starttime_ord]:feiyunyingche_jiedian.iloc[i[-1], endtime_ord]] = y[
                                                                                                                      feiyunyingche_jiedian.iloc[
                                                                                                                          i[
                                                                                                                              0], starttime_ord]:
                                                                                                                      feiyunyingche_jiedian.iloc[
                                                                                                                          i[
                                                                                                                              -1], endtime_ord]] + 1
                    for j in i:
                        y1[
                        feiyunyingche_jiedian.iloc[j, starttime_ord]:feiyunyingche_jiedian.iloc[j, endtime_ord]] = y1[
                                                                                                                   feiyunyingche_jiedian.iloc[
                                                                                                                       j, starttime_ord]:
                                                                                                                   feiyunyingche_jiedian.iloc[
                                                                                                                       j, endtime_ord]] + 1

            for part in paths:
                for i in part:
                    for j in range(len(i) - 1):
                        a = feiyunyingche_jiedian.iloc[i[j], endtime_ord]
                        b = df_kakou_time[
                            (df_kakou_time['origin_kid'] == feiyunyingche_jiedian.iloc[i[j], end_kid_ord]) & (
                                        df_kakou_time['des_kid'] == feiyunyingche_jiedian.iloc[
                                    i[j + 1], start_kid_ord])].iloc[0]['time']
                        c = feiyunyingche_jiedian.iloc[i[j + 1], starttime_ord]
                        y2[a:(a + b)] = y2[a:(a + b)] + 1
                        y3[(a + b):c] = y3[(a + b):c] + 1

        print('载客率：' + str(date) + '  ' + str(np.trapz(y1) / np.trapz(y)))
        print('空驶率：' + str(date) + '  ' + str(np.trapz(y2) / np.trapz(y)))
        print('等待率：' + str(date) + '  ' + str(np.trapz(y3) / np.trapz(y)))
        plt.plot(  # 画折线图y
            x, y,
            label='活跃状态',
            color='black', linestyle='-',
            lw=5  # 折线图的线条宽度
        )

        plt.plot(  # 画折线图y
            x, y1,
            label='载客状态',
            color='red', linestyle='--',
            lw=5  # 折线图的线条宽度
        )

        plt.plot(  # 画折线图y
            x, y2,
            label='空驶状态',
            color='dodgerblue', linestyle='-.',
            lw=5  # 折线图的线条宽度
        )

        plt.plot(  # 画折线图y
            x, y3,
            label='等待状态',
            color='darkorange', linestyle=':',
            lw=5  # 折线图的线条宽度
        )

    plt.ylim(0, ylimit)
    plt.xticks(ticks=np.array(range(25)) * 60 * 60, labels=range(25), fontsize=28)  # 数量多可以采用270度，数量少可以采用340度，得到更好的视图
    plt.yticks(fontsize=28)
    plt.xlabel('Time of a day', fontsize=35)
    plt.ylabel('Vehicle number', fontsize=35)

    # plt.title('工作日所需车辆时间分布(时间阈值900)',fontsize=38)
    plt.legend(fontsize=30)
    # plt.show()
    plt.savefig('./picture/'+'ronghe'+'/splitBytime/'+save_path)
    plt.close()

# def draw_kongzhi_time(dates,linestyle_color_list,save_path,jiedian_split_time_work,jiedian_split_time_nonwork,ylimit):
#     fig = plt.figure(figsize=(18, 12), dpi=1000)
#     for date_index in range(len(dates)):
#         if '10' in str(dates[date_index]) or '11' in str(dates[date_index]):
#             x = np.array(list(range(24))) + [0.5] * 24
#             y = np.array([0] * len(x))
#             x1 = np.array(list(range(24))) + [0.5] * 24
#             y1 = np.array([0] * len(x))
#             youhuahou_num = 0
#             for t in range(len(jiedian_split_time_nonwork) - 1):
#                 feiyunyingche_jiedian = pd.read_csv(open('./data/节点/' + str(dates[date_index]) + '_jiedian_' + str(jiedian_split_time_nonwork[t]) + '_' + str(jiedian_split_time_nonwork[t + 1]) + '.csv'))
#                 feiyunyingche_jiedian['start_time'] = (feiyunyingche_jiedian['start_time'] // 3600).astype(int)
#                 feiyunyingche_jiedian['end_time'] = (feiyunyingche_jiedian['end_time'] // 3600).astype(int)
#
#                 paths = []
#                 filePathList = os.listdir('./data/PathList/'+'ronghe'+'/splitBytime/'+str(dates[date_index]))
#                 for allDir in filePathList:
#                     if '_'+str(jiedian_split_time_nonwork[t])+'_'+str(jiedian_split_time_nonwork[t+1])+'_'  in allDir:
#                         child = os.path.join('%s/%s' % ('./data/PathList/'+'ronghe'+'/splitBytime/'+str(dates[date_index]), allDir))
#                         numpy_path = np.load(child, allow_pickle=True)
#                         paths.append(numpy_path)
#
#
#                 endtime_ord = -1
#                 starttime_ord = -1
#                 for i in range(len(feiyunyingche_jiedian.columns)):
#                     if feiyunyingche_jiedian.columns[i] == 'end_time':
#                         endtime_ord = i
#                     if feiyunyingche_jiedian.columns[i] == 'start_time':
#                         starttime_ord = i
#
#                 for part in paths:
#                     for i in part:
#                         y[feiyunyingche_jiedian.iloc[i[0], starttime_ord]:feiyunyingche_jiedian.iloc[i[-1], endtime_ord] + 1] = y[feiyunyingche_jiedian.iloc[i[0], starttime_ord]:feiyunyingche_jiedian.iloc[i[-1], endtime_ord] + 1] + 1
#
#                 for i in range(len(feiyunyingche_jiedian)):
#                     y1[feiyunyingche_jiedian.iloc[i,starttime_ord]:feiyunyingche_jiedian.iloc[i, endtime_ord] + 1]=y1[feiyunyingche_jiedian.iloc[i,starttime_ord]:feiyunyingche_jiedian.iloc[i, endtime_ord] + 1] + 1
#
#                 for part in paths:
#                     for i in part:
#                         youhuahou_num += 1
#             youhuaqian_num = len(set(pd.read_csv(open('./data/节点/'+str(dates[date_index])+'_jiedian.csv'))['car_id']))#全天节点
#
#             plt.plot(  # 画折线图y
#                 x, (youhuahou_num-np.array(y))/youhuahou_num,
#                 label='Optimized'+'('+str(dates[date_index])+')',
#                 lw=5,  # 折线图的线条宽度
#                 linestyle=linestyle_color_list[date_index*len(dates)][0],
#                 color=linestyle_color_list[date_index*len(dates)][1],
#                 marker='o',
#                 markerfacecolor='k'
#             )
#
#             plt.plot(  # 画折线图y
#                 x1, (youhuaqian_num-np.array(y1))/youhuaqian_num,
#                 label='Current'+'('+str(dates[date_index])+')',
#                 lw=5,  # 折线图的线条宽度
#                 linestyle=linestyle_color_list[date_index*len(dates)+1][0],
#                 color=linestyle_color_list[date_index*len(dates)+1][1],
#                 marker='o',
#                 markerfacecolor='k'
#             )
#         else:
#             x = np.array(list(range(24))) + [0.5] * 24
#             y = np.array([0] * len(x))
#             x1 = np.array(list(range(24))) + [0.5] * 24
#             y1 = np.array([0] * len(x))
#             youhuahou_num = 0
#             for t in range(len(jiedian_split_time_work) - 1):
#                 feiyunyingche_jiedian = pd.read_csv(open('./data/节点/' + str(dates[date_index]) + '_jiedian_' + str(
#                     jiedian_split_time_work[t]) + '_' + str(jiedian_split_time_work[t + 1]) + '.csv'))
#                 feiyunyingche_jiedian['start_time'] = (feiyunyingche_jiedian['start_time'] // 3600).astype(int)
#                 feiyunyingche_jiedian['end_time'] = (feiyunyingche_jiedian['end_time'] // 3600).astype(int)
#
#                 paths = []
#                 filePathList = os.listdir(
#                     './data/PathList/' + 'ronghe' + '/splitBytime/' + str(
#                         dates[date_index]))
#                 for allDir in filePathList:
#                     if '_'+str(jiedian_split_time_work[t])+'_'+str(jiedian_split_time_work[t+1])+'_'  in allDir:
#                         child = os.path.join('%s/%s' % (
#                         './data/PathList/' + 'ronghe' + '/splitBytime/' + str(
#                             dates[date_index]), allDir))
#                         numpy_path = np.load(child, allow_pickle=True)
#                         paths.append(numpy_path)
#
#                 endtime_ord = -1
#                 starttime_ord = -1
#                 for i in range(len(feiyunyingche_jiedian.columns)):
#                     if feiyunyingche_jiedian.columns[i] == 'end_time':
#                         endtime_ord = i
#                     if feiyunyingche_jiedian.columns[i] == 'start_time':
#                         starttime_ord = i
#
#                 for part in paths:
#                     for i in part:
#                         y[feiyunyingche_jiedian.iloc[i[0], starttime_ord]:feiyunyingche_jiedian.iloc[
#                                                                               i[-1], endtime_ord] + 1] = y[
#                                                                                                          feiyunyingche_jiedian.iloc[
#                                                                                                              i[
#                                                                                                                  0], starttime_ord]:
#                                                                                                          feiyunyingche_jiedian.iloc[
#                                                                                                              i[
#                                                                                                                  -1], endtime_ord] + 1] + 1
#
#                 for i in range(len(feiyunyingche_jiedian)):
#                     y1[
#                     feiyunyingche_jiedian.iloc[i, starttime_ord]:feiyunyingche_jiedian.iloc[i, endtime_ord] + 1] = y1[
#                                                                                                                    feiyunyingche_jiedian.iloc[
#                                                                                                                        i, starttime_ord]:
#                                                                                                                    feiyunyingche_jiedian.iloc[
#                                                                                                                        i, endtime_ord] + 1] + 1
#
#                 for part in paths:
#                     for i in part:
#                         youhuahou_num += 1
#             youhuaqian_num = len(set(pd.read_csv(open('./data/节点/'+str(dates[date_index])+'_jiedian.csv'))['car_id']))#全天节点
#
#             plt.plot(  # 画折线图y
#                 x, (youhuahou_num - np.array(y)) / youhuahou_num,
#                 label='Optimized' + '(' + str(dates[date_index]) + ')',
#                 lw=5,  # 折线图的线条宽度
#                 linestyle=linestyle_color_list[date_index * len(dates)][0],
#                 color=linestyle_color_list[date_index * len(dates)][1],
#                 marker='o',
#                 markerfacecolor='k'
#             )
#
#             plt.plot(  # 画折线图y
#                 x1, (youhuaqian_num - np.array(y1)) / youhuaqian_num,
#                 label='Current' + '(' + str(dates[date_index]) + ')',
#                 lw=5,  # 折线图的线条宽度
#                 linestyle=linestyle_color_list[date_index * len(dates) + 1][0],
#                 color=linestyle_color_list[date_index * len(dates) + 1][1],
#                 marker='o',
#                 markerfacecolor='k'
#             )
#
#     plt.xticks(fontsize=28)  # 数量多可以采用270度，数量少可以采用340度，得到更好的视图
#     plt.yticks(fontsize=28)
#     plt.xlabel('Time of a day', fontsize=35)
#     # plt.ylabel('车量数',fontsize=35)
#     plt.xlim(0, 24, 1)
#     plt.ylim(0, ylimit)
#     x_major_locator = MultipleLocator(1)
#     # 把x轴的刻度间隔设置为1，并存在变量里
#     ax = plt.gca()
#     # ax为两条坐标轴的实例
#     ax.xaxis.set_major_locator(x_major_locator)
#     plt.legend(fontsize=30, bbox_to_anchor=(1.2, -0.1), ncol=1)
#     plt.subplots_adjust(bottom=0.2)
#     # plt.title('非工作日车辆时间分布',fontsize=38)
#     plt.savefig('./picture/'+'ronghe'+'/splitBytime/'+save_path)
#     plt.close()


if __name__ == '__main__':
    global_config = Config('./config.ini')
    source_file = global_config.getRaw('设置条件', 'source_file')
    source_file = json.loads(source_file)  # str转list
    jiedian_split_time_work = global_config.getRaw('设置条件', 'jiedian_split_time_work')
    jiedian_split_time_work = json.loads(jiedian_split_time_work)
    jiedian_split_time_nonwork = global_config.getRaw('设置条件', 'jiedian_split_time_nonwork')
    jiedian_split_time_nonwork = json.loads(jiedian_split_time_nonwork)
    draw(jiedian_split_time_work,jiedian_split_time_nonwork)

