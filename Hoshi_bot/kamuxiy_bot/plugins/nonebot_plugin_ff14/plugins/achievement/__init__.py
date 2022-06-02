from nonebot.plugin import on_command
from io import BytesIO
from nonebot.params import Arg,CommandArg,ArgPlainText
from nonebot.adapters.onebot.v11 import MessageEvent,Message,Bot
from nonebot.adapters import MessageSegment
import httpx
from ....nonebot_plugin_ff14 import config

PLUGIN_COMMAND = "/成就"

PLUGIN_INFO = "查询成就"

HELP_INFO = """/成就 ID
"""


achievement = on_command("achievement",priority=5, aliases={"成就"})


@achievement.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    arg = args.extract_plain_text()
    if arg:
        args["id"] = arg


@achievement.got("id", prompt="想要查询的道具ID是多少？")
async def _get(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    item_id: str = args['id']
    if not item_id.isdecimal():
        if item_id == '取消':
            await achievement.finish()
        await achievement.reject("请输入成就ID，搜索请使用命令/搜索，取消请输入“取消”")
    item_info = await get_item_info(item_id)
    await achievement.finish(item_info)


async def get_item_info(_id):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("{}/achievement/{}".format(config.kafeapi, _id))
        except httpx.ConnectTimeout:
            return "请求超时，请检查服务器网络！"
        if not response.status_code == 200:
            return "查询失败，请检查ID是否正确！"
        else:
            try:
                _json = response.json()
            except Exception as e:
                return "请求失败！{}".format(e)
            name = _json['Name']
            description = _json['Description']
            version = _json['GamePatch']['Version']
            icon_url = _json['Icon']
            text = "名称：{}\n说明：{}\n版本：{}".format(name, description, version)
            try:
                res: httpx.Response = await client.get("{}{}".format(config.kafeapi, icon_url))
            except Exception as e:
                message = Message.template(MessageSegment.text(text))
            else:
                message = Message.template(MessageSegment.image(BytesIO(res.content)) + MessageSegment.text(text))
            return message
