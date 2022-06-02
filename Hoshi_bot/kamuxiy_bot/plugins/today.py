from nonebot import on_command, on_startswith
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import GroupMessageEvent,Bot,Message

from bilibili_api import article, sync
import urllib3
import json
flag=1
today = on_command("today", aliases={'日报', }, priority=5)
week=on_command("week", aliases={'周报', }, priority=5)
# today_loacl=on_command("today_loacl", aliases={'/日报', }, priority=5)
flag_1=on_command("/flag_1",priority=99)
flag_0=on_command("/flag_0",priority=99)
flag_c=on_command("/flag",priority=99)
@flag_1.handle()
async def handle_first_receive(event: GroupMessageEvent,message: Message = CommandArg()):
    global flag
    flag=1
    await flag_1.send("日报周报已打开")
@flag_0.handle()
async def handle_first_receive(event: GroupMessageEvent,message: Message = CommandArg()):
    global flag
    flag=0
    await flag_0.send("日报周报已关闭")
@flag_c.handle()
async def handle_first_receive(event: GroupMessageEvent,message: Message = CommandArg()):
    await flag_c.send("flag=="+str(flag))

@today.handle()
async def handle_first_receive(event: GroupMessageEvent,message: Message = CommandArg()):
    if(flag==1 or event.event.group_id==213665232):
        try:
            try:
                url = 'https://test.tianque.top/destiny2/today/'
    
                r = urllib3.PoolManager().request('GET', url)
                hjson = json.loads(r.data.decode())
    
                img_url = hjson["img_url"]
    
                #print(img_url)
                cq = "[CQ:image,file=" + img_url + ",id=40000]"
                #await today.send(Message('json：\n'+str(hjson)+
                #                        '\nimg_url：\n'+img_url+
                #                        '\n'+cq))
                await today.send(Message(cq))
            except:
                url = 'https://test.tianque.top/destiny2/today/'
    
                r = urllib3.PoolManager().request('GET', url)
                hjson = json.loads(r.data.decode())
    
                error_url = hjson["error"]
                await today.send("获取日报失败\n"+
                                "error:\n"+
                                error_url)
        except :
            await today.send("获取日报失败:\n服务器错误")

@week.handle()
async def handle_first_receive(event:GroupMessageEvent,message: Message = CommandArg()):
    if(flag==1 or event.group_id==213665232):
        try:
            
            ar = await article.get_article_list(rlid=175327)
            ar_id=ar["articles"][-1]["id"]
    
            ar_text=article.Article(ar_id)
            await ar_text.fetch_content()
            img_url=ar_text.json()["children"][2]["url"]
            cq = "[CQ:image,file=" + img_url + ",id=40000]"
            #await today.send(Message('json：\n'+str(hjson)+
            #                        '\nimg_url：\n'+img_url+
            #                        '\n'+cq))
            await week.send(Message(cq))
    
      
        except :
            await week.send("获取周报失败")
'''
@today_loacl.handle()
async def handle_first_receive(event: GroupMessageEvent,message: Message = CommandArg()):
    if(flag==1):
        try:
            url = 'http://download.kamuxiy.top:88/wp-content/uploads/today.jpg'
            cq = "[CQ:image,file=" + url+ ",id=40000]"
            await today_loacl.send(Message(cq))
        except :
            await today_loacl.send(Message("无可用本地日报"))
'''