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
# bot部分
# 注册事件相应器
st = on_command("stst", aliases={'/来份色图', '/来份涩图', '/来张涩图', '/下次一定','/来份秋荷','/色图','/涩图','/来点色图','/来点二次元', '/来份月猫', "/来份麻衣学姐" }, priority=1)

st10=on_command("来五份涩图",aliases={"来五份色图"},priority=1)
#benzi=on_command("来份本子",priority=5)
# show_img=on_command("显示图片", priority=1)

async def stapi():
    # url拼接
    url = "https://api.lolicon.app/setu/v2"

    apikey = "445119235fe2e4ef8d8646"
    r18 = "0"
    num = "1"
    proxy="i.pixiv.re"

    url_str = url + "?apikey=" + apikey + "&r18=" + r18 + "&num=" + num + "&proxy=" + proxy

    # 访问网站获取json
    r = urllib3.PoolManager().request('GET', url_str)
    hjson = json.loads(r.data.decode())

    #quota = hjson["quota"]
    quota="error"
    st_url = hjson["data"][0]["urls"]["original"]
    st_pid = hjson["data"][0]["pid"]
    st_painter = hjson["data"][0]["author"]
    st_title = hjson["data"][0]["title"]

    # 读取图片
    path = "/home/kamuxiy_s_bot/kamuxiyBot/cqhttp/data/images/setu/" + str(st_pid) + st_url[-4:]

    img = urllib3.PoolManager().request('GET', st_url)
    with open(path, 'wb') as f:
        f.write(img.data)

    api_return = [
        st_url,
        quota,
        st_pid,
        st_painter,
        path,
        st_title
    ]
    return api_return


'''打印测试
    #!
    print(url_str)
    print(hjson)
    print(data_list)
    print(data_json)
    print(st_url)
    print(st_pid)
'''

@st.handle()
async def handle_first_receive(event: MessageEvent,message: Message = CommandArg()):
    await st.send("请稍等，图片正在下载~~\n请不要重复请求")
    try:
        api_return = await stapi()
        try:
            # await st.send("测试：返回url\n" + api_return[0] +
            #             "\n测试：返回图片地址\n" + api_return[4])
            cq = "[CQ:image,file=" + str(api_return[0]) + ",id=40000]"
            # await st.send("测试：返回cq码\n" + cq)
            await st.send(Message(cq +
                                  "\n" + api_return[5] +
                                  "\n画师：" + api_return[3] +
                                  "\npid:" + str(api_return[2]) +
                                  "\n图片地址" + str(api_return[0])))
        except:
            await st.send("图片发送出错\n" +
                          "cq:\n" + cq +
                          "\n-----------------------------------------------" +
                          "\n" + api_return[5] +
                          "\n画师：" + api_return[3] +
                          "\npid:" + str(api_return[2]) +
                          "\n图片地址" + str(api_return[0]))
    except:
        await st.send("无法启动线程")



async def stapi_nodl():
    img_name=[]
    for i in range(5):
        t=time.time()
        img_name.append("pic_"+str(t)+".jpg")
        filepath = "/home/kamuxiy_s_bot/kamuxiyBot/cqhttp/data/images/setu/pic_"+str(t)+".jpg"
        url="https://iw233.cn/API/Ghs.php"
        urlr="https://iw233.cn/API/Random.php"
        urlwp="https://iw233.cn/API/MirlKoi.php"
        urlnew="http://iw233.fgimax2.fgnwctvip.com/API/Ghs.php?type=json"
    
        #r=urllib3.PoolManager().request('GET', url)
        #print(r.data)
        img_json=urllib3.PoolManager().request('GET',urlnew)

        hjson=json.loads(img_json.data.decode("utf-8-sig"))
        img_url=hjson["pic"]
        img=urllib3.PoolManager().request('GET',img_url)

        with open(filepath, 'wb') as f:
            f.write(img.data)
    return img_name

