from nonebot.adapters.onebot.v11 import Message,Bot,MessageEvent
from ... import _sub_plugins
from nonebot.plugin import on_command
from nonebot.params import Arg,CommandArg,ArgPlainText
plugin_help = on_command("ff14")


@plugin_help.handle()
async def _(bot: Bot, event: MessageEvent,args: Message = CommandArg()):
    arg = args.extract_plain_text()
    if arg:
        args['arg'] = arg
    else:
        names_str = ""
        for plugin in get_plugin_help_list():
            names_str += "{}:{}\n".format(plugin['name'], plugin['info'])
        names_str += "想查询哪个插件的帮助？或者输入list查询命令列表"
        await plugin_help.reject(names_str)


@plugin_help.got('arg')
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    arg = args['arg']
    plugin_help_list = get_plugin_help_list()
    help_info = ""
    if arg == "list":
        for _help in plugin_help_list:
            if _help['command']:
                help_info += "{}:{}".format(_help['command'], _help['info'])
        await plugin_help.finish(help_info)
    for _help in plugin_help_list:
        if arg == _help['name']:
            await plugin_help.finish(_help['help'])


def get_plugin_help_list():
    """获取子插件名称列表"""
    name_list = list()
    for sub_plugin in _sub_plugins:
        if sub_plugin.name == "help":
            continue
        try:
            help_info = {'name': sub_plugin.name, 'info': sub_plugin.module.PLUGIN_INFO,
                         'help': sub_plugin.module.HELP_INFO, 'command': sub_plugin.module.PLUGIN_COMMAND}
        except AttributeError:
            help_info = {'name': sub_plugin.name, 'info': "", 'help': "", 'command': ''}
        name_list.append(help_info)
    return name_list
