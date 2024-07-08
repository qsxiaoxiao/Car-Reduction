# -*- coding:utf-8 -*-
#author:jeremy
from config import Config
import json
import pandas as pd
from pathlib import Path

def jiedian_split_by_time(source_file):
    global_config = Config('./config.ini')
    jiedian_split_time_work = global_config.getRaw('设置条件', 'jiedian_split_time_work')
    jiedian_split_time_work = json.loads(jiedian_split_time_work)
    jiedian_split_time_nonwork = global_config.getRaw('设置条件', 'jiedian_split_time_nonwork')
    jiedian_split_time_nonwork = json.loads(jiedian_split_time_nonwork)
    source_data_path = global_config.getRaw('设置条件', 'source_data_path')
    restrict_time = int(global_config.getRaw('设置条件', 'restrict_time'))  # 卡口时间限制900s
    number = int(global_config.getRaw('设置条件', 'number'))  # 一次计算5w节点

    for date in source_file:
        df_jiedian = pd.read_csv(open(source_data_path+'/' + str(date) + '_jiedian.csv'),dtype={'start_kid': str, 'end_kid': str, 'car_id': str,'end_time':int,'start_time':int})
        df_jiedian_columns = df_jiedian.columns.values
        for c in range(len(df_jiedian_columns)):
            if df_jiedian_columns[c] == 'start_time':
                start_time_ord = c

        if '10' in str(date) or '11' in str(date):
            #非工作日
            for t in range(len(jiedian_split_time_nonwork)-1):
                path_file = Path(source_data_path+'/' + str(date)+'_jiedian_'+str(jiedian_split_time_nonwork[t])+'_'+str(jiedian_split_time_nonwork[t+1])+'.csv')
                if path_file.exists():
                    print('存在文件：' + source_data_path+'/' + str(date)+'_jiedian_'+str(jiedian_split_time_nonwork[t])+'_'+str(jiedian_split_time_nonwork[t+1])+'.csv')
                else:
                    index=[]
                    for i in range(len(df_jiedian)):
                        if int(jiedian_split_time_nonwork[t]) <= df_jiedian.iloc[i, start_time_ord]/3600.0 and df_jiedian.iloc[i, start_time_ord]/3600.0 < int(jiedian_split_time_nonwork[t+1]):
                            index.append(i)
                    df_jiedian.iloc[index].to_csv(source_data_path+'/' + str(date)+'_jiedian_'+str(jiedian_split_time_nonwork[t])+'_'+str(jiedian_split_time_nonwork[t+1])+'.csv',index=False)
        else:
            #工作日
            for t in range(len(jiedian_split_time_work)-1):
                path_file = Path(source_data_path+'/' + str(date)+'_jiedian_'+str(jiedian_split_time_work[t])+'_'+str(jiedian_split_time_work[t+1])+'.csv')
                if path_file.exists():
                    print('存在文件：' + source_data_path+'/' + str(date)+'_jiedian_'+str(jiedian_split_time_work[t])+'_'+str(jiedian_split_time_work[t+1])+'.csv')
                else:
                    index=[]
                    for i in range(len(df_jiedian)):
                        if int(jiedian_split_time_work[t]) <= df_jiedian.iloc[i, start_time_ord]/3600.0 and df_jiedian.iloc[i, start_time_ord]/3600.0 < int(jiedian_split_time_work[t+1]):
                            index.append(i)
                    df_jiedian.iloc[index].to_csv(source_data_path+'/' + str(date)+'_jiedian_'+str(jiedian_split_time_work[t])+'_'+str(jiedian_split_time_work[t+1])+'.csv',index=False)

