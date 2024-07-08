# -*- coding:utf-8 -*-
#author:jeremy

from config import Config
from jiedian import get_jiedian
import json
from path_split_time import get_path_split_time
from jiedian_split_time import jiedian_split_by_time
from path import get_path
from path_split_region import get_path_split_region
from jiedian_split_region import jiedian_split_by_region

if __name__ == '__main__':
    global_config = Config('./config.ini')
    source_file = global_config.getRaw('设置条件', 'source_file')
    source_file = json.loads(source_file)#str转list
    print(source_file)
    #get_jiedian(source_file)
    #jiedian_split_by_time(source_file)
    # jiedian_split_by_region(source_file)

    # get_path(source_file)
    #get_path_split_time(source_file)
    get_path_split_region(source_file)



