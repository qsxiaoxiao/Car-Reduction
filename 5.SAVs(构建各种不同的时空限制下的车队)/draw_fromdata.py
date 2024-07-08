# -*- coding:utf-8 -*-
#author:jeremy

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

def get_allDir(path):
    filename_list=[]
    dirList = os.listdir(path)
    for dir in dirList:
        dir_child = os.path.join(path, dir)
        if os.path.isdir(dir_child):
            filename_list=filename_list+get_allDir(dir_child)
        else:
            filename_list.append(dir_child)
    return filename_list

def draw_fromdata(input_filenam,output_filename):
    linestyle_color_list=[['-', 'black'], ['--', 'red'],['-.', 'dodgerblue'],[':', 'darkorange'], ]
    filename_list=get_allDir(input_filenam)
    pictureNames=['_checi.csv','_cheshu.csv','_cheshu_zaike_kongshi.csv','_zhuangtai.csv',
                  '_cheshu_beibu.csv','_cheshu_beibu_zaike_kongshi.csv','_cheshu_dongbu.csv','_cheshu_dongbu_zaike_kongshi.csv',
                  '_cheshu_futianA.csv','_cheshu_futianA_zaike_kongshi.csv','_cheshu_futianB.csv','_cheshu_futianB_zaike_kongshi.csv',
                  '_cheshu_luohu.csv','_cheshu_luohu_zaike_kongshi.csv','_cheshu_nanshan.csv','_cheshu_nanshan_zaike_kongshi.csv',
                  '_cheshu_xibu.csv','_cheshu_xibu_zaike_kongshi.csv','_zhuangtai_beibu.csv','_zhuangtai_dongbu.csv',
                  '_zhuangtai_futianA.csv','_zhuangtai_futianB.csv','_zhuangtai_luohu.csv','_zhuangtai_nanshan.csv',
                  '_zhuangtai_xibu.csv','_cheshu_time.csv','_cheshu_time_zaike_kongshi.csv','_zhuangtai_time.csv']

    for pictureName in pictureNames:
        save_filenames = []
        for filename in filename_list:
            for date in ['1205','1206','1207','1208','1209','1210','1211']:
                if date+pictureName in filename:
                    save_filenames.append(filename)
        dfs = []
        for fileName in save_filenames:
            df=pd.read_csv(fileName)
            df=df.iloc[:,1:]
            for col in df.columns:
                for date in ['1205','1206','1207','1208','1209','1210','1211']:
                    if '('+date+')' in col:
                        df=df.rename(columns={col:col.replace('('+date+')','')})
            dfs.append(df)
        if len(dfs)>0:
            data=pd.concat(dfs,ignore_index=True)
            fig = plt.figure(figsize=(18, 12), dpi=1000)
            for i in range(len(data.columns)):
                # print(i)
                col=data.columns[i]
                plt.plot(list(data.index),data.loc[:,col],
                        label=col,
                        lw=5,  # 折线图的线条宽度
                        linestyle=linestyle_color_list[i][0],
                        color=linestyle_color_list[i][1],)
            plt.xticks(ticks=np.array(range(8)) * len(dfs[0]), labels=range(8), fontsize=28)
            plt.yticks(fontsize=28)
            plt.xlim(0, len(data))
            plt.ylim(0, data.values.max()*1.1)
            plt.xlabel('day index', fontsize=35)
            # plt.ylabel(, fontsize=35)

            plt.legend(fontsize=30, bbox_to_anchor=(1.2, -0.1), ncol=1)
            plt.subplots_adjust(bottom=0.2)
            plt.savefig(output_filename+'/'+pictureName[1:].replace('.csv',''))
            plt.close()

if __name__ == '__main__':
    draw_fromdata('./picture/600 40000','./picture/600 40000')