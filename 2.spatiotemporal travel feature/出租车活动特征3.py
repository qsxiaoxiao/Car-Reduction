# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 01:34:28 2019

@author: SZU_Wongyq
"""

import pandas as pd
import numpy as np
import math
from scipy.spatial.distance import pdist, squareform

#提取出租车
def extractCar(inputFile,outputFile,type):
    df_car=pd.read_csv(open(inputFile)) 
    df_car=df_car[df_car['type']==type]#1:出租车;3:社会车
    df_car.to_csv(outputFile,index=False)#保存时不要索引
    print('车辆总出行次数：',len(df_car))
    return df_car

#为出租车匹配位置
def matchLocatin(inputFile,outputFile,df_car):
    df_location=pd.read_csv(open(inputFile,encoding='ANSI'),dtype=str)
    df_location=df_location[['k_id','x_m','y_m']]
    df_merge=pd.merge(df_car,df_location,left_on='id',right_on='k_id',how='inner')
    df_merge=df_merge.drop(columns=['k_id'])
    df_merge.to_csv(outputFile,index=False)#保存时不要索引
    print('能匹配到位置的车辆总出行次数：',len(df_merge))
    return df_merge

#计算ME（熵）
def ME(ids):
    s=0
    for p in probability(ids):
        s=s+p*math.log(p)
    return -s

#计算list中每个元素出现的概率    
def probability(l):
    num=pd.value_counts(l)#计算各个元素出现的次数
    l_probability=[]
    for i in set(l):#set取唯一值
        l_probability.append(num[i]/len(l))
    return l_probability

#计算rog，即原来的rms（活动半径）
def ROG(xs,ys):
    xs_mean=np.mean(xs)
    ys_mean=np.mean(ys)
    if(len(xs)==len(ys)):
        rms_s=[(x-xs_mean)**2+(y-ys_mean)**2 for x,y in zip(xs,ys)]
        rms_sum=np.sum(rms_s)
        return (rms_sum/len(xs))**0.5
    else:
        return -1

#求算数平均中心   
def centroid(xs,ys):
    xs_mean=np.mean(xs)
    ys_mean=np.mean(ys)
    coordinate=[xs_mean,ys_mean]
    return coordinate

#求标准差椭圆的长短半轴和方向
def e1e2Direction(xs,ys):
    xs_mean=np.mean(xs)
    ys_mean=np.mean(ys)
    # 求出标准误差椭圆的x轴，沿着顺时针，旋转的角度
    x_minus_mean=xs-xs_mean
    y_minus_mean=ys-ys_mean
    xy=np.array([x*y for x,y in zip(x_minus_mean,y_minus_mean)])
    A=sum(x_minus_mean**2)-sum(y_minus_mean**2)
    B=(A**2+4*sum(xy)**2)**0.5
    C=2*sum(xy)
    Angletheta = math.atan((A+B)/C)#得到旋转弧度
    direction = Angletheta * 180 / math.pi#弧度转角度
    if np.isnan(direction):#如果direction是nan执行if
        direction=0
        Angletheta=0
    tposedSx = (2*sum((x_minus_mean*math.cos(Angletheta)-y_minus_mean*math.sin(Angletheta))**2)/len(xs))**0.5#得到椭圆长短半轴
    tposedSy = (2*sum((x_minus_mean*math.sin(Angletheta)+y_minus_mean*math.cos(Angletheta))**2)/len(xs))**0.5
    return [tposedSx,tposedSy,direction]

#求dotch（凸多边形的直径）和tl（总出行距离）
def DOTCH_TL(xs,ys):
    points=[]
    for x,y in zip(xs,ys):
        points.append((x,y)) 
    distance=squareform(pdist(points))#计算各点之间的距离，distance的i行j列值表示第i个点到第j个点的距离
    dotch=np.max(distance)#distance中最大值为dotch
    travelLength=0
    for n in range(len(points)-1):
            travelLength+=distance[n][n+1]#travelLength为总出行距离
    return [dotch,travelLength]

#求te。出行经过的相邻卡口组成无向边，求边的熵
def TE(ids):
    travel=[]
    for n in range(len(ids)-1):
        if str(ids[n])<str(ids[n+1]):
            travel.append((ids[n],ids[n+1]))
        else:
            travel.append((ids[n+1],ids[n]))
    return ME(travel)

#求tfd（通过相邻卡口所用时间的方差）
def TFD(times):
    times_duration=[]
    for n in range(len(times)-1):
        times_duration.append(times[n+1]-times[n])
    return np.var(times_duration)

#使用指标评价车辆活动特征
def extractFeature(outputFile,df_merge):
    car_id_number=df_merge['car_id'].value_counts()
    car_id=list(car_id_number[car_id_number>1].index)#删除只出行一次的车辆，car_id表示出行次数大于1的车辆ID
    df_feature=pd.DataFrame(index=car_id,
                     columns=['N','n','me','centroidx','centroidy','e1','e2','rog','dotch',
                              'area','eccentricity','direction','not','tl','te','tfd'])
    print(len(car_id))
    n=1
    for c_id in car_id:
        print(n)
        n=n+1
        df_car=df_merge[df_merge['car_id']==c_id]#提取车辆ID为c_id的车辆出行记录
        df_car['time'] = df_car['time'].astype('float')#修改'time'列的类型
        df_car.sort_values("time",inplace=True)#该车辆出行记录按时间排序
        xs=np.array(df_car['x_m'])
        ys=np.array(df_car['y_m'])
        ids=np.array(df_car['id'])
        times=np.array(df_car['time'])
        xs=np.array([float(x) for x in xs])
        ys=np.array([float(y) for y in ys])
        times=np.array([float(t) for t in times])
        df_feature['N'][c_id]=len(ids)#途径卡口数
        df_feature['n'][c_id]=len(set(ids))#途径唯一卡口数
        df_feature['me'][c_id]=ME(ids)#卡口的熵
        coordinate=centroid(xs,ys)
        df_feature['centroidx'][c_id]=coordinate[0]#算术平均中心.x
        df_feature['centroidy'][c_id]=coordinate[1]#算术平均中心.y
        e1e2direction=e1e2Direction(xs,ys)
        if e1e2direction[0]>e1e2direction[1]:#e1为长半轴，e2为短半轴
            df_feature['e1'][c_id]=e1e2direction[0]
            df_feature['e2'][c_id]=e1e2direction[1]
            df_feature['eccentricity'][c_id]=(1-(e1e2direction[1]/e1e2direction[0])**2)**0.5#eccentricity为离心率
        else:
            df_feature['e1'][c_id]=e1e2direction[1]
            df_feature['e2'][c_id]=e1e2direction[0]
            df_feature['eccentricity'][c_id]=(1-(e1e2direction[0]/e1e2direction[1])**2)**0.5
        df_feature['direction'][c_id]=e1e2direction[2]#标准差椭圆的方向
        df_feature['rog'][c_id]=ROG(xs,ys)#rog为活动半径
        dotch_tl=DOTCH_TL(xs,ys)
        df_feature['dotch'][c_id]=dotch_tl[0]#dotch为凸多边形的直径
        df_feature['tl'][c_id]=dotch_tl[1]#tl为总出行距离
        df_feature['area'][c_id]=math.pi*e1e2direction[0]*e1e2direction[1]#标准差椭圆的面积
        df_feature['not'][c_id]=len(ids)-1#出行次数
        df_feature['te'][c_id]=TE(ids)#出行经过的相邻卡口组成无向边，te为边的熵
        df_feature['tfd'][c_id]=TFD(times)#tfd为通过相邻卡口所用时间的方差
    df_feature.index.name='car_id'
    df_feature.to_csv(outputFile)

#将时间提取为one-hot
def extractTimeTo24(outputFile,df_merge):
    car_id_number=df_merge['car_id'].value_counts()
    car_id=list(car_id_number[car_id_number>1].index)#删除只出行一次的车辆，car_id表示出行次数大于1的车辆ID
    df_feature=pd.DataFrame(index=car_id,
                 columns=['0_1','1_2','2_3','3_4','4_5','5_6',
                          '6_7','7_8','8_9','9_10','10_11','11_12',
                          '12_13','13_14','14_15','15_16','16_17','17_18',
                          '18_19','19_20','20_21','21_22','22_23','23_24'])
    df_feature.fillna(0,inplace=True)
    print(len(car_id))
    n=1
    for c_id in car_id:
        print(n)
        n=n+1
        times=list(df_merge[df_merge['car_id']==c_id]['time'])#提取车辆ID为c_id的车辆的出行时间
        times=[int(x)//3600 for x in times]#分钟转小时
        for t in times:
            df_feature[str(t)+'_'+str(t+1)][c_id]+=1
    df_feature.index.name='car_id'
    df_feature.to_csv(outputFile)

##12.5
#df_chuzuche_car=extractCar(r'C:\Users\SZU_Wongyq\Desktop\卡口\20161205_title.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161205_title_chuzuche.csv',1)
#df_chuzuche_merge=matchLocatin(r'C:\Users\SZU_Wongyq\Desktop\new_kakou_location_m.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161205_title_chuzuche_zuobiao.csv',df_chuzuche_car)
#extractFeature(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161205_title_chuzuche_zhibiao.csv',df_chuzuche_merge)
#extractTimeTo24(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161205_title_chuzuche_time_zhibiao.csv',df_chuzuche_merge)
#df_shehuiche_car=extractCar(r'C:\Users\SZU_Wongyq\Desktop\卡口\20161205_title.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161205_title_shehuiche.csv',3)
#df_shehuiche_merge=matchLocatin(r'C:\Users\SZU_Wongyq\Desktop\new_kakou_location_m.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161205_title_shehuiche_zuobiao.csv',df_shehuiche_car)
#extractFeature(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161205_title_shehuiche_zhibiao.csv',df_shehuiche_merge)
#extractTimeTo24(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161205_title_shehuiche_time_zhibiao.csv',df_shehuiche_merge)

##12.6
#df_chuzuche_car=extractCar(r'C:\Users\SZU_Wongyq\Desktop\卡口\20161206_title.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161206_title_chuzuche.csv',1)
#df_chuzuche_merge=matchLocatin(r'C:\Users\SZU_Wongyq\Desktop\new_kakou_location_m.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161206_title_chuzuche_zuobiao.csv',df_chuzuche_car)
#extractFeature(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161206_title_chuzuche_zhibiao.csv',df_chuzuche_merge)
#extractTimeTo24(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161206_title_chuzuche_time_zhibiao.csv',df_chuzuche_merge)
#df_shehuiche_car=extractCar(r'C:\Users\SZU_Wongyq\Desktop\卡口\20161206_title.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161206_title_shehuiche.csv',3)
#df_shehuiche_merge=matchLocatin(r'C:\Users\SZU_Wongyq\Desktop\new_kakou_location_m.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161206_title_shehuiche_zuobiao.csv',df_shehuiche_car)
#extractFeature(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161206_title_shehuiche_zhibiao.csv',df_shehuiche_merge)
#extractTimeTo24(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161206_title_shehuiche_time_zhibiao.csv',df_shehuiche_merge)
#
##12.7
#df_chuzuche_car=extractCar(r'C:\Users\SZU_Wongyq\Desktop\卡口\20161207_title.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161207_title_chuzuche.csv',1)
#df_chuzuche_merge=matchLocatin(r'C:\Users\SZU_Wongyq\Desktop\new_kakou_location_m.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161207_title_chuzuche_zuobiao.csv',df_chuzuche_car)
#extractFeature(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161207_title_chuzuche_zhibiao.csv',df_chuzuche_merge)
#extractTimeTo24(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161207_title_chuzuche_time_zhibiao.csv',df_chuzuche_merge)
#df_shehuiche_car=extractCar(r'C:\Users\SZU_Wongyq\Desktop\卡口\20161207_title.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161207_title_shehuiche.csv',3)
#df_shehuiche_merge=matchLocatin(r'C:\Users\SZU_Wongyq\Desktop\new_kakou_location_m.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161207_title_shehuiche_zuobiao.csv',df_shehuiche_car)
#extractFeature(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161207_title_shehuiche_zhibiao.csv',df_shehuiche_merge)
#extractTimeTo24(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161207_title_shehuiche_time_zhibiao.csv',df_shehuiche_merge)
#
##12.8
#df_chuzuche_car=extractCar(r'C:\Users\SZU_Wongyq\Desktop\卡口\20161208_title.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161208_title_chuzuche.csv',1)
#df_chuzuche_merge=matchLocatin(r'C:\Users\SZU_Wongyq\Desktop\new_kakou_location_m.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161208_title_chuzuche_zuobiao.csv',df_chuzuche_car)
#extractFeature(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161208_title_chuzuche_zhibiao.csv',df_chuzuche_merge)
#extractTimeTo24(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161208_title_chuzuche_time_zhibiao.csv',df_chuzuche_merge)
#df_shehuiche_car=extractCar(r'C:\Users\SZU_Wongyq\Desktop\卡口\20161208_title.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161208_title_shehuiche.csv',3)
#df_shehuiche_merge=matchLocatin(r'C:\Users\SZU_Wongyq\Desktop\new_kakou_location_m.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161208_title_shehuiche_zuobiao.csv',df_shehuiche_car)
#extractFeature(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161208_title_shehuiche_zhibiao.csv',df_shehuiche_merge)
#extractTimeTo24(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161208_title_shehuiche_time_zhibiao.csv',df_shehuiche_merge)

#12.9
df_chuzuche_car=extractCar(r'C:\Users\SZU_Wongyq\Desktop\卡口\20161209_title.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161209_title_chuzuche.csv',1)
df_chuzuche_merge=matchLocatin(r'C:\Users\SZU_Wongyq\Desktop\new_kakou_location_m.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161209_title_chuzuche_zuobiao.csv',df_chuzuche_car)
extractFeature(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161209_title_chuzuche_zhibiao.csv',df_chuzuche_merge)
extractTimeTo24(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161209_title_chuzuche_time_zhibiao.csv',df_chuzuche_merge)
df_shehuiche_car=extractCar(r'C:\Users\SZU_Wongyq\Desktop\卡口\20161209_title.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161209_title_shehuiche.csv',3)
df_shehuiche_merge=matchLocatin(r'C:\Users\SZU_Wongyq\Desktop\new_kakou_location_m.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161209_title_shehuiche_zuobiao.csv',df_shehuiche_car)
extractFeature(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161209_title_shehuiche_zhibiao.csv',df_shehuiche_merge)
extractTimeTo24(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161209_title_shehuiche_time_zhibiao.csv',df_shehuiche_merge)

##12.10
#df_chuzuche_car=extractCar(r'C:\Users\SZU_Wongyq\Desktop\卡口\20161210_title.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161210_title_chuzuche.csv',1)
#df_chuzuche_merge=matchLocatin(r'C:\Users\SZU_Wongyq\Desktop\new_kakou_location_m.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161210_title_chuzuche_zuobiao.csv',df_chuzuche_car)
#extractFeature(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161210_title_chuzuche_zhibiao.csv',df_chuzuche_merge)
#extractTimeTo24(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161210_title_chuzuche_time_zhibiao.csv',df_chuzuche_merge)
#df_shehuiche_car=extractCar(r'C:\Users\SZU_Wongyq\Desktop\卡口\20161210_title.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161210_title_shehuiche.csv',3)
#df_shehuiche_merge=matchLocatin(r'C:\Users\SZU_Wongyq\Desktop\new_kakou_location_m.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161210_title_shehuiche_zuobiao.csv',df_shehuiche_car)
#extractFeature(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161210_title_shehuiche_zhibiao.csv',df_shehuiche_merge)
#extractTimeTo24(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161210_title_shehuiche_time_zhibiao.csv',df_shehuiche_merge)

#12.11
#df_chuzuche_car=extractCar(r'C:\Users\SZU_Wongyq\Desktop\卡口\20161211_title.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161211_title_chuzuche.csv',1)
#df_chuzuche_merge=matchLocatin(r'C:\Users\SZU_Wongyq\Desktop\new_kakou_location_m.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161211_title_chuzuche_zuobiao.csv',df_chuzuche_car)
#extractFeature(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161211_title_chuzuche_zhibiao.csv',df_chuzuche_merge)
#extractTimeTo24(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161211_title_chuzuche_time_zhibiao.csv',df_chuzuche_merge)
#df_shehuiche_car=extractCar(r'C:\Users\SZU_Wongyq\Desktop\卡口\20161211_title.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161211_title_shehuiche.csv',3)
#df_shehuiche_merge=matchLocatin(r'C:\Users\SZU_Wongyq\Desktop\new_kakou_location_m.csv',r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161211_title_shehuiche_zuobiao.csv',df_shehuiche_car)
#extractFeature(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161211_title_shehuiche_zhibiao.csv',df_shehuiche_merge)
#extractTimeTo24(r'C:\Users\SZU_Wongyq\Desktop\2019.12.18\20161211_title_shehuiche_time_zhibiao.csv',df_shehuiche_merge)