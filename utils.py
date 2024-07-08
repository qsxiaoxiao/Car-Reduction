# -*- coding:utf-8 -*-
#author:jeremy


import collections
from pandas import Series
import pandas as pd
import time
import os
from shapely.geometry import Point,Polygon
import shapefile
import math
import numpy as np

#删除只有一次出行车辆
def shanchu_yicichuxing(df):
    #统计拍摄次数
    tongji=Series(collections.Counter(df.index)).to_frame().rename(columns={0:'num'})
    #拍摄次数大于1的车辆id
    carid=tongji[tongji['num']>1].index
    #保留拍摄次数大于1的车辆
    return df.loc[carid]

#每辆非运营车通过两卡口之间的时间差，需要运行10mins
def shijiancha(df):
    df=df.sort_values(ascending=True,by=['car_id','time'])#时间从小到大排序
    #print(df)
    kakou_shijiancha=[]
    chushi_carid=-1
    chushi_time=-1
    #a=0#计数
    for index, row in df.iterrows():
        #print(a)
        #a=a+1
        if index!=chushi_carid:
            chushi_carid=index
            chushi_time=row['time']
        else:
            kakou_shijiancha.append(row['time']-chushi_time)
            chushi_time=row['time']
            #print(kakou_shijiancha)
    #print(kakou_shijiancha)
    return kakou_shijiancha

#计算上下四分位数,lis按从小到大排过序
def count_quartiles(lis):
    s=pd.Series(lis)
    q1=s.quantile(q=0.25)
    q3=s.quantile(q=0.75)
    return q1,q3

#计算上下边缘,lis按从小到大排过序
def count_margin(q1, q3, a):
    iqr = q3 - q1
    upper = q3 + a*iqr
    floor = q1 - a*iqr
    return upper, floor

#切割一日出行
def qiege(df, upper, floor):
    df=df.sort_values(ascending=True,by=['time'])#时间从小到大排序
    qiege_df=[] #df切割后放入qiege_df
    chushi_df=pd.DataFrame(columns=df.columns,dtype=object)
    chushi_df.index.name='car_id'
    chushi_time=-1
    i=0
    for index, row in df.iterrows():
        i=i+1
        if i==1:
            chushi_time=row['time']
            chushi_df=chushi_df.append(row)
        else:#
            if row['time']-chushi_time>=upper:
                qiege_df.append(chushi_df)
                chushi_df=pd.DataFrame(columns=df.columns,dtype=object)
                chushi_df.index.name='car_id'
                chushi_df=chushi_df.append(row)
            elif row['time']-chushi_time<=floor:
                chushi_df=chushi_df.append(row)
            else:
                chushi_df=chushi_df.append(row)
            chushi_time=row['time']
        if i==len(df):
            qiege_df.append(chushi_df)
    return qiege_df

#构建（起点卡口，终点卡口，出发时刻，到达时刻）为一个节点
def goujian_jiedian(df,upper, floor):
    df=df.sort_values(ascending=True,by=['car_id','time'])#时间从小到大排序
    l_jiedian = []
    #jiedian = pd.DataFrame(columns=['start_kid','end_kid','start_time','end_time'])
    car_ids=list(set(df.index))
    n=0
    for car_id in car_ids:
        n=n+1
        #print(n)
        one_feiyunying=df.loc[car_id]
        qiege_dfs=qiege(one_feiyunying,upper, floor)
        for qiege_df in qiege_dfs:
            if len(qiege_df)>1:
                #print(qiege_df)
                if qiege_df.iloc[0]['id']!=qiege_df.iloc[len(qiege_df)-1]['id']:
                #print(qiege_df)
                    qiege_df=qiege_df.sort_values(ascending=True,by=['car_id','time'])#时间从小到大排序
                    l_jiedian.append([qiege_df.iloc[0]['id'],qiege_df.iloc[len(qiege_df)-1]['id'],
                                   qiege_df.iloc[0]['time'],qiege_df.iloc[len(qiege_df)-1]['time'],str(car_id)])
                    #print(qiege_df.iloc[0]['id'])
                    #print(qiege_df.iloc[len(qiege_df)-1]['id'])
                    #print(qiege_df.iloc[0]['time'])
                    #print(qiege_df.iloc[len(qiege_df)-1]['time'])
                    #print(type(str(car_id)))
                    #print(str(car_id))
                    '''new_line=pd.Series({'start_kid':qiege_df.iloc[0]['id'],
                                        'end_kid':qiege_df.iloc[len(qiege_df)-1]['id'],
                                        'start_time':qiege_df.iloc[0]['time'],
                                        'end_time':qiege_df.iloc[len(qiege_df)-1]['time']}) '''
                    #jiedian=jiedian.append(new_line,ignore_index=True)
                    #print(jiedian)
    jiedian = pd.DataFrame(l_jiedian,columns=['start_kid','end_kid','start_time','end_time','car_id'])
    #print(jiedian)
    return jiedian

