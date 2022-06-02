from nonebot.plugin import on_command
from nonebot.adapters import MessageTemplate,MessageSegment
from urllib import parse
from nonebot.params import Arg,CommandArg,ArgPlainText
from nonebot.adapters.onebot.v11 import MessageEvent,Message,Bot
import httpx
from ....nonebot_plugin_ff14 import config


PLUGIN_COMMAND = "/道具"

PLUGIN_INFO = "查询道具"

HELP_INFO = """/道具 ID
"""


items = on_command("item", priority=5, aliases={"道具"})


@items.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    arg = str(event.get_message()).strip()
    if arg:
        args["id"] = arg


@items.got("id", prompt="想要查询的道具ID是多少？")
async def _get(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    item_id: str = args['id']
    if not item_id.isdecimal():
        if item_id == '取消':
            await items.finish()
        await items.reject("请输入道具ID，搜索请使用命令/搜索，取消请输入“取消”")
    item_info = await get_item_info(item_id)

    await items.finish(item_info)


async def get_item_info(_id):
    # MessageTemplate(MessageSegment.text())
    async with httpx.AsyncClient() as client:
        response = await client.get("{}/item/{}".format(config.kafeapi, _id))
        if not response.status_code == 200:
            return "请求失败！"
        else:
            try:
                _json = response.json()
            except Exception as e:
                return "请求失败！{}".format(e)
            item_name = _json['Name']
            url = "https://ff14.huijiwiki.com/wiki/{}".format(parse.quote("物品:{}".format(item_name)))
            return url

# def make_message():
#
