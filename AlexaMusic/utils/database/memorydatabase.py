# Copyright (C) 2025 by Alexa_Help @ Github, < https://github.com/TheTeamAlexa >
# Subscribe On YT < Jankari Ki Duniya >. All rights reserved. © Alexa © Yukki.

"""
TheTeamAlexa is a project of Telegram bots with variety of purposes.
Copyright (c) 2021 ~ Present Team Alexa <https://github.com/TheTeamAlexa>

This program is free software: you can redistribute it and can modify
as you want or you can collabe if you have new ideas.
"""


import config
from config import PRIVATE_BOT_MODE
from AlexaMusic.core.mongo import mongodb

channeldb = mongodb.cplaymode
commanddb = mongodb.commands
cleandb = mongodb.cleanmode
playmodedb = mongodb.playmode
playtypedb = mongodb.playtypedb
langdb = mongodb.language
authdb = mongodb.adminauth
videodb = mongodb.yukkivideocalls
onoffdb = mongodb.onoffper
suggdb = mongodb.suggestion
autoenddb = mongodb.autoend


# Shifting to memory [ mongo sucks often]
loop = {}
playtype = {}
playmode = {}
channelconnect = {}
langm = {}
pause = {}
mute = {}
audio = {}
video = {}
active = []
activevideo = []
command = []
cleanmode = []
nonadmin = {}
vlimit = []
maintenance = []
suggestion = {}
autoend = {}


# Auto End Stream


async def is_autoend() -> bool:
    chat_id = 123
    mode = autoend.get(chat_id)
    if not mode:
        user = await autoenddb.find_one({"chat_id": chat_id})
        if not user:
            autoend[chat_id] = False
            return False
        autoend[chat_id] = True
        return True
    return mode


async def autoend_on():
    chat_id = 123
    autoend[chat_id] = True
    user = await autoenddb.find_one({"chat_id": chat_id})
    if not user:
        return await autoenddb.insert_one({"chat_id": chat_id})


async def autoend_off():
    chat_id = 123
    autoend[chat_id] = False
    user = await autoenddb.find_one({"chat_id": chat_id})
    if user:
        return await autoenddb.delete_one({"chat_id": chat_id})


# SUGGESTION


async def is_suggestion(chat_id: int) -> bool:
    mode = suggestion.get(chat_id)
    if not mode:
        user = await suggdb.find_one({"chat_id": chat_id})
        if not user:
            suggestion[chat_id] = True
            return True
        suggestion[chat_id] = False
        return False
    return mode


async def suggestion_on(chat_id: int):
    suggestion[chat_id] = True
    user = await suggdb.find_one({"chat_id": chat_id})
    if user:
        return await suggdb.delete_one({"chat_id": chat_id})


async def suggestion_off(chat_id: int):
    suggestion[chat_id] = False
    user = await suggdb.find_one({"chat_id": chat_id})
    if not user:
        return await suggdb.insert_one({"chat_id": chat_id})


# LOOP PLAY
async def get_loop(chat_id: int) -> int:
    lop = loop.get(chat_id)
    return lop or 0


async def set_loop(chat_id: int, mode: int):
    loop[chat_id] = mode


# Channel Play IDS
async def get_cmode(chat_id: int) -> int:
    mode = channelconnect.get(chat_id)
    if not mode:
        mode = await channeldb.find_one({"chat_id": chat_id})
        if not mode:
            return None
        channelconnect[chat_id] = mode["mode"]
        return mode["mode"]
    return mode


