import json
from functools import partial
import re
import FrameAPI
import os
import importlib

PluginList = []

# 默认config.json目录：../../PyPluginConfig/AsoulFansCounting
# 或者 ./PyPluginConfig

def CheckCommand(MessageType, MessageContain,CommandMap):
    for x in CommandMap.keys():
        t = json.loads(x)
        MatchResult = re.match(t[1], MessageContain)
        if(t[0] == MessageType and MatchResult != None):
            return (CommandMap[x],MatchResult.groups())
    return None

def MainHandler(Message,BOT):
    for message in Message:
        for plugin in PluginList:
            if(message['type'] == 'GroupMessage'):
                CommandMap = plugin.GroupCommandMap
            elif(message['type'] == 'FriendMessage'):
                CommandMap = plugin.FriendCommandMap
            else:
                CommandMap = None
            if CommandMap != None:
                for item in message['messageChain']:
                    try:
                        t = CheckCommand(
                                item['type'], item['text'], CommandMap)
                        if t != None:
                            print("Message Recognized ,running Plugin ",plugin,"'s action ",t[0])
                            plugin.FuncMap[t[0]](t[1],sender = message['sender'],bot = BOT)
                    except KeyError:
                        pass

def PluginImporter():
    global PluginList
    L = os.listdir('./PyPlugin/')
    for x in L:
        PluginName = importlib.import_module('PyPlugin.'+x)
        PluginList.append(PluginName)

if __name__ == '__main__':
    PluginImporter()
    BOT = FrameAPI.HttpBot()
    BOT.Login()
    BOT.MessageChecker(MainHandler)