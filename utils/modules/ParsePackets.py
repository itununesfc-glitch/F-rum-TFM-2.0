#coding: utf-8
import re, json, random, urllib, traceback, time as _time, base64, hashlib, struct, zlib

# Modules
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers
from Captcha import Captcha
from Lua import Lua
from Exceptions import *

# Library
from collections import deque

class ParsePackets:
    def __init__(self, player, server):
        self.client = player
        self.server = player.server
        self.Cursor = player.Cursor

    async def parsePacket(self, packetID, C, CC, packet):
        if C == Identifiers.recv.Old_Protocol.C:
            if CC == Identifiers.recv.Old_Protocol.Old_Protocol:
                data = packet.readUTFBytes(packet.readShort())
                if isinstance(data, bytes):
                    data = data.decode()
                await self.client.parsePackets.parsePacketUTF(data)
                return

        elif C == Identifiers.recv.Sync.C:
            if CC == Identifiers.recv.Sync.Object_Sync:
                roundCode = packet.readInt()
                if roundCode == self.client.room.lastRoundCode:
                    p = ByteArray()
                    while (packet.bytesAvailable()):
                        p.writeShort(packet.readShort())
                        code = packet.readShort()
                        p.writeShort(code)
                        if (code != 1):
                            p.writeBytes(packet.readUTFBytes(16)).writeBoolean(True)
                    self.client.room.sendAllOthers(self.client, Identifiers.send.Sync, p.toByteArray())
                return

            elif CC == Identifiers.recv.Sync.Mouse_Movement:
                packet2 = ByteArray().writeInt(self.client.playerCode).toByteArray() + packet.toByteArray()              
                a, e, i = packet.readInt(), packet.readBoolean(), packet.readBoolean()
                if not self.client.posY == 0 and not self.client.posX == 0:
                    lasty, lastx = self.client.posY, self.client.posX
                else:
                    lasty, lastx = 0, 0
                self.client.posX, self.client.posY = packet.readInt() * 800 // 2700, packet.readInt() * 800 // 2700
                if not lasty == 0 and not lastx == 0:
                    if not lasty == self.client.posY or not lastx == self.client.posX:
                        self.client.afkkilltimerreset()
                        if self.client.isAfk:
                            self.client.isAfk = False
                self.client.velX, self.client.velY, self.client.isJumping = packet.readShort(), packet.readShort(), packet.readBoolean()                
                self.client.room.sendAllOthers(self.client, Identifiers.send.Player_Movement, packet2)
                return

            elif CC == Identifiers.recv.Sync.Mort:
                roundCode, loc_1 = packet.readInt(), packet.readByte()
                if roundCode == self.client.room.lastRoundCode:
                    self.client.isDead = True
                    if not self.client.room.noAutoScore: self.client.playerScore += 1
                    self.client.sendPlayerDied()

                    if self.client.room.getPlayerCountUnique() >= self.server.leastMice:
                        if self.client.room.isSurvivor:
                            for client in self.client.room.clients.copy().values():
                                if client.isShaman:
                                    client.survivorDeath += 1
                                    if client.survivorDeath == 4:
                                        id = 2260
                                        if not id in client.playerConsumables:
                                            client.playerConsumables[id] = 1
                                        else:
                                            count = client.playerConsumables[id] + 1
                                            client.playerConsumables[id] = count
                                        client.sendAnimZeldaInventory(4, id, 1)
                                        client.survivorDeath = 0

                    if not self.client.room.currentShamanName == "":
                        player = self.client.room.clients.get(self.client.room.currentShamanName)

                        if player != None and not self.client.room.noShamanSkills:
                            if player.bubblesCount > 0:
                                if self.client.room.getAliveCount() != 1:
                                    player.bubblesCount -= 1
                                    self.client.sendPlaceObject(self.client.room.objectID + 2, 59, self.client.posX, 450, 0, 0, 0, True, True)

                            if player.desintegration:
                                self.client.parseSkill.sendSkillObject(6, self.client.posX, 395, 0)
                    self.client.room.checkChangeMap()
                return

            elif CC == Identifiers.recv.Sync.Player_Position:
                direction = packet.readBoolean()
                self.client.room.sendAll(Identifiers.send.Player_Position, ByteArray().writeInt(self.client.playerCode).writeBoolean(direction).toByteArray())
                return

            elif CC == Identifiers.recv.Sync.Shaman_Position:
                direction = packet.readBoolean()
                self.client.room.sendAll(Identifiers.send.Shaman_Position, ByteArray().writeInt(self.client.playerCode).writeBoolean(direction).toByteArray())
                return

            elif CC == Identifiers.recv.Sync.Crouch:
                crouch = packet.readByte()
                self.client.room.sendAll(Identifiers.send.Crouch, ByteArray().writeInt(self.client.playerCode).writeByte(crouch).writeByte(0).toByteArray())
                return

        elif C == Identifiers.recv.Room.C:
            if CC == Identifiers.recv.Room.Map_26:
                if self.client.room.currentMap == 26:
                    posX, posY, width, height = packet.readShort(), packet.readShort(), packet.readShort(), packet.readShort()
                    bodyDef = {}
                    bodyDef["type"] = 12
                    bodyDef["width"] = width
                    bodyDef["height"] = height
                    self.client.room.addPhysicObject(0, posX, posY, bodyDef)
                return

            elif CC == Identifiers.recv.Room.Shaman_Message:
                type, x, y = packet.readByte(), packet.readShort(), packet.readShort()
                self.client.room.sendAll(Identifiers.send.Shaman_Message, ByteArray().writeByte(type).writeShort(x).writeShort(y).toByteArray())
                return

            elif CC == Identifiers.recv.Room.Convert_Skill:
                objectID = packet.readInt()
                self.client.parseSkill.sendConvertSkill(objectID)
                return

            elif CC == Identifiers.recv.Room.Demolition_Skill:
                objectID = packet.readInt()
                self.client.parseSkill.sendDemolitionSkill(objectID)
                return

            elif CC == Identifiers.recv.Room.Projection_Skill:
                posX, posY, dir = packet.readShort(), packet.readShort(), packet.readShort()
                self.client.parseSkill.sendProjectionSkill(posX, posY, dir)
                return

            elif CC == Identifiers.recv.Room.Enter_Hole:
                holeType, roundCode, monde, distance, holeX, holeY = packet.readByte(), packet.readInt(), packet.readInt(), packet.readShort(), packet.readShort(), packet.readShort()
                if roundCode == self.client.room.lastRoundCode and (self.client.room.currentMap == -1 or monde == self.client.room.currentMap or self.client.room.EMapCode != 0):
                    self.client.playerWin(holeType, distance)
                return

            elif CC == Identifiers.recv.Room.Get_Cheese:
                roundCode, cheeseX, cheeseY, distance = packet.readInt(), packet.readShort(), packet.readShort(), packet.readShort()
                if roundCode == self.client.room.lastRoundCode:
                    self.client.sendGiveCheese(distance)
                return

            elif CC == Identifiers.recv.Room.Place_Object:
                if not self.client.isShaman:
                    return
                if self.client.isShaman:
                    roundCode, objectID, code, px, py, angle, vx, vy, dur, origin = packet.readByte(), packet.readInt(), packet.readShort(), packet.readShort(), packet.readShort(), packet.readShort(), packet.readByte(), packet.readByte(), packet.readBoolean(), packet.readBoolean()
                    if self.client.room.isTotemEditor:
                        if self.client.tempTotem[0] < 20:
                            self.client.tempTotem[0] = int(self.client.tempTotem[0]) + 1
                            self.client.sendTotemItemCount(self.client.tempTotem[0])
                            self.client.tempTotem[1] += "#2#" + chr(1).join(map(str, [code, px, py, angle, vx, vy, int(dur)]))
                    else:
                        if code == 44:
                            if not self.client.useTotem:
                                self.client.sendTotem(self.client.totem[1], px, py, self.client.playerCode)
                                self.client.useTotem = True

                        self.client.sendPlaceObject(objectID, code, px, py, angle, vx, vy, dur, False)
                        self.client.parseSkill.placeSkill(objectID, code, px, py, angle)
                    if self.client.room.luaRuntime != None:
                        data = self.client.room.luaRuntime.runtime.eval("{}")
                        data["id"] = objectID
                        data["type"] = code
                        data["x"] = px
                        data["y"] = py
                        data["angle"] = angle
                        data["ghost"] = not dur
                        self.client.room.luaRuntime.emit("SummoningEnd", (self.client.playerName, code, px, py, angle, vx, vy, data))
                return

            elif CC == Identifiers.recv.Room.Ice_Cube:
                playerCode, px, py = packet.readInt(), packet.readShort(), packet.readShort()
                if self.client.isShaman and not self.client.isDead and not self.client.room.isSurvivor and self.client.room.numCompleted > 1:
                    if self.client.iceCount != 0 and playerCode != self.client.playerCode:
                        for client in self.client.room.clients.copy().values():
                            if client.playerCode == playerCode and not client.isShaman:
                                client.isDead = True
                                if not self.client.room.noAutoScore: self.client.playerScore += 1
                                client.sendPlayerDied()
                                self.client.sendPlaceObject(self.client.room.objectID + 2, 54, px, py, 0, 0, 0, True, True)
                                self.client.iceCount -= 1
                                self.client.room.checkChangeMap()
                return

            elif CC == Identifiers.recv.Room.Bridge_Break:
                if self.client.room.currentMap in [6, 10, 110, 116]:
                    bridgeCode = packet.readShort()
                    self.client.room.sendAllOthers(self.client, Identifiers.send.Bridge_Break, ByteArray().writeShort(bridgeCode).toByteArray())
                return

            elif CC == Identifiers.recv.Room.Defilante_Points:
                self.client.defilantePoints += 1
                return

            elif CC == Identifiers.recv.Room.Restorative_Skill:
                objectID, id = packet.readInt(), packet.readInt()
                self.client.parseSkill.sendRestorativeSkill(objectID, id)
                return

            elif CC == Identifiers.recv.Room.Recycling_Skill:
                id = packet.readShort()
                self.client.parseSkill.sendRecyclingSkill(id)
                return

            elif CC == Identifiers.recv.Room.Gravitational_Skill:
                velX, velY = packet.readShort(), packet.readShort()
                self.client.parseSkill.sendGravitationalSkill(0, velX, velY)
                return

            elif CC == Identifiers.recv.Room.Antigravity_Skill:
                objectID = packet.readInt()
                self.client.parseSkill.sendAntigravitySkill(objectID)
                return

            elif CC == Identifiers.recv.Room.Handymouse_Skill:
                handyMouseByte, objectID = packet.readByte(), packet.readInt()
                if self.client.room.lastHandymouse[0] == -1:
                    self.client.room.lastHandymouse = [objectID, handyMouseByte]
                else:
                    self.client.parseSkill.sendHandymouseSkill(handyMouseByte, objectID)
                    self.client.room.sendAll(Identifiers.send.Skill, chr(77) + chr(1))
                    self.client.room.lastHandymouse = [-1, -1]
                return

            elif CC == Identifiers.recv.Room.Enter_Room:
                community, roomName = packet.readUTF(), packet.readUTF()
                if self.client.playerName in ["", " "]:
                    self.client.transport.close()
                else:
                    if roomName == "":
                        self.client.startBulle(self.server.recommendRoom(self.client.langue))
                    elif not roomName == self.client.roomName or not self.client.room.isEditor or not len(roomName) > 64 or not self.client.roomName == "%s-%s" %(self.client.langue, roomName):
                        if self.client.privLevel.lower(7): roomName = self.server.checkRoom(roomName, self.client.langue)
                        roomEnter = self.server.rooms.get(roomName if roomName.startswith("*") else ("%s-%s" %(self.client.langue, roomName)))
                        if roomEnter == None or self.client.privLevel.upper(7):
                            self.client.startBulle(roomName)
                        else:
                            if not roomEnter.roomPassword == "":
                                await self.client.sendData(Identifiers.send.Room_Password, ByteArray().writeUTF(roomName).toByteArray())
                            else:
                                self.client.startBulle(roomName)
                    return

            elif CC == Identifiers.recv.Room.Room_Password:
                roomPass, roomName = packet.readUTF(), packet.readUTF()
                roomEnter = self.server.rooms.get(roomName if roomName.startswith("*") else ("%s-%s" %(self.client.langue, roomName)))
                if roomEnter == None or self.client.privLevel.upper(7):
                    self.client.startBulle(roomName)
                else:
                    if not roomEnter.roomPassword == roomPass:
                        await self.client.sendData(Identifiers.send.Room_Password, ByteArray().writeUTF(roomName).toByteArray())
                    else:
                        self.client.startBulle(roomName)
                return

            elif CC == Identifiers.recv.Room.Send_Music:
                if not self.client.isGuest:
                    id = Utils.getYoutubeID(packet.readUTF())
                    if not id == None:
                        data = json.loads(urllib.urlopen("https://www.googleapis.com/youtube/v3/videos?id=%s&key=AIzaSyDQ7jD1wcD5A_GeV4NfZqWJswtLplPDr74&part=snippet,contentDetails" %(id)).read())
                        if not data["pageInfo"]["totalResults"] == 0:
                            duration = Utils.Duration(data["items"][0]["contentDetails"]["duration"])
                            duration = 300 if duration > 300 else duration
                            title = data["items"][0]["snippet"]["title"]
                            if filter(lambda music: music["By"] == self.client.playerName, self.client.room.musicVideos):
                                self.client.sendLangueMessage("", "$ModeMusic_VideoEnAttente")
                            elif filter(lambda music: music["Title"] == title, self.client.room.musicVideos):
                                self.client.sendLangueMessage("", "$DejaPlaylist")
                            else:
                                self.client.sendLangueMessage("", "$ModeMusic_AjoutVideo", "<V>" + str(len(self.client.room.musicVideos) + 1))
                                self.client.room.musicVideos.append({"By": self.client.playerName, "Title": title, "Duration": str(duration), "VideoID": id})
                                if len(self.client.room.musicVideos) == 1:
                                    self.client.sendMusicVideo(True)
                                    self.client.room.isPlayingMusic = True
                                    self.client.room.musicSkipVotes = 0
                        else:
                            self.client.sendLangueMessage("", "$ModeMusic_ErreurVideo")
                    else:
                        self.client.sendLangueMessage("", "$ModeMusic_ErreurVideo")
                return

            elif CC == Identifiers.recv.Room.Music_Time:
                time = packet.readInt()
                if len(self.client.room.musicVideos) > 0:
                    self.client.room.musicTime = time
                    duration = self.client.room.musicVideos[0]["Duration"]
                    if time >= int(duration) - 5 and self.client.room.canChangeMusic:
                        self.client.room.canChangeMusic = False
                        del self.client.room.musicVideos[0]
                        self.client.room.musicTime = 0
                        if len(self.client.room.musicVideos) >= 1:
                            self.client.sendMusicVideo(True)
                        else:
                            self.client.room.isPlayingMusic = False
                return

            elif CC == Identifiers.recv.Room.Send_PlayList:
                packet = ByteArray().writeShort(len(self.client.room.musicVideos))
                for music in self.client.room.musicVideos:
                    packet.writeUTF(str(music["Title"].encode("UTF-8"))).writeUTF(str(music["By"].encode("UTF-8")))
                await self.client.sendData(Identifiers.send.Music_PlayList, packet.toByteArray())
                return

        elif C == Identifiers.recv.Chat.C:
            if CC == Identifiers.recv.Chat.Chat_Message:
                message = packet.readUTF()
                if message in ["\n", "\r", chr(2), "<BR>", "<br>"]:
                    self.server.sendStaffMessage(7, "<font color='#00C0FF'>[ANTI-BOT] - Suspect BOT - IP: [</font><J>"+str(self.client.ipAddress)+"<font color='#00C0FF'>]</font>")
                    self.client.transport.close()
                    return

                if message.startswith("!") and self.client.room.luaRuntime != None:
                    self.client.room.luaRuntime.emit("ChatCommand", (self.client.playerName, message[1:]))
                    if message[1:] in self.client.room.luaRuntime.HiddenCommands:
                        return

                if self.client.privLevel.upper(5) or self.client.vipTime > 0:
                    pass
                elif message == self.client.lastMessage:
                    self.client.sendLangueMessage("", "$Message_Identique")
                    return

                elif _time.time() - self.client.CHTTime < 1.2:
                    self.client.sendLangueMessage("", "$Doucement")
                    self.client.CHTTime = _time.time()
                    return

                if self.client.isGuest:
                    self.client.sendLangueMessage("", "$Créer_Compte_Parler")
                    return

                elif message != "" and len(message) < 256:
                    sucess = False
                    isSuspect = self.client.privLevel.lower(5) and self.server.checkMessage(self.client, message)
                    self.client.lastMessage = message
                    if self.client.privLevel.upper(1):
                        self.client.CHTTime = _time.time()
                        if not self.client.isMute:
                            self.client.room.sendAllChat(self.client.playerName, message, self.server.checkMessage(self.client, message))
                        else:
                            muteInfo = self.server.getModMuteInfo(self.client.playerName)
                            timeCalc = Utils.getHoursDiff(muteInfo[1])
                            if timeCalc > 0:
                                self.client.sendModMute(self.client.playerName, timeCalc, muteInfo[0], True)
                                return
                            else:
                                self.client.isMute = False
                                self.server.removeModMute(self.client.playerName)
                                self.client.room.sendAllChat(self.client.playerName, message, isSuspect)

                    if not self.client.playerName in self.server.chatMessages:
                         messages = deque([], 60)
                         messages.append([_time.strftime("%Y/%m/%d %H:%M:%S"), message])
                         self.server.chatMessages[self.client.playerName] = messages
                    else:
                        self.server.chatMessages[self.client.playerName].append([_time.strftime("%Y/%m/%d %H:%M:%S"), message])
                return

            elif CC == Identifiers.recv.Chat.Staff_Chat:
                type, message = packet.readByte(), packet.readUTF()
                if ((type == 0 and self.client.privLevel.upper(3)) or (type == 1 and self.client.privLevel.upper(9)) or ((type == 2 or type == 5) and self.client.privLevel.upper(3)) or ((type == 3 or type == 4) and self.client.privLevel.upper(3)) or ((type == 6 or type == 7) and self.client.privLevel.upper(3)) or (type == 8 and self.client.privLevel.upper(3)) or (type == 9 and self.client.privLevel.upper(3))):
                    self.server.sendStaffChat(type, self.client.langue, self.client.playerName, message, self.client)
                return

            elif CC == Identifiers.recv.Chat.Commands:
                command = packet.readUTF()
                try:
                    if _time.time() - self.client.CMDTime > 0.7:
                        self.client.parseCommands.parseCommand(command)
                        self.client.CMDTime = _time.time()
                except UserWarning:
                    pass
                except:
                    with open("./include/MErros.log", "a") as f:
                        f.write("\n" + "=" * 60 + "\n- Time: %s\n- Player: %s\n- Command: \n" %(_time.strftime("%d/%m/%Y - %H:%M:%S"), self.client.playerName))
                        traceback.print_exc(file = f)
                        self.server.sendStaffMessage(7, "<BL>[<R>ERROR<BL>] The player <R>%s made an error in commands." %(self.client.playerName))
                return

        elif C == Identifiers.recv.Player.C:
            if CC == Identifiers.recv.Player.Emote:
                emoteID, playerCode = packet.readByte(), packet.readInt()
                flag = packet.readUTF() if emoteID == 10 else ""
                self.client.sendPlayerEmote(emoteID, flag, True, False)
                if playerCode != -1:
                    if emoteID == 14:
                        self.client.sendPlayerEmote(14, flag, False, False)
                        self.client.sendPlayerEmote(15, flag, False, False)
                        client = list(filter(lambda p: p.playerCode == playerCode, self.server.players.values()))[0]
                        if client != None:
                            client.sendPlayerEmote(14, flag, False, False)
                            client.sendPlayerEmote(15, flag, False, False)

                    elif emoteID == 18:
                        self.client.sendPlayerEmote(18, flag, False, False)
                        self.client.sendPlayerEmote(19, flag, False, False)
                        client = list(filter(lambda p: p.playerCode == playerCode, self.server.players.values()))[0]
                        if client != None:
                            client.sendPlayerEmote(17, flag, False, False)
                            client.sendPlayerEmote(19, flag, False, False)

                    elif emoteID == 22:
                        self.client.sendPlayerEmote(22, flag, False, False)
                        self.client.sendPlayerEmote(23, flag, False, False)
                        client = list(filter(lambda p: p.playerCode == playerCode, self.server.players.values()))[0]
                        if client != None:
                            client.sendPlayerEmote(22, flag, False, False)
                            client.sendPlayerEmote(23, flag, False, False)

                    elif emoteID == 26:
                        self.client.sendPlayerEmote(26, flag, False, False)
                        self.client.sendPlayerEmote(27, flag, False, False)
                        client = list(filter(lambda p: p.playerCode == playerCode, self.server.players.values()))[0]
                        if client != None:
                            client.sendPlayerEmote(26, flag, False, False)
                            client.sendPlayerEmote(27, flag, False, False)
                            self.client.room.sendAll(Identifiers.send.Joquempo, ByteArray().writeInt(self.client.playerCode).writeByte(random.randint(0, 2)).writeInt(client.playerCode).writeByte(random.randint(0, 2)).toByteArray())

                if self.client.isShaman:
                    self.client.parseSkill.parseEmoteSkill(emoteID)

                if self.client.room.luaRuntime != None:
                    self.client.room.luaRuntime.emit("EmotePlayed", (self.client.playerName, emoteID))
                return

            elif CC == Identifiers.recv.Player.Langue:
                self.client.langueID = packet.readByte()
                if self.client.langueID:
                    self.client.langue = Utils.getLangues(self.client.langueID)
                else:
                    self.client.langue = "EN"
                return

            elif CC == Identifiers.recv.Player.Emotions:
                self.client.room.sendAllOthers(self, Identifiers.send.Emotion, ByteArray().writeInt(self.client.playerCode).writeByte(packet.readByte()).toByteArray())
                return

            elif CC == Identifiers.recv.Player.Shaman_Fly:
                fly = packet.readBoolean()
                self.client.parseSkill.sendShamanFly(fly)
                return

            elif CC == Identifiers.recv.Player.Shop_List:
                self.client.parseShop.sendShopList()
                return

            elif CC == Identifiers.recv.Player.Buy_Skill:
                skill = packet.readByte()
                self.client.parseSkill.buySkill(skill)
                return

            elif CC == Identifiers.recv.Player.Redistribute:
                self.client.parseSkill.redistributeSkills()
                return
                
            elif CC == Identifiers.recv.Player.Report:
                username, type, comments = packet.readUTF().split("#")[0], packet.readByte(), packet.readUTF()
                self.client.modoPwet.makeReport(username, type, comments)
                return

            elif CC == Identifiers.recv.Player.Ping:
                if (_time.time() - self.client.PInfo[1]) >= 5:
                    self.client.PInfo[1] = _time.time()
                    self.client.lastping = not self.client.lastping
                    await self.client.sendData(Identifiers.send.Ping, ByteArray().writeByte(self.client.PInfo[0]).writeBoolean(self.client.lastping).toByteArray())
                    self.client.PInfo[0] += 1
                    if self.client.PInfo[0] == 31:
                        self.client.PInfo[0] = 0
                return

            elif CC == Identifiers.recv.Player.Meep:
                posX, posY = packet.readShort(), packet.readShort()
                self.client.room.sendAll(Identifiers.send.Meep_IMG, ByteArray().writeInt(self.client.playerCode).toByteArray())
                self.client.room.sendAll(Identifiers.send.Meep, ByteArray().writeInt(self.client.playerCode).writeShort(posX).writeShort(posY).writeInt(10 if self.client.isShaman else 5).toByteArray())
                return

            elif CC == Identifiers.recv.Player.Bolos:
                sla, sla2, id, type = packet.readByte(), packet.readByte(), packet.readByte(), packet.readByte()
                return

            elif CC == Identifiers.recv.Player.Calendario:
                playerName = packet.readUTF()
                playerName = playerName.split("#")[0]
                player = self.server.players.get(playerName)
                if player:
                    await self.client.sendData([8, 70], ByteArray().writeUTF(player.playerName).writeUTF(player.playerLook).writeInt(0).writeShort(len(player.titleList)).writeShort(len(player.shopBadges)).writeShort(0).toByteArray())
                return

            elif CC == Identifiers.recv.Player.Vampire:
                self.client.sendVampireMode(True)
                return

        elif C == Identifiers.recv.Buy_Fraises.C:
            return

        elif C == Identifiers.recv.Tribe.C:
            if CC == Identifiers.recv.Tribe.Tribe_House:
                if not self.client.tribeName == "":
                    self.client.startBulle("*\x03%s" %(self.client.tribeName))
                return

            elif CC == Identifiers.recv.Tribe.Bot_Bolo:
                return

        elif C == Identifiers.recv.Shop.C:
            if CC == Identifiers.recv.Shop.Equip_Clothe:
                self.client.parseShop.equipClothe(packet)
                return

            elif CC == Identifiers.recv.Shop.Save_Clothe:
                self.client.parseShop.saveClothe(packet)
                return

            elif CC == Identifiers.recv.Shop.Info:
                self.client.parseShop.sendShopInfo()
                return

            elif CC == Identifiers.recv.Shop.Equip_Item:
                self.client.parseShop.equipItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Item:
                self.client.parseShop.buyItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Custom:
                self.client.parseShop.customItemBuy(packet)
                return

            elif CC == Identifiers.recv.Shop.Custom_Item:
                self.client.parseShop.customItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Clothe:
                self.client.parseShop.buyClothe(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Shaman_Item:
                self.client.parseShop.buyShamanItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Equip_Shaman_Item:
                self.client.parseShop.equipShamanItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Shaman_Custom:
                self.client.parseShop.customShamanItemBuy(packet)
                return

            elif CC == Identifiers.recv.Shop.Custom_Shaman_Item:
                self.client.parseShop.customShamanItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Send_Gift:
                self.client.parseShop.sendGift(packet)
                return

            elif CC == Identifiers.recv.Shop.Gift_Result:
                self.client.parseShop.giftResult(packet)
                return
            
            elif CC == Identifiers.recv.Shop.Buy_Visu_Done:
                p = ByteArray(packet.toByteArray())
                self = self
                self.server = self.server
                self.client = self.client
                self.client.shop = self.client.parseShop
                visuID = p.readShort()
                lookBuy = p.readUTF()
                look = self.server.shopOutfitsCheck[str(visuID)][0].split(";")
                look[0] = int(look[0])
                count = 0
                if self.client.shopFraises >= self.client.fullLookPrice:
                      for visual in look[1].split(","):
                            if not visual == "0":
                                item, customID = visual.split("_", 1) if "_" in visual else [visual, ""] 
                                item = int(item) 
                                itemID = self.client.getFullItemID(count, item) 
                                itemInfo = self.client.getItemInfo(count, item) 
                            if len(self.client.shopItems) == 1: 
                                if not self.client.shop.checkInShop(itemID):
                                	self.client.shopItems += str(itemID)+"_" if self.client.shopItems == "" else "," + str(itemID)+"_"
                                	if not itemID in self.client.custom:
                                     		self.client.custom.append(itemID)
                                	else:
                                    		if not str(itemID) in self.client.custom:
                                          		self.client.custom.append(str(itemID))
                            else:
                            	if not self.client.shop.checkInShop(str(itemID)):
                                 	self.client.shopItems += str(itemID)+"_" if self.client.shopItems == "" else "," + str(itemID)+"_"
                                 	if not itemID in self.client.custom:
                                      		self.client.custom.append(itemID)
                                 	else:
                                      		if not str(itemID) in self.client.custom:
                                           		self.client.custom.append(str(itemID))
                      count += 1

                      self.client.clothes.append("%02d/%s/%s/%s" %(len(self.client.clothes), lookBuy, "78583a", "fade55" if self.client.shamanSaves >= 1000 else "95d9d6"))
                      furID = self.client.getFullItemID(22, look[0])
                      self.client.shopItems += str(furID) if self.client.shopItems == "" else "," + str(furID)
                      self.client.shopFraises -= self.client.fullLookPrice

                self.client.shop.sendShopList(False)

        elif C == Identifiers.recv.Modopwet.C:
            if CC == Identifiers.recv.Modopwet.Modopwet:
                if self.client.privLevel.uppermost() >= 7:
                    isOpen = packet.readBoolean()
                    self.client.isModoPwet = isOpen
                return

            elif CC == Identifiers.recv.Modopwet.Delete_Report:
                if self.client.privLevel.uppermost() >= 7:
                    playerName, closeType = packet.readUTF().split("#")[0], packet.readByte()
                    self.client.modoPwet.deleteReport(playerName, int(closeType))
                return

            elif CC == Identifiers.recv.Modopwet.Watch:
                if self.client.privLevel.uppermost() >= 7:
                    playerName = packet.readUTF().split("#")[0]
                    if not self.client.playerName == playerName:
                        roomName = self.server.players[playerName].roomName if playerName in self.server.players else ""
                        if not roomName == "" and not roomName == self.client.roomName and not "[Editeur]" in roomName and not "[Totem]" in roomName:
                            self.client.startBulle(roomName)
                return

            elif CC == Identifiers.recv.Modopwet.Ban_Hack:
                if self.client.privLevel.uppermost() >= 7:
                    playerName, iban = packet.readUTF().split("#")[0], packet.readBoolean()
                    self.client.modoPwet.banHack(playerName,iban)
                return

            elif CC == Identifiers.recv.Modopwet.Change_Language:
                if self.client.privLevel.uppermost() >= 7:
                    language, modopwetOnlyPlayerReports, sortBy = packet.readUTF(), packet.readBoolean(), packet.readBoolean()
                    self.client.modoPwetLanguage = language.upper()
                    self.client.modoPwet.openModoPwet(self.client.isModoPwet, modopwetOnlyPlayerReports, sortBy)
                return

            elif CC == Identifiers.recv.Modopwet.Modopwet_Notifications:
                if self.client.privLevel.uppermost() >= 7:
                    isTrue = packet.readBoolean()
                    self.client.isModoPwetNotifications = isTrue
                return

            elif CC == Identifiers.recv.Modopwet.Chat_Log:
                if self.client.privLevel.uppermost() >= 7:
                    playerName = packet.readUTF().split("#")[0]
                    self.client.modoPwet.openChatLog(playerName)
                return
                
        elif C == Identifiers.recv.Login.C:
            if CC == Identifiers.recv.Login.Create_Account:
                playerName, password, email, captcha, url = Utils.parsePlayerName(packet.readUTF()), packet.readUTF(), packet.readUTF().lower(), packet.readUTF(), packet.readUTF()
                if self.client.checkTimeAccount():
                    createTime = _time.time() - self.client.CRTTime
                    if createTime < 5.2:
                        self.server.sendStaffMessage(7, "[<V>ANTI-BOT</V>][<J>"+self.client.ipAddress+"</J>] Player is creating account so fast.")
                        self.client.transport.close()
                        return

                    canLogin = False
                    for urlCheck in self.server.serverURL:
                        if url.startswith(urlCheck):
                            canLogin = True
                            break

                    if not canLogin:
                        self.server.sendStaffMessage(7, "[<V>URL</V>][<J>%s</J>][<V>%s</V>][<R>%s</R>] Invalid login url." %(self.client.ipAddress, playerName, url))
                        await self.client.sendData(Identifiers.old.send.Player_Ban_Login, [0, "Access from website: %s" %(self.server.serverURL[0])])
                        self.client.transport.close()
                        return

                    if self.server.checkExistingUser(playerName):
                        await self.client.sendData(Identifiers.send.Login_Result, ByteArray().writeByte(3).writeUTF(playerName + str(random.randint(0, 50))).writeUTF("").toByteArray())
                        self.client.wrongLoginAttempts += 1
                    

                    elif not re.match("^(?=^(?:(?!.*_$).)*$)(?=^(?:(?!_{2,}).)*$)[A-Za-z][A-Za-z0-9_]{2,11}$", playerName) or playerName in ["", " "] or password in ["", " "]:
                        await self.client.sendData(Identifiers.send.Login_Result, ByteArray().writeByte(4).writeUTF(playerName).writeUTF("").toByteArray())

                    elif not self.client.currentCaptcha == captcha or captcha in ["", " "]:
                        await self.client.sendData(Identifiers.send.Login_Result, ByteArray().writeByte(7).writeUTF("").writeUTF("").toByteArray())
                        self.client.wrongLoginAttempts += 1

                    elif self.client.wrongLoginAttempts >= 15:
                        self.server.sendStaffMessage(7, "[<V>ANTI-BOT</V>][<J>%s</J>][<V>%s</V>] Kick - Trying to brute force." %(self.client.ipAddress, playerName))
                        self.client.sendPlayerBan(0, "Trying to brute force", True)
                        await self.client.sendData([26, 3], [""])
                    else:
                        self.Cursor.execute("insert into Users(Username, Password, Email, ShopCheeses, ShopFraises, RegDate, Tag, Langue) values (%s, %s, %s, %s, %s, %s, %s, %s)", [playerName, password, email, self.server.initialCheeses, self.server.initialFraises, Utils.getTime(), '#0000', self.client.langue.lower()])
                        if not email in self.server.usersByEmail:
                            self.server.usersByEmail[email] = []
                        self.server.usersByEmail[email].append(playerName)
                        self.client.sendAccountTime()
                        self.client.loginPlayer(playerName, password, "1")
                        self.client.sendNewConsumable(0, 10)
                        self.server.sendStaffMessage(7, "[<J>%s</J>] <ROSE>The player <J>%s</J> <ROSE>created an account on server." %(self.client.ipAddress, playerName))
                    return
                else:
                    await self.client.sendData(Identifiers.send.Login_Result, ByteArray().writeByte(5).writeUTF(playerName).writeUTF("").toByteArray())

            elif CC == Identifiers.recv.Login.Login:
                playerName, password, url, startRoom, resultKey = Utils.parsePlayerName(packet.readUTF()), packet.readUTF(), packet.readUTF(), packet.readUTF(), packet.readInt()
                loginTime = _time.time() - self.client.LOGTime
                authKey = self.client.authKey
                for value in self.server.loginKeys:
                    authKey ^= value

                # if authKey != resultKey:
                    # self.server.appendBadIP(self.client.ipAddress)
                    # self.client.sendPlayerBan(0, "You'll not be able to play self game ever.", True)

                if loginTime < 2 and loginTime > 1:
                    self.client.sendPlayerBan(0, "You're logging in so fast! Try to log in again but slower.", True)
                    self.server.sendStaffMessage(7, "[<V>ANTI-BOT</V>][<J>%s</J>][<V>%s</V>] Player logged in so fast and kicked." %(self.client.ipAddress, self.client.playerName))
                    self.client.transport.close()
                    return

                elif self.client.wrongLoginAttempts >= 10:
                    self.server.sendStaffMessage(7, "[<V>ANTI-BOT</V>][<J>%s</J>][<V>%s</V>] Kick - Trying to brute force." %(self.client.ipAddress, playerName))
                    self.client.sendPlayerBan(0, "Trying to brute force", True)
                    await self.client.sendData([26, 3], [""])
                elif playerName == "" or password == "" or playerName == " ":
                    await self.client.sendData(Identifiers.send.Login_Result, ByteArray().writeByte(2).writeUTF(playerName).writeUTF("").toByteArray())
                    self.client.wrongLoginAttempts += 1
                for urlCheck in self.server.serverURL:
                    if url.startswith(urlCheck):
                        canLogin = True
                        break
                if not canLogin:
                    self.server.sendStaffMessage(7, "[<V>URL</V>][<J>%s</J>][<V>%s</V>][<R>%s</R>] Invalid login url." %(self.client.ipAddress, playerName, url))
                    await self.client.sendData(Identifiers.old.send.Player_Ban_Login, [0, "Access from website: %s" %(self.server.serverURL[0])])
                    self.client.transport.close()
                else:
                    self.client.loginPlayer(playerName, password, startRoom)
                return

            elif CC == Identifiers.recv.Login.Captcha:
                captchas = {
                    "IELR": b'\x00\x00\x02$x\x9c\xed\x951H#Q\x10\x86\x17\xddhTP\xc4\x10ml4M\n\xaf\xb10\x07\x82\x10\xad$\xa6\xd5\xc6B\x85\xc3F\x90\xa4\xf0\xe0\n\x13\xbd\xf6b\xb9\x16\xa6P\x11!(\xd8\x19HL\xa1wVZX\xe8\xa9UPA\x04\xe5\n\x89\x1c\x87\xfa\xfc\x9f\x99\x07{\xcbK\\\xa2\xae\x88;\xf0\xb1;\xf3\xdeL\xe6\xcf\xbe\x9dU\x94N\xc5\xa5\xae)\xb6\xd9\xf6\x01\xac\x8a1\xf6\xd6=Xe\\\xeb\x19hz\xc7\x9a\x1d&{\xaf\x05|\xe3E<\x1e\x8f!G\xf8\x85\xd0\xe7\x9cJ\xea}\x96\xe4\xdc\x82\x1b\xb0\x01\x9aK\xd4\xa3\xb7r\xf4\xd9\x06F\xc0,\xd8\x05\x7f\x80\x19\xcd\x01\xea)\xe1\xf1x\xae\xb0\x7f\xd0\xef\xf7?\xa5W\xe4,I\xea\r\x15\xc9\xe5\xfc*A_+\xfa\x1a\x00?\xc0\x16\xb8\x06\xbf\xc1\x02\x18\x03\x1d\xa0\xd2\xe4\xf3\xfdF}\x8c\x80\x19\xe4l\xa7R)\xee\x0f\x9a\xc8\x19\x95\xac\xcd\xd3\x9a1\xdfC\xf1\xbfO\xf4\xc3\xdf\xa9>0\r\x92\xe0\x12\x9c\x80U0\x01\xfc\xfc\x0c>\xe3\xbd[\xa1>\xba@3\xea\xdc\xc3X&\x93\x99K\xa7\xd3\xde\x02uEN\xbbdm\x87\xd6zu\xb1z\x10\xa5\xf8\xb1.^\x87\xfa\xdd\xe0+\xe99%}\xeb`\x8at7\xbe\xf0L9W\xf2\xef\x97J\xfe\x85\xdb\xedf\xc1`\x90i\x9a\xc6\xb2\xd9\xec#\xfc\x1e\xb1\x1a\xfam\x9es#\xa9UF\xb5\xa4g\xd9\xe9t\xde\xf9|>-\x99L.\xa2\xce!\x9d\xcbM:\xa7\xfd\xa0\xe5\x95\xe7\xa5\x98;\xc7\x06\xff?\xbc^/\x0b\x85B\x8c\x9f\xf3g\xda~.\x97\xd3p\x1d\xa6ySn\xf1\xf7@\xcc\x9d\xe5\x02\xbe\xd1*\xd0\x9f\xd83)Y\x17\xb3*A>\xff\xff6(\xd6\xe5r\xb9^\xa8\xed\x92M\xcc\x9d\t\x83\xff\xc5DN@\xb2&f\xd5\xb8.\xd6\xa2\xe4\xcf\xf8\x9e\xaa\xaa\x92\x14KM\xcc\x9d\xc7g\x16\x89D^\x9b\xa3p8\xfc\x1d\xd7\x1eP\r\xac\xd6{Nz\x1b\x0c~\xb1oo\xb1=\xfc9\xfeS\xf2sKo\x9f\xf8\xba\xc3\xe18\xc0,\x98\x86\xce-p\r~\x82\xb7\xd4o\xa5U\xc5b\xb1\xeeh4j\xeb\xb7\xf5\xdb\xfam\xfdW\xa0B\xa2\xf9\x01\x99eX\xd9',
                    "TCQC": b'\x00\x00\x03ux\x9c\xed\x96\x7fHSQ\x14\xc7/2\xb5$\x16\x99\x93\x122\x02\x83\xd5\x04\xdb\x04\x15T\x86D\x12#h\xd4\x1f1\xe6\x1f\x8ac\x7fH\xea\x1f\x13\xa2\x10t\xfe*J"\xa9\x7f4K\xa2\x02\x19aj\x85\x89F\x90\xa6E\x7f,\n\xcc\xa4Y\x16Y&\xc6\x9an\xc5\xe6v\xfb^\xde\x1d=\xc66\xcb\x1f[R\x07>\xbc\xb7\xfb\xce=;\xdf{\xde=\xf7\x11\x92G\x92$\xddd\x9d\x9b\xac\xa9\xa9)\xaf\xb6\xb6\xd6\x00\xce\x81;`\x02\xcc\x03\t\x88v~\xcb\xb1\xd8\xd6\xd6\xd6=\xf5\xf5\xf5Z\xe4\x7f\xc2l6w\xe0:\x02\xbe\x829~\x7f\x95?;\x0c\xe4\xb8gs\xa2\x9d\xf7R\x16\xaaV\xdf\xc1k\xd0\xcb\xc7K\xa1\x89\xf9%\xad\x83\xfa\xfd\xafU\xf4kE\xc5\xc4\xc6\xc6\xd2\x801f\xfb@\x97D"YHNN^\x94\xcb\xe5\xdf\xd4j\xf5\xcb\x92\x92\x92\xd1\x9a\x9a\x1a\x7f\xad\x9eUWW\xbf(..\x9e+((`>\x0b2\x99\xac\x1bs\xd2E\xff\xc5\xe2\xdc\x02\x0e\xe0\x06\x1f\xc1Y \x89\x90V"\xd6\x96\x98\x98H\x91wX\xca\xcb\xcb\xa9N\xa7\xa3\x85\x85\x85T\xa5R\xdd\xc8\xc8\xc8`\xb5\xca\xc4\xfc\x19\x12\xb0v\x1c\x17`\xcf\x8f\x81\xc5\x10>g"\xa8\x97Y\x0cr~e2\x99h~~~Ovv\xb6\x86RZ\t\xae\xcd\xcc\xccx\xfb\xfb\xfb\xe9\xe4\xe4$\xf5z\xbd\xa3n\xb7\xbb\x0e\xd7:\xd4\xd2\x1d\x1f\x1fo\xc3\xdc\x04"\xd4\x89\xe5\xfd\x00\xec\xe51w\x82\xfb||\x04\xfc\x10i\xdb\xc2\xfe\x13\xe8\x88Pg[D\xd5\x12R\x89}\xf5\xa9\xa2\xa2\x82\xfa|\xbeY\xbb\xdd\xde\x07\xad\x17\xc1\xa3\x96\x96\x16\xaa\xd1h\xba\xb3\xb2\xb26\xe3\xf7\x01p\x1a<\x01\x0e0\x08\xfa,\x16\x0b\xcd\xc9\xc9\x19\xc1^\x08\x8c+#\x82F\x0f\xbf^\x8f\xb0\xae`\x96\x80\xda\xbe\x03\xe3z\xbd\x9e\x0e\x0f\x0f\xe7\x8a\x9e\xbd%B\x9e\x99A\xe6I\xa1\xf5\x10\x98noo\xa7V\xabu\xc1\xe3\xf1\xdc\xc3o\x13P\x81\x18\x06\x9f\xef\x0b\x13\'\x1a\xb6\xa9\xac\xac\xcc\xdb\xd8\xd8\xe8mhh\x88\x11\x8d\xfb\xf7[8\xf3\xbf\xa7I\xd3\xd3\xd3G\xa0\xf1\x12\x18\x03s\xe0\xf1\xd4\xd4\x14\xdb\xf3>\x85B\xb1T\x9cH\x1a[wV\xdb1\xadV+\x1e\xf7k\x91\x05\xf8g\x13\xa1\xc7Z\x82\xf8\xb0\xfdi\x06\xbb\xb0\xef\xdf\x1b\x0c\x06\xda\xd6\xd6\xe6\xb3\xd9l\x14\xbd\xe0\xb6\xd3\xe94b\x1dv\x83\xc08\x91\xb4\xd2\x94\x94\x14:??\xdf!\x95J\xc5\xe3\xac\xff\xb0\xc4\xee\x82\xedD\xe81\x07\xc9\xaf\xfetA\xe4\xc3z\xd3\x0e`$\xc2{1\xcb\xc7\x1f\xfa}RSS\x9fWUUY\x1c\x0e\xc7\x07\xe8\x9du\xb9\\\xce\xce\xceN\x8a3\xec\x8aR\xa9\x8c\x88Pn\x83EEEthhH\x170\x9eK\x82\x9f\x1f\x8c\t\xb0\x95\x08g\xaa+\x84\xcf\x18\x90\x86\x8a\x93\x96\x96F\x8dF\xa3\xa3\xa7\xa7\xe7\x0bz\xfe\x1b\xac\xc1e\xa0\x03\xdbx\xfd\xd7\xca>\xb3>\x8c\xef\xbe\xf4 \xcfX\xae\xac>\xec\xbdeu\x1b\x07\xcdD8S\xfc\xc6\xe6\xf5r\x1fV\xd7\x93`\x80\x08\xba\x9a\x7f3\x8e\x02\x1a\x8f\x83.\xbe\xf7\xc7x/8\n\xb6\xae\xb2\xfea\xc4\xdb\xbf\xca17\x80\x9b@\xbf\x8c\xb9\xac\xb7+y\xafg=\xdf\x0e\xac\xe0<?\x13\xa4+\xc85\x8e\xaf\xe7\xc65~\x87Vb\x12\xe4\x96\x03N\x81\x01~\xf6?\xe5\xdf\x02\xec\x9b \xe1\x0fs\x8f\xfb\x8b\xb5\x063\x96\xaf\x1a\xd4\xb2o"^\xaf\xf5\xa6a%\xf6/i\rg?\x01\xdd\x8b\xa0\x91',
                    "EYSH": b'\x00\x00\x036x\x9c\xed\x95_HSa\x18\xc6\xcf\xdc\xc2\x90%\x14\x1b\x81\x82\x18\x88\x19B\x82\xa1\x10\x8e\xc0.Db\xe0\xd8\x85%.\x89\x16A\x0b\x9b\xa0lA\xea\x94\xd9.\xb6\x0b\xa3\rBhV\x90\xa4\x15\xae\xdaM7N\x82\x16h\xe1\xc5\x88\xc0lhH\xb9\xf0O\x92C\xd7\xd8\xfaz>\xfdN[\x87\xcdMB#\xdb\x03?\xf6\x9d\xf7|\xe7\xbc\xe7\xd9\xfb\x9e\xf7p\x9c\x82\x93I\x9ep\x19e\x94QF\xff\xa8r\x01\xd9\x04\xaa\x17l\xad\x14\\{\x9a\xc5\xef\xc5\xdd\xcb\x01\x96A\x18\xcc\x02\x93 \xcf\xac\xe0\x1e\x07Y\xfc\xd3\x1f\xfa\x90tuu\xa5\xb3O\xc9\xf2\x11\x89D\x92\xcco-[\xbf\x03Y,\x96\x0f\x96\xc04\x90\xb2\xd8\xe3\x04\xd7S\xae\xc7\xe5\x19\x10\xe4W\xb3\xf8\x834}\xc9-\x16\x8b\x02\xde.\x00\x1bp\x83\xf7`\x05\xa4\xe3\xf9\x1a\xf3\xba\xdc\xde\xde~`\x93\xfd>\xf6\\W\xd8\xf1(;>\x1e\xb7\'\xc2b\xc7\xd8q5\xb7Q\xe79>\x0f\xd0\t\xee\xebH\x10\xdf\xd3\xd7\xd7w\xc4l6\xab\xf0<\xc6\xee\xee\xee;\xf8}\x05\x96\xc0"[\xf7\xb3su\xa0\x04kzM*\xafT\xeb5\xc9\xc9\xc9Y\x1b\x1c\x1c\xec\xb1\xdb\xed\xc9\xf6\x9de\xcf\xf5\x05t\xb0\xb5Y\xb0\xc7\xcf\xe2U\xc9\xf2\x80\x8a\xb8\x18\xad\xd5\xdb\xa2\xa2"R^^~\xbf\xb9\xb9\x99\xaf\xd5\x1a\x98\x04\xcfX\r\xb5\xf0Dk*K\xb3g7\xd3\x1c{\x0e\xd2\xda\xdaJ\xacV+\x11\x89D\xf1\xbd\xcc\x8b\xf6\xf1G.\xd6\xa3o\xb8Xo\xf3\xa2\xf5\x9c\xe7b\xfdY\xc2\xc5j\xf5\xb5\xb4\xb4\x94(\x14\n\xa2R\xa9\x88V\xab%F\xa3q\x1d\xac\xa3\x88]\x85\x97\xad\xd6j\xab\xfamVQ\x9f\xd4o[[["\xbfT-,\x1e\x04\xc5\x82s\xfc{u\x19\x1e^666\x865\x1a\rA\xcd\xc2\x9d\x9d\x9dS&\x93\x89444\x90\x9a\x9a\x1aZKRPP@{\x8a\xcf3\xb2\x1d\xe6\x12\x88\x9f!\xfc\xac\xb08\x1c\x0e2<<\xec\'\x84<\x07v\xa0\x07\xa7@18SXXH\xe4r\xf9Heee\xaa\xf7\xea\x9cN\xa7#2\x99l^,\x16\xf3y\x1e\n\xf2\xabX\xdc\xbaC~\xf9\x19r\x91\x1d\xd3yER\xd1\xdb\xdb\xbb\xeat:?\xb8\\\xaeQ\x8f\xc7s{bbB\x1f\x08\x04\x82J\xa5\xf2{YY\xd9\t\xb5Z-\xc2\x7fS\xcd\xc5z\x81\xcf\xd3"\xc8\xcf\xcf\x01\xd5\x0e\xf9M\xf8\xfd\x88\xfb.\t\xe5\x92J\xa5$//O\x8f\x9e\xad\x83\xa7K\xc0\x0c\x9c 0>>N|>\x1fYXX \xa1P\x88\xcc\xcc\xcc\x10\xaf\xd7;9666544D\xdfU\xb3\xdb\xed>\x89\xbd% \x17\xf0\xf9\xf7\xef\x90\xdf_\xb3*\t\xc9\xf6K\x13\x9c\xa3\xcf|\x93\xdb\x98\xdf\x91\xec\xec\xec\x00\xe6\xee\xdd\xa6\xa6\xa6\xfaH$\xf2\xcd`0Dm6\xdb@4\x1a\xf5\xc0\xe7$X\x01?\x82\xc1`\xd8\xef\xf7\x8fb=\x00\xac\xa0\x05\xd4\x83*p\x08\xec\x05\xdb\xe1\xfdoh\x1f\xbc\x1c\x06\xb4\xe6\x1a`\x007\xc0#\xe0\x05\xd3 \x04\x16\x81\x8f\xcd\x94~\xd0\xc3z\x8b\xf6X\x05\xc8\x07\xe2]\xf4\xbf\xc8\xe0\xe5(\xa8\x05\xe7A\x07\xb8\x05\x9e\x82\xd7\xe03X\x05Y\xbb\xc8s*\xfdO^3\x8a\xe9\'biP)',
                    "IPVF": b'\x00\x00\x03\x06x\x9c\xed\x95_H\x93Q\x18\xc6\xbfm\xbaj#\x11\xdc\xf0\xa2u\x11\x8d\xb2\x9b\xba\xd9\xbc\xd1\x0c\xba2\x11\xd6\xc56\x89\xf0b\xb4\x8bM#R\xc41[9p\x8ej\x04e7\xc1\x98\x12D\x1b6dE\xc1\xba\n"CA\x90,\x92\xba\xd1\x04\xb3\x02\xe9\xa2Z+\x9co\xcf\xd1\xf3\xb1\xcf\xb9\xe5\x04\xf7\x87\xe8\x81\x1f\xdb{v\xde\xf7;\xcf\xf9\xdes&\x08\x8d\x82\xa6"&\xfc\xa3R\x10Q\xa9\xd7\xb0\x93\x92\xc1\xcf>\xd0\x08\xda\xc1\x150\x0c\x9e\x81y\xf0\x03l\xc7\xb3\xba\x0c\xf6G\x8b5\x18\x81\x15\xb8\xc0\x1d\xf0\x14\xbc\x03?\xc1G0\x0e\xee\x01\x1f8\x07N\x82\x03\xa0b\x9b^\xe7\xc0\x89\x02{\xaeB\xfdc\xe04\xb8\x08n\x81G\xe05\xf8\x06\x96\xc1\x14x\x00\xae\x03\'h\x06u`\xf7\x0e\xaf\x8dy\xfd\xc2\xf7+\xd7\x1c\x95\xd7\xeb\xfd[\x8d=|m\xa7@\x07\x08\x80(\xf7\xb0\xcc=\xcd\x80\x87\xdc+\xf3l\x02G\xc1\xde"\xf5W\x15`\x0f\x9a\x02\xcc\xebj2\x99\xa4\xe9\xe9i\x8aD"\x14\x08\x04\xc8\xedv\xa7\xba\xbb\xbb\x93.\x97k\x15~\'\x07\x07\x07\x87\x83\xc1\xe0Jgg\'\xf9|\xbe\xfb\xa9T\xea%\xf2\x96x\xcf}H$\x12\x14\x8f\xc7\x17Y~oo/Y\xadV2\x1a\x8d\xa4\xd1h\x88?\xab\x94\x07\xa7\x95?\xff.8\xec\xf1x\x98\'\xea\xe9\xe9\xa1\xae\xae.\xe6u\xcds8\x1c^\xdb\x03\xec\xc5\xa7\xd9\xd9\xd9\x85X,\x96\xf2\xfb\xfd\xd4\xdf\xdf\xff\xe6\x06422r\x1cc\xecN\x19\xe7\xf5\xceK\xbce\xa3T\xba\xc4\x9foW(\x14\xcf\xe1\xf5\x89\xc9dbq\xbbd\xce~>\xe7\xb7R\xa9\x14\xc7\x1e\xb31\xb5Z}\xcdl6\x87\x90\xb7\x00>c\xbf\x08\xf9/\x1a\x1a\x1a\xfcZ\xad6\xb3N9(*\xac{\xb9m\xb3\xd9\x98\xdf\xa8L&cq\x0b\xff\xbd\x02\x9c\xe5sf$ya>\xd6&\x19{U[[\xbbR__\x1fG_\xfc\xea\xeb\xeb#\xa7\xd39\xe6p8\x9aQ\xb7\x06\xfdP\x04;[j\t\xacTVV\xcecM\x07\x07\x06\x06X\x9c\xab\x07\xcfH\xf2\x82|\xcc\xcdc\xf1\\\xdc\x14\xeb\xca\xe5r\xd2\xe9t\xd4\xd4\xd4D\xd8K\xd6\xfbd\xb1XH\xaf\xd7+FGG\x8b`m\x93\xc4\xbb\xea\xbd\xb0~\xf7\x8a\xb1\x94\x04\x98\x146\xf7e\x07\xff=\xc4c\xf6\xee\xbf\x83\x1aI\xdd\r\xa0\xf7\xc9`0\x90\xddn_\xc4\xb3\xae\x82#\xd8\xdfB\xfa\xcb\x94\xf8N\xc2\x19q(gFZm|\xee\x18\xb0\xf0\xef\x97\xf3\xacS\xc7\xfd2\xdf\x13\xc0\x01\xaa\xb7\xf8\xaf\xdb\t\x89w\x95+#\xb6\xe5\x91\xdb"\xa4\xff\xc7\xde\n\xeb\xe7B\xb5\xcd:\xac\xaf\xd9\xd9\x8e\x80\xaf\xfc\x93\xc5\x85\xeaw\xf1\xaej\xcd\x88[rf\xa4uH\xd8\xd8\xaf\x17\xb2\xd4\xcd\xa7\x8e\xa8j\xfe\x9e\'\xf8{/D\xbf\x8bwSMF\xac\xca\x99\x91\x96RH{e\xe7_\x9e\xa5n>u\xb2\xa9T\xfd^j\x15\xbb\xdf\xcbI\xc5\xe8\xf7r\xd5\xff~\xf7z\x97\xc0\xae\xa1\xa1\xa1R\xaf\xa9X\xca\xe5\xf5\x0f3V_\xd0',
                    "IKSJ": b'\x00\x00\x03Qx\x9c\xed\x96_HSQ\x1c\xc7/\xe2\x1aD\xf4\x07\xdd\xd6|)\x82\xc0\xf9\xb2\x81\xf4\xe0\x12\x96\x0fE\x84\xd4\x1e\x1aQ\x04\x0e4\x1f\xf6\x92\x04\xa1$\xe1\xe6T$\x1f6\xa4\x02K\xe6|0A\xa4,\x08#\x88\xad\x87\xf6\xb0\x97\x82Jh\xe1\x1cN\x13\x93\xd5\xa2lb\x9b\xa7\xef\xaf\xfd.\xca\xd8\xc4\xe120\x7f\xf0\xe1\x9e\xdf=\xe7\xdc\xf3\xfb\xfe~\xe7\x9e{%\xa9Z*-\x1e\x93v\xec\xbf4\xa5\x10\xe2_\xc7\xb0UFZ\xe7A\xc9\xcc\xcc\xccn\xbb\xdd\xbe\x1f\xa8\xba\xba\xba\xcap=\x0c\x8e:\x9d\xce\n\\\r\xe0X{{\xbb\x11\xd7\x13\xe0\xa4\xc3\xe18\x83\xab\x19X\xd0\xbe\x84\xab\x15\\A\xdb\x86k\x13\xb8\x8e\xf6\r{\xda:\xc1-\xe0\x06w\xc0=\xe0\x05C`\x04\x8c\x81\xa7\xe09\xf0\x83W \x08\xde\x80\xf7 \x04"`\x16|\x06q\xb0\x08\x96A\n\xe4\xa3Y`|\x12\xb1\xd1\xfc\xaf\xfc<z\xee\x14\xafC\xeb\xbd\xe6\xf5)\x0e\x1f\xc7E\xf1=\xe2x)\xee\x01\xd6Az\\\xac\x8ft\xb6\xb1n\xd2\x7f\x95\xf3Ay\xa9\xe3<Q\xbe\xceq\xfe(\x8f&\xce+\xe5W\x0f*8\xef\x87:::\xca\xb8\x1e\xfb\xba\xbb\xbb\xa9>\x8a\xbe\xbe\xbe\x8d\xea\xdcKZA\xd8f\xb3=F\x8d\x8b\xd0^\x02\x0bk\xc6\\\xe31t\xffT\xc6\xdc\xdb \x0e\x96A\x14\xb4\xe5XG\xc3\xcf\x98\xddh`\x7f\xc9j9\x8e\x07j\xb5\xfa\x1b\xf4V\x99L&\xf2G\xb9\xbf\x9e\xfbI\xcf\xe9\x8c\xb9\xa3\xdc\x97Ig\x96u\xcc\xdc7Rp\x05\xf9Y+\xc7A\xba\xa8\xbew\xfb\xfb\xfb\xc9w\x82\x0b\xd2\xaa\x86\xb3Y\xe6&\xb9\xaf\x92\xfd\x1a)\x9d\x97\xb9,c\x1d<\xb6\xb5\xa0\xd1\xe7or\x8dL\xe02\xf4F\x83\xc1 \xf9\xf7\xa5U\xad\x96\x1cs\'\xb9\xff\xf8\x06\xd6y\xc8ck7\x1d\xf1\xe6\x8cjAu*\x06j\xe8\x15\xa9TJx\xbd^a0\x18(\xbe\x1fR\xfa\xdd\xcbfTOz\xcfi\xdc0(_g\x9d/<nO\xc1"\xcf\xdf\xe4\xb3*\xc4>iNj\xb5Z\xd1\xd2\xd2\x92\xc2\xb7)\x14\x8dFS\x16\x8b\xa5W\xa9T\xe6z\x06\xc5\x7fSJ\xeb\xa1\xbc\xd5e\x19#\x9fU\xd1\x82F\x9f\xbf\xc9g\xd50\xfb5\xd2\xaa\xfe#\x1a\x8d\xe6<\xca\xfdibbBLOO\xf7\x84\xc3\xe1\x83\xeb\xfc\x93hy\xeeB\x96>\xf9\x1c\x18*h\xf4\xf9\x9b|V5\xb3\xdf\xc4\xfe\xdao\n\xedQ\xa1\xd7\xeb\'\xc7\xc7\xc7W\xa0\xf7#x\x02\x96\\.\xd7\xaf\xc6\xc6\xc6\xba\xc1\xc1A\x15|9W\xb4\xffI\xf3O)]\xd7]\xe0%\xf7]\xdc\x1aY9M>\xab\xe43dD\xca~\x16\x8f\xf1\xfd*\xa3\xd1X\x0emf\xf0\xd6\xedv\x0b\x8f\xc7#\x02\x81\x80\x88\xc5b\x7f@\xfb\x9d\xcf\xe7\x9b\xc7\xff\x810\x9b\xcdB\xa7\xd3\t\x85BAs\xa7@\xd1V\t\xcbatVQ,%\xecG\xd9We\x8c\xab\xe4\xfb\xcf\xd6\xdc;\x00z\xc1\xbc\x94~o\xe7\xf0\xfd\xf6Z\xad\xd6\x86d2\xe9\x89D"1\xbf\xdf\xbf\x12\n\x85D"\x91X\xc49\xf0"\x1e\x8f\xf7 O\r\xa0\x1a\xa8\xb6\xe9\xff\xba\x02\xba\xe4=\xd1\x0c< \x00b\x0c\xb5\x07\xb8\x8f\xc6\xe8\x80b\x9b\xe6\xa2\x94k]\x0fz\xf8\\\xf8\x00\x12 \xc4\xfe\xce\x9e\xd8\xd9\x13\xb4\'\xbe\x83\xe2m\xaa9\x9b\xe5\xd2\xfa\x1b\x83\x12\x85\xe8',
                    "LWFF": b'\x00\x00\x03^x\x9c\xed\x96]H\x93Q\x1c\xc6_\xe6\\Pm\x11e\x03!P\xbb\x91E\x10\xb4\x0b\x85.\xb6\x8bp\x0c\xaf$\x85\xd9"\x83P\xd9@1\xc5\x06\x06N\x1d\xeaPJ\xc3\x0c\xf4FI\xa1\xe6\x84\xb6\xa2"f\r5\x1a\x997\xc2\xd0\x84f\x94\x11\xbaAn\x82E\xc5N\xcf\xd1\xf3\xb2i\xbes\x96\xd3>|\xe0\xc7\xfbq\xfe\xef{\xces>\xfe\xe7p\xdci\xee\xb0\xf8\x1e\xb7\xab\xffRI6\x9bm\xa7\xdb\xb0]\xa2^\x97\xccf\xf3,\xf0\x80\x01p\x1d\\\x06\x05 \xbb\xbe\xbe\xfe\xa8\xc5b\xd9\xd7\xd2\xd2\xb2\xd3m\xdd*Q\xcf\xd4\x13\xf5\x96_WWG\xbd^c\xde_\x80\x0f \x0c\x1e\xa3\xac\x14\xd7T\xb0\xd3m\xfe\x15\xc9\x00\x01\xef\x05\xca\x97X9\xd5\x81\xe6\xe6\xe6\xb3\xf09b4\x1aIuu5)..\xbe\x8a\xe7\x13\xe8\xa3\x93,n\x84]\x85\x88\xae3VL\xa2\x94\xcb\xea\xe8\x17(\x9fZ\xd3\x061xC\xdf\x89D"\x92\x96\x96F\xe7\xbd\x0f,VUU\x11\x8dFs+++k\xb9\x8c\x13\xf6\x92+P\xb6\x1d~kX\x1d\xa5\x02\xe5\xce5m\xb8\x02\xber\xab\xdb\x96\x02\xbe\xc9\xe5r_NN\xcelEE\x05\x1d\xfb\xe7\x06\x83\x81\xce\x05\xa9\xd5j\x15\xaa\xf3\xfcV\x99\xd8\x84\xec\xac\xeeS\x02\xe5\xfd\\\xc4\xd7!\x10\x02\xdd\xdcj\xbf\xb5\xec>\x9b\xff\x9fT*\xed(,,|\x08\xbfA\xf0\x08D\xafy\xbeNm\x02\xfcl\xa4\x8f\xdc\xca\x1a\x15R\x07\x17\xf1u\x83\xdd+\xb8\x88_\x11\x98\x03\xcf\xa2\xfe\xb7j~J$\x12\xa2P(H^^^\x00~\xc7\xe8\xdcW\xab\xd5\x04\xf3a\xbb\xe72\x9f7\x1e\xc4\x88\xb9\xc8b2\xc1w0\xc4\xde\xf3\xed\xbb\xc0E\xc66f\x1eJNN\x16\xc3\xab\xb6\xac\xac\x8c\xaesR^^\xbe\x0c\xbdOOO\xe7\xd7|"\xc5\xe7\x8d\xda\x181\xf9,\x86_\xc7\x1a\xf6\x9e\xf7\xf1\x8a\x8b\x8c\xadN\xa9T\x12\xf0\xb4\xb2\xb2\xd2D\x08\xe9\x06C`\x86\xac\xc8\x0f\xde\x05\x83A\xe2v\xbbgFGG\xef\xfa|\xbe\xa1\xc1\xc1\xc1\xb7\xad\xad\xad\xa1\x86\x86\x86\'mmm\x15===\x19\x13\x13\x13I\x88\xddj\xbf|\xde\xc8\x8d\x11\xa3\x89\xf26-\x93\xc9\x8e\xa1\x1dgh\xe3KJJ\x08r\x11\xb1\xdb\xed\xafC\xa1\xd0\x02^}\x86\xc8\xf8\xf8\xf8\xd8\xe4\xe4\xa4\x95\x86\xb0\xd8\x0c \x01)\xa0]\xab\xd5\x12\x95J\xd5\xd9\xde\xden\xc0\xb3\x19\xdc\x04\xf7\x03\x81\xc0\xf4\xf0\xf0\xf0"\xfc\x86\x9b\x9a\x9a\xc2}}}\x8b\x1e\x8fgzaa\xc1\x8d\xf2\x01\xd0\xc9\xe2\x8d\xa0\x00\xa8\xc0qp\x04\xc4\xd3?|\xdeX\x0f>\x97d\xeat:\xa2\xd7\xeb\x89\xd3\xe9\x0c\xb3\xb1rQ\xbf]]]\xc4d2y\xe1[\x89\xc7\x83 \x9e<\x14O\xcc~\xcc{z\xe6\x19hll\xfc\x84\xeb\x14\xf6\xfd;\xbd\xbd\xbd\x16\xaf\xd7\xcb\xf7\x8f\r\xd0~\xf0\x82y\xf0\x05\x886\xf0\xfcSn\xe1\xc18^\xf2\xfb\xfd\x0e|\x1f\xa4\xde\x1c\x0eG\xa8\xa8\xa8H\xeer\xb9\xf8o\xf9\xd8\xecu\xfe\xb77\x8e:c\xc5D\x8b\xaey\x15;\xdf\xfa\x18\xf4^\x8d~\x10G\x9d\xf16\xf2\xbaV2\xc4\xeb\xa95\xe6\x91^\xcf\x01Y\x02\xd6\xd1\xef\x88\x9e\xe5j\xe0\xf5%\xbc\xd2|\x7f\x1b\x08\xed\xf3B\xda\x03Os\x7f\xb0G!\xa5\xb2}\x9d\xee\xf3\xf3@\xb2\x893\xfd\x9e\xbf\xc4\xa3\x906\xe3uW\xff\x8e~\x00\x0e6qN',
                    "DNIC": b'\x00\x00\x03\x10x\x9c\xed\x95_HSQ\x1c\xc7/\x9b\x0e\x86c0\xcae\xe6\x83\x0c\xdcC\x85\x0cz\x08b\xb8\x1eF\xa6F \x94\xb3\x17\x1f\x12\x12J\xdc\x93\x13\x9d\xb1\xcd\x07\xa5\x82\xe9\x83\x05\x05>D\x0f\xc2\xdc@"$\x88$\x89\xc0\x07_\xa74\xc5\x1c\xb6\x82D\x92\x05e:\xfb\xf5=\xf8\xbbu\xbbl\x13\x9c\xb7D\xfb\xc1\x87s\xcf\xef\x9c\xf3;\xbf\xef\xf9w%\xc9)\x1d-\x1a\x97r\x98\x91\x88r\xb5\x1d4\x13Z\xdf\x83\xb2C\xa4y\x10Z\xc3\x87H\xaf\xd8\xdb\xd5C\xb8\xc7C\x07\\\xaf\x19\x90LEE\x05\xfd\x80-..\xaeLOO\x8f\xcd\xcf\xcf{\xa1\xffJ2\x99$\xbb\xddN\xc5\xc5\xc5\xd5\x8a\xb1&\x1e\xb7\xa2\x8a5\xa3\x9a\xc3\x01b\x06\x83!\x8dr\x03\xa4\xc0]P\xa4\xa1\xae\\vIR\xe8\x15\x98\xcdf\xaa\xaa\xaa\xa2\xfa\xfa\xfa\x8c\xd7\xeb\x1d]ZZ\x9aI\xa5R\xb4\xb0\xb0@\x85\xda\xdc\xdc\x1cE\xa3Q\n\x85B\xe4\xf1xFjkk\r\x7f\xf9<\xf9Y\xe75\x85\xef\x18\x18e\xff\x84\xa2\x0f\xe9\xf5z\xb1\x97:\xee\xd7\xc5\xfe\x80*V+\xd7m`\x9d}\xf7JJJ\xceMMMy2\x99Llrrr+\x16\x8bm$\x12\x89ob\x19@\x14\x84\x80\x07\x9c\x06Z\xadC\x94\xf3q\xa8\xfc\xf2\xd9\xfc\xaa\xe83\xc1\xe5e\xee\x13Q\xd5\xe5~.\xae\x0fs\xfdI\x9e\xf9\r\xac\xaf\x89\xf5\n\xdd\xb3@\xabu\xf8(m\xdf)\x9d\xca\xaf\xe3\\7\xb8\x8f\xf8>\xce\xf5\xa7\xdc\'\xc9\xfeRE\xac\x8c\xf4\xfb^\xbe\xe3\xf63\xbb\xc8K\x8bu\x90\xf7\xf0u\x96\xb63\xdc&\xe7\x9cb\x7f\x845\x9d\x90\xb2\xbfU\tE\x8c\x0c\xfb\xf6\xd2r\xadC\x1a\x14\xed\xa0Y~\xabF\xb2\xb4=\xe3\xb6\x18\x97\x11\xf6_\xe4\xfas.\xa3\xaaX\xa3\x8a\x18\xf2\xdd-\x95\xfe\xb4\xb3 \xad\x88\xb9\x17f\x88\xc7\xe3;\xf5\xc9\xf6VU\xe3\x9f$\xdf\xc35p\x87\xbfo\x03]0\x18\x14\xe7\\>\xdf\xd9\xde\xaa.E\xac\x97\xec\x13k\'\xee\x82\x18+\xd6+\xc5\xfe\xa1<\xb9\xe9#\x91\x88\x15\xf3\x9d\xea\xeb\xeb;\x8f\xb2\t\xdc\xc2\xbb\x8e"\xf8\x00\x8c\x81W`\x16\xac\x80u\x91\x1b\xc8\xa7W\xd6\xf5\x0b\x93\xc9D\x18\x93\x8f\xcf`\xcd\xe7\xf3Q[[\x1b\xb5\xb4\xb4\xbc\xc1?\xeb\x11|o\x1b\x1b\x1b\xc9\xe9t\x0e777_E^n\xf8\xae\xbb\xddn\xb2X,d4\x1a\xc5\xdbNx\xa3\xc9j\xb5Ree\xe5\x07\x87\xc3\xe1\xeb\xec\xec\xcc\x95\xff&\xf8\x04\xe2\xec\x8f\x80\xfb\xc1m\xbb\t\xc4\x1cb\x1dN\x82\xd2\xfe\xfe\xfe\x9d\xb4J\xaa}\x12l\xd5\xd5\xd5}ihhx\x88o\xbb\xaa\xcf\x11\xde_\xcb\xc0\xc0\xc0\x85\x9a\x9a\x1a*//\'\x9b\xcd\xd6\n\xbd7\xe0O\xbb\\.\x82\xbe\xc7==="\xb7\x17`\x06\xa4z{{7\xbb\xbb\xbb)\x10\x08\x10\xf4}\xef\xe8\xe8Xnoo\x1f\xf7\xfb\xfd\x85\xe6_\x88\x95!\xfe*(\xd3h\x1eq>\xb5\x88\xbb[\x1b\x84\xce\xb0\xc6k\xba_\xcc\x18\x0e\x87\x975\xdc\xdb\xfdhB\xf3\xbf\xce\xe1\xbf\x15n?\x01\xd6\x9cux'
                }
                self.client.currentCaptcha = random.choice(list(captchas))
                await self.client.sendData(Identifiers.send.Captcha, captchas[self.client.currentCaptcha])
                return

            elif CC == Identifiers.recv.Login.Player_MS:
                await self.client.sendData(Identifiers.send.Player_MS)
                return

            elif CC == Identifiers.recv.Login.Dummy:
                # if self.client.awakeTimer.when() - _time.time() < 110.0:
                    # self.client.awakeTimer.reset(120)
                return

            elif CC in [Identifiers.recv.Login.Player_Info, Identifiers.recv.Login.Player_Info2, Identifiers.recv.Login.Temps_Client, Identifiers.recv.Login.Undefined, Identifiers.recv.Informations.Letter, Identifiers.recv.Login.Player_FPS]:
                return

            elif CC == Identifiers.recv.Login.Rooms_List:
                mode = packet.readByte()
                self.client.lastGameMode = mode
                self.client.sendGameMode(mode)
                return

        elif C == Identifiers.recv.Transformation.C:
            if CC == Identifiers.recv.Transformation.Transformation_Object:
                objectID = packet.readShort()
                if not self.client.isDead and self.client.room.currentMap in range(200, 211):
                    self.client.room.sendAll(Identifiers.send.Transformation, ByteArray().writeInt(self.client.playerCode).writeShort(objectID).toByteArray())
                return

        elif C == Identifiers.recv.Informations.C:
            if CC == Identifiers.recv.Informations.Game_Log:
                errorC, errorCC, oldC, oldCC, error = packet.readByte(), packet.readByte(), packet.readByte(), packet.readByte(), packet.readUTF()
                if self.server.isDebug:
                    if errorC == 1 and errorCC == 1:
                        print("[%s] [%s][OLD] GameLog Error - C: %s CC: %s error: %s" %(_time.strftime("%H:%M:%S"), self.client.playerName, oldC, oldCC, error))
                    elif errorC == 60 and errorCC == 1:
                        if oldC == Identifiers.tribulle.send.ET_SignaleDepartMembre or oldC == Identifiers.tribulle.send.ET_SignaleExclusion: return
                        print("[%s] [%s][TRIBULLE] GameLog Error - Code: %s error: %s" %(_time.strftime("%H:%M:%S"), self.client.playerName, oldC, error))
                    else:
                        print("[%s] [%s] GameLog Error - C: %s CC: %s error: %s" %(_time.strftime("%H:%M:%S"), self.client.playerName, errorC, errorCC, error))
                return

            elif CC == Identifiers.recv.Informations.Player_Ping:
                try:
                    VC = (ord(packet.toByteArray()) + 1)
                    if self.client.PInfo[0] == VC:
                        self.client.PInfo[2] = int(_time.time() - self.client.PInfo[1])
                except: pass
                return

            elif CC == Identifiers.recv.Informations.Change_Shaman_Type:
                type = packet.readByte()
                self.client.shamanType = type
                self.client.sendShamanType(type, (self.client.shamanSaves >= 2500 and self.client.hardModeSaves >= 1000))
                return

            elif CC == Identifiers.recv.Informations.Send_Gift:
                await self.client.sendData(Identifiers.send.Send_Gift, 1)
                return

            elif CC == Identifiers.recv.Informations.Computer_Info:
                return

            elif CC == Identifiers.recv.Informations.Change_Shaman_Color:
                color = packet.readInt()
                self.client.shamanColor = "%06X" %(0xFFFFFF & color)
                return

            elif CC == Identifiers.recv.Informations.Request_Info:
                await self.client.sendData(Identifiers.send.Request_Info, ByteArray().writeUTF("http://195.154.124.74/outils/info.php").toByteArray())
                return

        elif C == Identifiers.recv.Lua.C:
            if CC == Identifiers.recv.Lua.Lua_Script:
                script = packet.readUTFBytes(((packet.readByte() << 24) & 0xFF) | packet.readShort()).decode()
                if self.client.privLevel.upper(10):
                    if not self.client.luaadmin:
                        if self.client.room.luaRuntime == None:
                            self.client.room.luaRuntime = Lua(self.client.room, self.server)
                        self.client.room.luaRuntime.owner = self.client
                        self.client.room.luaRuntime.RunCode(script)
                    else: self.client.runLuaScript(script)
                return

            elif CC == Identifiers.recv.Lua.Key_Board:
                key, down, posX, posY = packet.readShort(), packet.readBoolean(), packet.readShort(), packet.readShort()
                if key == 72:
                    self.client.room.sendAll(Identifiers.send.Paw, ByteArray().writeInt(self.client.playerCode).toByteArray())
                elif key == 85:
                    self.client.room.sendAll(Identifiers.send.Giftbox, ByteArray().writeInt(self.client.playerCode).toByteArray())
                if self.client.room.luaRuntime != None:
                    self.client.room.luaRuntime.emit("Keyboard", (self.client.playerName, key, down, posX, posY))
             #       print(key, down, posX, posY)
                return

            elif CC == Identifiers.recv.Lua.Mouse_Click:
                posX, posY = packet.readShort(), packet.readShort()
                #print(posX, posY)
                if self.client.room.luaRuntime != None:
                    self.client.room.luaRuntime.emit("Mouse", (self.client.playerName, posX, posY))
                return

            elif CC == Identifiers.recv.Lua.Popup_Answer:
                popupID, answer = packet.readInt(), packet.readUTF()
                self.client.others.popupCallback(popupID, answer)
                self.client.shopPanel.popupCback(popupID, answer)
                if self.client.room.luaRuntime != None:
                    self.client.room.luaRuntime.emit("PopupAnswer", (popupID, self.client.playerName, answer))
                return

            elif CC == Identifiers.recv.Lua.Text_Area_Callback:
                textAreaID, event = packet.readInt(), packet.readUTF()
                print((textAreaID, event))
                self.client.others.textAreaCallback(textAreaID, event)
                self.client.shopPanel.textACback(textAreaID, event)
                if self.client.room.luaRuntime != None:
                    self.client.room.luaRuntime.emit("TextAreaCallback", (textAreaID, self.client.playerName, event))
                return

            elif CC == Identifiers.recv.Lua.Color_Picked:
                colorPickerId, color = packet.readInt(), packet.readInt()
                try:
                    if colorPickerId == 10000:
                        if color != -1:
                            self.client.nameColor = "%06X" %(0xFFFFFF & color)
                            self.client.room.setNameColor(self.client.playerName, color)
                            self.client.sendMessage("<ROSE>Your name color has changed successfully")
                    elif colorPickerId == 10001:
                        if color != -1:
                            self.client.mouseColor = "%06X" %(0xFFFFFF & color)
                            self.client.playerLook = "1;%s" %(self.client.playerLook.split(";")[1])
                            self.client.sendMessage("<ROSE>Your mouse color has changed successfully.\nWait for the next round.")
                except: self.client.sendMessage("<ROSE>Incorrect color.")
                return

        elif C == Identifiers.recv.Cafe.C:
            if CC == Identifiers.recv.Cafe.Reload_Cafe:
                if self.client.canUseCafe:
                    self.client.loadCafeMode()
                    self.client.canUseCafe = False
                    self.server.loop.call_later(2, setattr, self.client, "canUseCafe", True)
                return

            elif CC == Identifiers.recv.Cafe.Open_Cafe_Topic:
                topicID = packet.readInt()
                self.client.openCafeTopic(topicID)
                return

            elif CC == Identifiers.recv.Cafe.Create_New_Cafe_Topic:
                if self.client.privLevel.upper(1):
                    message, title = packet.readUTF(), packet.readUTF()
                    self.client.createNewCafeTopic(message, title)
                return

            elif CC == Identifiers.recv.Cafe.Create_New_Cafe_Post:
                if self.client.privLevel.upper(1):
                    First, message = packet.readInt(), packet.readUTF()
                    self.client.createNewCafePost(0, message)
                return

            elif CC == Identifiers.recv.Cafe.Open_Cafe:
                self.client.isCafe = packet.readBoolean()
                return

            elif CC == Identifiers.recv.Cafe.Vote_Cafe_Post:
                if self.client.privLevel.upper(1):
                    topicID, postID, mode = packet.readInt(), packet.readInt(), packet.readBoolean()
                    self.client.voteCafePost(topicID, postID, mode)
                return

            elif CC == Identifiers.recv.Cafe.Delete_Cafe_Message:
                if self.client.privLevel.uppermost() >= 7:
                    topicID, postID = packet.readInt(), packet.readInt()
                    self.client.deleteCafePost(topicID, postID)
                return

            elif CC == Identifiers.recv.Cafe.Delete_All_Cafe_Message:
                if self.client.privLevel.uppermost() >= 7:
                    topicID, playerName = packet.readInt(), packet.readUTF()
                    self.client.deleteAllCafePost(topicID, playerName)
                return

        elif C == Identifiers.recv.Inventory.C:
            if CC == Identifiers.recv.Inventory.Open_Inventory:
                self.client.sendInventoryConsumables()
                return

            elif CC == Identifiers.recv.Inventory.Use_Consumable:
                id = packet.readShort()
                self.client.useConsumable(id)
                return

            elif CC == Identifiers.recv.Inventory.Equip_Consumable:
                id, equip = packet.readShort(), packet.readBoolean()
                if id in self.client.equipedConsumables:
                    self.client.equipedConsumables.remove(id)
                else:
                    self.client.equipedConsumables.append(id)
                return

            elif CC == Identifiers.recv.Inventory.Trade_Invite:
                playerName = packet.readUTF()
                playerName = playerName.split("#")[0]
                self.client.tradeInvite(playerName)
                return

            elif CC == Identifiers.recv.Inventory.Cancel_Trade:
                playerName = packet.readUTF()
                playerName = playerName.split("#")[0]
                self.client.cancelTrade(playerName)
                return

            elif CC == Identifiers.recv.Inventory.Trade_Add_Consusmable:
                id, isAdd = packet.readShort(), packet.readBoolean()
                try:
                    self.client.tradeAddConsumable(id, isAdd)
                except: pass
                return

            elif CC == Identifiers.recv.Inventory.Trade_Result:
                isAccept = packet.readBoolean()
                self.client.tradeResult(isAccept)
                return

        elif C == Identifiers.recv.Tribulle.C:
            if CC == Identifiers.recv.Tribulle.Tribulle:
                if not self.client.isGuest:# and self.client.canUseTribulle:
                    #self.client.canUseTribulle = False
                    code = packet.readShort()
                    self.client.tribulle.parseTribulleCode(code, packet)
                    #self.server.loop.call_later(1.5, setattr, self.client, "canUseTribulle", True)
                return

        elif C == Identifiers.recv.Transformice.C:
            if CC == Identifiers.recv.Transformice.Invocation:
                objectCode, posX, posY, rotation, position, invocation = packet.readShort(), packet.readShort(), packet.readShort(), packet.readShort(), packet.readUTF(), packet.readBoolean()
                if self.client.isShaman:
                    showInvocation = True
                    if self.client.room.isSurvivor:
                        showInvocation = invocation
                    pass
                    if showInvocation:
                        try:
                            self.client.room.sendAllOthers(self.client, Identifiers.send.Invocation, ByteArray().writeInt(self.client.playerCode).writeShort(objectCode).writeShort(posX).writeShort(posY).writeShort(rotation).writeUTF(position).writeBoolean(invocation).toByteArray())
                        except: pass

                    if self.client.room.luaRuntime != None:
                        self.client.room.luaRuntime.emit("SummoningStart", (self.client.playerName, objectCode, posX, posY, rotation))
                return

            elif CC == Identifiers.recv.Transformice.Remove_Invocation:
                if self.client.isShaman:
                    self.client.room.sendAllOthers(self.client, Identifiers.send.Remove_Invocation, ByteArray().writeInt(self.client.playerCode).toByteArray())
                    if self.client.room.luaRuntime != None:
                        self.client.room.luaRuntime.emit("SummoningCancel", (self.client.playerName))
                return

            elif CC == Identifiers.recv.Transformice.Change_Shaman_Badge:
                badge = packet.readByte()
                if str(badge) or badge == 0 in self.client.shamanBadges:
                    self.client.equipedShamanBadge = str(badge)
                    self.client.sendProfile(self.client.playerName)
                return

            elif CC == Identifiers.recv.Transformice.NPC_Functions:
                id = packet.readByte()
                if id == 4:
                    self.client.openNpcShop(packet.readUTF())
                else:
                    self.client.buyNPCItem(packet.readByte())
                return
            
            elif CC == 50:
                tr = packet.readByte()
                if int(tr) == 1:
                    class_id = packet.readUTF()
                    popupID = packet.readInt()
                    big = packet.readBoolean()
                    big_big = packet.readBoolean()
                    answer = "yes" if packet.readBoolean() else "no"
                else:
                    popupID = packet.readInt()
                    answer = "yes" if packet.readBoolean() else "no"
                self.client.others.popupCallback(popupID, answer)
                self.client.shopPanel.popupCback(popupID, answer)

            elif CC == Identifiers.recv.Transformice.Map_Info:
                self.client.room.cheesesList = []
                cheesesCount = packet.readByte()
                i = 0
                while i < cheesesCount // 2:
                    cheeseX, cheeseY = packet.readShort(), packet.readShort()
                    self.client.room.cheesesList.append([cheeseX, cheeseY])
                    i += 1

                self.client.room.holesList = []
                holesCount = packet.readByte()
                i = 0
                while i < holesCount // 3:
                    holeType, holeX, holeY = packet.readShort(), packet.readShort(), packet.readShort()
                    self.client.room.holesList.append([holeType, holeX, holeY])
                    i += 1
                return
            
            elif CC == Identifiers.recv.Transformice.Full_Look:
                p = ByteArray(packet.toByteArray())
                visuID = p.readShort()
                from functools import reduce
                self.client.shop = self.client.parseShop
                shopItems = [] if self.client.shopItems == "" else self.client.shopItems.split(",")
                look = self.server.shopOutfitsCheck[str(visuID)][0].split(";")
                look[0] = int(look[0])
                lengthCloth = len(self.client.clothes)
                buyCloth = 5 if (lengthCloth == 0) else (50 if lengthCloth == 1 else 100)

                self.client.visuItems = {-1: {"ID": -1, "Buy": buyCloth, "Bonus": True, "Customizable": False, "HasCustom": False, "CustomBuy": 0, "Custom": "", "CustomBonus": False}, 22: {"ID": self.client.getFullItemID(22, look[0]), "Buy": self.client.getItemInfo(22, look[0])[6], "Bonus": False, "Customizable": False, "HasCustom": False, "CustomBuy": 0, "Custom": "", "CustomBonus": False}}

                count = 0
                for visual in look[1].split(","):
                    if not visual == "0":
                        item, customID = visual.split("_", 1) if "_" in visual else [visual, ""]
                        item = int(item)
                        itemID = self.client.getFullItemID(count, item)
                        itemInfo = self.client.getItemInfo(count, item)
                        self.client.visuItems[count] = {"ID": itemID, "Buy": itemInfo[6], "Bonus": False, "Customizable": bool(itemInfo[2]), "HasCustom": customID != "", "CustomBuy": itemInfo[7], "Custom": customID, "CustomBonus": False}
                        if self.client.shop.checkInShop(self.client.visuItems[count]["ID"]):
                            self.client.visuItems[count]["Buy"] -= itemInfo[6]
                        if len(self.client.custom) == 1:
                            if itemID in self.client.custom:
                                self.client.visuItems[count]["HasCustom"] = True
                            else:
                                self.client.visuItems[count]["HasCustom"] = False
                        else:
                            if str(itemID) in self.client.custom:
                                self.client.visuItems[count]["HasCustom"] = True
                            else:
                                self.client.visuItems[count]["HasCustom"] = False
                    count += 1
                hasVisu = map(lambda y: 0 if y in shopItems else 1, map(lambda x: x["ID"], self.client.visuItems.values()))
                visuLength = reduce(lambda x, y: x + y, hasVisu)
                allPriceBefore = 0
                allPriceAfter = 0
                promotion = 70.0 / 100

                p.writeShort(visuID)
                p.writeByte(0)
                p.writeUTF(self.server.shopOutfitsCheck[str(visuID)][0])
                #print(int(visuLength))
                p.writeByte(int(visuLength))

                for category in self.client.visuItems.keys():
                    if len(self.client.visuItems.keys()) == category:
                        category = 22
                    itemID = self.client.getSimpleItemID(category, self.client.visuItems[category]["ID"])

                    buy = [self.client.visuItems[category]["Buy"], int(self.client.visuItems[category]["Buy"] * promotion)]
                    customBuy = [self.client.visuItems[category]["CustomBuy"], int(self.client.visuItems[category]["CustomBuy"] * promotion)]

                    p.writeInt(self.client.visuItems[category]["ID"])
                    p.writeByte(2 if self.client.visuItems[category]["Bonus"] else (1 if not self.client.shop.checkInShop(self.client.visuItems[category]["ID"]) else 0))
                    p.writeShort(buy[0])
                    p.writeShort(buy[1])
                    p.writeByte(3 if not self.client.visuItems[category]["Customizable"] else (2 if self.client.visuItems[category]["CustomBonus"] else (1 if self.client.visuItems[category]["HasCustom"] == False else 0)))
                    p.writeShort(customBuy[0])
                    p.writeShort(customBuy[1])

                    allPriceBefore += buy[0] + customBuy[0]
                    allPriceAfter += (0 if (self.client.visuItems[category]["Bonus"]) else (0 if self.client.shop.checkInShop(itemID) else buy[1])) + (0 if (not self.client.visuItems[category]["Customizable"]) else (0 if self.client.visuItems[category]["CustomBonus"] else (0 if self.client.visuItems[category]["HasCustom"] else (customBuy[1]))))

                p.writeShort(allPriceBefore)
                p.writeShort(allPriceAfter)
                self.client.fullLookPrice = allPriceAfter

                await self.client.sendData(Identifiers.send.Buy_Full_Look, p.toByteArray())
        
                return

        elif C == Identifiers.recv.Language.C:
            if CC == Identifiers.recv.Language.Set_Language:
                langue = packet.readUTF().upper()
                self.client.langue = langue
                if "-" in self.client.langue:
                    self.client.langue = self.client.langue.split("-")[1]
                self.client.langueID = Utils.getLangueID(self.client.langue.upper())
                await self.client.sendData(Identifiers.send.Set_Language, ByteArray().writeUTF(langue).writeUTF(self.server.langs.get(self.client.langue.lower())[1]).writeShort(0).writeBoolean(False).writeBoolean(True).writeUTF('').toByteArray())
                return
                
            elif CC == Identifiers.recv.Language.Language_List:
                data = ByteArray().writeShort(len(self.server.langs)).writeUTF(self.client.langue.lower())
                for info in self.server.langs.get(self.client.langue.lower()):
                    data.writeUTF(info)

                for info in self.server.languages:
                    if info[0] != self.client.langue.lower():
                        data.writeUTF(info[0])
                        data.writeUTF(info[1])
                        data.writeUTF(info[2])
                await self.client.sendData(Identifiers.send.Language_List, data.toByteArray())                                              
                return
                
        elif C == Identifiers.recv.Missions.C:
            if CC == Identifiers.recv.Missions.Open_Missions:
                self.client.missions.sendMissions()

            elif CC == Identifiers.recv.Missions.Change_Mission:
                missionID = packet.readShort()
                self.client.missions.changeMission(str(missionID))
            
            elif CC == Identifiers.recv.Missions.Cafe:
                topicID, delete = packet.readInt(), packet.readBoolean()
                self.client.MessageType(topicID, delete)
            
            elif CC == Identifiers.recv.Missions.Warn:
                self.client.warns()

        if not self.server.isDebug:
            print("[%s] Packet not implemented - C: %s - CC: %s - packet: %s" %(self.client.playerName, C, CC, repr(packet.toByteArray())))

    async def parsePacketUTF(self, packet):
        values = packet.split(chr(1))
        C, CC, values = ord(values[0][0]), ord(values[0][1]), values[1:]

        if C == Identifiers.old.recv.Player.C:
            if CC == Identifiers.old.recv.Player.Conjure_Start:
                self.client.room.sendAll(Identifiers.old.send.Conjure_Start, values)
                return

            elif CC == Identifiers.old.recv.Player.Conjure_End:
                self.client.room.sendAll(Identifiers.old.send.Conjure_End, values)
                return

            elif CC == Identifiers.old.recv.Player.Conjuration:
                self.server.loop.call_later(10, self.client.sendConjurationDestroy, int(values[0]), int(values[1]))
                self.client.room.sendAll(Identifiers.old.send.Add_Conjuration, values)
                return

            elif CC == Identifiers.old.recv.Player.Snow_Ball:
                self.client.sendPlaceObject(0, 34, int(values[0]), int(values[1]), 0, 0, 0, False, True)
                return

            elif CC == Identifiers.old.recv.Player.Bomb_Explode:
                self.client.room.sendAll(Identifiers.old.send.Bomb_Explode, values)
                return

        elif C == Identifiers.old.recv.Room.C:
            if CC == Identifiers.old.recv.Room.Anchors:
                self.client.room.sendAll(Identifiers.old.send.Anchors, values)
                self.client.room.anchors.extend(values)
                return

            elif CC == Identifiers.old.recv.Room.Begin_Spawn:
                if not self.client.isDead:
                    self.client.room.sendAll(Identifiers.old.send.Begin_Spawn, [self.client.playerCode] + values)
                return

            elif CC == Identifiers.old.recv.Room.Spawn_Cancel:
                self.client.room.sendAll(Identifiers.old.send.Spawn_Cancel, [self.client.playerCode])
                return

            elif CC == Identifiers.old.recv.Room.Totem_Anchors:
                if self.client.room.isTotemEditor:
                    if self.client.tempTotem[0] < 20:
                        self.client.tempTotem[0] = int(self.client.tempTotem[0]) + 1
                        self.client.sendTotemItemCount(self.client.tempTotem[0])
                        self.client.tempTotem[1] += "#3#" + chr(1).join(map(str, [values[0], values[1], values[2]]))
                return

            elif CC == Identifiers.old.recv.Room.Move_Cheese:
                self.client.room.sendAll(Identifiers.old.send.Move_Cheese, values)
                return

            elif CC == Identifiers.old.recv.Room.Bombs:
                self.client.room.sendAll(Identifiers.old.send.Bombs, values)
                return

        elif C == Identifiers.old.recv.Balloons.C:
            if CC == Identifiers.old.recv.Balloons.Place_Balloon:
                self.client.room.sendAll(Identifiers.old.send.Balloon, values)
                return

            elif CC == Identifiers.old.recv.Balloons.Remove_Balloon:
                self.client.room.sendAllOthers(self.client, Identifiers.old.send.Balloon, [self.client.playerCode, "0"])
                return

        elif C == Identifiers.old.recv.Map.C:
            if CC == Identifiers.old.recv.Map.Vote_Map:
                if len(values) == 0:
                    self.client.room.receivedNo += 1
                else:
                    self.client.room.receivedYes += 1
                return

            elif CC == Identifiers.old.recv.Map.Load_Map:
                try:
                    values[0] = values[0].replace("@", "")
                    self.client.room.EMapLoaded = 0
                    if values[0].isdigit():
                        code = int(values[0])
                        self.client.room.CursorMaps.execute("select * from Maps where Code = ?", [code])
                        rs = self.client.room.CursorMaps.fetchone()
                        if rs:
                            if self.client.playerID == rs["Builder"] or self.client.privLevel.upper(6):
                                await self.client.sendData(Identifiers.old.send.Load_Map, [rs["XML"], rs["YesVotes"], rs["NoVotes"], rs["Perma"]])
                                self.client.room.EMapXML = rs["XML"]
                                self.client.room.EMapLoaded = code
                                self.client.room.EMapValidated = False
                            else:
                                await self.client.sendData(Identifiers.old.send.Load_Map_Result, [])
                        else:
                            await self.client.sendData(Identifiers.old.send.Load_Map_Result, [])
                    else:
                        await self.client.sendData(Identifiers.old.send.Load_Map_Result, [])
                except: pass
                return

            elif CC == Identifiers.old.recv.Map.Validate_Map:
                mapXML = values[0]
                if self.client.room.isEditor:
                    await self.client.sendData(Identifiers.old.send.Map_Editor, [""])
                    self.client.room.EMapValidated = False
                    self.client.room.EMapCode = 1
                    self.client.room.EMapXML = mapXML
                    #self.client.room.EMapLoaded = 0
                    self.client.room.mapChange()
                return

            elif CC == Identifiers.old.recv.Map.Map_Xml:
                self.client.room.EMapXML = values[0]
                return

            elif CC == Identifiers.old.recv.Map.Return_To_Editor:
                self.client.room.EMapCode = 0
                await self.client.sendData(Identifiers.old.send.Map_Editor, ["", ""])
                return

            elif CC == Identifiers.old.recv.Map.Export_Map:
                isTribeHouse = len(values) != 0
                if self.client.cheeseCount < 1500 and self.client.privLevel.lower(5) and not isTribeHouse:
                    await self.client.sendData(Identifiers.old.send.Editor_Message, [""])
                    self.client.sendMessage("<ROSE>You need <b>1500</b> cheeses to export a map.")
                elif self.client.shopCheeses < (5 if isTribeHouse else 40) and self.client.privLevel.lower(5):
                    await self.client.sendData(Identifiers.old.send.Editor_Message, ["", ""])
                elif self.client.room.EMapValidated or isTribeHouse:
                    if self.client.privLevel.lower(5):
                        self.client.shopCheeses -= 5 if isTribeHouse else 40
                    code = 0
                    if self.client.room.EMapLoaded != 0:
                        code = self.client.room.EMapLoaded
                        self.client.room.CursorMaps.execute("update Maps set XML = ?, Updated = ? where Code = ?", [self.client.room.EMapXML, Utils.getTime(), code])
                    else:
                        self.server.lastMapCode += 1
                        code = self.server.lastMapCode
                        self.client.room.CursorMaps.execute("insert into Maps(Builder, XML, Perma) values (?, ?, ?)", [self.client.playerID, self.client.room.EMapXML, 22 if isTribeHouse else 0])

                    await self.client.sendData(Identifiers.old.send.Map_Editor, ["0"])
                    self.client.enterRoom(self.server.recommendRoom(self.client.langue))
                    await self.client.sendData(Identifiers.old.send.Map_Exported, [code])
                return

            elif CC == Identifiers.old.recv.Map.Reset_Map:
                self.client.room.EMapLoaded = 0
                return

            elif CC == Identifiers.old.recv.Map.Exit_Editor:
                await self.client.sendData(Identifiers.old.send.Map_Editor, ["0"])
                self.client.enterRoom(self.server.recommendRoom(self.client.langue))
                return

        elif C == Identifiers.old.recv.Draw.C:
            if CC == Identifiers.old.recv.Draw.Drawing:
                if self.client.privLevel.includes(10):
                    self.client.room.sendAllOthers(self.client, Identifiers.old.send.Drawing_Start, values)
                return

            elif CC == Identifiers.old.recv.Draw.Point:
                if self.client.privLevel.includes(10):
                    self.client.room.sendAllOthers(self.client, Identifiers.old.send.Drawing_Point, values)
                return

            elif CC == Identifiers.old.recv.Draw.Clear:
                if self.client.privLevel.includes(10):
                    self.client.room.sendAll(Identifiers.old.send.Drawing_Clear, values)
                return

        if self.server.isDebug:
            print("[%s][OLD] Packet not implemented - C: %s - CC: %s - values: %s" %(self.client.playerName, C, CC, repr(values)))
