from nonebot.plugin import on_command, on_startswith, require
from nonebot.rule import to_me

from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import MessageEvent,Message,Bot, GroupMessageEvent

from bs4 import BeautifulSoup
import urllib3
import json
import matplotlib.pyplot as plt
import os
import random
import time


HMST = on_command("HMST", aliases={'/图库', }, priority=5)

files = []
@HMST.handle()
async def handle_first_receive(event: MessageEvent,message: Message = CommandArg()):
    try:
        all_files = os.listdir('/home/kamuxiy_s_bot/kamuxiyBot/cqhttp/data/images/setu/')
        #print(all_files)
        #print(len(all_files))
    
        path = r'/home/kamuxiy_s_bot/kamuxiyBot/cqhttp/data/images/setu/'
    
        # print(os.listdir(path))
    
        ls = os.listdir(path)
    
        
        def get_all_file(dir_path):
            global files
            for filepath in os.listdir(dir_path):
                tmp_path = os.path.join(dir_path,filepath)
                if os.path.isdir(tmp_path):
                    get_all_file(tmp_path)
                else:
                    files.append(tmp_path)
            return files
        
        def calc_files_size(files_path):
            files_size = 0
            for f in files_path:
                files_size += os.path.getsize(f)
            return files_size
    
    
    
        files = get_all_file(path)
        st=str(round(calc_files_size(files)/1024/1024/1024, 2))+' G'
        await HMST.send("本地图库内图片数量：\n"+str(len(all_files))+"\n本地图库大小：\n"+st)
        files.clear()
    except:
        await HMST.send("获取本地图库失败")
        files.clear()