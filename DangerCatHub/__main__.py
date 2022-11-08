import glob
import os
import sys
from pathlib import Path

from DangerCat_config import Config
from DangerCatHub import LOGS, bot, tbot
from DangerCatHub.clients.session import H2, H3, H4, H5
from DangerCatHub.utils import (join_it, load_module,
                                logger_check, plug_channel,
                                start_msg, update_sudo)
from DangerCatHub.version import __dangerbotver__

# Global Variables #
DANGERCAT_PIC = "https://telegra.ph/file/7b5e8f87a0848fd18d30e.jpg"


# Client Starter
async def hells(session=None, client=None, session_name="Main"):
    if session:
        LOGS.info(f"••• Starting Client [{session_name}] •••")
        try:
            await client.start()
            return 1
        except:
            LOGS.error(f"Error in {session_name}!! Check & try again!")
            return 0
    else:
        return 0


# Load plugins based on config UNLOAD
async def plug_load(path):
    files = glob.glob(path)
    for name in files:
        with open(name) as CATHUB:
            path1 = Path(CATHUB.name)
            shortname = path1.stem
            if shortname.replace(".py", "") in Config.UNLOAD:
                os.remove(Path(f"DangerCatHub/plugins/{shortname}.py"))
            else:
                load_module(shortname.replace(".py", ""))


# Final checks after startup
async def dangerbot_is_on(total):
    await update_sudo()
    await logger_check(bot)
    await start_msg(tbot, DANGERCAT_PIC, __dangerbotver__, total)
    await join_it(bot)
    await join_it(H2)
    await join_it(H3)
    await join_it(H4)
    await join_it(H5)


# Hellbot starter...
async def start_dangerbot():
    try:
        tbot_id = await tbot.get_me()
        Config.BOT_USERNAME = f"@{tbot_id.username}"
        bot.tgbot = tbot
        LOGS.info("••• Starting DangerCat (TELETHON) •••")
        C1 = await hells(Config.DANGERCAT_SESSION, bot, "DANGERCAT_SESSION")
        C2 = await hells(Config.SESSION_2, H2, "SESSION_2")
        C3 = await hells(Config.SESSION_3, H3, "SESSION_3")
        C4 = await hells(Config.SESSION_4, H4, "SESSION_4")
        C5 = await hells(Config.SESSION_5, H5, "SESSION_5")
        await tbot.start()
        total = C1 + C2 + C3 + C4 + C5
        LOGS.info("••• DangerBot Startup Completed •••")
        LOGS.info("••• Starting to load Plugins •••")
        await plug_load("DangerCatHub/plugins/*.py")
        await plug_channel(bot, Config.PLUGIN_CHANNEL)
        LOGS.info("⚡ Your DangerCat Is Now Working ⚡")
        LOGS.info("Head to @Danger_Bots for Updates.")
        LOGS.info(f"» Total Clients = {str(total)} «")
        await dangerbot_is_on(total)
    except Exception as e:
        LOGS.error(f"{str(e)}")
        sys.exit()


bot.loop.run_until_complete(start_dangerbot())

if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    try:
        bot.run_until_disconnected()
    except ConnectionError:
        pass


# hellbot