@st10.handle()
async def handle_first_receive(bot:Bot,event:GroupMessageEvent,message: Message = CommandArg()):
    await st10.send("请稍等，图片正在下载~~\n请不要重复请求")
    try:
        img_name=await stapi_nodl()
        filepath="setu/"
        '''
        if api_return[5]:
            await st10.send("url读取失败")
        else:
            await st10.send("url读取完成")
        '''
        try:
            cq0 = "[CQ:image,file={},id=40000]".format(str(filepath+img_name[0]))
            cq1 = "[CQ:image,file={},id=40000]".format(str(filepath+img_name[1]))
            cq2 = "[CQ:image,file={},id=40000]".format(str(filepath+img_name[2]))
            cq3 = "[CQ:image,file={},id=40000]".format(str(filepath+img_name[3]))
            cq4 = "[CQ:image,file={},id=40000]".format(str(filepath+img_name[4]))
            #await st10.send(cq0+'\n'+cq1+'\n'+cq2+'\n'+cq3+'\n'+cq4)
            
            #await st10.send("cq赋值完成")
            
            #d_1=[{"type": "node","data": {"name": "ほしのすみか","uin": "310719275","content": cq0}},{"type": "node","data": {"name": "ほしのすみか","uin": "310719275","content": cq1}}]
            d=[{"type": "node","data": {"name": "ほしのすみか","uin": "310719275","content": cq0}},{"type": "node","data": {"name": "ほしのすみか","uin": "310719275","content": cq1}},{"type": "node","data": {"name": "ほしのすみか","uin": "310719275","content": cq2}},{"type": "node","data": {"name": "ほしのすみか","uin": "310719275","content": cq3}},{"type": "node","data": {"name": "ほしのすみか","uin": "310719275","content": cq4}}]
            #await st10.send(d)
            #await bot.send_group_forward_msg(group_id=event.group_id,messages=d_1)
            await bot.send_group_forward_msg(group_id=event.group_id,messages=d)
            if(event.group_id!=932215453):
                await bot.send_group_forward_msg(group_id=932215453,messages=d)
            if os.path.exists("demofile.txt"):
                os.remove("demofile.txt")
        except:
            await st10.send("图片发送出错")
    except:
        await st10.send("无法启动线程")


scheduler = require('nonebot_plugin_apscheduler').scheduler

#tim = on_command("/time_demo", priority=5)
#@tim.handle()
#async def tm():
name="定时发送涩图"
h=12
m=30
print("创建定时任务'"+name+"'于每天"+str(h).rjust(2,'0')+":"+str(m).rjust(2,'0'))
@scheduler.scheduled_job('cron', hour=h,minute=m)
async def tm():

    #driver = get_driver()
    #BOT_ID = str(driver.config.bot_id)
    bot = driver.bots["310719275"]
    
    group_id=932215453
    group_id1=213665232

    try:
        img_name=await stapi_nodl()
        filepath="setu/"
        '''
        if api_return[5]:
            await st10.send("url读取失败")
        else:
            await st10.send("url读取完成")
        '''
        try:
            cq0 = "[CQ:image,file={},id=40000]".format(str(filepath+img_name[0]))
            cq1 = "[CQ:image,file={},id=40000]".format(str(filepath+img_name[1]))
            cq2 = "[CQ:image,file={},id=40000]".format(str(filepath+img_name[2]))
            cq3 = "[CQ:image,file={},id=40000]".format(str(filepath+img_name[3]))
            cq4 = "[CQ:image,file={},id=40000]".format(str(filepath+img_name[4]))
            '''
            await st10.send(cq0+'\n'+cq1+'\n'+cq2+'\n'+cq3+'\n'+cq4)
            
            await st10.send("cq赋值完成")
            '''
            #d_1=[{"type": "node","data": {"name": "ほしのすみか","uin": "310719275","content": cq0}},{"type": "node","data": {"name": "ほしのすみか","uin": "310719275","content": cq1}}]
            d=[{"type": "node","data": {"name": "ほしのすみか","uin": "310719275","content": "自动发涩图功能"}}, {"type": "node","data": {"name": "ほしのすみか","uin": "310719275","content": cq0}},{"type": "node","data": {"name": "ほしのすみか","uin": "310719275","content": cq1}},{"type": "node","data": {"name": "ほしのすみか","uin": "310719275","content": cq2}},{"type": "node","data": {"name": "ほしのすみか","uin": "310719275","content": cq3}},{"type": "node","data": {"name": "ほしのすみか","uin": "310719275","content": cq4}}]
            #await st10.send(d)
            #await bot.send_group_forward_msg(group_id=event.group_id,messages=d_1)
            await bot.send_group_forward_msg(group_id=group_id,messages=d)
            await bot.send_group_forward_msg(group_id=group_id1,messages=d)
            
        except:
            await bot.call_api("send_private_msg",user_id=2181656404,message="图片发送出错")
    except:
        await bot.call_api("send_private_msg",user_id=2181656404,message="无法启动线程")
        

'''
@benzi.handle()
async def handle_first_receive(message: Message = CommandArg()):
    
    page=random.randint(1,300)
    url="zhb.eehentai.com/page/"+str(page)
    
    a=urllib3.PoolManager().request("GET", url)
    #print(a.data.decode())
    bf=BeautifulSoup(a.data.decode(),"lxml")
    dict=bf.find_all("div")
    #print(dict[4].attrs["class"])
    b_name_list=[]
    for name in dict:
        try:
            if name.attrs["class"][0]=="gallery":
    
                b_name_list.append(name.get_text().replace("\n",""))
        except KeyError:
            pass
    
    await benzi.send("随机本子推荐：\n"+b_name_list[random.randint(0,len(b_name_list))])
'''