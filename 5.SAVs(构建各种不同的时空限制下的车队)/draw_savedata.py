# -*- coding:utf-8 -*-
#author:jeremy

import networkx as nx
import pandas as pd
import numpy as np
import random
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

def draw(restrict_time, number,jiedian_split_time_work,jiedian_split_time_nonwork):
    '''
    画非营运车辆的出行次数（整体）、出行车数（整体、分区、分时）、状态（整体、分区、分时）
    :param restrict_time:
    :param number:
    :return:
    '''
    create_dir('./picture')
    create_dir('./picture' + '/' + str(restrict_time) + ' ' + str(number))
    create_dir('./picture' + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'Nosplit_data')
    create_dir('./picture' + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'splitByregion_data')
    create_dir('./picture' + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'splitBytime_data')

    draw_checi([1205],
                [['-', 'dodgerblue']],
                restrict_time, number, '1205_checi',550000)

    draw_cheshu([1205],
                [['-', 'dodgerblue'], ['-', 'darkorange']],
                restrict_time, number, '1205_cheshu',200000)
    draw_cheshu_xianyou_zaike_kongshi([1205],
                [['-', 'dodgerblue'], ['-', 'darkorange']],
                restrict_time, number, '1205_cheshu_zaike_kongshi', 200000)
    draw_cheshu_region([1205],
                [['-', 'dodgerblue'], ['-', 'darkorange']],
                restrict_time, number, 'beibu','1205_cheshu_beibu',50000)
    draw_cheshu_region_xianyou_zaike_kongshi([1205],
                       [['-', 'dodgerblue'], ['-', 'darkorange']],
                       restrict_time, number, 'beibu', '1205_cheshu_beibu_zaike_kongshi', 50000)
    draw_cheshu_region([1205],
                       [['-', 'dodgerblue'], ['-', 'darkorange']],
                       restrict_time, number, 'dongbu', '1205_cheshu_dongbu',50000)
    draw_cheshu_region_xianyou_zaike_kongshi([1205],
                       [['-', 'dodgerblue'], ['-', 'darkorange']],
                       restrict_time, number, 'dongbu', '1205_cheshu_dongbu_zaike_kongshi', 50000)
    draw_cheshu_region([1205],
                       [['-', 'dodgerblue'], ['-', 'darkorange']],
                       restrict_time, number, 'futianA', '1205_cheshu_futianA',50000)
    draw_cheshu_region_xianyou_zaike_kongshi([1205],
                       [['-', 'dodgerblue'], ['-', 'darkorange']],
                       restrict_time, number, 'futianA', '1205_cheshu_futianA_zaike_kongshi', 50000)
    draw_cheshu_region([1205],
                       [['-', 'dodgerblue'], ['-', 'darkorange']],
                       restrict_time, number, 'futianB', '1205_cheshu_futianB',50000)
    draw_cheshu_region_xianyou_zaike_kongshi([1205],
                       [['-', 'dodgerblue'], ['-', 'darkorange']],
                       restrict_time, number, 'futianB', '1205_cheshu_futianB_zaike_kongshi', 50000)
    draw_cheshu_region([1205],
                       [['-', 'dodgerblue'], ['-', 'darkorange']],
                       restrict_time, number, 'luohu', '1205_cheshu_luohu',50000)
    draw_cheshu_region_xianyou_zaike_kongshi([1205],
                       [['-', 'dodgerblue'], ['-', 'darkorange']],
                       restrict_time, number, 'luohu', '1205_cheshu_luohu_zaike_kongshi', 50000)
    draw_cheshu_region([1205],
                       [['-', 'dodgerblue'], ['-', 'darkorange']],
                       restrict_time, number, 'nanshan', '1205_cheshu_nanshan',50000)
    draw_cheshu_region_xianyou_zaike_kongshi([1205],
                       [['-', 'dodgerblue'], ['-', 'darkorange']],
                       restrict_time, number, 'nanshan', '1205_cheshu_nanshan_zaike_kongshi', 50000)
    draw_cheshu_region([1205],
                       [['-', 'dodgerblue'], ['-', 'darkorange']],
                       restrict_time, number, 'xibu', '1205_cheshu_xibu',50000)
    draw_cheshu_region_xianyou_zaike_kongshi([1205],
                       [['-', 'dodgerblue'], ['-', 'darkorange']],
                       restrict_time, number, 'xibu', '1205_cheshu_xibu_zaike_kongshi', 50000)
    draw_cheshu_time([1205],
                       [['-', 'dodgerblue'], ['-', 'darkorange']],
                       restrict_time, number, '1205_cheshu_time',jiedian_split_time_work,jiedian_split_time_nonwork,200000)
    draw_cheshu_time_xianyou_zaike_kongshi([1205],
                     [['-', 'dodgerblue'], ['-', 'darkorange']],
                     restrict_time, number, '1205_cheshu_time_zaike_kongshi', jiedian_split_time_work, jiedian_split_time_nonwork,
                     200000)

    draw_zhuangtai(1205,
                 restrict_time, number, '1205_zhuangtai',200000)
    draw_zhuangtai_region(1205,
                   restrict_time, number, 'beibu', '1205_zhuangtai_beibu',50000)
    draw_zhuangtai_region(1205,
                   restrict_time, number, 'dongbu', '1205_zhuangtai_dongbu',50000)
    draw_zhuangtai_region(1205,
                   restrict_time, number, 'futianA', '1205_zhuangtai_futianA',50000)
    draw_zhuangtai_region(1205,
                   restrict_time, number, 'futianB', '1205_zhuangtai_futianB',50000)
    draw_zhuangtai_region(1205,
                   restrict_time, number, 'luohu', '1205_zhuangtai_luohu',50000)
    draw_zhuangtai_region(1205,
                   restrict_time, number, 'nanshan', '1205_zhuangtai_nanshan',50000)
    draw_zhuangtai_region(1205,
                   restrict_time, number, 'xibu', '1205_zhuangtai_xibu',50000)
    draw_zhuangtai_time(1205,
                 restrict_time, number, '1205_zhuangtai_time',jiedian_split_time_work,jiedian_split_time_nonwork,200000)



    # draw_checi([1210],
    #             [['--', 'dodgerblue']],
    #             restrict_time, number, '1210_checi',550000)
    # draw_cheshu([1210],
    #             [['--', 'dodgerblue'], ['--', 'darkorange']],
    #             restrict_time, number, '1210_cheshu',200000)
    # draw_cheshu_xianyou_zaike_kongshi([1210],
    #             [['--', 'dodgerblue'], ['--', 'darkorange']],
    #             restrict_time, number, '1210_cheshu_zaike_kongshi', 200000)
    # draw_cheshu_region([1210],
    #                    [['--', 'dodgerblue'], ['--', 'darkorange']],
    #                    restrict_time, number, 'beibu', '1210_cheshu_beibu',50000)
    # draw_cheshu_region_xianyou_zaike_kongshi([1210],
    #                   [['--', 'dodgerblue'], ['--', 'darkorange']],
    #                   restrict_time, number, 'beibu', '1210_cheshu_beibu_zaike_kongshi', 50000)
    # draw_cheshu_region([1210],
    #                    [['--', 'dodgerblue'], ['--', 'darkorange']],
    #                    restrict_time, number, 'dongbu', '1210_cheshu_dongbu',50000)
    # draw_cheshu_region_xianyou_zaike_kongshi([1210],
    #                   [['--', 'dodgerblue'], ['--', 'darkorange']],
    #                   restrict_time, number, 'dongbu', '1210_cheshu_dongbu_zaike_kongshi', 50000)
    # draw_cheshu_region([1210],
    #                    [['--', 'dodgerblue'], ['--', 'darkorange']],
    #                    restrict_time, number, 'futianA', '1210_cheshu_futianA',50000)
    # draw_cheshu_region_xianyou_zaike_kongshi([1210],
    #                   [['--', 'dodgerblue'], ['--', 'darkorange']],
    #                   restrict_time, number, 'futianA', '1210_cheshu_futianA_zaike_kongshi', 50000)
    # draw_cheshu_region([1210],
    #                    [['--', 'dodgerblue'], ['--', 'darkorange']],
    #                    restrict_time, number, 'futianB', '1210_cheshu_futianB',50000)
    # draw_cheshu_region_xianyou_zaike_kongshi([1210],
    #                   [['--', 'dodgerblue'], ['--', 'darkorange']],
    #                   restrict_time, number, 'futianB', '1210_cheshu_futianB_zaike_kongshi', 50000)
    # draw_cheshu_region([1210],
    #                    [['--', 'dodgerblue'], ['--', 'darkorange']],
    #                    restrict_time, number, 'luohu', '1210_cheshu_luohu',50000)
    # draw_cheshu_region_xianyou_zaike_kongshi([1210],
    #                   [['--', 'dodgerblue'], ['--', 'darkorange']],
    #                   restrict_time, number, 'luohu', '1210_cheshu_luohu_zaike_kongshi', 50000)
    # draw_cheshu_region([1210],
    #                    [['--', 'dodgerblue'], ['--', 'darkorange']],
    #                    restrict_time, number, 'nanshan', '1210_cheshu_nanshan',50000)
    # draw_cheshu_region_xianyou_zaike_kongshi([1210],
    #                   [['--', 'dodgerblue'], ['--', 'darkorange']],
    #                   restrict_time, number, 'nanshan', '1210_cheshu_nanshan_zaike_kongshi', 50000)
    # draw_cheshu_region([1210],
    #                    [['--', 'dodgerblue'], ['--', 'darkorange']],
    #                    restrict_time, number, 'xibu', '1210_cheshu_xibu',50000)
    # draw_cheshu_region_xianyou_zaike_kongshi([1210],
    #                   [['--', 'dodgerblue'], ['--', 'darkorange']],
    #                   restrict_time, number, 'xibu', '1210_cheshu_xibu_zaike_kongshi', 50000)
    # draw_cheshu_time([1210],
    #             [['--', 'dodgerblue'], ['--', 'darkorange']],
    #             restrict_time, number, '1210_cheshu_time',jiedian_split_time_work,jiedian_split_time_nonwork,200000)
    # draw_cheshu_time_xianyou_zaike_kongshi([1210],
    #                 [['--', 'dodgerblue'], ['--', 'darkorange']],
    #                 restrict_time, number, '1210_cheshu_time_zaike_kongshi', jiedian_split_time_work, jiedian_split_time_nonwork,
    #                 200000)
    #
    # draw_zhuangtai(1210,
    #                restrict_time, number, '1210_zhuangtai',150000)
    # draw_zhuangtai_region(1210,
    #                       restrict_time, number, 'beibu', '1210_zhuangtai_beibu',40000)
    # draw_zhuangtai_region(1210,
    #                       restrict_time, number, 'dongbu', '1210_zhuangtai_dongbu',40000)
    # draw_zhuangtai_region(1210,
    #                       restrict_time, number, 'futianA', '1210_zhuangtai_futianA',40000)
    # draw_zhuangtai_region(1210,
    #                       restrict_time, number, 'futianB', '1210_zhuangtai_futianB',40000)
    # draw_zhuangtai_region(1210,
    #                       restrict_time, number, 'luohu', '1210_zhuangtai_luohu',40000)
    # draw_zhuangtai_region(1210,
    #                       restrict_time, number, 'nanshan', '1210_zhuangtai_nanshan',40000)
    # draw_zhuangtai_region(1210,
    #                       restrict_time, number, 'xibu', '1210_zhuangtai_xibu',40000)
    # draw_zhuangtai_time(1210,
    #                restrict_time, number, '1210_zhuangtai_time',jiedian_split_time_work,jiedian_split_time_nonwork,150000)




    # draw_kongzhi([1205],
    #              [['-', 'dodgerblue'], ['-', 'darkorange']],
    #              restrict_time, number, '1205_kongzhi',1)
    # draw_kongzhi_region([1205],
    #                     [['-', 'dodgerblue'], ['-', 'darkorange']],
    #                     restrict_time, number, 'beibu', '1205_kongzhi_beibu',1)
    # draw_kongzhi_region([1205],
    #                     [['-', 'dodgerblue'], ['-', 'darkorange']],
    #                     restrict_time, number, 'dongbu', '1205_kongzhi_dongbu',1)
    # draw_kongzhi_region([1205],
    #                     [['-', 'dodgerblue'], ['-', 'darkorange']],
    #                     restrict_time, number, 'futianA', '1205_kongzhi_futianA',1)
    # draw_kongzhi_region([1205],
    #                     [['-', 'dodgerblue'], ['-', 'darkorange']],
    #                     restrict_time, number, 'futianB', '1205_kongzhi_futianB',1)
    # draw_kongzhi_region([1205],
    #                     [['-', 'dodgerblue'], ['-', 'darkorange']],
    #                     restrict_time, number, 'luohu', '1205_kongzhi_luohu',1)
    # draw_kongzhi_region([1205],
    #                     [['-', 'dodgerblue'], ['-', 'darkorange']],
    #                     restrict_time, number, 'nanshan', '1205_kongzhi_nanshan',1)
    # draw_kongzhi_region([1205],
    #                     [['-', 'dodgerblue'], ['-', 'darkorange']],
    #                     restrict_time, number, 'xibu', '1205_kongzhi_xibu',1)
    # draw_kongzhi_time([1205],
    #              [['-', 'dodgerblue'], ['-', 'darkorange']],
    #              restrict_time, number, '1205_kongzhi',jiedian_split_time_work,jiedian_split_time_nonwork,1)


    # draw_kongzhi([1210],
    #              [['--', 'dodgerblue'], ['--', 'darkorange']],
    #              restrict_time, number, '1210_kongzhi',1)
    # draw_kongzhi_region([1210],
    #                     [['--', 'dodgerblue'], ['--', 'darkorange']],
    #                     restrict_time, number, 'beibu', '1210_kongzhi_beibu',1)
    # draw_kongzhi_region([1210],
    #                     [['--', 'dodgerblue'], ['--', 'darkorange']],
    #                     restrict_time, number, 'dongbu', '1210_kongzhi_dongbu',1)
    # draw_kongzhi_region([1210],
    #                     [['--', 'dodgerblue'], ['--', 'darkorange']],
    #                     restrict_time, number, 'futianA', '1210_kongzhi_futianA',1)
    # draw_kongzhi_region([1210],
    #                     [['--', 'dodgerblue'], ['--', 'darkorange']],
    #                     restrict_time, number, 'futianB', '1210_kongzhi_futianB',1)
    # draw_kongzhi_region([1210],
    #                     [['--', 'dodgerblue'], ['--', 'darkorange']],
    #                     restrict_time, number, 'luohu', '1210_kongzhi_luohu',1)
    # draw_kongzhi_region([1210],
    #                     [['--', 'dodgerblue'], ['--', 'darkorange']],
    #                     restrict_time, number, 'nanshan', '1210_kongzhi_nanshan',1)
    # draw_kongzhi_region([1210],
    #                     [['--', 'dodgerblue'], ['--', 'darkorange']],
    #                     restrict_time, number, 'xibu', '1210_kongzhi_xibu',1)
    # # draw_kongzhi_time([1210],
    #              [['--', 'dodgerblue'], ['--', 'darkorange']],
    #              restrict_time, number, '1210_kongzhi',jiedian_split_time_work,jiedian_split_time_nonwork,1)


