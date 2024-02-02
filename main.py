from bilibili_api import search, sync, video as bilivideo, credential
import time, json, requests, crawler, api, tools, asyncio, image_printer as printer
import asyncio
import threading

# 从bili_credential.json文件中读取credential
with open("bili_credential.json", "r") as f:
    credential_json = json.load(f)
    credential = credential.Credential(
        sessdata=credential_json["sessdata"],
        bili_jct=credential_json["bili_jct"])
videos = tools.get_today_video(credential)
