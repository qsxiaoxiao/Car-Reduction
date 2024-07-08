from utils import *
from pathlib import Path
from config import Config

def jiedian_split_by_region(source_file):
    global_config = Config('./config.ini')
    source_data_path = global_config.getRaw('设置条件', 'source_data_path')

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

    for date in source_file:
        create_dir(source_data_path)
        path_file = Path(source_data_path + '/' + str(date) + '_jiedian_' + 'xibu' + '.csv')
        if path_file.exists():
            print('存在文件：' + source_data_path + '/' + str(date) + '_jiedian_' + 'xibu' + '.csv')
        else:
            xibu_jiedian_index = []
            nanshan_jiedian_index = []
            futianA_jiedian_index = []
            futianB_jiedian_index = []
            luohu_jiedian_index = []
            beibu_jiedian_index = []
            dongbu_jiedian_index = []
            qita_jiedian_index = []
            df_jiedian = pd.read_csv(open(source_data_path + '/' + str(date) + '_jiedian.csv'),
                                     dtype={'start_kid': str, 'end_kid': str, 'car_id': str, 'end_time': int,
                                            'start_time': int})

            for index, row in df_jiedian.iterrows():
                # print(index)  # 输出每行的索引值
                if row['start_kid'] in xibu_kakou_list:
                    xibu_jiedian_index.append(index)
                elif row['start_kid'] in nanshan_kakou_list:
                    nanshan_jiedian_index.append(index)
                elif row['start_kid'] in futianA_kakou_list:
                    futianA_jiedian_index.append(index)
                elif row['start_kid'] in futianB_kakou_list:
                    futianB_jiedian_index.append(index)
                elif row['start_kid'] in luohu_kakou_list:
                    luohu_jiedian_index.append(index)
                elif row['start_kid'] in beibu_kakou_list:
                    beibu_jiedian_index.append(index)
                elif row['start_kid'] in dongbu_kakou_list:
                    dongbu_jiedian_index.append(index)
                elif row['start_kid'] in qita_kakou_list:
                    qita_jiedian_index.append(index)

            df_jiedian.iloc[xibu_jiedian_index].to_csv(source_data_path + '/' + str(date) + '_jiedian_' + 'xibu.csv',index=False)
            df_jiedian.iloc[nanshan_jiedian_index].to_csv(source_data_path + '/' + str(date) + '_jiedian_' + 'nanshan.csv',index=False)
            df_jiedian.iloc[futianA_jiedian_index].to_csv(source_data_path + '/' + str(date) + '_jiedian_' + 'futianA.csv',index=False)
            df_jiedian.iloc[futianB_jiedian_index].to_csv(source_data_path + '/' + str(date) + '_jiedian_' + 'futianB.csv',index=False)
            df_jiedian.iloc[luohu_jiedian_index].to_csv(source_data_path + '/' + str(date) + '_jiedian_' + 'luohu.csv',index=False)
            df_jiedian.iloc[beibu_jiedian_index].to_csv(source_data_path + '/' + str(date) + '_jiedian_' + 'beibu.csv',index=False)
            df_jiedian.iloc[dongbu_jiedian_index].to_csv(source_data_path + '/' + str(date) + '_jiedian_' + 'dongbu.csv',index=False)
            df_jiedian.iloc[qita_jiedian_index].to_csv(source_data_path + '/' + str(date) + '_jiedian_' + 'qita.csv',index=False)