async def set_cmode(chat_id: int, mode: int):
    channelconnect[chat_id] = mode
    await channeldb.update_one(
        {"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True
    )


# PLAY TYPE WHETHER ADMINS ONLY OR EVERYONE
async def get_playtype(chat_id: int) -> str:
    mode = playtype.get(chat_id)
    if not mode:
        mode = await playtypedb.find_one({"chat_id": chat_id})
        if not mode:
            playtype[chat_id] = "Everyone"
            return "Everyone"
        playtype[chat_id] = mode["mode"]
        return mode["mode"]
    return mode


async def set_playtype(chat_id: int, mode: str):
    playtype[chat_id] = mode
    await playtypedb.update_one(
        {"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True
    )


# play mode whether inline or direct query
async def get_playmode(chat_id: int) -> str:
    mode = playmode.get(chat_id)
    if not mode:
        mode = await playmodedb.find_one({"chat_id": chat_id})
        if not mode:
            playmode[chat_id] = "Direct"
            return "Direct"
        playmode[chat_id] = mode["mode"]
        return mode["mode"]
    return mode


async def set_playmode(chat_id: int, mode: str):
    playmode[chat_id] = mode
    await playmodedb.update_one(
        {"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True
    )


# language
async def get_lang(chat_id: int) -> str:
    mode = langm.get(chat_id)
    if not mode:
        lang = await langdb.find_one({"chat_id": chat_id})
        if not lang:
            langm[chat_id] = "en"
            return "en"
        langm[chat_id] = lang["lang"]
        return lang["lang"]
    return mode


async def set_lang(chat_id: int, lang: str):
    langm[chat_id] = lang
    await langdb.update_one({"chat_id": chat_id}, {"$set": {"lang": lang}}, upsert=True)


# Muted
async def is_muted(chat_id: int) -> bool:
    mode = mute.get(chat_id)
    return mode or False


async def mute_on(chat_id: int):
    mute[chat_id] = True


async def mute_off(chat_id: int):
    mute[chat_id] = False


# Pause-Skip
async def is_music_playing(chat_id: int) -> bool:
    mode = pause.get(chat_id)
    return mode or False


async def music_on(chat_id: int):
    pause[chat_id] = True


async def music_off(chat_id: int):
    pause[chat_id] = False


# Active Voice Chats
async def get_active_chats() -> list:
    return active


async def is_active_chat(chat_id: int) -> bool:
    return chat_id in active


async def add_active_chat(chat_id: int):
    if chat_id not in active:
        active.append(chat_id)


async def remove_active_chat(chat_id: int):
    if chat_id in active:
        active.remove(chat_id)


# Active Video Chats
async def get_active_video_chats() -> list:
    return activevideo


async def is_active_video_chat(chat_id: int) -> bool:
    return chat_id in activevideo


async def add_active_video_chat(chat_id: int):
    if chat_id not in activevideo:
        activevideo.append(chat_id)


async def remove_active_video_chat(chat_id: int):
    if chat_id in activevideo:
        activevideo.remove(chat_id)


# Delete command mode
async def is_commanddelete_on(chat_id: int) -> bool:
    return chat_id not in command


async def commanddelete_off(chat_id: int):
    if chat_id not in command:
        command.append(chat_id)


async def commanddelete_on(chat_id: int):
    try:
        command.remove(chat_id)
    except Exception:
        pass


# Clean Mode
async def is_cleanmode_on(chat_id: int) -> bool:
    return chat_id not in cleanmode


async def cleanmode_off(chat_id: int):
    if chat_id not in cleanmode:
        cleanmode.append(chat_id)


async def cleanmode_on(chat_id: int):
    try:
        cleanmode.remove(chat_id)
    except Exception:
        pass


# Non Admin Chat
async def check_nonadmin_chat(chat_id: int) -> bool:
    user = await authdb.find_one({"chat_id": chat_id})
    return bool(user)


async def is_nonadmin_chat(chat_id: int) -> bool:
    mode = nonadmin.get(chat_id)
    if not mode:
        user = await authdb.find_one({"chat_id": chat_id})
        if not user:
            nonadmin[chat_id] = False
            return False
        nonadmin[chat_id] = True
        return True
    return mode


async def add_nonadmin_chat(chat_id: int):
    nonadmin[chat_id] = True
    is_admin = await check_nonadmin_chat(chat_id)
    if is_admin:
        return
    return await authdb.insert_one({"chat_id": chat_id})


async def remove_nonadmin_chat(chat_id: int):
    nonadmin[chat_id] = False
    is_admin = await check_nonadmin_chat(chat_id)
    if not is_admin:
        return
    return await authdb.delete_one({"chat_id": chat_id})


# Video Limit
async def is_video_allowed(chat_idd) -> str:
    chat_id = 123456
    if not vlimit:
        dblimit = await videodb.find_one({"chat_id": chat_id})
        if not dblimit:
            vlimit.clear()
            vlimit.append(config.VIDEO_STREAM_LIMIT)
            limit = config.VIDEO_STREAM_LIMIT
        else:
            limit = dblimit["limit"]
            vlimit.clear()
            vlimit.append(limit)
    else:
        limit = vlimit[0]
    if limit == 0:
        return False
    count = len(await get_active_video_chats())
    if count == int(limit) and not await is_active_video_chat(chat_idd):
        return False
    return True


async def get_video_limit() -> str:
    if not vlimit:
        chat_id = 123456
        dblimit = await videodb.find_one({"chat_id": chat_id})
        return dblimit["limit"] if dblimit else config.VIDEO_STREAM_LIMIT
    else:
        return vlimit[0]


async def set_video_limit(limt: int):
    chat_id = 123456
    vlimit.clear()
    vlimit.append(limt)
    return await videodb.update_one(
        {"chat_id": chat_id}, {"$set": {"limit": limt}}, upsert=True
    )


# On Off
async def is_on_off(on_off: int) -> bool:
    onoff = await onoffdb.find_one({"on_off": on_off})
    return bool(onoff)


async def add_on(on_off: int):
    is_on = await is_on_off(on_off)
    if is_on:
        return
    return await onoffdb.insert_one({"on_off": on_off})


async def add_off(on_off: int):
    is_off = await is_on_off(on_off)
    if not is_off:
        return
    return await onoffdb.delete_one({"on_off": on_off})


# Maintenance


async def is_maintenance():
    if maintenance:
        return 1 not in maintenance
    get = await onoffdb.find_one({"on_off": 1})
    if not get:
        maintenance.clear()
        maintenance.append(2)
        return True
    else:
        maintenance.clear()
        maintenance.append(1)
        return False


async def maintenance_off():
    maintenance.clear()
    maintenance.append(2)
    is_off = await is_on_off(1)
    if not is_off:
        return
    return await onoffdb.delete_one({"on_off": 1})


async def maintenance_on():
    maintenance.clear()
    maintenance.append(1)
    is_on = await is_on_off(1)
    if is_on:
        return
    return await onoffdb.insert_one({"on_off": 1})


# Audio Video Limit

from pytgcalls.types.input_stream.quality import AudioQuality, VideoQuality


async def save_audio_bitrate(chat_id: int, bitrate: str):
    audio[chat_id] = bitrate


async def save_video_bitrate(chat_id: int, bitrate: str):
    video[chat_id] = bitrate


async def get_aud_bit_name(chat_id: int) -> str:
    mode = audio.get(chat_id)
    return mode or "High"


async def get_vid_bit_name(chat_id: int) -> str:
    mode = video.get(chat_id)
    return mode or "Medium"


async def get_audio_bitrate(chat_id: int) -> str:
    mode = audio.get(chat_id)
    if not mode:
        return AudioQuality.HIGH
    if str(mode) == "High":
        return AudioQuality.STUDIO
    elif str(mode) == "Medium":
        return AudioQuality.HIGH
    elif str(mode) == "Low":
        return AudioQuality.LOW()


async def get_video_bitrate(chat_id: int) -> str:
    mode = video.get(chat_id)
    if not mode:
        if PRIVATE_BOT_MODE == str(True):
            return VideoQuality.FHD_1080p
        else:
            return VideoQuality.HD_720p
    if str(mode) == "High":
        return VideoQuality.QHD_2K
    elif str(mode) == "Medium":
        return VideoQuality.FHD_1080p
    elif str(mode) == "Low":
        return VideoQuality.HD_720p