def draw_checi(dates,linestyle_color_list,restrict_time,number,save_path,ylimit):
    '''
    按小时分布的非营运车辆出行次数（拍摄次数）
    :param dates: 日期
    :param linestyle_color_list:线型颜色
    :param restrict_time:
    :param number:
    :param save_path:
    :param ylimit:y轴最大值
    :return:
    '''
    for date_index in range(len(dates)):
        feiyunyingche = pd.read_csv(open(r'./data/非运营车卡口记录（带坐标）/2016' + str(dates[date_index]) + '_title_feiyunyingche_zuobiao.csv'))
        feiyunyingche['time'] = feiyunyingche['time'] // 3600
        feiyunyingche_tongji = collections.Counter(feiyunyingche['time'])  # 统计非运营车辆的时间分布
        feiyunyingche_tongji = Series(feiyunyingche_tongji).to_frame().rename(columns={0: 'num'}).sort_index()
        x = np.array(list(feiyunyingche_tongji.index)) + [0.5] * 24
        y = list(feiyunyingche_tongji['num'])
        df=pd.DataFrame(data=y,index=x,columns=['checi'+'('+str(dates[date_index])+')'])
        df.to_csv('./picture/'+str(restrict_time)+' '+str(number)+'/Nosplit_data/'+save_path+'.csv')

