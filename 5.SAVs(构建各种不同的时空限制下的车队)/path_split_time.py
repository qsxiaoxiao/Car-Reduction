# -*- coding:utf-8 -*-
#author:jeremy

import pandas as pd
import networkx as nx
import datetime
import sys
from networkx.algorithms import bipartite
import os
import numpy as np
from config import Config
import time
from pathlib import Path
from utils import create_dir,write_log
import json
import gc


def get_path_split_time(source_file):
    global_config = Config('./config.ini')
    source_data_path = global_config.getRaw('设置条件', 'source_data_path')
    store_data_path = global_config.getRaw('设置条件', 'store_data_path')
    jiedian_split_time_work = global_config.getRaw('设置条件', 'jiedian_split_time_work')
    jiedian_split_time_work = json.loads(jiedian_split_time_work)
    jiedian_split_time_nonwork = global_config.getRaw('设置条件', 'jiedian_split_time_nonwork')
    jiedian_split_time_nonwork = json.loads(jiedian_split_time_nonwork)
    restrict_time = int(global_config.getRaw('设置条件', 'restrict_time'))  # 卡口时间限制900s
    number = int(global_config.getRaw('设置条件', 'number'))  # 一次计算5w节点
    create_dir(store_data_path + '/' + str(restrict_time) + ' ' + str(number))
    create_dir(store_data_path + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'splitBytime')


    df_kakou_time = pd.read_csv(open(r'./data/kakou_time.csv'),dtype={'origin_kid': str, 'des_kid': str})
    df_kakou_time = df_kakou_time[df_kakou_time['time'] <= restrict_time]
    while True:
        error = 0
        for date in source_file:
            create_dir(store_data_path + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'splitBytime' + '/' + str(date))
            if '10' in str(date) or '11' in str(date):
                # 非工作日
                for t in range(len(jiedian_split_time_nonwork) - 1):
                    df_jiedian = pd.read_csv(open(source_data_path+'/' + str(date)+'_jiedian_'+str(jiedian_split_time_nonwork[t])+'_'+str(jiedian_split_time_nonwork[t+1])+'.csv'),
                                             dtype={'start_kid': str, 'end_kid': str, 'car_id': str})

                    xunhuan_cishu=(len(df_jiedian)//number)+1
                    for i_slic in range(xunhuan_cishu):
                    # for i_slic in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]:

                        path_file = Path(store_data_path + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'splitBytime' + '/' + str(date) + '/' + str(date) + '_path_' + str(jiedian_split_time_nonwork[t])+'_'+str(jiedian_split_time_nonwork[t+1])+'_'+ str(number) + '_' + str(restrict_time) + '_' + str(i_slic + 1) + '.npy')
                        if path_file.exists():
                            print('存在文件：'+store_data_path + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'splitBytime' + '/' + str(date) + '/' + str(date) + '_path_' + str(jiedian_split_time_nonwork[t])+'_'+str(jiedian_split_time_nonwork[t+1])+'_'+ str(number) + '_' + str(restrict_time) + '_' + str(i_slic + 1) + '.npy')
                        else:
                            try:
                                print(str(number)+'节点')
                                write_log(str(number)+'节点')
                                print('时间限制：'+str(restrict_time))
                                write_log('时间限制：'+str(restrict_time))

                                # print('第31块节点')
                                print('第'+str(i_slic)+'块节点（0-'+str(xunhuan_cishu-1)+'）')
                                write_log('第'+str(i_slic)+'块节点（0-'+str(xunhuan_cishu-1)+'）')
                                if i_slic<xunhuan_cishu-1:
                                    df_jiedian1 = df_jiedian[i_slic*number:(i_slic+1)*number]
                                else:
                                    df_jiedian1 = df_jiedian[i_slic * number:]
                                df_jiedian1['jiedian_id'] = df_jiedian1.index

                                print('df_jiedian长度：'+str(len(df_jiedian)))
                                write_log('df_jiedian长度：'+str(len(df_jiedian)))
                                print('df_jiedian1长度：'+str(len(df_jiedian1)))
                                write_log('df_jiedian1长度：'+str(len(df_jiedian1)))

                                df_q_kakou = pd.merge(df_jiedian1, df_kakou_time, left_on='end_kid', right_on='origin_kid', how='inner')
                                df_q_kakou['q_kakou_time'] = df_q_kakou['time'] + df_q_kakou['end_time']
                                ######获取列的索引
                                df_q_kakou_columns = df_q_kakou.columns.values
                                for c in range(len(df_q_kakou_columns)):
                                    if df_q_kakou_columns[c] == 'des_kid':
                                        des_kid_ord = c
                                    if df_q_kakou_columns[c] == 'q_kakou_time':
                                        q_kakou_time_ord = c
                                    if df_q_kakou_columns[c] == 'jiedian_id':
                                        jiedian_id_ord = c
                                print('行数：'+str(len(df_q_kakou)))
                                write_log('行数：'+str(len(df_q_kakou)))
                                print('df_q_kakou完成')
                                write_log('df_q_kakou完成')

                                # G = nx.Graph()
                                # top_nodes=set()
                                edge=[]
                                for i in range(len(df_q_kakou)):
                                    # print(i)
                                    df_h_jiedian = df_jiedian1[(df_jiedian1['start_kid'] == df_q_kakou.iloc[i, des_kid_ord]) & (
                                                df_jiedian1['start_time'] > df_q_kakou.iloc[i, q_kakou_time_ord])]
                                    df_h_jiedian_index = list(df_h_jiedian.index)
                                    for h_index in df_h_jiedian_index:
                                        edge.append([str(df_q_kakou.iloc[i, jiedian_id_ord]), str(h_index) + '^'])
                                        # G.add_edges_from([[str(df_q_kakou.iloc[i, jiedian_id_ord]), str(h_index) + '^']])
                                        # top_nodes.add(str(df_q_kakou.iloc[i, jiedian_id_ord]))
                                print('边计算完成')
                                write_log('边计算完成')

                                G = nx.Graph()
                                ######计算二分图中一个部分的点
                                top_nodes=[e[0] for e in edge]
                                # top_nodes = list(top_nodes)
                                top_nodes = list(set(top_nodes))
                                print('顶点数：'+str(len(top_nodes)))
                                write_log('顶点数：'+str(len(top_nodes)))

                                ######二分图计算最大匹配
                                G.add_edges_from(edge)
                                print('边数：'+str(len(G.edges())))
                                write_log('边数：'+str(len(G.edges())))
                                matching = nx.bipartite.eppstein_matching(G, top_nodes=top_nodes)  # 快
                                print('重复的匹配数：'+str(len(matching)))
                                write_log('重复的匹配数：'+str(len(matching)))
                                del edge

                                ######去除最大匹配中的重复值
                                new_match = []
                                for m in matching:
                                    if '^' in m:
                                        new_match.append((int(matching[m]), int(m[:-1])))
                                print('不重复匹配数：'+str(len(new_match)))
                                write_log('不重复匹配数：'+str(len(new_match)))

                                ######将匹配形成路径
                                new_match = np.array(new_match)
                                DiG = nx.DiGraph()
                                DiG.add_edges_from(new_match)
                                path_heji = list(nx.topological_sort(DiG))  # path合在一起
                                print('路径覆盖节点数：'+str(len(path_heji)))
                                write_log('路径覆盖节点数：'+str(len(path_heji)))
                                path = [] # 存储覆盖路径
                                q = 0
                                for i in range(len(path_heji)):
                                    if path_heji[i] not in new_match[:, 0]:
                                        path.append(path_heji[q:i + 1])
                                        q = i + 1
                                print('路径数（未添加单个节点）：'+str(len(path)))
                                write_log('路径数（未添加单个节点）：'+str(len(path)))
                                print('第一条路径长度：' + str(len(path[0])))

                                ######计算没有被匹配的点，单个节点为一条轨迹的节点
                                dange = set(df_jiedian1.index) - set(path_heji)  # 存储单个的节点
                                print('单个节点数：'+str(len(dange)))
                                write_log('单个节点数：'+str(len(dange)))
                                for d in dange:
                                    path.append([d])
                                print('路径数（添加单个节点）：'+str(len(path)))
                                write_log('路径数（添加单个节点）：'+str(len(path)))

                                print('车辆数：'+str(len(set(df_jiedian1['car_id']))))
                                write_log('车辆数：'+str(len(set(df_jiedian1['car_id']))))
                                numpy_path = np.array(path)
                                np.save(store_data_path + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'splitBytime' + '/' + str(date) + '/' + str(date) + '_path_' + str(jiedian_split_time_nonwork[t])+'_'+str(jiedian_split_time_nonwork[t+1])+'_'+ str(number) + '_' + str(restrict_time) + '_' + str(i_slic + 1) + '.npy', numpy_path)
                                print('存储路径完成')
                                write_log('存储路径完成')
                                del df_jiedian1, df_q_kakou, matching, new_match
                                gc.collect()
                            except Exception as e:
                                error = error + 1
                                print(e)
                                write_log(str(e))
            else:
                # 工作日
                for t in range(len(jiedian_split_time_work) - 1):
                    df_jiedian = pd.read_csv(open(source_data_path + '/' + str(date) + '_jiedian_' + str(jiedian_split_time_work[t]) + '_' + str(jiedian_split_time_work[t + 1]) + '.csv'),dtype={'start_kid': str, 'end_kid': str, 'car_id': str})

                    xunhuan_cishu = (len(df_jiedian) // number) + 1
                    for i_slic in range(xunhuan_cishu):
                        # for i_slic in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]:

                        path_file = Path(store_data_path + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'splitBytime' + '/' + str(date) + '/' + str(date) + '_path_' + str(jiedian_split_time_work[t]) + '_' + str(jiedian_split_time_work[t + 1]) + '_' + str(number) + '_' + str(restrict_time) + '_' + str(i_slic + 1) + '.npy')
                        if path_file.exists():
                            print('存在文件：' + store_data_path + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'splitBytime' + '/' + str(date) + '/' + str(date) + '_path_' + str(jiedian_split_time_work[t]) + '_' + str(jiedian_split_time_work[t + 1]) + '_' + str(number) + '_' + str(restrict_time) + '_' + str(i_slic + 1) + '.npy')
                        else:
                            try:
                                print(str(number) + '节点')
                                write_log(str(number) + '节点')
                                print('时间限制：' + str(restrict_time))
                                write_log('时间限制：' + str(restrict_time))

                                # print('第31块节点')
                                print('第' + str(i_slic) + '块节点（0-' + str(xunhuan_cishu - 1) + '）')
                                write_log('第' + str(i_slic) + '块节点（0-' + str(xunhuan_cishu - 1) + '）')
                                if i_slic < xunhuan_cishu - 1:
                                    df_jiedian1 = df_jiedian[i_slic * number:(i_slic + 1) * number]
                                else:
                                    df_jiedian1 = df_jiedian[i_slic * number:]
                                df_jiedian1['jiedian_id'] = df_jiedian1.index

                                print('df_jiedian长度：' + str(len(df_jiedian)))
                                write_log('df_jiedian长度：' + str(len(df_jiedian)))
                                print('df_jiedian1长度：' + str(len(df_jiedian1)))
                                write_log('df_jiedian1长度：' + str(len(df_jiedian1)))

                                df_q_kakou = pd.merge(df_jiedian1, df_kakou_time, left_on='end_kid',
                                                      right_on='origin_kid', how='inner')
                                df_q_kakou['q_kakou_time'] = df_q_kakou['time'] + df_q_kakou['end_time']
                                ######获取列的索引
                                df_q_kakou_columns = df_q_kakou.columns.values
                                for c in range(len(df_q_kakou_columns)):
                                    if df_q_kakou_columns[c] == 'des_kid':
                                        des_kid_ord = c
                                    if df_q_kakou_columns[c] == 'q_kakou_time':
                                        q_kakou_time_ord = c
                                    if df_q_kakou_columns[c] == 'jiedian_id':
                                        jiedian_id_ord = c
                                print('行数：' + str(len(df_q_kakou)))
                                write_log('行数：' + str(len(df_q_kakou)))
                                print('df_q_kakou完成')
                                write_log('df_q_kakou完成')

                                # G = nx.Graph()
                                # top_nodes=set()
                                edge = []
                                for i in range(len(df_q_kakou)):
                                    # print(i)
                                    df_h_jiedian = df_jiedian1[
                                        (df_jiedian1['start_kid'] == df_q_kakou.iloc[i, des_kid_ord]) & (
                                                df_jiedian1['start_time'] > df_q_kakou.iloc[i, q_kakou_time_ord])]
                                    df_h_jiedian_index = list(df_h_jiedian.index)
                                    for h_index in df_h_jiedian_index:
                                        edge.append([str(df_q_kakou.iloc[i, jiedian_id_ord]), str(h_index) + '^'])
                                        # G.add_edges_from([[str(df_q_kakou.iloc[i, jiedian_id_ord]), str(h_index) + '^']])
                                        # top_nodes.add(str(df_q_kakou.iloc[i, jiedian_id_ord]))
                                print('边计算完成')
                                write_log('边计算完成')

                                G = nx.Graph()
                                ######计算二分图中一个部分的点
                                top_nodes = [e[0] for e in edge]
                                # top_nodes = list(top_nodes)
                                top_nodes = list(set(top_nodes))
                                print('顶点数：' + str(len(top_nodes)))
                                write_log('顶点数：' + str(len(top_nodes)))

                                ######二分图计算最大匹配
                                G.add_edges_from(edge)
                                print('边数：' + str(len(G.edges())))
                                write_log('边数：' + str(len(G.edges())))
                                matching = nx.bipartite.eppstein_matching(G, top_nodes=top_nodes)  # 快
                                print('重复的匹配数：' + str(len(matching)))
                                write_log('重复的匹配数：' + str(len(matching)))
                                del edge

                                ######去除最大匹配中的重复值
                                new_match = []
                                for m in matching:
                                    if '^' in m:
                                        new_match.append((int(matching[m]), int(m[:-1])))
                                print('不重复匹配数：' + str(len(new_match)))
                                write_log('不重复匹配数：' + str(len(new_match)))

                                ######将匹配形成路径
                                new_match = np.array(new_match)
                                DiG = nx.DiGraph()
                                DiG.add_edges_from(new_match)
                                path_heji = list(nx.topological_sort(DiG))  # path合在一起
                                print('路径覆盖节点数：' + str(len(path_heji)))
                                write_log('路径覆盖节点数：' + str(len(path_heji)))
                                path = []  # 存储覆盖路径
                                q = 0
                                for i in range(len(path_heji)):
                                    if path_heji[i] not in new_match[:, 0]:
                                        path.append(path_heji[q:i + 1])
                                        q = i + 1
                                print('路径数（未添加单个节点）：' + str(len(path)))
                                write_log('路径数（未添加单个节点）：' + str(len(path)))
                                print('第一条路径长度：' + str(len(path[0])))

                                ######计算没有被匹配的点，单个节点为一条轨迹的节点
                                dange = set(df_jiedian1.index) - set(path_heji)  # 存储单个的节点
                                print('单个节点数：' + str(len(dange)))
                                write_log('单个节点数：' + str(len(dange)))
                                for d in dange:
                                    path.append([d])
                                print('路径数（添加单个节点）：' + str(len(path)))
                                write_log('路径数（添加单个节点）：' + str(len(path)))

                                print('车辆数：' + str(len(set(df_jiedian1['car_id']))))
                                write_log('车辆数：' + str(len(set(df_jiedian1['car_id']))))
                                numpy_path = np.array(path)
                                np.save(store_data_path + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'splitBytime' + '/' + str(date) + '/' + str(date) + '_path_' + str(jiedian_split_time_work[t]) + '_' + str(jiedian_split_time_work[t + 1]) + '_' + str(number) + '_' + str(restrict_time) + '_' + str(i_slic + 1) + '.npy', numpy_path)
                                print('存储路径完成')
                                write_log('存储路径完成')
                                del df_jiedian1, df_q_kakou, matching, new_match
                                gc.collect()
                            except Exception as e:
                                error = error + 1
                                print(e)
                                write_log(str(e))

        if error==0:
            print('所有节点文件计算路径完成')
            break

