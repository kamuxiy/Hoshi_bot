from nonebot.plugin import on_command
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import MessageEvent,Message,Bot
from io import BytesIO
from nonebot.params import Arg,CommandArg,ArgPlainText
from nonebot.adapters import MessageSegment
from nonebot.matcher import Matcher
import httpx
from ....nonebot_plugin_ff14 import config

PLUGIN_COMMAND = "/称号"

PLUGIN_INFO = "查询称号"

HELP_INFO = """/称号 ID
"""


title = on_command("title", priority=5, aliases={"称号"})


@title.handle()
async def _(matcher: Matcher,bot: Bot, event: MessageEvent, state: Message = CommandArg()):
    args = state.extract_plain_text()
    if args:
        matcher.set_arg("id", state)


@title.got("id", prompt="想要查询的道具ID是多少？")
async def _get(bot: Bot, event: MessageEvent, state: Message = CommandArg(),item_id: str=ArgPlainText("id")):
    if not item_id.isdecimal():
        if item_id == '取消':
            await title.finish()
        await title.reject("请输入称号ID，搜索请使用命令/搜索，取消请输入“取消”")
    item_info = await get_item_info(item_id)
    await title.finish(item_info)


async def get_item_info(_id):
    content_link_type = {'Achievement': '成就'}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("{}/title/{}".format(config.kafeapi, _id))
        except httpx.ConnectTimeout:
            return "请求超时，请检查服务器网络！"
        if not response.status_code == 200:
            return "查询失败，请检查ID是否正确！"
        else:
            try:
                _json = response.json()
            except Exception as e:
                return "请求失败！{}".format(e)
            for key in _json:
                print("{}: {}".format(key, _json[key]))
            name = _json['Name']
            content_link = _json['GameContentLinks']
            content_link_str = ""
            for _type in content_link:
                content_link_str += "{}: {}\n".format(content_link_type[_type], content_link[_type]['Title'])
            # description = _json['Description']
            version = _json['GamePatch']['Version']
            icon_url = _json['Icon']
            text = "名称：{}\n获取：\n{}版本：{}".format(name, content_link_str, version)
            try:
                res: httpx.Response = await client.get("{}{}".format(config.kafeapi, icon_url))
            except Exception as e:
                logger.error(e)
                message = Message.template(MessageSegment.text(text))
            else:
                message = Message.template(MessageSegment.image(BytesIO(res.content)) + MessageSegment.text(text))
            return message
