# -*- coding:utf-8 -*-
#author:jeremy

import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib
import tensorly as tl
import numpy as np
import json
import time
import random
from datetime import datetime
from tensorly.decomposition import non_negative_tucker
import collections
from pandas import Series
import argparse

from utils import *
from pathlib import Path
from config import Config

def get_jiedian(source_file):
    '''
    将卡口记录形成节点输出至文件
    :param source_file:  #[1205,1206,1207,1208,1209,1210,1211]
    :return:
    '''
    global_config = Config('./config.ini')
    source_data_path = global_config.getRaw('设置条件', 'source_data_path')

    for date in source_file:
        jiedian_file = Path(source_data_path+'/' + str(date) + '_jiedian.csv')
        if jiedian_file.exists():
           print('存在文件：'+source_data_path+'/' + str(date) + '_jiedian.csv')
        else:
            feiyunyingche=pd.read_csv(open(r'./data/非运营车卡口记录（带坐标）/2016'+str(date)+'_title_feiyunyingche_zuobiao.csv'),index_col='car_id')
            feiyunyingche=shanchu_yicichuxing(feiyunyingche)
            list_kakou_shijiancha=shijiancha(feiyunyingche)
            list_kakou_shijiancha.sort()#升序
            q1, q3=count_quartiles(list_kakou_shijiancha)
            upper, floor=count_margin(q1, q3, 1.6)
            print(len(list_kakou_shijiancha))
            print(q1, q3)
            print(upper, floor)
            #运行4hours
            goujian_jiedian(feiyunyingche,upper, floor).to_csv(source_data_path+'/' + str(date) + '_jiedian.csv',index=False)
