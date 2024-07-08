# -*- coding:utf-8 -*-
#author:jeremy

from config import Config
from utils import GCJ2WGS,kakou_jiedao,create_dir,np_ronghe
import numpy as np
from pathlib import Path
import pandas as pd

def get_path_split_region(source_file):
    global_config = Config('./config.ini')
    source_data_path = global_config.getRaw('设置条件', 'source_data_path')
    store_data_path = global_config.getRaw('设置条件', 'store_data_path')
    restrict_time = int(global_config.getRaw('设置条件', 'restrict_time'))  # 卡口时间限制900s
    number = int(global_config.getRaw('设置条件', 'number'))  # 一次计算5w节点

    xibu_zhongxin = global_config.getRaw('设置条件', 'xibu_zhongxin')
    xibu_zhongxin = xibu_zhongxin.strip('[]').split(',')
    nanshan_zhongxin = global_config.getRaw('设置条件', 'nanshan_zhongxin')
    nanshan_zhongxin = nanshan_zhongxin.strip('[]').split(',')
    futian_zhongxinA = global_config.getRaw('设置条件', 'futian_zhongxinA')
    futian_zhongxinA = futian_zhongxinA.strip('[]').split(',')
    futian_zhongxinB = global_config.getRaw('设置条件', 'futian_zhongxinB')
    futian_zhongxinB = futian_zhongxinB.strip('[]').split(',')
    luohu_zhongxin = global_config.getRaw('设置条件', 'luohu_zhongxin')
    luohu_zhongxin = luohu_zhongxin.strip('[]').split(',')
    beibu_zhongxin = global_config.getRaw('设置条件', 'beibu_zhongxin')
    beibu_zhongxin = beibu_zhongxin.strip('[]').split(',')
    dongbu_zhongxin = global_config.getRaw('设置条件', 'dongbu_zhongxin')
    dongbu_zhongxin = dongbu_zhongxin.strip('[]').split(',')

    df = kakou_jiedao(r'./data/new_kakou_location_m.csv', r'./data/深圳街道数据wgs84_/空间街道办.shp')
    df_columns = df.columns.values
    for c in range(len(df_columns)):
        if df_columns[c] == 'jiedao':
            jiedao_ord = c
        if df_columns[c] == 'k_id':
            id_ord = c

    xibu_kakou_list = []
    nanshan_kakou_list = []
    futianA_kakou_list = []
    futianB_kakou_list = []
    luohu_kakou_list = []
    beibu_kakou_list = []
    dongbu_kakou_list = []
    qita_kakou_list = []
    for i in range(len(df)):
        if df.iloc[i, jiedao_ord] in xibu_zhongxin:
            xibu_kakou_list.append(df.iloc[i, id_ord])
        elif df.iloc[i, jiedao_ord] in nanshan_zhongxin:
            nanshan_kakou_list.append(df.iloc[i, id_ord])
        elif df.iloc[i, jiedao_ord] in futian_zhongxinA:
            futianA_kakou_list.append(df.iloc[i, id_ord])
        elif df.iloc[i, jiedao_ord] in futian_zhongxinB:
            futianB_kakou_list.append(df.iloc[i, id_ord])
        elif df.iloc[i, jiedao_ord] in luohu_zhongxin:
            luohu_kakou_list.append(df.iloc[i, id_ord])
        elif df.iloc[i, jiedao_ord] in beibu_zhongxin:
            beibu_kakou_list.append(df.iloc[i, id_ord])
        elif df.iloc[i, jiedao_ord] in dongbu_zhongxin:
            dongbu_kakou_list.append(df.iloc[i, id_ord])
        else:
            qita_kakou_list.append(df.iloc[i, id_ord])

    create_dir(store_data_path + '/' + str(restrict_time) + ' ' + str(number))
    create_dir(store_data_path + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'splitByregion')


    for date in source_file:
        create_dir(store_data_path + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'splitByregion' + '/' + str(date))
        path_file = Path(store_data_path + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'splitByregion' + '/' + str(
                date) + '/' + str(date) + '_path_' + 'xibu' + '.npy')
        if path_file.exists():
            print('存在文件：' + store_data_path + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'splitByregion' + '/' + str(
                date) + '/' + str(date) + '_path_' + 'xibu' + '.npy')
        else:
            xibu_path_list = []
            nanshan_path_list = []
            futianA_path_list = []
            futianB_path_list = []
            luohu_path_list = []
            beibu_path_list = []
            dongbu_path_list = []
            qita_path_list = []
            path_list=np_ronghe(store_data_path + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'Nosplit' + '/' + str(date))
            df_jiedian = pd.read_csv(open(source_data_path + '/' + str(date) + '_jiedian.csv'),
                                     dtype={'start_kid': str, 'end_kid': str, 'car_id': str, 'end_time': int,
                                            'start_time': int})
            for p in path_list:
                if df_jiedian['start_kid'][p[0]] in xibu_kakou_list:
                    xibu_path_list.append(p)
                elif df_jiedian['start_kid'][p[0]] in nanshan_kakou_list:
                    nanshan_path_list.append(p)
                elif df_jiedian['start_kid'][p[0]] in futianA_kakou_list:
                    futianA_path_list.append(p)
                elif df_jiedian['start_kid'][p[0]] in futianB_kakou_list:
                    futianB_path_list.append(p)
                elif df_jiedian['start_kid'][p[0]] in luohu_kakou_list:
                    luohu_path_list.append(p)
                elif df_jiedian['start_kid'][p[0]] in beibu_kakou_list:
                    beibu_path_list.append(p)
                elif df_jiedian['start_kid'][p[0]] in dongbu_kakou_list:
                    dongbu_path_list.append(p)
                elif df_jiedian['start_kid'][p[0]] in qita_kakou_list:
                    qita_path_list.append(p)

            xibu_path_numpy = np.array(xibu_path_list)
            nanshan_path_numpy = np.array(nanshan_path_list)
            futianA_path_numpy = np.array(futianA_path_list)
            futianB_path_numpy = np.array(futianB_path_list)
            luohu_path_numpy = np.array(luohu_path_list)
            beibu_path_numpy = np.array(beibu_path_list)
            dongbu_path_numpy = np.array(dongbu_path_list)
            qita_path_numpy = np.array(qita_path_list)
            np.save(store_data_path + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'splitByregion' + '/' + str(
                date) + '/' + str(date) + '_path_' + 'xibu' + '.npy', xibu_path_numpy)
            np.save(store_data_path + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'splitByregion' + '/' + str(
                date) + '/' + str(date) + '_path_' + 'nanshan' + '.npy', nanshan_path_numpy)
            np.save(store_data_path + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'splitByregion' + '/' + str(
                date) + '/' + str(date) + '_path_' + 'futianA' + '.npy', futianA_path_numpy)
            np.save(store_data_path + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'splitByregion' + '/' + str(
                date) + '/' + str(date) + '_path_' + 'futianB' + '.npy', futianB_path_numpy)
            np.save(store_data_path + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'splitByregion' + '/' + str(
                date) + '/' + str(date) + '_path_' + 'luohu' + '.npy', luohu_path_numpy)
            np.save(store_data_path + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'splitByregion' + '/' + str(
                date) + '/' + str(date) + '_path_' + 'beibu' + '.npy', beibu_path_numpy)
            np.save(store_data_path + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'splitByregion' + '/' + str(
                date) + '/' + str(date) + '_path_' + 'dongbu' + '.npy', dongbu_path_numpy)
            np.save(store_data_path + '/' + str(restrict_time) + ' ' + str(number) + '/' + 'splitByregion' + '/' + str(
                date) + '/' + str(date) + '_path_' + 'qita' + '.npy', qita_path_numpy)