def create_dir(file_name):
    """
    创建文件夹
    :param file_name:
    :return:
    """
    if os.path.exists(file_name):
        return
    else:
        os.mkdir(file_name)

def write_log(s):
    start_date = time.strftime('%Y-%m-%d', time.localtime())
    with open(r'./log/log_{}.txt'.format(start_date), 'a+', encoding='utf-8')as f:
        f.write(str(s) + '\n')

def GCJ2WGS(lon,lat):
    '''
    GCJ坐标系转WGS84
    :param lon: 经度
    :param lat: 纬度
    :return:
    '''
    # location格式如下：locations[1] = "113.923745,22.530824"
    a = 6378245.0 # 克拉索夫斯基椭球参数长半轴a
    ee = 0.00669342162296594323 #克拉索夫斯基椭球参数第一偏心率平方
    PI = 3.14159265358979324 # 圆周率
    # 以下为转换公式
    x = lon - 105.0
    y = lat - 35.0
    # 经度
    dLon = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x));
    dLon += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0;
    dLon += (20.0 * math.sin(x * PI) + 40.0 * math.sin(x / 3.0 * PI)) * 2.0 / 3.0;
    dLon += (150.0 * math.sin(x / 12.0 * PI) + 300.0 * math.sin(x / 30.0 * PI)) * 2.0 / 3.0;
    #纬度
    dLat = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x));
    dLat += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0;
    dLat += (20.0 * math.sin(y * PI) + 40.0 * math.sin(y / 3.0 * PI)) * 2.0 / 3.0;
    dLat += (160.0 * math.sin(y / 12.0 * PI) + 320 * math.sin(y * PI / 30.0)) * 2.0 / 3.0;
    radLat = lat / 180.0 * PI
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * PI);
    dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * PI);
    wgsLon = lon - dLon
    wgsLat = lat - dLat
    return wgsLon,wgsLat

def kakou_jiedao(kakou_path,shp_path):
    '''
    卡口匹配街道（不完全）
    :param kakou_path: 卡口文件路径   e.g. r'./data/new_kakou_location_m.csv'
    :param shp_path:  shp文件路径    e.g. r'./data/深圳街道数据wgs84_/空间街道办.shp'
    :return: 匹配好街道的df
    '''
    df = pd.read_csv(kakou_path)
    df['jiedao']=''
    df_columns = df.columns.values
    for c in range(len(df_columns)):
        if df_columns[c] == 'x':
            x_ord = c
        if df_columns[c] == 'y':
            y_ord = c
        if df_columns[c] == 'jiedao':
            jiedao_ord = c

    shp_file = shapefile.Reader(shp_path,encoding='ansi')
    for i in range(shp_file.numRecords): #遍历所有记录
        if len(shp_file.records()[i][1])>0: #shp文件中有空名称的街道，需要排除
            polygon=Polygon(shp_file.shapes()[i].points)
            name=shp_file.records()[i][1]
            for j in range(len(df)):
                if polygon.contains(Point(GCJ2WGS(df.iloc[j, x_ord], df.iloc[j, y_ord]))):
                    df.iloc[j, jiedao_ord]=name
    return df

def np_ronghe(path):
    result=[]
    filePathList = os.listdir(path)
    for allDir in filePathList:
        child = os.path.join('%s\%s' % (path, allDir))
        numpy_path = np.load(child, allow_pickle=True)
        for p in numpy_path:
            result.append(p)
    return result



