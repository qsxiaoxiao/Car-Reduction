# -*- coding:utf-8 -*-
#author:jeremy
import sys
import pandas as pd
from urllib.request import urlopen
import json

def return_shijian(origin_kid_x,origin_kid_y,des_kid_x,des_kid_y):
    url = 'http://api.map.baidu.com/direction/v2/driving?'
    url=url+'origin='+str(origin_kid_y)+','+str(origin_kid_x)+'&destination='+str(des_kid_y)+','+str(des_kid_x)+'&coord_type=wgs84&tactics=2&ak='+'lWpbR5OCQYybppqci2kGYgFd'
    #print(url)
    req = urlopen(url)
    res  = req.read().decode()
    if json.loads(res)['status']==0:#成功返回
        #print(1)
        shijian = json.loads(res)['result']['routes'][0]['duration']
    else:
        #print(json.loads(res)['status'])
        shijian=-1
    return int(shijian)

feiyunyingche_1205=pd.read_csv(open(r'.\data\非运营车卡口记录（带坐标）\20161205_title_feiyunyingche_zuobiao.csv'),index_col='car_id',dtype={'id':str})
feiyunyingche_1206=pd.read_csv(open(r'.\data\非运营车卡口记录（带坐标）\20161206_title_feiyunyingche_zuobiao.csv'),index_col='car_id',dtype={'id':str})
feiyunyingche_1207=pd.read_csv(open(r'.\data\非运营车卡口记录（带坐标）\20161207_title_feiyunyingche_zuobiao.csv'),index_col='car_id',dtype={'id':str})
feiyunyingche_1208=pd.read_csv(open(r'.\data\非运营车卡口记录（带坐标）\20161208_title_feiyunyingche_zuobiao.csv'),index_col='car_id',dtype={'id':str})
feiyunyingche_1209=pd.read_csv(open(r'.\data\非运营车卡口记录（带坐标）\20161209_title_feiyunyingche_zuobiao.csv'),index_col='car_id',dtype={'id':str})
feiyunyingche_1210=pd.read_csv(open(r'.\data\非运营车卡口记录（带坐标）\20161210_title_feiyunyingche_zuobiao.csv'),index_col='car_id',dtype={'id':str})
feiyunyingche_1211=pd.read_csv(open(r'.\data\非运营车卡口记录（带坐标）\20161211_title_feiyunyingche_zuobiao.csv'),index_col='car_id',dtype={'id':str})
kakou_time = pd.read_csv(open(r'.\data\kakou_time.csv'),dtype={'origin_kid':str,'des_kid':str,'time':int})
kid_baidu=list(set(list(set(feiyunyingche_1205['id']))+list(set(feiyunyingche_1206['id']))+list(set(feiyunyingche_1207['id']))+
    list(set(feiyunyingche_1208['id']))+list(set(feiyunyingche_1209['id']))+list(set(feiyunyingche_1210['id']))+list(set(feiyunyingche_1211['id'])))-set(kakou_time['origin_kid']))
print(len(kid_baidu))
yuan_id=set(kakou_time['origin_kid'])
for i in yuan_id:
    print(i)
    for j in kid_baidu:
        new_line = pd.Series({'origin_kid': i,
                              'des_kid':j,
                              'time': -1})
        kakou_time = kakou_time.append(new_line, ignore_index=True)
        new_line = pd.Series({'origin_kid': j,
                              'des_kid': i,
                              'time': -1})
        kakou_time = kakou_time.append(new_line, ignore_index=True)
print(kakou_time)
print(len(yuan_id))
print(len(kid_baidu))
print(sum(kakou_time.duplicated(subset=['origin_kid','des_kid'])))
for i in range(len(kid_baidu)):
    for j in range(len(kid_baidu)):
        print(i,j)
        if i!=j:  #其实应该有i==j，只不过时间为0
            new_line=pd.Series({'origin_kid':kid_baidu[i],
                                'des_kid':kid_baidu[j],
                                'time':-1})
            kakou_time=kakou_time.append(new_line,ignore_index=True)
        if i == j:
            new_line = pd.Series({'origin_kid': kid_baidu[i],
                                  'des_kid': kid_baidu[j],
                                  'time': 0})
            kakou_time = kakou_time.append(new_line, ignore_index=True)

print(kakou_time)
print(kakou_time.duplicated(subset=['origin_kid','des_kid']))
print(sum(kakou_time.duplicated(subset=['origin_kid','des_kid'])))

kakou_time.to_csv(r'.\data\kakou_time.csv',index=False)


new_kakou_location_m=pd.read_csv(open(r'.\data\new_kakou_location_m.csv'))

while True:
    #反复运行，直到全部都有时间
    kakou_time=pd.read_csv(open(r'.\data\kakou_time.csv'),dtype={'origin_kid':str,'des_kid':str,'time':int})
    for index, row in kakou_time.iterrows():
        if row['time']==-1:
            print(row['origin_kid'])
            print(row['des_kid'])
            origin_kid_x=new_kakou_location_m[new_kakou_location_m['k_id']==row['origin_kid']]['x'].iloc[0]
            origin_kid_y=new_kakou_location_m[new_kakou_location_m['k_id']==row['origin_kid']]['y'].iloc[0]
            des_kid_x=new_kakou_location_m[new_kakou_location_m['k_id']==row['des_kid']]['x'].iloc[0]
            des_kid_y=new_kakou_location_m[new_kakou_location_m['k_id']==row['des_kid']]['y'].iloc[0]
            #print(origin_kid_x)
            #print(origin_kid_y)
            #print(des_kid_x)
            #print(des_kid_y)
            shijian=return_shijian(origin_kid_x,origin_kid_y,des_kid_x,des_kid_y)
            print(shijian)
            if shijian!=-1:
                kakou_time.loc[index,'time']=shijian
    #print(kakou_time)
    kakou_time.to_csv(r'.\data\kakou_time.csv',index=False)