#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter

# Custom your logger
# 
# from nonebot.log import logger, default_format
# logger.add("error.log",
#            rotation="00:00",
#            diagnose=False,
#            level="ERROR",
#            format=default_format)

# You can pass some keyword args config to init function
nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)

nonebot.load_builtin_plugins("echo")
nonebot.load_builtin_plugins("single_session")
nonebot.load_plugin("kamuxiy_bot.plugins.st")
nonebot.load_plugin("kamuxiy_bot.plugins.st_r18")
nonebot.load_plugin("kamuxiy_bot.plugins.today")
nonebot.load_plugin("kamuxiy_bot.plugins.HMST")
nonebot.load_plugin("kamuxiy_bot.plugins.benzi")
nonebot.load_plugin("kamuxiy_bot.plugins.fudu")
nonebot.load_plugin("kamuxiy_bot.plugins.nonebot_plugin_ff14")

nonebot.load_plugin('nonebot_plugin_picsearcher')
nonebot.load_plugin('nonebot_plugin_petpet')
nonebot.load_plugin('nonebot_plugin_ygo')
#nonebot.load_plugin('nonebot_bison')
#nonebot.load_plugin('nonebot_plugin_ddcheck')
# Please DO NOT modify this file unless you know what you are doing!
# As an alternative, you should use command `nb` or modify `pyproject.toml` to load plugins
#nonebot.load_from_toml("pyproject.toml")

# Modify some config / config depends on loaded configs
# 
# config = driver.config
# do something...


if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