def draw_cheshu(dates,linestyle_color_list,restrict_time,number,save_path,ylimit):
    '''
    按小时分布的优化前出行车数和优化后出行车数
    :param dates:
    :param linestyle_color_list:
    :param restrict_time:
    :param number:
    :param save_path:
    :param ylimit:
    :return:
    '''
    for date_index in range(len(dates)):
        feiyunyingche_jiedian = pd.read_csv(open('./data/节点/'+str(dates[date_index])+'_jiedian.csv'))
        feiyunyingche_jiedian['start_time'] = (feiyunyingche_jiedian['start_time'] // 3600).astype(int)
        feiyunyingche_jiedian['end_time'] = (feiyunyingche_jiedian['end_time'] // 3600).astype(int)
        print('城区总出行数：' + str(dates[date_index]) + '  ' + str(len(feiyunyingche_jiedian)))
        print('城区总车辆数（现实场景下）：' + str(dates[date_index]) + '  ' + str(len(set(feiyunyingche_jiedian['car_id']))))
        print('城区摄像头数：' + str(dates[date_index]) + '  ' + str(len(set(list(feiyunyingche_jiedian['start_kid'])+list(feiyunyingche_jiedian['end_kid'])))))

        paths = []
        filePathList = os.listdir('./data/PathList/'+str(restrict_time)+' '+str(number)+'/Nosplit/'+str(dates[date_index]))
        for allDir in filePathList:
            child = os.path.join('%s/%s' % ('./data/PathList/'+str(restrict_time)+' '+str(number)+'/Nosplit/'+str(dates[date_index]), allDir))
            numpy_path = np.load(child, allow_pickle=True)
            paths.append(numpy_path)

        x = np.array(list(range(24)))+[0.5]*24
        y = np.array([0] * len(x))
        x1 = np.array(list(range(24)))+[0.5]*24
        y1 = np.array([0] * len(x))
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
            y1[feiyunyingche_jiedian.iloc[i,starttime_ord]:feiyunyingche_jiedian.iloc[i, endtime_ord] + 1]=y1[feiyunyingche_jiedian.iloc[i,starttime_ord]:feiyunyingche_jiedian.iloc[i, endtime_ord] + 1] + 1

        print('城区当日峰值车辆数（现实场景下）：' + str(dates[date_index]) + '  ' + str(y1.max()))
        print('城区当日峰值车辆数（我们车队下）：' + str(dates[date_index]) + '  ' + str(y.max()))
        car_num=0
        for part in paths:
            car_num=car_num+len(part)
        print('城区总车辆数（我们车队下）：' + str(dates[date_index]) + '  ' + str(car_num))

        df = pd.DataFrame(data=np.array([y,y1]).T, index=x, columns=['Minimized vehicle number'+'('+str(dates[date_index])+')',
                                                         'Current on-road vehicle number'+'('+str(dates[date_index])+')'])
        df.to_csv('./picture/'+str(restrict_time)+' '+str(number)+'/Nosplit_data/'+save_path + '.csv')



def draw_cheshu_xianyou_zaike_kongshi(dates,linestyle_color_list,restrict_time,number,save_path,ylimit):
    for date_index in range(len(dates)):
        feiyunyingche_jiedian = pd.read_csv(open('./data/节点/' + str(dates[date_index]) + '_jiedian.csv'))
        feiyunyingche_jiedian['start_time'] = (feiyunyingche_jiedian['start_time']).astype(int)
        feiyunyingche_jiedian['end_time'] = (feiyunyingche_jiedian['end_time']).astype(int)
        feiyunyingche_jiedian['start_kid'] = (feiyunyingche_jiedian['start_kid']).astype(str)
        feiyunyingche_jiedian['end_kid'] = (feiyunyingche_jiedian['end_kid']).astype(str)
        df_kakou_time = pd.read_csv(open('./data/kakou_time.csv'), dtype={'origin_kid': str, 'des_kid': str})

        df_kakou_time = df_kakou_time[df_kakou_time['time'] <= restrict_time]  # 卡口时间限制900s

        paths = []
        filePathList = os.listdir('./data/PathList/' + str(restrict_time) + ' ' + str(number) + '/Nosplit/' + str(dates[date_index]))
        for allDir in filePathList:
            child = os.path.join('%s/%s' % (
            './data/PathList/' + str(restrict_time) + ' ' + str(number) + '/Nosplit/' + str(dates[date_index]), allDir))
            numpy_path = np.load(child, allow_pickle=True)
            paths.append(numpy_path)

        x = np.array(list(range(24))) + [0.5] * 24
        y = np.array([0] * len(x))#载客+空驶
        x1 = np.array(list(range(24))) + [0.5] * 24
        y1 = np.array([0] * len(x))#现有

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


        for i in range(len(feiyunyingche_jiedian)):
            y1[(feiyunyingche_jiedian.iloc[i, starttime_ord])//3600:(feiyunyingche_jiedian.iloc[i, endtime_ord])//3600 + 1] = y1[(feiyunyingche_jiedian.iloc[i, starttime_ord])//3600:(feiyunyingche_jiedian.iloc[i, endtime_ord])//3600 + 1] + 1

        for part in paths:
            for i in part:
                for j in range(len(i)-1):
                    a = feiyunyingche_jiedian.iloc[i[j], starttime_ord]
                    c = feiyunyingche_jiedian.iloc[i[j], endtime_ord]
                    b = df_kakou_time[(df_kakou_time['origin_kid'] == feiyunyingche_jiedian.iloc[i[j], end_kid_ord]) & (df_kakou_time['des_kid'] == feiyunyingche_jiedian.iloc[i[j + 1], start_kid_ord])].iloc[0]['time']
                    if (c + b)//3600==(feiyunyingche_jiedian.iloc[i[j+1], starttime_ord])//3600:
                        y[a//3600:(c + b)//3600] = y[a//3600:(c + b)//3600]  + 1
                    else:
                        y[a//3600:(c + b)//3600+1] = y[a//3600:(c + b)//3600+1]  + 1
                y[(feiyunyingche_jiedian.iloc[i[-1], starttime_ord])//3600:(feiyunyingche_jiedian.iloc[i[-1], endtime_ord])//3600+1] = y[(feiyunyingche_jiedian.iloc[i[-1], starttime_ord])//3600:(feiyunyingche_jiedian.iloc[i[-1], endtime_ord])//3600+1] + 1

        print('城区当日峰值载客+空驶车辆数（我们车队下）：' + str(dates[date_index]) + '  ' + str(y.max()))

        df = pd.DataFrame(data=np.array([y,y1]).T, index=x,
                          columns=['zaike+kongshi' + '(' + str(dates[date_index]) + ')',
                                   'Current on-road vehicle number' + '(' + str(dates[date_index]) + ')'])
        df.to_csv('./picture/' + str(restrict_time) + ' ' + str(number) + '/Nosplit_data/' + save_path+'.csv')

def draw_cheshu_region(dates,linestyle_color_list,restrict_time,number,region,save_path,ylimit):
    '''
    按小时分布的优化前出行车数和优化后出行车数（分区）
    :param dates:
    :param linestyle_color_list:
    :param restrict_time:
    :param number:
    :param region:
    :param save_path:
    :param ylimit:
    :return:
    '''
    for date_index in range(len(dates)):
        feiyunyingche_jiedian = pd.read_csv(open('./data/节点/'+str(dates[date_index])+'_jiedian.csv'))
        feiyunyingche_jiedian['start_time'] = (feiyunyingche_jiedian['start_time'] // 3600).astype(int)
        feiyunyingche_jiedian['end_time'] = (feiyunyingche_jiedian['end_time'] // 3600).astype(int)

        paths = np.load('./data/PathList/'+str(restrict_time)+' '+str(number)+'/splitByregion/'+str(dates[date_index])+'/'+str(dates[date_index])+'_path_'+region+'.npy', allow_pickle=True)
        x = np.array(list(range(24)))+[0.5]*24
        y = np.array([0] * len(x))
        x1 = np.array(list(range(24)))+[0.5]*24
        y1 = np.array([0] * len(x))
        endtime_ord = -1
        starttime_ord = -1
        for i in range(len(feiyunyingche_jiedian.columns)):
            if feiyunyingche_jiedian.columns[i] == 'end_time':
                endtime_ord = i
            if feiyunyingche_jiedian.columns[i] == 'start_time':
                starttime_ord = i

        for i in paths:
            y[feiyunyingche_jiedian.iloc[i[0], starttime_ord]:feiyunyingche_jiedian.iloc[i[-1], endtime_ord] + 1] = y[feiyunyingche_jiedian.iloc[i[0], starttime_ord]:feiyunyingche_jiedian.iloc[i[-1], endtime_ord] + 1] + 1

        feiyunyingche_jiedian_region = pd.read_csv(open('./data/节点/' + str(dates[date_index]) + '_jiedian_'+region+'.csv'))
        feiyunyingche_jiedian_region['start_time'] = (feiyunyingche_jiedian_region['start_time'] // 3600).astype(int)
        feiyunyingche_jiedian_region['end_time'] = (feiyunyingche_jiedian_region['end_time'] // 3600).astype(int)
        print(str(region) + '总出行数：' + str(dates[date_index]) + '  ' + str(len(feiyunyingche_jiedian_region)))
        print(str(region) + '总车辆数（现实场景下）：' + str(dates[date_index]) + '  ' + str(len(set(feiyunyingche_jiedian_region['car_id']))))
        print(str(region) + '摄像头数：' + str(dates[date_index]) + '  ' + str(len(set(feiyunyingche_jiedian_region['start_kid']))))

        endtime_ord = -1
        starttime_ord = -1
        for i in range(len(feiyunyingche_jiedian_region.columns)):
            if feiyunyingche_jiedian_region.columns[i] == 'end_time':
                endtime_ord = i
            if feiyunyingche_jiedian_region.columns[i] == 'start_time':
                starttime_ord = i
        for i in range(len(feiyunyingche_jiedian_region)):
            y1[feiyunyingche_jiedian_region.iloc[i,starttime_ord]:feiyunyingche_jiedian_region.iloc[i, endtime_ord] + 1]=y1[feiyunyingche_jiedian_region.iloc[i,starttime_ord]:feiyunyingche_jiedian_region.iloc[i, endtime_ord] + 1] + 1

        print(str(region) + '当日峰值车辆数（现实场景下）：' + str(dates[date_index]) + '  ' + str(y1.max()))
        print(str(region) + '当日峰值车辆数（我们车队下）：' + str(dates[date_index]) + '  ' + str(y.max()))
        print(str(region) + '总车辆数（我们车队下）：' + str(dates[date_index]) + '  ' + str(len(paths)))

        df = pd.DataFrame(data=np.array([y,y1]).T, index=x,
                          columns=['Minimized vehicle number'+'('+str(dates[date_index])+')',
                                   'Current on-road vehicle number'+'('+str(dates[date_index])+')'])
        df.to_csv('./picture/'+str(restrict_time)+' '+str(number)+'/splitByregion_data/'+save_path + '.csv')


def draw_cheshu_region_xianyou_zaike_kongshi(dates,linestyle_color_list,restrict_time,number,region,save_path,ylimit):
    for date_index in range(len(dates)):
        feiyunyingche_jiedian = pd.read_csv(open('./data/节点/'+str(dates[date_index])+'_jiedian.csv'))
        feiyunyingche_jiedian['start_time'] = (feiyunyingche_jiedian['start_time']).astype(int)
        feiyunyingche_jiedian['end_time'] = (feiyunyingche_jiedian['end_time']).astype(int)
        feiyunyingche_jiedian['start_kid'] = (feiyunyingche_jiedian['start_kid']).astype(str)
        feiyunyingche_jiedian['end_kid'] = (feiyunyingche_jiedian['end_kid']).astype(str)
        df_kakou_time = pd.read_csv(open('./data/kakou_time.csv'), dtype={'origin_kid': str, 'des_kid': str})

        df_kakou_time = df_kakou_time[df_kakou_time['time'] <= restrict_time]  # 卡口时间限制900s

        paths = np.load('./data/PathList/'+str(restrict_time)+' '+str(number)+'/splitByregion/'+str(dates[date_index])+'/'+str(dates[date_index])+'_path_'+region+'.npy', allow_pickle=True)
        x = np.array(list(range(24)))+[0.5]*24
        y = np.array([0] * len(x))
        x1 = np.array(list(range(24)))+[0.5]*24
        y1 = np.array([0] * len(x))
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

        for i in paths:
            for j in range(len(i) - 1):
                a = feiyunyingche_jiedian.iloc[i[j], starttime_ord]
                c = feiyunyingche_jiedian.iloc[i[j], endtime_ord]
                b = df_kakou_time[(df_kakou_time['origin_kid'] == feiyunyingche_jiedian.iloc[i[j], end_kid_ord]) & (
                            df_kakou_time['des_kid'] == feiyunyingche_jiedian.iloc[i[j + 1], start_kid_ord])].iloc[0][
                    'time']
                if (c + b) // 3600 == (feiyunyingche_jiedian.iloc[i[j + 1], starttime_ord]) // 3600:
                    y[a // 3600:(c + b) // 3600] = y[a // 3600:(c + b) // 3600] + 1
                else:
                    y[a // 3600:(c + b) // 3600 + 1] = y[a // 3600:(c + b) // 3600 + 1] + 1
            y[(feiyunyingche_jiedian.iloc[i[-1], starttime_ord]) // 3600:(feiyunyingche_jiedian.iloc[
                i[-1], endtime_ord]) // 3600 + 1] = y[(feiyunyingche_jiedian.iloc[i[-1], starttime_ord]) // 3600:(
                                                                                                                 feiyunyingche_jiedian.iloc[
                                                                                                                     i[
                                                                                                                         -1], endtime_ord]) // 3600 + 1] + 1
        print('fenqu当日峰值载客+空驶车辆数（我们车队下）：' + str(dates[date_index]) + '  ' + str(y.max()))

        feiyunyingche_jiedian_region = pd.read_csv(open('./data/节点/' + str(dates[date_index]) + '_jiedian_'+region+'.csv'))
        feiyunyingche_jiedian_region['start_time'] = (feiyunyingche_jiedian_region['start_time'] // 3600).astype(int)
        feiyunyingche_jiedian_region['end_time'] = (feiyunyingche_jiedian_region['end_time'] // 3600).astype(int)

        endtime_ord = -1
        starttime_ord = -1
        for i in range(len(feiyunyingche_jiedian_region.columns)):
            if feiyunyingche_jiedian_region.columns[i] == 'end_time':
                endtime_ord = i
            if feiyunyingche_jiedian_region.columns[i] == 'start_time':
                starttime_ord = i
        for i in range(len(feiyunyingche_jiedian_region)):
            y1[feiyunyingche_jiedian_region.iloc[i,starttime_ord]:feiyunyingche_jiedian_region.iloc[i, endtime_ord] + 1]=y1[feiyunyingche_jiedian_region.iloc[i,starttime_ord]:feiyunyingche_jiedian_region.iloc[i, endtime_ord] + 1] + 1

        df = pd.DataFrame(data=np.array([y,y1]).T, index=x,
                          columns=['zaike+kongshi'+'('+str(dates[date_index])+')',
                                   'Current on-road vehicle number'+'('+str(dates[date_index])+')'])
        df.to_csv('./picture/'+str(restrict_time)+' '+str(number)+'/splitByregion_data/'+save_path + '.csv')

def draw_cheshu_time(dates,linestyle_color_list,restrict_time,number,save_path,jiedian_split_time_work,jiedian_split_time_nonwork,ylimit):
    '''
    按小时分布的优化前出行车数和优化后出行车数（分时，优化使用相同时间阈值）
    :param dates:
    :param linestyle_color_list:
    :param restrict_time:
    :param number:
    :param save_path:
    :param jiedian_split_time_work:
    :param jiedian_split_time_nonwork:
    :param ylimit:
    :return:
    '''
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
                filePathList = os.listdir('./data/PathList/' + str(restrict_time) + ' ' + str(number) + '/splitBytime/' + str(dates[date_index]))
                for allDir in filePathList:
                    if '_'+str(jiedian_split_time_nonwork[t])+'_'+str(jiedian_split_time_nonwork[t+1])+'_'  in allDir:
                        child = os.path.join('%s/%s' % ('./data/PathList/' + str(restrict_time) + ' ' + str(number) + '/splitBytime/' + str(dates[date_index]), allDir))
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

            df = pd.DataFrame(data=np.array([y,y1]).T, index=x,
                              columns=['Minimized vehicle number' + '(' + str(dates[date_index]) + ')',
                                       'Current on-road vehicle number' + '(' + str(dates[date_index]) + ')'])
            df.to_csv(
                './picture/' + str(restrict_time) + ' ' + str(number) + '/splitBytime_data/' + save_path + '.csv')
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
                filePathList = os.listdir('./data/PathList/' + str(restrict_time) + ' ' + str(number) + '/splitBytime/' + str(dates[date_index]))
                for allDir in filePathList:
                    if '_'+str(jiedian_split_time_work[t])+'_'+str(jiedian_split_time_work[t+1])+'_' in allDir:
                        child = os.path.join('%s/%s' % ('./data/PathList/' + str(restrict_time) + ' ' + str(number) + '/splitBytime/' + str(dates[date_index]), allDir))
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

            df = pd.DataFrame(data=np.array([y,y1]).T, index=x,
                              columns=['Minimized vehicle number' + '(' + str(dates[date_index]) + ')',
                                       'Current on-road vehicle number' + '(' + str(dates[date_index]) + ')'])
            df.to_csv(
                './picture/' + str(restrict_time) + ' ' + str(number) + '/splitBytime_data/' + save_path + '.csv')

def draw_cheshu_time_xianyou_zaike_kongshi(dates,linestyle_color_list,restrict_time,number,save_path,jiedian_split_time_work,jiedian_split_time_nonwork,ylimit):
    df_kakou_time = pd.read_csv(open('./data/kakou_time.csv'), dtype={'origin_kid': str, 'des_kid': str})
    df_kakou_time = df_kakou_time[df_kakou_time['time'] <= restrict_time]  # 卡口时间限制900s

    for date_index in range(len(dates)):
        if '10' in str(dates[date_index]) or '11' in str(dates[date_index]):
            x = np.array(list(range(24))) + [0.5] * 24
            y = np.array([0] * len(x))
            x1 = np.array(list(range(24))) + [0.5] * 24
            y1 = np.array([0] * len(x))
            for t in range(len(jiedian_split_time_nonwork) - 1):
                feiyunyingche_jiedian = pd.read_csv(open('./data/节点/'+ str(dates[date_index]) + '_jiedian_'+str(jiedian_split_time_nonwork[t])+'_'+str(jiedian_split_time_nonwork[t+1])+'.csv'))

                paths = []
                filePathList = os.listdir('./data/PathList/' + str(restrict_time) + ' ' + str(number) + '/splitBytime/' + str(dates[date_index]))
                for allDir in filePathList:
                    if '_'+str(jiedian_split_time_nonwork[t])+'_'+str(jiedian_split_time_nonwork[t+1])+'_'  in allDir:
                        child = os.path.join('%s/%s' % ('./data/PathList/' + str(restrict_time) + ' ' + str(number) + '/splitBytime/' + str(dates[date_index]), allDir))
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

            df = pd.DataFrame(data=np.array([y,y1]).T, index=x,
                              columns=['zaike+kongshi' + '(' + str(dates[date_index]) + ')',
                                       'Current on-road vehicle number' + '(' + str(dates[date_index]) + ')'])
            df.to_csv(
                './picture/' + str(restrict_time) + ' ' + str(number) + '/splitBytime_data/' + save_path + '.csv')
        else:
            x = np.array(list(range(24))) + [0.5] * 24
            y = np.array([0] * len(x))
            x1 = np.array(list(range(24))) + [0.5] * 24
            y1 = np.array([0] * len(x))
            for t in range(len(jiedian_split_time_work) - 1):
                feiyunyingche_jiedian = pd.read_csv(open('./data/节点/'+ str(dates[date_index]) + '_jiedian_'+str(jiedian_split_time_work[t])+'_'+str(jiedian_split_time_work[t+1])+'.csv'))

                paths = []
                filePathList = os.listdir('./data/PathList/' + str(restrict_time) + ' ' + str(number) + '/splitBytime/' + str(dates[date_index]))
                for allDir in filePathList:
                    if '_'+str(jiedian_split_time_work[t])+'_'+str(jiedian_split_time_work[t+1])+'_' in allDir:
                        child = os.path.join('%s/%s' % ('./data/PathList/' + str(restrict_time) + ' ' + str(number) + '/splitBytime/' + str(dates[date_index]), allDir))
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

            df = pd.DataFrame(data=np.array([y,y1]).T, index=x,
                              columns=['zaike+kongshi' + '(' + str(dates[date_index]) + ')',
                                       'Current on-road vehicle number' + '(' + str(dates[date_index]) + ')'])
            df.to_csv(
                './picture/' + str(restrict_time) + ' ' + str(number) + '/splitBytime_data/' + save_path + '.csv')


def draw_zhuangtai(date,restrict_time,number,save_path,ylimit):
    '''
    按秒分布的优化后车辆状态
    :param date:
    :param restrict_time:
    :param number:
    :param save_path:
    :param ylimit:
    :return:
    '''
    feiyunyingche_jiedian = pd.read_csv(open('./data/节点/'+str(date)+'_jiedian.csv'))
    feiyunyingche_jiedian['start_time'] = (feiyunyingche_jiedian['start_time']).astype(int)
    feiyunyingche_jiedian['end_time'] = (feiyunyingche_jiedian['end_time']).astype(int)
    feiyunyingche_jiedian['start_kid'] = (feiyunyingche_jiedian['start_kid']).astype(str)
    feiyunyingche_jiedian['end_kid'] = (feiyunyingche_jiedian['end_kid']).astype(str)
    df_kakou_time = pd.read_csv(open('./data/kakou_time.csv'),dtype={'origin_kid': str, 'des_kid': str})

    df_kakou_time = df_kakou_time[df_kakou_time['time'] <= restrict_time]  # 卡口时间限制900s

    paths = []
    filePathList = os.listdir('./data/PathList/'+str(restrict_time)+' '+str(number)+'/Nosplit/'+str(date))
    for allDir in filePathList:
        child = os.path.join('%s/%s' % ('./data/PathList/'+str(restrict_time)+' '+str(number)+'/Nosplit/'+str(date), allDir))
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

    x = np.array(list(range(24 * 60 * 60)))
    y = np.array([0] * len(x))  # 总共活跃时间
    y1 = np.array([0] * len(x))  # 载客状态
    y2 = np.array([0] * len(x))  # 路上行驶时间
    y3 = np.array([0] * len(x))  # 等待时间
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

    print('城区当日峰值车辆数（活跃状态）：' + str(date) + '  ' + str(y.max()))
    print('城区当日峰值车辆数（载客状态）：' + str(date) + '  ' + str(y1.max()))
    print('城区当日峰值车辆数（行驶状态）：' + str(date) + '  ' + str(y2.max()))
    print('城区当日峰值车辆数（等待状态）：' + str(date) + '  ' + str(y3.max()))
    print('载客率：' + str(date) + '  ' + str(np.trapz(y1)/np.trapz(y)))
    print('空驶率：' + str(date) + '  ' + str(np.trapz(y2) / np.trapz(y)))
    print('等待率：' + str(date) + '  ' + str(np.trapz(y3) / np.trapz(y)))

    df = pd.DataFrame(data=np.array([y, y1,y2,y3]).T, index=x,
                      columns=['活跃状态','载客状态','空驶状态','等待状态'])
    df.to_csv('./picture/'+str(restrict_time)+' '+str(number)+'/Nosplit_data/'+save_path + '.csv')


def draw_zhuangtai_region(date,restrict_time,number,region,save_path,ylimit):
    '''
    按秒分布的优化后车辆状态（分区）
    :param date:
    :param restrict_time:
    :param number:
    :param region:
    :param save_path:
    :param ylimit:
    :return:
    '''
    feiyunyingche_jiedian = pd.read_csv(open('./data/节点/'+str(date)+'_jiedian.csv'))
    feiyunyingche_jiedian['start_time'] = (feiyunyingche_jiedian['start_time']).astype(int)
    feiyunyingche_jiedian['end_time'] = (feiyunyingche_jiedian['end_time']).astype(int)
    feiyunyingche_jiedian['start_kid'] = (feiyunyingche_jiedian['start_kid']).astype(str)
    feiyunyingche_jiedian['end_kid'] = (feiyunyingche_jiedian['end_kid']).astype(str)
    df_kakou_time = pd.read_csv(open('./data/kakou_time.csv'),dtype={'origin_kid': str, 'des_kid': str})

    df_kakou_time = df_kakou_time[df_kakou_time['time'] <= restrict_time]  # 卡口时间限制900s

    paths = np.load('./data/PathList/' + str(restrict_time) + ' ' + str(number) + '/splitByregion/' + str(date) + '/' + str(date) + '_path_' + region + '.npy', allow_pickle=True)

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

    x = np.array(list(range(24 * 60 * 60)))
    y = np.array([0] * len(x))  # 总共活跃时间
    y1 = np.array([0] * len(x))  # 载客状态
    y2 = np.array([0] * len(x))  # 路上行驶时间
    y3 = np.array([0] * len(x))  # 等待时间
    for i in paths:
        y[feiyunyingche_jiedian.iloc[i[0], starttime_ord]:feiyunyingche_jiedian.iloc[i[-1], endtime_ord]] = y[feiyunyingche_jiedian.iloc[i[0], starttime_ord]:feiyunyingche_jiedian.iloc[i[-1], endtime_ord]] + 1
        for j in i:
            y1[feiyunyingche_jiedian.iloc[j, starttime_ord]:feiyunyingche_jiedian.iloc[j, endtime_ord]] = y1[feiyunyingche_jiedian.iloc[j, starttime_ord]:feiyunyingche_jiedian.iloc[j, endtime_ord]] + 1

    for i in paths:
        for j in range(len(i) - 1):
            a = feiyunyingche_jiedian.iloc[i[j], endtime_ord]
            b = df_kakou_time[(df_kakou_time['origin_kid'] == feiyunyingche_jiedian.iloc[i[j], end_kid_ord]) & (df_kakou_time['des_kid'] == feiyunyingche_jiedian.iloc[i[j + 1], start_kid_ord])].iloc[0]['time']
            c = feiyunyingche_jiedian.iloc[i[j + 1], starttime_ord]
            y2[a:(a + b)] = y2[a:(a + b)] + 1
            y3[(a + b):c] = y3[(a + b):c] + 1

    print(str(region) + '当日峰值车辆数（活跃状态）：' + str(date) + '  ' + str(y.max()))
    print(str(region) + '当日峰值车辆数（载客状态）：' + str(date) + '  ' + str(y1.max()))
    print(str(region) + '当日峰值车辆数（行驶状态）：' + str(date) + '  ' + str(y2.max()))
    print(str(region) + '当日峰值车辆数（等待状态）：' + str(date) + '  ' + str(y3.max()))
    print('载客率：' + str(date) + '  ' + str(np.trapz(y1) / np.trapz(y)))
    print('空驶率：' + str(date) + '  ' + str(np.trapz(y2) / np.trapz(y)))
    print('等待率：' + str(date) + '  ' + str(np.trapz(y3) / np.trapz(y)))

    df = pd.DataFrame(data=np.array([y, y1,y2,y3]).T, index=x,
                      columns=['活跃状态','载客状态','空驶状态','等待状态'])
    df.to_csv('./picture/'+str(restrict_time)+' '+str(number)+'/splitByregion_data/'+save_path + '.csv')


def draw_zhuangtai_time(date,restrict_time,number,save_path,jiedian_split_time_work,jiedian_split_time_nonwork,ylimit):
    '''
    按秒分布的优化后车辆状态（分时，优化使用相同时间阈值）
    :param date:
    :param restrict_time:
    :param number:
    :param save_path:
    :param jiedian_split_time_work:
    :param jiedian_split_time_nonwork:
    :param ylimit:
    :return:
    '''
    df_kakou_time = pd.read_csv(open('./data/kakou_time.csv'), dtype={'origin_kid': str, 'des_kid': str})
    df_kakou_time = df_kakou_time[df_kakou_time['time'] <= restrict_time]  # 卡口时间限制900s
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
            filePathList = os.listdir('./data/PathList/'+str(restrict_time)+' '+str(number)+'/splitBytime/'+str(date))
            for allDir in filePathList:
                if '_'+str(jiedian_split_time_nonwork[t])+'_'+str(jiedian_split_time_nonwork[t+1])+'_'  in allDir:
                    child = os.path.join('%s/%s' % ('./data/PathList/'+str(restrict_time)+' '+str(number)+'/splitBytime/'+str(date), allDir))
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

        df = pd.DataFrame(data=np.array([y, y1,y2,y3]).T, index=x,
                          columns=['活跃状态', '载客状态', '空驶状态', '等待状态'])
        df.to_csv('./picture/'+str(restrict_time)+' '+str(number)+'/splitBytime_data/'+save_path + '.csv')
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
                './data/PathList/' + str(restrict_time) + ' ' + str(number) + '/splitBytime/' + str(date))
            for allDir in filePathList:
                if '_'+str(jiedian_split_time_work[t])+'_'+str(jiedian_split_time_work[t+1])+'_'  in allDir:
                    child = os.path.join('%s/%s' % (
                    './data/PathList/' + str(restrict_time) + ' ' + str(number) + '/splitBytime/' + str(date), allDir))
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

        df = pd.DataFrame(data=np.array([y, y1,y2,y3]).T, index=x,
                          columns=['活跃状态', '载客状态', '空驶状态', '等待状态'])
        df.to_csv('./picture/'+str(restrict_time)+' '+str(number)+'/splitBytime_data/'+save_path + '.csv')



# def draw_kongzhi(dates,linestyle_color_list,restrict_time,number,save_path,ylimit):
#     fig = plt.figure(figsize=(18, 12), dpi=1000)
#     for date_index in range(len(dates)):
#         feiyunyingche_jiedian = pd.read_csv(open('./data/节点/'+str(dates[date_index])+'_jiedian.csv'))
#         feiyunyingche_jiedian['start_time'] = (feiyunyingche_jiedian['start_time'] // 3600).astype(int)
#         feiyunyingche_jiedian['end_time'] = (feiyunyingche_jiedian['end_time'] // 3600).astype(int)
#
#         paths = []
#         filePathList = os.listdir('./data/PathList/'+str(restrict_time)+' '+str(number)+'/Nosplit/'+str(dates[date_index]))
#         for allDir in filePathList:
#             child = os.path.join('%s/%s' % ('./data/PathList/'+str(restrict_time)+' '+str(number)+'/Nosplit/'+str(dates[date_index]), allDir))
#             numpy_path = np.load(child, allow_pickle=True)
#             paths.append(numpy_path)
#
#         x = np.array(list(range(24)))+[0.5]*24
#         y = np.array([0] * len(x))
#         x1 = np.array(list(range(24)))+[0.5]*24
#         y1 = np.array([0] * len(x))
#         endtime_ord = -1
#         starttime_ord = -1
#         for i in range(len(feiyunyingche_jiedian.columns)):
#             if feiyunyingche_jiedian.columns[i] == 'end_time':
#                 endtime_ord = i
#             if feiyunyingche_jiedian.columns[i] == 'start_time':
#                 starttime_ord = i
#
#         for part in paths:
#             for i in part:
#                 y[feiyunyingche_jiedian.iloc[i[0], starttime_ord]:feiyunyingche_jiedian.iloc[i[-1], endtime_ord] + 1] = y[feiyunyingche_jiedian.iloc[i[0], starttime_ord]:feiyunyingche_jiedian.iloc[i[-1], endtime_ord] + 1] + 1
#
#         for i in range(len(feiyunyingche_jiedian)):
#             y1[feiyunyingche_jiedian.iloc[i,starttime_ord]:feiyunyingche_jiedian.iloc[i, endtime_ord] + 1]=y1[feiyunyingche_jiedian.iloc[i,starttime_ord]:feiyunyingche_jiedian.iloc[i, endtime_ord] + 1] + 1
#
#         youhuahou_num = 0
#         for part in paths:
#             for i in part:
#                 youhuahou_num += 1
#         youhuaqian_num = len(set(feiyunyingche_jiedian['car_id']))
#
#         plt.plot(  # 画折线图y
#             x, (youhuahou_num-np.array(y))/youhuahou_num,
#             label='Optimized'+'('+str(dates[date_index])+')',
#             lw=5,  # 折线图的线条宽度
#             linestyle=linestyle_color_list[date_index*len(dates)][0],
#             color=linestyle_color_list[date_index*len(dates)][1],
#             marker='o',
#             markerfacecolor='k'
#         )
#
#         plt.plot(  # 画折线图y
#             x1, (youhuaqian_num-np.array(y1))/youhuaqian_num,
#             label='Current'+'('+str(dates[date_index])+')',
#             lw=5,  # 折线图的线条宽度
#             linestyle=linestyle_color_list[date_index*len(dates)+1][0],
#             color=linestyle_color_list[date_index*len(dates)+1][1],
#             marker='o',
#             markerfacecolor='k'
#         )
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
#     plt.savefig('./picture/'+str(restrict_time)+' '+str(number)+'/Nosplit/'+save_path)
#     plt.close()
#
# def draw_kongzhi_region(dates,linestyle_color_list,restrict_time,number,region,save_path,ylimit):
#     fig = plt.figure(figsize=(18, 12), dpi=1000)
#     for date_index in range(len(dates)):
#         feiyunyingche_jiedian = pd.read_csv(open('./data/节点/'+str(dates[date_index])+'_jiedian.csv'))
#         feiyunyingche_jiedian['start_time'] = (feiyunyingche_jiedian['start_time'] // 3600).astype(int)
#         feiyunyingche_jiedian['end_time'] = (feiyunyingche_jiedian['end_time'] // 3600).astype(int)
#
#         paths = np.load('./data/PathList/'+str(restrict_time)+' '+str(number)+'/splitByregion/'+str(dates[date_index])+'/'+str(dates[date_index])+'_path_'+region+'.npy', allow_pickle=True)
#         x = np.array(list(range(24)))+[0.5]*24
#         y = np.array([0] * len(x))
#         x1 = np.array(list(range(24)))+[0.5]*24
#         y1 = np.array([0] * len(x))
#         endtime_ord = -1
#         starttime_ord = -1
#         for i in range(len(feiyunyingche_jiedian.columns)):
#             if feiyunyingche_jiedian.columns[i] == 'end_time':
#                 endtime_ord = i
#             if feiyunyingche_jiedian.columns[i] == 'start_time':
#                 starttime_ord = i
#
#         for i in paths:
#             y[feiyunyingche_jiedian.iloc[i[0], starttime_ord]:feiyunyingche_jiedian.iloc[i[-1], endtime_ord] + 1] = y[feiyunyingche_jiedian.iloc[i[0], starttime_ord]:feiyunyingche_jiedian.iloc[i[-1], endtime_ord] + 1] + 1
#
#         feiyunyingche_jiedian_region = pd.read_csv(open('./data/节点/' + str(dates[date_index]) + '_jiedian_'+region+'.csv'))
#         feiyunyingche_jiedian_region['start_time'] = (feiyunyingche_jiedian_region['start_time'] // 3600).astype(int)
#         feiyunyingche_jiedian_region['end_time'] = (feiyunyingche_jiedian_region['end_time'] // 3600).astype(int)
#         endtime_ord = -1
#         starttime_ord = -1
#         for i in range(len(feiyunyingche_jiedian_region.columns)):
#             if feiyunyingche_jiedian_region.columns[i] == 'end_time':
#                 endtime_ord = i
#             if feiyunyingche_jiedian_region.columns[i] == 'start_time':
#                 starttime_ord = i
#         for i in range(len(feiyunyingche_jiedian_region)):
#             y1[feiyunyingche_jiedian_region.iloc[i,starttime_ord]:feiyunyingche_jiedian_region.iloc[i, endtime_ord] + 1]=y1[feiyunyingche_jiedian_region.iloc[i,starttime_ord]:feiyunyingche_jiedian_region.iloc[i, endtime_ord] + 1] + 1
#
#         youhuahou_num = 0
#         for i in paths:
#             youhuahou_num += 1
#         youhuaqian_num = len(set(feiyunyingche_jiedian_region['car_id']))
#
#         plt.plot(  # 画折线图y
#             x, (youhuahou_num-np.array(y))/youhuahou_num,
#             label='Optimized'+'('+str(dates[date_index])+')',
#             lw=5,  # 折线图的线条宽度
#             linestyle=linestyle_color_list[date_index*len(dates)][0],
#             color=linestyle_color_list[date_index*len(dates)][1],
#             marker='o',
#             markerfacecolor='k'
#         )
#
#         plt.plot(  # 画折线图y
#             x1, (youhuaqian_num-np.array(y1))/youhuaqian_num,
#             label='Current'+'('+str(dates[date_index])+')',
#             lw=5,  # 折线图的线条宽度
#             linestyle=linestyle_color_list[date_index*len(dates)+1][0],
#             color=linestyle_color_list[date_index*len(dates)+1][1],
#             marker='o',
#             markerfacecolor='k'
#         )
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
#     plt.savefig('./picture/'+str(restrict_time)+' '+str(number)+'/splitByregion/'+save_path)
#     plt.close()
#
# def draw_kongzhi_time(dates,linestyle_color_list,restrict_time,number,save_path,jiedian_split_time_work,jiedian_split_time_nonwork,ylimit):
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
#                 filePathList = os.listdir('./data/PathList/'+str(restrict_time)+' '+str(number)+'/splitBytime/'+str(dates[date_index]))
#                 for allDir in filePathList:
#                     if '_'+str(jiedian_split_time_nonwork[t])+'_'+str(jiedian_split_time_nonwork[t+1])+'_'  in allDir:
#                         child = os.path.join('%s/%s' % ('./data/PathList/'+str(restrict_time)+' '+str(number)+'/splitBytime/'+str(dates[date_index]), allDir))
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
#                     './data/PathList/' + str(restrict_time) + ' ' + str(number) + '/splitBytime/' + str(
#                         dates[date_index]))
#                 for allDir in filePathList:
#                     if '_'+str(jiedian_split_time_work[t])+'_'+str(jiedian_split_time_work[t+1])+'_'  in allDir:
#                         child = os.path.join('%s/%s' % (
#                         './data/PathList/' + str(restrict_time) + ' ' + str(number) + '/splitBytime/' + str(
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
#     plt.savefig('./picture/'+str(restrict_time)+' '+str(number)+'/splitBytime/'+save_path)
#     plt.close()

if __name__ == '__main__':
    global_config = Config('./config.ini')
    source_file = global_config.getRaw('设置条件', 'source_file')
    source_file = json.loads(source_file)  # str转list
    jiedian_split_time_work = global_config.getRaw('设置条件', 'jiedian_split_time_work')
    jiedian_split_time_work = json.loads(jiedian_split_time_work)
    jiedian_split_time_nonwork = global_config.getRaw('设置条件', 'jiedian_split_time_nonwork')
    jiedian_split_time_nonwork = json.loads(jiedian_split_time_nonwork)
    draw(300,40000,jiedian_split_time_work,jiedian_split_time_nonwork)




