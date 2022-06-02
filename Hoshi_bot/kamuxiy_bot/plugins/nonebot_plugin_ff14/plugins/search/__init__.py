import nonebot
from nonebot.plugin import on_command
from nonebot.adapters.onebot.v11 import MessageEvent,Message,Bot
from nonebot.params import Arg,CommandArg,ArgPlainText
import httpx
from httpx import Response
from ....nonebot_plugin_ff14 import config
from urllib import parse

PLUGIN_COMMAND = "/搜索"

PLUGIN_INFO = "搜索信息"

HELP_INFO = """/搜索 类型 名称
"""


search = on_command("search", priority=5, aliases={"搜索"})
# TODO:精准搜索


@search.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    arg = args.extract_plain_text()
    if arg:
        arg = arg.split(" ")
        if len(arg) == 1:
            if not arg[0] == "道具":
                args['name'] = arg[0]
            args['type'] = "道具"
        if len(arg) == 2:
            args['type'] = arg[0]
            args['name'] = arg[1]


@search.got("type", prompt="想搜索什么？请输入道具名称或搜索类型（道具, 成就）")
async def _get(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    _type = args["type"]
    if _type in ['道具', '成就', '称号']:
        args['type'] = _type
    else:
        args['type'] = '道具'


@search.got("name", prompt="名称是什么？")
async def _get(bot: Bot, event: MessageEvent, state: Message = CommandArg()):
    search_result = await get_result(state['type'], state['name'])
    await search.finish(search_result)


async def get_result(_type: str, name: str):
    async with httpx.AsyncClient() as client:
        search_type = {"道具": "Item", "成就": "Achievement", "称号": "Title"}
        url = "{}".format(config.kafeapi) + parse.quote("/search/?indexes={}&string={}&limit=10"
                                                        .format(search_type[_type], name))
        response: Response = await client.get(url)
        if not response.status_code == 200:
            nonebot.logger.error(response.text)
            return "请求失败！"
        else:
            _json = response.json()
            if _json['Results']:
                return make_message(_json['Results'], _type)
            else:
                return "未搜到任何内容！"


def make_message(results, _type):
    message = ""
    for item in results:
        message += "{}  {}\n".format(item["ID"], item["Name"])
    message += "请输入'/{} ID' 查询对应内容的详细信息".format(_type)
    return message
