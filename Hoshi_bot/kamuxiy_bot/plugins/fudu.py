from nonebot.plugin import on_command, on_startswith, require, on_message
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.params import Arg,CommandArg,ArgPlainText
from nonebot.adapters.onebot.v11 import MessageEvent,Message,Bot, GroupMessageEvent
from nonebot.adapters import *
import urllib3
import json
#fudu = on_message(priority=99)
fudu = on_command("fudu", aliases={'获取历史记录', }, priority=5)
@fudu.handle()
async def handle_first_receive(bot:Bot,event: MessageEvent,message: Message = CommandArg()):
    #await fudu.send("111")
    if event.group_id == 730144072:
        mage=await bot.call_api("get_group_msg_history",group_id = event.group_id)
    
        #message1=str(message['messages'][-2]["message"])
        #message2=str(message['messages'][-1]["message"])
        #if  message2==message1:
        #        await fudu.send("[CQ:image,file='http://101.43.165.10/wp-content/uploads/2022/05/QQ图片20220510101153.jpg',id=40000]")
        await fudu.send(type(mage))