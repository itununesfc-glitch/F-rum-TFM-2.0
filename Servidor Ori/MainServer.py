#coding: utf-8
import os, sys, json, time, random, sqlite3, pymysql, traceback, zlib, asyncio, urllib.request
from discord_webhook import DiscordWebhook

# Others
sys.dont_write_bytecode = True
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))

import modules as module

# Imports Components
from utils import *
from modules import *

loop = asyncio.get_event_loop()

# Library
from datetime import datetime, timedelta
from importlib import reload

class Client:
    def __init__(self, _server):

        # String
        self.langue = ""
        self.loop = loop
        self.packages = ByteArray()
        self.roomName = ""
        self.marriage = ""
        self.shopItems = ""
        self.tribeName = ""
        self.mouseName = ""
        self.nameColor = ""
        self.tradeName = ""
        self.playerName = ""
        self.playerTag = ""
        self.cacheTag = ""
        self.lastNpc = ""
        self.shamanItems = ""
        self.lastMessage = ""
        self.tribeMessage = ""
        self.tribeRanks = ""
        self.tempMouseColor = ""
        self.silenceMessage = ""
        self.afkkilltimer = None
        self.currentCaptcha = ""
        self.mouseColor = "78583a"
        self.shamanColor = "95d9d6"
        self.profileColor = ""
        self.playerLook = "1;0,0,0,0,0,0,0,0,0"
        self.shamanLook = "0,0,0,0,0,0,0,0,0,0"
        self.realCountry = ""
        self.modoPwetLanguage = "ALL"

        # Integer
        self.pet = 0
        self.posX = 0
        self.posY = 0
        self.velX = 0
        self.velY = 0
        self.fur = 0
        self.furEnd = 0
        self.gender = 0
        self.verifed = False
        self.petEnd = 0
        self.lastOn = 0
        self.regDate = 0
        self.langueID = 0
        self.playerID = 0
        self.banHours = 0
        self.iceCount = 2
        self.shamanExp = 0
        self.tribeCode = 0
        self.tribeRank = 0
        self.tribeChat = 0
        self.loginTime = 0
        self.hazelnuts = 0
        self.playTime = 0
        self.tribulleID = 0
        self.titleStars = 0
        self.firstCount = 0
        self.playerCode = 0
        self.shamanType = 0
        self.tribeHouse = 0
        self.tribeJoined = 0
        self.playerKarma = 0
        self.lastTopicID = 0
        self.silenceType = 0
        self.vipTime = 0
        self.playerScore = 0
        self.titleNumber = 0
        self.cheeseCount = 0
        self.colorProfileCC = 0
        self.shopFraises = 0
        self.shamanSaves = 0
        self.shamanLevel = 1
        self.lastGameMode = 0
        self.bubblesCount = 0
        self.currentPlace = 0
        self.chec = 0
        self.survivorDeath = 0
        self.shamanCheeses = 0
        self.hardModeSaves = 0
        self.bootcampCount = 0
        self.lastReportID = 0
        self.shopCheeses = 100
        self.shamanExpNext = 32
        self.ambulanceCount = 0
        self.defilantePoints = 0
        self.divineModeSaves = 0
        self.equipedShamanBadge = 0
        self.playerStartTimeMillis = 0
        self.wrongLoginAttempts = 0
        self.lastPacketID = random.randint(0, 99)
        self.authKey = 0

        # Bool
        self.isAfk = False
        self.isDead = False
        self.isMute = False
        self.isCafe = False
        self.isGuest = False
        self.isVoted = False
        self.isTrade = False
        self.useTotem = False
        self.isHidden = False
        self.isClosed = False
        self.isShaman = False
        self.hasEnter = False
        self.isSuspect = False
        self.isVampire = False
        self.isLuaAdmin = False
        self.hasCheese = False
        self.isJumping = False
        self.resetTotem = False
        self.canRespawn = False
        self.enabledLua = False
        self.isNewPlayer = False
        self.isEnterRoom = False
        self.tradeConfirm = False
        self.canSkipMusic = False
        self.isReloadCafe = False
        self.isMovingLeft = False
        self.isMovingRight = False
        self.isFacingRight = False
        self.isOpportunist = False
        self.qualifiedVoted = False
        self.desintegration = False
        self.canShamanRespawn = False
        self.validatingVersion = False
        self.canRedistributeSkills = False
        self.isVip = False
        self.canUseSpawnAll = True
        self.LucasPro = True
        self.canUseCafe = True
        self.canUseTribulle = True
        self.luaadmin = False
        self.isTribeOpen = False
        self.isModoPwet = False
        self.isModoPwetNotifications = False

        # Others
        self.Cursor = Cursor
        self.CursorCafe = CursorCafe
        self.CMDTime = time.time()
        self.CAPTime = time.time()
        self.CTBTime = time.time()
        self.CHTTime = time.time()
        self.LOGTime = time.time()
        self.CRTTime = time.time()

        # Nonetype
        self.room = None
        self.awakeTimer = None
        self.skipMusicTimer = None
        self.resSkillsTimer = None
        self.spawnTimer = None
        self.vipTimer = None
        self.privLevel = None
        self.server = _server
        self.lastping = False

        # List
        self.totem = [0, ""]
        self.dailyMissions = [0, 0, 0, 0]
        self.PInfo = [0, 0, 400]
        self.tempTotem = [0, ""]
        self.racingStats = [0] * 4
        self.survivorStats = [0] * 4
        self.defilanteStats = [0] * 3

        self.voteBan = []
        self.clothes = []
        self.titleList = []
        self.shopBadges = []
        self.friendsList = []
        self.tribeInvite = []
        self.shamanBadges = []
        self.ignoredsList = []
        self.mulodromePos = []
        self.shopTitleList = []
        self.marriageInvite = []
        self.firstTitleList = []
        self.cheeseTitleList = []
        self.shamanTitleList = []
        self.bootcampTitleList = []
        self.hardModeTitleList = []
        self.equipedConsumables = []
        self.ignoredTribeInvites = []
        self.divineModeTitleList = []
        self.specialTitleList = []
        self.ignoredMarriageInvites = []
        self.cloneData = [0, 0]
        self.invitedTribeHouses = []

        # Dict
        self.playerSkills = {}
        self.tradeConsumables = {}
        self.playerMissions = {}
        self.playerConsumables = {}
        self.visuItems = {}
        self.custom = []

    def getnewlen(self,b):
        var_2068 = 0
        var_2053 = 0
        var_176 = b
        while var_2053 < 10:
            var_56 = var_176.readByte() & 255
            var_2068 = var_2068 | (var_56 & 127) << 7 * var_2053
            var_2053 += 1
            if not ((var_56 & 128) == 128 and var_2053 < 5):
                return var_2068+1, var_2053

    def data_received(self, data):
        if data == b'<policy-file-request/>\x00':
            self.transport.write(b'<cross-domain-policy><allow-access-from domain=\"*\" to-ports=\"*\"/></cross-domain-policy>\x00')
            self.transport.close()
            return
            
        for i in range(5):
            if not data[i] & 128:
                break
        
        asyncio.ensure_future(self.parseString(ByteArray(data[i + 1:])))

    def eof_received(self):
        pass

    def connection_made(self, transport):
        self.transport = transport
        self.ipAddress = transport.get_extra_info("peername")[0]

        self.tribulle = module.Tribulle(self, self.server)
        self.modoPwet = ModoPwet(self, self.server)
        self.shopPanel = ShopPanel(self, self.server)
        self.parseShop = module.ParseShop(self, self.server)
        self.parseSkill = module.ParseSkill(self, self.server)
        self.parsePackets = module.ParsePackets(self, self.server)
        self.parseCommands = module.ParseCommands(self, self.server)
        self.others = module.Others(self)
        self.missions = module.Missions(self, self.server)

        if self.ipAddress != "127.0.0.1":
            r = urllib.request.urlopen(f"https://freegeoip.app/json/{self.ipAddress}")
            d = json.loads(r.read())
            r.close()
            self.realCountry = d["country_code"]
            self.realCity = d["city"]
        else:
            self.realCountry = "XX"
            self.realCity = "Localhost"
        
        if self.realCountry in ["EN", "FR", "FR", "BR", "ES", "CN", "TR", "VK", "PL", "HU", "NL", "RO", "ID", "DE", "E2", "AR", "PH", "LT", "JP", "CH", "FI", "CZ", "SK", "HR", "BU", "LV", "HE", "IT", "ET", "AZ", "PT"]:
            self.langueCode = self.realCountry
        else:
            self.langueCode = "EN"

        if self.ipAddress in self.server.badIPS:
            self.server.appendBadIP(self.ipAddress)

        if self.ipAddress in self.server.connectedCounts:
            self.server.connectedCounts[self.ipAddress] += 1
        else:
            self.server.connectedCounts[self.ipAddress] = 1

        if self.server.connectedCounts[self.ipAddress] >= 5 or self.ipAddress in self.server.IPPermaBanCache or self.ipAddress in self.server.IPTempBanCache:
            self.transport.close()

    def connection_lost(self, args):
        self.isClosed = True
        if self.ipAddress in self.server.connectedCounts:
            count = self.server.connectedCounts[self.ipAddress] - 1
            if count <= 0:
                del self.server.connectedCounts[self.ipAddress]
            else:
                self.server.connectedCounts[self.ipAddress] = count

        if self.playerName in self.server.players:
            del self.server.players[self.playerName]

            if self.isTrade:
                self.cancelTrade(self.tradeName)

            if self.playerName in self.server.chatMessages:
                self.server.chatMessages[self.playerName] = {}
                del self.server.chatMessages[self.playerName]

            for player in self.server.players.copy().values():
                if self.playerName and player.playerName in self.friendsList and player.friendsList:
                    player.tribulle.sendFriendDisconnected(self.playerName)

            if self.tribeCode != 0:
                self.tribulle.sendTribeMemberDisconnected()

            if self.privLevel.upper(4) and self.privLevel.lower(11):
                self.server.sendStaffMessage(4, "<ROSE>[%s][%s] <CH>%s <N>has disconnected." %(self.server.privileges["privs"][self.privLevel.uppermost()], self.langue, self.playerName), True)

            self.updateDatabase()
            
            if self.playerName in self.server.reports:
                if not self.server.reports[self.playerName]["status"] == "banned":
                    self.server.reports[self.playerName]["status"] = "disconnected"
                    self.modoPwet.updateModoPwet()

        if self.room != None:
            self.room.removeClient(self)

        self.transport.close()

    def sendOldPacket(self, identifiers, values):
        self.sendPacket([1, 1], ByteArray().writeUTF(chr(1).join(map(str, ["".join(map(chr, identifiers))] + values))).toByteArray())

    def sendPacket(self, identifiers, data=b""):
        asyncio.ensure_future(self.sendData(identifiers, data))

    async def sendData(self, identifiers, data=b""):
        if self.isClosed:
            return

        if isinstance(data, list):
            data = ByteArray().writeUTF(chr(1).join(map(str, ["".join(map(chr, identifiers))] + data))).toByteArray()
            identifiers = [1, 1]

        elif isinstance(data, int):
            data = chr(data)

        if isinstance(data, str):
            data = data.encode()

        self.lastPacketID = (self.lastPacketID + 1) % 255
        packet = ByteArray()
        length = len(data) + 2
        packet2 = ByteArray()
        calc1 = length >> 7
        while calc1 != 0:
            packet2.writeByte(((length & 127) | 128))
            length = calc1
            calc1 = calc1 >> 7
        packet2.writeByte((length & 127))
        packet.writeBytes(packet2.toByteArray()).writeByte(identifiers[0]).writeByte(identifiers[1]).writeBytes(data)
        self.transport.write(packet.toByteArray())
        
    def sendPacketTribulle(self, code, result):
        self.sendPacket([60, 3], ByteArray().writeShort(code).writeBytes(result).toByteArray())

    async def parseString(self, packet):
        if self.isClosed:
            return

        packetID, C, CC = packet.readByte(), packet.readByte(), packet.readByte()
        tokens = [C, CC]
        if not self.validatingVersion:
            if (C == Identifiers.recv.Informations.C and CC == Identifiers.recv.Informations.Correct_Version) and not (self.isClosed):
                version, lang, ckey = packet.readShort(), packet.readUTF(), packet.readUTF()

                if not ckey == self.server.CKEY and version != self.server.Version:
                    print("[%s] [WARN] Invalid version or CKey (%s, %s)" %(time.strftime("%H:%M:%S"), version, ckey))
                    self.transport.close()
                else:
                    self.validatingVersion = True
                    self.sendCorrectVersion(self.langueCode)
            else:
                self.transport.close()
        else:
            try:
                self.lastPacketID = packetID
                await self.parsePackets.parsePacket(packetID, C, CC, packet)
            except:
                with open("./include/SErros.log", "a") as f:
                    traceback.print_exc(file=f)
                    f.write("\n")
                    self.server.sendStaffMessage(7, "<BL>[<R>ERROR<BL>] The player <R>%s found an error in system." %(self.playerName))

    def loginPlayer(self, playerName, password, startRoom):
        playerName = "Souris" if playerName == "" else playerName
        self.mouseName = playerName
        if password == "":
            playerName = self.server.checkAlreadyExistingGuest("*" + (playerName[0].isdigit() or len(playerName) > 12 or len(playerName) < 3 or "Souris" if "+" in playerName else playerName))
            startRoom = "\x03[Tutorial] %s" %(playerName)
            self.isGuest = True

        elif "@" in playerName:
            if playerName.lower() in self.server.usersByEmail:
                usersList = self.server.usersByEmail[playerName.lower()]
                if len(usersList) == 1:
                    playerName = usersList[0]
                else:
                    self.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(11).writeUTF("¤".join(usersList)).writeUTF("").toByteArray())
                    return
            else:
                self.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(2).writeUTF(playerName).writeUTF("").toByteArray())
                return

        playerTag = ""
        if "#" in playerName and not "@" in playerName and not self.isGuest:
            playerName, playerTag = playerName.split("#")

        if not self.isGuest and playerName in self.server.userPermaBanCache:
            self.sendPacket(Identifiers.old.send.Player_Ban_Login, [self.server.getPermBanInfo(playerName)])
            self.transport.close()
            return

        if not self.isGuest:
            banInfo = self.server.getTempBanInfo(playerName)
            timeCalc = Utils.getHoursDiff(banInfo[1])
            if timeCalc <= 0:
                self.server.removeTempBan(playerName)
            else:
                self.sendPacket(Identifiers.old.send.Player_Ban_Login, [timeCalc, banInfo[0]])
                self.transport.close()
                return

        if self.server.checkConnectedAccount(playerName):
            self.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(1).writeUTF(playerName + ("" if playerTag == "" else ("#" + playerTag))).writeUTF("").toByteArray())
        else:
            gifts, messages = "", ""
            if not self.isGuest and not playerName == "":
                Cursor.execute("select * from Users where Username = %s and Password = %s", [playerName, password])
                rs = Cursor.fetchone()
                if rs:
                    self.playerID = rs[2]
                    self.emailAddress = rs[3]
                    self.privLevel = PrivLevel(rs[4])
                    self.titleNumber = rs[5]
                    self.firstCount = rs[6]
                    self.cheeseCount = rs[7]
                    self.shamanCheeses = rs[8]
                    self.shopCheeses = rs[9]
                    self.shopFraises = rs[10]
                    self.shamanSaves = rs[11]
                    self.hardModeSaves = rs[12]
                    self.divineModeSaves = rs[13]
                    self.bootcampCount = rs[14]
                    self.shamanType = rs[15]
                    self.shopItems = rs[16]
                    self.shamanItems = rs[17]
                    self.clothes = list(map(str, filter(None, rs[18].split("|"))))
                    self.playerLook = rs[19]
                    self.shamanLook = rs[20]
                    self.mouseColor = rs[21]
                    self.shamanColor = rs[22]
                    self.regDate = rs[23]
                    self.shopBadges = list(map(int, filter(None, rs[24].split(","))))
                    self.cheeseTitleList = list(map(float, filter(None, rs[25].split(","))))
                    self.firstTitleList = list(map(float, filter(None, rs[26].split(","))))
                    self.shamanTitleList = list(map(float, filter(None, rs[27].split(","))))
                    self.shopTitleList = list(map(float, filter(None, rs[28].split(","))))
                    self.bootcampTitleList = list(map(float, filter(None, rs[29].split(","))))
                    self.hardModeTitleList = list(map(float, filter(None, rs[30].split(","))))
                    self.divineModeTitleList = list(map(float, filter(None, rs[31].split(","))))
                    self.specialTitleList = list(map(float, filter(None, rs[32].split(","))))
                    self.banHours = rs[33]
                    self.shamanLevel = rs[34]
                    self.shamanExp = rs[35]
                    self.shamanExpNext = rs[36]
                    for skill in map(str, filter(None, rs[37].split(";"))):
                        values = skill.split(":")
                        if len(values) >= 2:
                            self.playerSkills[int(values[0])] = int(values[1])
                    self.lastOn = rs[38]
                    friendsList = list(map(int, filter(None, rs[39].split(","))))
                    ignoredsList = list(map(int, filter(None, rs[40].split(","))))
                    for friend in friendsList:
                        self.friendsList.append(self.server.getPlayerName(friend))
                    for ignored in ignoredsList:
                        self.ignoredsList.append(self.server.getPlayerName(ignored))
                    self.gender = rs[41]
                    self.marriage = self.server.getPlayerName(rs[42])
                    gifts = rs[43]
                    message = rs[44]
                    self.survivorStats = list(map(int, rs[45].split(",")))
                    self.racingStats = list(map(int, rs[46].split(",")))
                    self.defilanteStats = list(map(int, rs[47].split(",")))
                    for consumable in map(str, filter(None, rs[48].split(";"))):
                        values = consumable.split(":")
                        if len(values) >= 2:
                            self.playerConsumables[int(values[0])] = int(values[1])
                    self.equipedConsumables = list(map(int, filter(None, rs[49].split(","))))
                    self.pet = rs[50]
                    self.petEnd = 0 if self.pet == 0 else Utils.getTime() + rs[51]
                    self.shamanBadges = list(map(int, filter(None, rs[52].split(","))))
                    self.equipedShamanBadge = rs[53]
                    self.totem = [rs[54], rs[55].replace("%"[0], chr(1))]
                    self.custom = list(map(str, filter(None, rs[56].split(","))))
                    self.tribeCode = rs[57]
                    self.tribeRank = rs[58]
                    self.tribeJoined = rs[59]
                    self.playerTag = rs[60]
                    self.cacheTag = self.playerTag
                    self.playTime = rs[61]
                    self.loginTime = Utils.getTime()
                    self.fur = rs[62]
                    self.furEnd = rs[63]
                    self.hazelnuts = rs[64]
                    vipTime = rs[65]
                    self.vipTime = vipTime
                    self.isVip = vipTime != 0
                    verifed = rs[66]
                    if verifed == None or verifed == '' or verifed == "": verifed = 0
                    self.verifed = int(verifed) != 0
                else:
                    self.server.loop.call_later(10, lambda: self.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(2).writeUTF(playerName + ("" if playerTag == "" else ("#" + playerTag))).writeUTF("").toByteArray()))
                    return

            if self.privLevel is None:
                self.privLevel = PrivLevel("1")
            if self.privLevel.includes(-1):
                self.sendPacket(Identifiers.old.send.Player_Ban_Login, ["Blocked account."])
                self.transport.close()
                return

            self.server.lastPlayerCode += 1
            self.playerName = playerName
            self.playerCode = self.server.lastPlayerCode
            if not self.isGuest:
                s = f"\n <V>[ {self.playerName} ]</V> <G>{time.strftime('%d.%m.%Y - %H:%M:%S')}</G> <G>( </G><VI>{self.ipAddress}</VI><G> - {self.realCountry} - {self.realCity}</G><G> )</G>"
                self.Cursor.execute("insert into loginlog(username,ip,yazi,Timestamp) values (%s, %s, %s, %s)",[self.playerName, self.ipAddress, s, Utils.getTime()])
               # Cursor.execute("insert into loginlog (%s, %s, %s, %s)",[self.playerName, self.ipAddress, f"\n <V>[ {self.playerName} ]</V> <G>{time.strftime('%d.%m.%Y - %H:%M:%S')}</G> <G>( </G><VI>{self.ipAddress}</VI><G> - {self.realCountry} - {self.realCity}</G><G> )</G>", Utils.getTime()])

            for name in ["cheese", "first", "shaman", "shop", "bootcamp", "hardmode", "divinemode"]:
                self.checkAndRebuildTitleList(name)

            self.sendCompleteTitleList()
            self.parseShop.checkAndRebuildBadges()

            for title in self.titleList:
                if str(title).split(".")[0] == str(self.titleNumber):
                    self.titleStars = int(str(title).split(".")[1])
                    break

            self.isMute = playerName in self.server.userMuteCache
            self.server.players[self.playerName] = self

            self.sendLogin()
            self.afkkilltimerreset()
            self.sendPlayerIdentification()
            self.parseShop.sendShamanItems()
            self.parseSkill.sendShamanSkills(False)
            self.parseSkill.sendExp(self.shamanLevel, self.shamanExp, self.shamanExpNext)
            if self.shamanSaves >= 500:
                self.sendShamanType(self.shamanType, (self.shamanSaves >= 2500 and self.hardModeSaves >= 1000))

            self.server.checkPromotionsEnd()
            self.sendPacket(Identifiers.send.Time_Stamp, ByteArray().writeInt(Utils.getTime()).toByteArray())
            self.sendPromotions()

            if self.vipTime != 0:
                self.checkVip(vipTime)

            if self.tribeCode != 0:
                tribeInfo = self.tribulle.getTribeInfo(self.tribeCode)
                self.tribeName = tribeInfo[0]
                self.tribeMessage = tribeInfo[1]
                self.tribeHouse = tribeInfo[2]
                self.tribeRanks = tribeInfo[3]
                self.tribeChat = tribeInfo[4]

            self.sendPacket([60, 4], chr(1))
            self.tribulle.sendFriendsList(None)
            if self.langue.lower() in self.server.chats and not self.playerName in self.server.chats[self.langue.lower()]:
                self.server.chats[self.langue.lower()].append(self.playerName)
            elif not self.langue.lower() in self.server.chats:
                self.server.chats[self.langue.lower()] = [self.playerName]
            self.sendPacketTribulle(62, ByteArray().writeUTF(self.langue.lower()).toByteArray())
            self.missions.loadMissions()

            for player in self.server.players.copy().values():
                if self.playerName and player.playerName in self.friendsList and player.friendsList:
                    player.tribulle.sendFriendConnected(self.playerName)

            if self.tribeCode != 0:
                self.tribulle.sendTribeMemberConnected()

            if self.privLevel.upper(4) and self.privLevel.lower(11):
                self.server.sendStaffMessage(4, "<ROSE>[%s][%s] <CH>%s <N>just connected." %(self.server.privileges["privs"][self.privLevel.uppermost()], self.langue, self.playerName), True)

            self.sendInventoryConsumables()
            self.parseShop.checkGiftsAndMessages(gifts, messages)
            self.resSkillsTimer = self.server.loop.call_later(600, setattr, self, "canRedistributeSkills", True)
            self.startBulle(self.server.checkRoom(startRoom, self.langue) if not startRoom == "" and not startRoom == "1" else self.server.recommendRoom(self.langue))

    def checkAndRebuildTitleList(self, type):
        titlesLists = [self.cheeseTitleList, self.firstTitleList, self.shamanTitleList, self.shopTitleList, self.bootcampTitleList, self.hardModeTitleList, self.divineModeTitleList]
        titles = [self.server.cheeseTitleList, self.server.firstTitleList, self.server.shamanTitleList, self.server.shopTitleList, self.server.bootcampTitleList, self.server.hardModeTitleList, self.server.divineModeTitleList]
        typeID = 0 if type == "cheese" else 1 if type == "first" else 2 if type == "shaman" else 3 if type == "shop" else 4 if type == "bootcamp" else 5 if type == "hardmode" else 6 if type == "divinemode" else 0
        count = self.cheeseCount if type == "cheese" else self.firstCount if type == "first" else self.shamanSaves if type == "shaman" else self.parseShop.getShopLength() if type == "shop" else self.bootcampCount if type == "bootcamp" else self.hardModeSaves if type == "hardmode" else self.divineModeSaves if type == "divinemode" else 0
        tempCount = count
        rebuild = False
        while tempCount > 0:
            if tempCount in titles[typeID]:
                if not titles[typeID][tempCount] in titlesLists[typeID]:
                    rebuild = True
                    break
            tempCount -= 1

        if rebuild:
            titlesLists[typeID] = []
            x = 0
            while x <= count:
                if x in titles[typeID]:
                    title = titles[typeID][x]
                    i = 0
                    while i < len(titlesLists[typeID]):
                        if str(titlesLists[typeID][i]).startswith(str(title).split(".")[0]):
                            del titlesLists[typeID][i]
                        i += 1
                    titlesLists[typeID].append(title)
                x += 1

        self.cheeseTitleList = titlesLists[0]
        self.firstTitleList = titlesLists[1]
        self.shamanTitleList = titlesLists[2]
        self.shopTitleList = titlesLists[3]
        self.bootcampTitleList = titlesLists[4]
        self.hardModeTitleList = titlesLists[5]
        self.divineModeTitleList = titlesLists[6]


    def updateDatabase(self):
        if not self.isGuest:
            Cursor.execute("update Users set PrivLevel = %s, TitleNumber = %s, FirstCount = %s, CheeseCount = %s, ShamanCheeses = %s, ShopCheeses = %s, ShopFraises = %s, ShamanSaves = %s, HardModeSaves = %s, DivineModeSaves = %s, BootcampCount = %s, ShamanType = %s, ShopItems = %s, ShamanItems = %s, Clothes = %s, Look = %s, ShamanLook = %s, MouseColor = %s, ShamanColor = %s, Badges = %s, CheeseTitleList = %s, FirstTitleList = %s, ShamanTitleList = %s, ShopTitleList = %s, BootcampTitleList = %s, HardModeTitleList = %s, DivineModeTitleList = %s, SpecialTitleList = %s, BanHours = %s, ShamanLevel = %s, ShamanExp = %s, ShamanExpNext = %s, Skills = %s, LastOn = %s, FriendsList = %s, IgnoredsList = %s, Gender = %s, Marriage = %s, TribeCode = %s, TribeRank = %s, TribeJoined = %s, SurvivorStats = %s, RacingStats = %s, DefilanteStats = %s, Consumables = %s, EquipedConsumables = %s, Pet = %s, PetEnd = %s, ShamanBadges = %s, EquipedShamanBadge = %s, Tag = %s, Time = %s, Fur = %s, FurEnd = %s, Hazelnut = %s, OldNames = %s where Username = %s", [self.privLevel.output(), self.titleNumber, self.firstCount, self.cheeseCount, self.shamanCheeses, self.shopCheeses, self.shopFraises, self.shamanSaves, self.hardModeSaves, self.divineModeSaves, self.bootcampCount, self.shamanType, self.shopItems, self.shamanItems, "|".join(map(str, self.clothes)), self.playerLook, self.shamanLook, self.mouseColor, self.shamanColor, ",".join(map(str, self.shopBadges)), ",".join(map(str, self.cheeseTitleList)), ",".join(map(str, self.firstTitleList)), ",".join(map(str, self.shamanTitleList)), ",".join(map(str, self.shopTitleList)), ",".join(map(str, self.bootcampTitleList)), ",".join(map(str, self.hardModeTitleList)), ",".join(map(str, self.divineModeTitleList)), ",".join(map(str, self.specialTitleList)), self.banHours, self.shamanLevel, self.shamanExp, self.shamanExpNext, ";".join(map(lambda skill: "%s:%s" %(skill[0], skill[1]), self.playerSkills.items())), self.tribulle.getTime(), ",".join(map(str, filter(None, [self.server.getPlayerID(friend) for friend in self.friendsList]))), ",".join(map(str, filter(None, [self.server.getPlayerID(ignored) for ignored in self.ignoredsList]))), self.gender, self.server.getPlayerID(self.marriage), self.tribeCode, self.tribeRank, self.tribeJoined, ",".join(map(str, self.survivorStats)), ",".join(map(str, self.racingStats)), ",".join(map(str, self.defilanteStats)), ";".join(map(lambda consumable: "%s:%s" %(consumable[0], consumable[1]), self.playerConsumables.items())), ",".join(map(str, self.equipedConsumables)), self.pet, abs(Utils.getSecondsDiff(self.petEnd)), ",".join(map(str, self.shamanBadges)), self.equipedShamanBadge, self.cacheTag, self.playTime + abs(Utils.getSecondsDiff(self.loginTime)), self.fur, abs(Utils.getSecondsDiff(self.furEnd)), self.hazelnuts, 1 if self.verifed else 0, self.playerName])

    def startBulle(self, roomName):
        if not self.isEnterRoom:
            self.isEnterRoom = True
            self.server.loop.call_later(0.4, self.sendBulle)
            self.server.loop.call_later(0.8, lambda: self.enterRoom(roomName))
            self.server.loop.call_later(6, setattr, self, "isEnterRoom", False)

    def enterRoom(self, roomName):
        if self.isTrade:
            self.cancelTrade(self.tradeName)

        roomName = roomName.replace("<", "&lt;")
        roomNamer = roomName
        if not roomName.startswith("*") and not (len(roomName) > 3 and roomName[2] == "-" and self.privLevel.upper(7)):
            roomName = "EN-%s" %(roomName)

        for rooms in ["\x03[Editeur] ", "\x03[Totem] ", "\x03[Tutorial] "]:
            if roomName.startswith(rooms) and not self.playerName == roomName.split(" ")[1]:
                roomName = "EN-%s" %(self.playerName)

        if self.room != None:
            self.room.removeClient(self)

        self.roomName = roomName
        self.roomName1 = "%s-%s" %(self.langue, roomNamer)
        self.sendGameType(11 if "music" in roomName else 4, 0)
        self.sendEnterRoom(roomName)
        self.server.addClientToRoom(self, roomName)
        self.sendPacket(Identifiers.old.send.Anchors, self.room.anchors)
        self.sendPacket([29, 1], "")

        for player in self.server.players.copy().values():
            if self.playerName and player.playerName in self.friendsList and player.friendsList:
                player.tribulle.sendFriendChangedRoom(self.playerName, self.langueID)

        if self.tribeCode != 0:
            self.tribulle.sendTribeMemberChangeRoom()

        if self.room.isMusic and self.room.isPlayingMusic:
            self.sendMusicVideo(False)

        if roomName.startswith("music") or roomName.startswith("*music"):
            self.canSkipMusic = False
            if self.skipMusicTimer != None:
                self.skipMusicTimer.cancel()
            self.skipMusicTimer = self.server.loop.call_later(900, setattr, self, "canSkipMusic", True)
        self.others.changeRoom()

        if self.room.isFuncorp:
            self.sendLangueMessage("", "<FC>$FunCorpActive</FC>")
    
    def afkkilltimerreset(self):
        if self.afkkilltimer != None:
            self.afkkilltimer.cancel()
        self.afkkilltimer = self.loop.call_later(1200, self.transport.close)

    def resetPlay(self):
        self.iceCount = 2
        self.bubblesCount = 0
        self.currentPlace = 0
        self.ambulanceCount = 0
        self.defilantePoints = 0
        self.posY = 0
        self.posX = 0

        self.isAfk = True
        self.isDead = False
        self.useTotem = False
        self.hasEnter = False
        self.isShaman = False
        self.isVampire = False
        self.hasCheese = False
        self.isSuspect = False
        self.canRespawn = False
        self.isNewPlayer = False
        self.isOpportunist = False
        self.desintegration = False
        self.canShamanRespawn = False

    def sendAccountTime(self):
        date = datetime.now() + timedelta(hours=1)
        eventTime_ = int(str(time.mktime(date.timetuple())).split(".")[0])
        self.Cursor.execute("select IP from Account where IP = %s", [self.ipAddress])
        rrf = self.Cursor.fetchone()
        if rrf is None:
           self.Cursor.execute("insert into Account values (%s, %s)", [self.ipAddress, eventTime_])
        else:
           self.Cursor.execute("update Account set Time = %s where IP = %s", [eventTime_, self.ipAddress])

    def checkTimeAccount(self):
        self.Cursor.execute("SELECT Time FROM Account WHERE IP = %s", [self.ipAddress])
        rrf = self.Cursor.fetchone()
        return rrf is None or int(str(time.time()).split(".")[0]) >= int(rrf[0])

    def startPlay(self):
        self.playerStartTimeMillis = self.room.gameStartTimeMillis
        self.isNewPlayer = self.isDead
        self.sendMap(newMapCustom=True) if self.room.mapCode != -1 else self.sendMap() if self.room.isEditor and self.room.EMapCode != 0 else self.sendMap(True)

        shamanCode, shamanCode2 = 0, 0
        if self.room.isDoubleMap:
            shamans = self.room.getDoubleShamanCode()
            shamanCode = shamans[0]
            shamanCode2 = shamans[1]
        else:
            shamanCode = self.room.getShamanCode()

        if self.playerCode == shamanCode or self.playerCode == shamanCode2:
            self.isShaman = True

        if self.isShaman and not self.room.noShamanSkills:
            self.parseSkill.getkills()

        if self.room.currentShamanName != "" and not self.room.noShamanSkills:
            self.parseSkill.getPlayerSkills(self.room.currentShamanSkills)

        if self.room.currentSecondShamanName != "" and not self.room.noShamanSkills:
            self.parseSkill.getPlayerSkills(self.room.currentSecondShamanSkills)

        self.sendPlayerList()
        if self.room.catchTheCheeseMap and not self.room.noShamanSkills:
            self.sendPacket(Identifiers.old.send.Catch_The_Cheese_Map, [shamanCode])
            self.sendPacket(Identifiers.send.Player_Get_Cheese, ByteArray().writeInt(shamanCode).writeBoolean(True).toByteArray())
            if not self.room.currentMap in [108, 109]:
                self.sendShamanCode(shamanCode, shamanCode2)
        else:
            self.sendShamanCode(shamanCode, shamanCode2)

        self.sendSync(self.room.getSyncCode())
        self.sendRoundTime(self.room.roundTime + (self.room.gameStartTime - Utils.getTime()) + self.room.addTime)
        self.sendMapStartTimer(False) if self.isDead or self.room.isTutorial or self.room.isTotemEditor or self.room.isBootcamp or self.room.isDefilante or self.room.getPlayerCountUnique() < 2 else self.sendMapStartTimer(True)

        if self.room.isTotemEditor:
            self.initTotemEditor()

        if self.room.isMulodrome:
            if not self.playerName in self.room.redTeam and not self.playerName in self.room.blueTeam:
                if not self.isDead:
                    self.isDead = True
                    self.sendPlayerDied()

        if self.room.isSurvivor and self.isShaman:
            self.sendPacket(Identifiers.send.Can_Meep, 1)

        if self.room.currentMap in range(200, 211) and not self.isShaman:
            self.sendPacket(Identifiers.send.Can_Transformation, 1)

        if self.room.isVillage:
            self.server.loop.call_later(0.2, self.sendNpcs)
        
        if self.room.isRacing:
            self.room.removeTextArea(13, self.playerName)
            self.room.CursorMaps.execute("select Player, Time from maps where Code = ?", [self.room.mapCode])
            rs = self.room.CursorMaps.fetchone()
            if rs == None:
                pass
            if int(rs[1]) > 3: #srec
                time = float(rs[1] / 100.0 if rs[1] > 100 else rs[1] / 10.0)
                self.Cursor.execute(f"select Username from Users where PlayerID = {rs[0]}")
                try:
                    player = self.Cursor.fetchone()[0]
                except: 
                    player = "None"
                    time = 0
                if self.LucasPro:
                    self.room.addTextArea(13, f"Record {player} (<font color=\"#ffffff\">{str(time)})", self.playerName,630 ,30, 185, 20, 0x5E3441, 0x5E3441, 50, False)
                else:
                    if self.langueID == 3:
                        self.sendMessage(f"O recorde deste mapa foi batido por <V>{player}</V> (<J>{str(time)}</J>s)")
                    else: self.sendMessage(f"The record has broken by <V>{player}</V> (<J>{str(time)}</J>s)")
            else:
                if self.langueID == 3:
                    self.sendMessage("Nao ha recordes nesse mapa.")
                else: self.sendMessage("There are no broken records on this map.")

    def getPlayerData(self):
        return ByteArray().writeUTF(self.playerName + self.playerTag).writeInt(self.playerCode).writeBoolean(self.isShaman).writeBoolean(self.isDead).writeShort(self.playerScore).writeBoolean(self.hasCheese).writeShort(self.titleNumber).writeByte(self.titleStars).writeByte(self.gender).writeUTF("").writeUTF("1;0,0,0,0,0,0,0,0,0,0" if self.room.isBootcamp else (str(self.fur) + ";" + self.playerLook.split(";")[1] if self.fur != 0 else self.playerLook)).writeBoolean(False).writeInt(int(self.tempMouseColor if not self.tempMouseColor == "" else self.mouseColor, 16)).writeInt(int(self.shamanColor, 16)).writeInt(0).writeInt(int(self.nameColor, 16) if self.nameColor != "" else -1).toByteArray()

    def spawnNPC(self, npcId, npcName, npcTitle, starePlayer, npcLook, npcPosX, npcPosY):
        self.sendPacket(Identifiers.send.NPC, ByteArray().writeInt(npcId).writeUTF(npcName).writeShort(npcTitle).writeBoolean(starePlayer).writeUTF(npcLook).writeShort(npcPosX).writeShort(npcPosY).writeShort(1).writeByte(11).writeShort(0).toByteArray())

    def sendShamanCode(self, shamanCode, shamanCode2):
        self.sendPacket(Identifiers.send.Shaman_Info, ByteArray().writeInt(shamanCode).writeInt(shamanCode2).writeByte(self.server.getShamanType(shamanCode)).writeByte(self.server.getShamanType(shamanCode2)).writeShort(self.server.getShamanLevel(shamanCode)).writeShort(self.server.getShamanLevel(shamanCode2)).writeShort(self.server.getShamanBadge(shamanCode)).writeShort(self.server.getShamanBadge(shamanCode2)).toByteArray())

    def sendCorrectVersion(self, community = "en"):
        self.sendPacket(Identifiers.send.Correct_Version, ByteArray().writeInt(len(self.server.players)).writeUTF(community).writeUTF("").writeInt(self.server.authKey).writeBoolean(False).toByteArray())
        self.sendPacket(Identifiers.send.Banner_Login, ByteArray().writeBoolean(True).writeByte(self.server.adventureID).writeShort(256).toByteArray())
        self.sendPacket(Identifiers.send.Image_Login, ByteArray().writeUTF(self.server.adventureIMG).toByteArray())
        #self.awakeTimer = self.server.loop.call_later(300, self.transport.close)

    def sendLogin(self):
        if self.isGuest:
            self.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(1).writeByte(10).toByteArray())
            self.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(2).writeByte(5).toByteArray())
            self.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(3).writeByte(15).toByteArray())
            self.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(4).writeByte(200).toByteArray())

    def sendPlayerIdentification(self):
        packet = ByteArray().writeInt(self.playerID).writeUTF(self.playerName + self.playerTag).writeInt(self.playTime).writeByte(self.langueID).writeInt(self.playerCode).writeBoolean(True)
        privsAuthoratization = {1:-1, 2:3, 3:5, 4:-1, 5:13, 6:15, 7:11, 8:5, 9:5, 10:5, 11:10, 12:10}
        permsList = []
        for priv in self.privLevel.privileges:
            permsList.append(privsAuthoratization[priv])

        cafePerm = -1
        if self.privLevel.upper(8) or self.privLevel.includes(3):
            cafePerm = 3

        if not self.privLevel.includes(2):
            permsList.insert(1, cafePerm)

        if not self.privLevel.includes(11):
            if self.privLevel.includes(10, 4):
                permsList.append(10)

        packet.writeByte(len(permsList))
        for perm in permsList:
            packet.writeByte(perm)

        packet.writeBoolean(False)
        packet.writeShort(255)
        packet.writeShort(len(self.server.langs2))
        for lang in self.server.langs2:
            packet.writeUTF(lang[0])
            packet.writeUTF(lang[1])
        self.sendPacket(Identifiers.send.Player_Identification, packet.toByteArray())

    def sendPromotions(self):
        for promotion in self.server.shopPromotions:
            self.sendPacket(Identifiers.send.Promotion, ByteArray().writeBoolean(True).writeBoolean(True).writeInt(promotion[0] * (10000 if promotion[1] > 99 else 100) + promotion[1] + (10000 if promotion[1] > 99 else 0)).writeBoolean(True).writeInt(promotion[3]).writeByte(promotion[2]).toByteArray())

        if len(self.server.shopPromotions) > 0:
            promotion = self.server.shopPromotions[0]
            item = promotion[0] * (10000 if promotion[1] > 99 else 100) + promotion[1] + (10000 if promotion[1] > 99 else 0)
            self.sendPacket(Identifiers.send.Promotion_Popup, ByteArray().writeByte(promotion[0]).writeByte(promotion[1]).writeByte(promotion[2]).writeShort(self.server.shopBadges.get(item, 0)).toByteArray())

    def sendGameType(self, gameType, serverType):
        self.sendPacket(Identifiers.send.Room_Type, gameType)
        self.sendPacket(Identifiers.send.Room_Server, serverType)

    def sendEnterRoom(self, roomName, lang=""):
        if lang == "": lang = self.langue
        found = False
        rooms = roomName[3:]
        count = "".join(i for i in rooms if i.isdigit())
        for room in ["vanilla", "survivor", "racing", "music", "bootcamp", "defilante", "village", "#village+"]:
            if rooms.startswith(room) and not count == "" or rooms.isdigit():
                found = not (int(count) < 1 or int(count) > 1000000000 or rooms == room)

        self.sendPacket(Identifiers.send.Enter_Room, ByteArray().writeBoolean(found).writeUTF("*?" if self.isTribeOpen else roomName).writeUTF("int" if roomName.startswith("*") else lang).toByteArray())

    def sendMap(self, newMap=False, newMapCustom=False):
        if self.room.EMapXML != "":
            xml = self.room.EMapXML.encode()
        else:
            xml = b"" if newMap else self.room.mapXML.encode() if isinstance(self.room.mapXML, str) else self.room.mapXML if newMapCustom else self.room.EMapXML.encode() if isinstance(self.room.EMapXML, str) else self.room.EMapXML
        xml = zlib.compress(xml)
        self.sendPacket(Identifiers.send.New_Map, ByteArray().writeInt(self.room.currentMap if newMap else self.room.mapCode if newMapCustom else -1).writeShort(self.room.getPlayerCount()).writeByte(self.room.lastRoundCode).writeInt(len(xml)).writeBytes(xml).writeUTF("" if newMap else self.room.mapName if newMapCustom else "-").writeByte(0 if newMap else self.room.mapPerma if newMapCustom else 100).writeBoolean(self.room.mapInverted if newMapCustom else False).toByteArray())
        if self.isVip or self.privLevel.upper(10):
            self.room.bindKeyBoard(self.playerName, 72)
            self.room.bindKeyBoard(self.playerName, 85)

    def sendPlayerList(self):
        self.sendPacket(Identifiers.send.Players_List, ByteArray().writeShort(self.room.getPlayerList()[0]).writeBytes(self.room.getPlayerList()[1]).toByteArray())

    def sendSync(self, playerCode):
        self.sendPacket(Identifiers.old.send.Sync, [playerCode, ""] if (self.room.mapCode != 1 or self.room.EMapCode != 0) else [playerCode])

    def sendRoundTime(self, time):
        self.sendPacket(Identifiers.send.Round_Time, ByteArray().writeShort(0 if time < 0 or time > 32767 else time).toByteArray())

    def sendMapStartTimer(self, startMap):
        self.sendPacket(Identifiers.send.Map_Start_Timer, ByteArray().writeBoolean(startMap).toByteArray())

    def sendPlayerDisconnect(self):
        self.room.sendAll(Identifiers.old.send.Player_Disconnect, [self.playerCode])

    def sendPlayerDied(self):
        self.room.sendAll(Identifiers.old.send.Player_Died, [self.playerCode, self.playerScore])
        self.hasCheese = False

        if self.room.getAliveCount() < 1 or self.room.catchTheCheeseMap or self.isAfk:
            self.canShamanRespawn = False

        if ((self.room.checkIfTooFewRemaining() and not self.canShamanRespawn) or (self.room.checkIfShamanIsDead() and not self.canShamanRespawn) or (self.room.checkIfDoubleShamansAreDead())):
            self.room.send20SecRemainingTimer()

        if self.canShamanRespawn:
            self.isDead = False
            self.isAfk = False
            self.hasCheese = False
            self.hasEnter = False
            self.canShamanRespawn = False
            self.playerStartTimeMillis = time.time()
            self.room.sendAll(Identifiers.send.Player_Respawn, ByteArray().writeBytes(self.getPlayerData()).writeBoolean(False).writeBoolean(True).toByteArray())
            for player in self.room.clients.copy().values():
                player.sendShamanCode(self.playerCode, 0)

            if self.room.luaRuntime != None:
                self.room.luaRuntime.emit("PlayerRespawn", (self.playerName))

        if self.room.luaRuntime != None:
            self.room.luaRuntime.emit("PlayerDied", (self.playerName))

    def sendConjurationDestroy(self, x, y):
        self.room.sendAll(Identifiers.old.send.Conjuration_Destroy, [x, y])

    def sendGiveCheese(self, distance=-1):
        if distance != -1 and distance != 1000 and not self.room.catchTheCheeseMap and self.room.countStats:
            if distance >= 30:
                self.isSuspect = True

        self.room.canChangeMap = False
        if not self.hasCheese:
            self.room.sendAll(Identifiers.send.Player_Get_Cheese, ByteArray().writeInt(self.playerCode).writeBoolean(True).toByteArray())
            self.hasCheese = True

            self.room.numGetCheese += 1
            if self.room.currentMap in range(108, 114):
                if self.room.numGetCheese >= 10:
                    self.room.killShaman()

            if self.room.isTutorial:
                self.sendPacket(Identifiers.send.Tutorial, 1)
        self.room.canChangeMap = True

        if self.room.luaRuntime != None:
            self.room.luaRuntime.emit("PlayerGetCheese", (self.playerName))

    def playerWin(self, holeType, distance=-1):
        if distance != -1 and distance != 1000 and self.isSuspect and self.room.countStats:
            if distance >= 30:
                self.server.sendStaffMessage(7, "[<V>ANTI-HACK</V>][<J>%s</J>][<V>%s</V>] Instant win detected." %(self.ipAddress, self.playerName))
                self.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, "Instant win detected."])
                self.transport.close()
                return

        timeTaken = int((time.time() - (self.playerStartTimeMillis if self.room.autoRespawn else self.room.gameStartTimeMillis)) * 100)
        if timeTaken > 5:
            self.room.canChangeMap = False
            canGo = self.room.checkIfShamanCanGoIn() if self.isShaman else True
            if not canGo:
                self.sendSaveRemainingMiceMessage()

            if self.isDead or not self.hasCheese and not self.isOpportunist:
                canGo = False

            if self.room.isTutorial:
                self.sendPacket(Identifiers.send.Tutorial, 2)
                self.hasCheese = False
                self.server.loop.call_later(10, lambda: self.startBulle(self.server.recommendRoom(self.langue)))
                self.sendRoundTime(10)
                return

            if self.room.isEditor:
                if not self.room.EMapValidated and self.room.EMapCode != 0:
                    self.room.EMapValidated = True
                    self.sendPacket(Identifiers.old.send.Map_Validated, [""])

            if canGo:
                self.isDead = True
                self.hasCheese = False
                self.hasEnter = True
                self.room.numCompleted += 1
                place = self.room.numCompleted
                if self.room.isDoubleMap:
                    if holeType == 1:
                        self.room.FSnumCompleted += 1
                    elif holeType == 2:
                        self.room.SSnumCompleted += 1
                    else:
                        self.room.FSnumCompleted += 1
                        self.room.SSnumCompleted += 1

                self.currentPlace = place

                if place == 1:
                    self.playerScore += (4 if self.room.isRacing else 16) if not self.room.noAutoScore else 0
                    if self.room.getPlayerCountUnique() >= self.server.leastMice and self.room.countStats and not self.isShaman and not self.canShamanRespawn:
                        self.firstCount += Config.firstCount

                        if self.room.getPlayerCountUnique() >= self.server.leastMice and self.firstCount in self.server.firstTitleList:
                            title = self.server.firstTitleList[self.firstCount]
                            self.checkAndRebuildTitleList("first")
                            self.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
                            self.sendCompleteTitleList()
                            self.sendTitleList()
                    
                    if self.room.isRacing and self.room.getPlayerCountUnique() >= 4:#srec
                        self.room.CursorMaps.execute("select Player, Time from maps where Code = ?", [self.room.mapCode])
                        rs = self.room.CursorMaps.fetchone()
                        if int(rs[1]) > timeTaken or int(rs[1]) == 0:
                            t = float(timeTaken / 100.0 if timeTaken > 100 else timeTaken / 10.0)
                            self.room.CursorMaps.execute("update maps set Player = ?, Time = ? where Code = ?", [self.playerID, timeTaken, self.room.mapCode])
                            for player in self.room.clients.copy().values():
                                if player.langueID == 3:
                                    player.sendMessage(f"<V>{self.playerName}</V> bateu o recorde deste mapa (<J>{t}</J>s)")
                                else: player.sendMessage(f"<V>{self.playerName}</V> broken the record (<J>{t}</J>s)")

                elif place == 2:
                    self.playerScore += (3 if self.room.isRacing else 14) if not self.room.noAutoScore else 0
                elif place == 3:
                    self.playerScore += (2 if self.room.isRacing else 12) if not self.room.noAutoScore else 0
                else:
                    self.playerScore += (1 if self.room.isRacing else 10) if not self.room.noAutoScore else 0

                if self.room.isMulodrome:
                    if self.playerName in self.room.redTeam:
                        self.room.redCount += 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1
                    elif self.playerName in self.room.blueTeam:
                        self.room.blueCount += 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1
                    self.room.sendMulodromeRound()

                if self.room.isDefilante:
                    if not self.room.noAutoScore: self.playerScore += self.defilantePoints

                if self.room.getPlayerCountUnique() >= 2 and self.room.countStats and not self.room.isBootcamp:
                    if self.playerCode == self.room.currentShamanCode or self.playerCode == self.room.currentSecondShamanCode:
                        self.shamanCheeses += Config.cheeseCount
                    else:
                        self.cheeseCount += Config.cheeseCount

                        count = 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1
                        self.shopCheeses += count
                        self.shopFraises += count

                        self.sendGiveCurrency(0, count)
                        self.parseSkill.earnExp(False, 20)

                        if self.cheeseCount in self.server.cheeseTitleList:
                            title = self.server.cheeseTitleList[self.cheeseCount]
                            self.checkAndRebuildTitleList("cheese")
                            self.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
                            self.sendCompleteTitleList()
                            self.sendTitleList()

                elif self.room.getPlayerCountUnique() >= self.server.leastMice and self.room.isBootcamp:
                    self.bootcampCount += Config.bootcampCount

                    if self.bootcampCount in self.server.bootcampTitleList:
                        title = self.server.bootcampTitleList[self.bootcampCount]
                        self.checkAndRebuildTitleList("bootcamp")
                        self.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
                        self.sendCompleteTitleList()
                        self.sendTitleList()

                self.room.giveShamanSave(self.room.currentSecondShamanName if holeType == 2 and self.room.isDoubleMap else self.room.currentShamanName, 0)
                if self.room.currentShamanType != 0:
                    self.room.giveShamanSave(self.room.currentShamanName, self.room.currentShamanType)

                if self.room.currentSecondShamanType != 0:
                    self.room.giveShamanSave(self.room.currentSecondShamanName, self.room.currentSecondShamanType)

                self.sendPlayerWin(place, timeTaken)
                if self.room.luaRuntime != None:
                    self.room.luaRuntime.emit("PlayerWon", (self.playerName, str((time.time() - self.room.gameStartTimeMillis)*1000)[5:], str((time.time() - self.playerStartTimeMillis)*1000)[5:]))

                if self.room.mapCode == 2018:
                    self.sendGiveConsumables(2257, random.randint(10, 15))

                if self.room.getPlayerCount() >= 2 and self.room.checkIfTooFewRemaining() and not self.room.isDoubleMap:
                    enterHole = False
                    for player in self.room.clients.copy().values():
                        if player.isShaman and player.isOpportunist:
                            player.isOpportunist = True
                            player.playerWin(0)
                            enterHole = True
                            break
                    self.room.checkChangeMap()
                else:
                    self.room.checkChangeMap()

            self.room.canChangeMap = True
        else:
            self.isDead = True
            self.sendPlayerDied()

    def sendSaveRemainingMiceMessage(self):
        self.sendPacket(Identifiers.old.send.Save_Remaining, [])

    def sendGiveCurrency(self, type, count):
        self.sendPacket(Identifiers.send.Give_Currency, ByteArray().writeByte(type).writeByte(count).toByteArray())

    def sendPlayerWin(self, place, timeTaken):
        self.room.sendAll(Identifiers.send.Player_Win, ByteArray().writeByte(1 if self.room.isDefilante else (2 if self.playerName in self.room.blueTeam else 3 if self.playerName in self.room.blueTeam else 0)).writeInt(self.playerCode).writeShort(self.playerScore).writeByte(255 if place >= 255 else place).writeShort(65535 if timeTaken >= 65535 else timeTaken).toByteArray())
        self.hasCheese = False

    def sendCompleteTitleList(self):
        self.titleList = []
        self.titleList.append(0.1)
        self.titleList.extend(self.shopTitleList)
        self.titleList.extend(self.firstTitleList)
        self.titleList.extend(self.cheeseTitleList)
        self.titleList.extend(self.shamanTitleList)
        self.titleList.extend(self.bootcampTitleList)
        self.titleList.extend(self.hardModeTitleList)
        self.titleList.extend(self.divineModeTitleList)
        self.titleList.extend(self.specialTitleList)

        if self.privLevel.includes(10) and not self.privLevel.includes(12):
            self.titleList.extend([440.9, 442.9, 444.9, 445.9, 446.9, 447.9, 448.9, 449.9, 450.9, 451.9, 452.9, 453.9])

    def sendTitleList(self):
        self.sendPacket(Identifiers.old.send.Titles_List, [self.titleList])

    def sendUnlockedTitle(self, title, stars):
        self.room.sendAll(Identifiers.old.send.Unlocked_Title, [self.playerCode, title, stars])

    def sendMessage(self, message):
        self.sendPacket(Identifiers.send.Message, ByteArray().writeUTF(message).toByteArray())

    def sendClientMessage(self, message, tab=False):
        self.sendPacket(Identifiers.send.Recv_Message, ByteArray().writeBoolean(tab).writeUTF(message).writeByte(0).writeUTF("").toByteArray())

    def sendProfile(self, playerName):
        if "#" in playerName:
            playerName = playerName.split("#")[0]

        player = self.server.players.get(playerName)
        if player != None and not player.isGuest:
            priv = player.privLevel.uppermost()
            colour = int(player.nameColor, 16) if player.nameColor != "" and player.privLevel.uppermost() > 8 else int(self.server.privileges['colors'][player.privLevel.uppermost()], 16)#int({1:"009C9C", 2:"009C9C", 3:"009C9C", 4:"09e609", 5:"FE8446", 6:"0074DF", 7:"B9BC2E", 8:"FFC000", 9:"DF013A", 10:"EA1C50", 11:"ff0d00"}[player.privLevel.uppermost()], 16)
            packet = ByteArray().writeUTF(player.playerName + player.playerTag).writeInt(player.playerID).writeInt(str(player.regDate)[:10])
            packet.writeInt(colour).writeByte(player.gender).writeUTF(player.tribeName).writeUTF(player.marriage)

            for stat in [player.shamanSaves, player.shamanCheeses, player.firstCount, player.cheeseCount, player.hardModeSaves, player.bootcampCount, player.divineModeSaves]:
                packet.writeInt(stat)

            packet.writeShort(player.titleNumber).writeShort(len(player.titleList))
            for title in player.titleList:
                packet.writeShort(int(title - (title % 1)))
                packet.writeByte(int(round((title % 1) * 10)))

            packet.writeUTF(((str(player.fur) + ";" + player.playerLook.split(";")[1]) if player.fur != 0 else player.playerLook) + ";" + player.mouseColor)
            packet.writeShort(player.shamanLevel)

            badges = list(map(int, player.shopBadges))
            listBadges = []
            for badge in badges:
                if not badge in listBadges:
                    listBadges.append(badge)

            packet.writeShort(len(listBadges) * 2)
            for badge in listBadges:
                packet.writeShort(badge).writeShort(badges.count(badge))

            stats = [[30, player.racingStats[0], 1500, 124], [31, player.racingStats[1], 10000, 125], [33, player.racingStats[2], 10000, 127], [32, player.racingStats[3], 10000, 126], [26, player.survivorStats[0], 1000, 120], [27, player.survivorStats[1], 800, 121], [28, player.survivorStats[2], 20000, 122], [29, player.survivorStats[3], 10000, 123], [42, player.defilanteStats[0], 1500, 288], [43, player.defilanteStats[1], 10000, 287], [44, player.defilanteStats[2], 100000, 286]]
            packet.writeByte(len(stats))
            for stat in stats:
                packet.writeByte(stat[0]).writeInt(stat[1]).writeInt(stat[2]).writeShort(stat[3])

            shamanBadges = player.shamanBadges
            packet.writeByte(player.equipedShamanBadge).writeByte(len(shamanBadges))

            for shamanBadge in shamanBadges:
                packet.writeByte(shamanBadge)

            self.sendPacket(Identifiers.send.Profile, packet.writeBoolean(True).writeInt(0).toByteArray())

    def sendPlayerBan(self, hours, reason, silent):
        self.sendPacket(Identifiers.old.send.Player_Ban, [hours * 3600000, reason])
        if not silent and self.room != None:
            for player in self.room.clients.copy().values():
                player.sendLangueMessage("", "<ROSE>• [Moderation] $Message_Ban", self.playerName, str(hours), reason)
        self.server.disconnectIPAddress(self.ipAddress)

    def sendPlayerEmote(self, emoteID, flag, others, lua):
        packet = ByteArray().writeInt(self.playerCode).writeByte(emoteID)
        if not flag == "": packet.writeUTF(flag)
        self.room.sendAllOthers(self, Identifiers.send.Player_Emote, packet.writeBoolean(lua).toByteArray()) if others else self.room.sendAll(Identifiers.send.Player_Emote, packet.writeBoolean(lua).toByteArray())

    def sendEmotion(self, emotion):
        self.room.sendAllOthers(self, Identifiers.send.Emotion, ByteArray().writeInt(self.playerCode).writeByte(emotion).toByteArray())

    def sendPlaceObject(self, objectID, code, px, py, angle, vx, vy, dur, sendAll):
        packet = ByteArray()
        packet.writeInt(objectID)
        packet.writeShort(code)
        packet.writeShort(px)
        packet.writeShort(py)
        packet.writeShort(angle)
        packet.writeByte(vx)
        packet.writeByte(vy)
        packet.writeBoolean(dur)
        if self.isGuest or sendAll:
            packet.writeByte(0)
        else:
            packet.writeBytes(self.parseShop.getShamanItemCustom(code))

        if not sendAll:
            self.room.sendAllOthers(self, Identifiers.send.Spawn_Object, packet.toByteArray())
            self.room.objectID = objectID
        else:
            self.room.sendAll(Identifiers.send.Spawn_Object, packet.toByteArray())

    def sendTotem(self, totem, x, y, playerCode):
        self.sendPacket(Identifiers.old.send.Totem, ["%s#%s#%s%s" %(playerCode, x, y, totem)])

    def sendTotemItemCount(self, number):
        if self.room.isTotemEditor:
            self.sendPacket(Identifiers.send.Totem_Item_Count, ByteArray().writeShort(number * 2).toByteArray())

    def initTotemEditor(self):
        if self.resetTotem:
            self.sendTotemItemCount(0)
            self.resetTotem = False
        else:
            if not self.totem[1] == "":
                self.tempTotem[0] = self.totem[0]
                self.tempTotem[1] = self.totem[1]
                self.sendTotemItemCount(self.tempTotem[0])
                self.sendTotem(self.tempTotem[1], 400, 204, self.playerCode)
            else:
                self.sendTotemItemCount(0)

    def sendShamanType(self, mode, canDivine):
        self.sendPacket(Identifiers.send.Shaman_Type, ByteArray().writeByte(mode).writeBoolean(canDivine).writeInt(int(self.shamanColor, 16)).toByteArray())
        
    def sendBanConsideration(self):
        self.sendPacket(Identifiers.old.send.Ban_Consideration, ["0"])

    def loadCafeMode(self):
        can = self.privLevel.upper(1)
        if not can:
            self.sendLangueMessage("", "<ROSE>$PasAutoriseParlerSurServeur")
        self.sendPacket(Identifiers.send.Open_Cafe, ByteArray().writeBoolean(can).toByteArray())

        packet = ByteArray().writeBoolean(True)
        self.CursorCafe.execute("select * from cafetopics order by Date desc limit 0, 20")
        for rs in self.CursorCafe.fetchall():
            packet.writeInt(rs["TopicID"]).writeUTF(rs["Title"]).writeInt(self.server.getPlayerID(rs["Author"])).writeInt(rs["Posts"]).writeUTF(rs["LastPostName"]).writeInt(Utils.getSecondsDiff(rs["Date"]))
        self.sendPacket(Identifiers.send.Cafe_Topics_List, packet.toByteArray())
        self.warns() 
    
    def warns(self):
        self.CursorCafe.execute("select * from cafeposts where status = 2 and name = ? order by postid asc", [self.playerName])
        self.sendPacket([144, 11], ByteArray().writeShort(len(self.CursorCafe.fetchall())).toByteArray())
    
    def check(self, s):
        if self.privLevel.uppermost() < 7:
            return 0
        else:
            self.CursorCafe.execute("select count(*) as count from cafeposts where TopicID = ? and Status = 0", [s])
            return int(self.CursorCafe.fetchone()["count"])

    def openCafeTopic(self, topicID):
        packet = ByteArray().writeBoolean(True).writeInt(topicID).writeBoolean(self.check(topicID) != 0).writeBoolean(True)
        self.CursorCafe.execute("select * from cafeposts where TopicID = ? order by PostID asc", [topicID])
        for rs in self.CursorCafe.fetchall():
            if rs["Status"] != 2 or self.privLevel.uppermost() >= 7 or rs["Name"] == self.playerName:
                if self.privLevel.uppermost() >= 7 and rs["Status"] == 0:
                    packet.writeInt(rs["PostID"]).writeInt(self.server.getPlayerID(rs["Name"])).writeInt(Utils.getSecondsDiff(rs["Date"])).writeUTF(rs["Name"]).writeUTF(rs["Post"]).writeBoolean(str(self.playerCode) not in rs["Votes"].split(",")).writeShort(rs["Points"]).writeUTF(rs["ModeratedBY"]).writeByte(rs["Status"])
                    self.chec = rs["PostID"]
                    break
                elif not rs["Status"] == 0:
                    packet.writeInt(rs["PostID"]).writeInt(self.server.getPlayerID(rs["Name"])).writeInt(Utils.getSecondsDiff(rs["Date"])).writeUTF(rs["Name"]).writeUTF(rs["Post"]).writeBoolean(str(self.playerCode) not in rs["Votes"].split(",")).writeShort(rs["Points"]).writeUTF(rs["ModeratedBY"]).writeByte(rs["Status"])
        self.lastTopicID = topicID          
        self.sendPacket(Identifiers.send.Open_Cafe_Topic, packet.toByteArray())

    def createNewCafeTopic(self, title, message):
        if not self.server.checkMessage(self, title):
            self.CursorCafe.execute("insert into cafetopics values (null, ?, ?, '', 0, ?, ?)", [title, self.playerName, Utils.getTime(), self.langue])
            self.createNewCafePost(self.CursorCafe.lastrowid, message)
        self.loadCafeMode()
    
    def MessageType(self, topicID, status):
        if status:
            self.CursorCafe.execute("update cafeposts set Status = 2, ModeratedBY = ? where PostID = ?", [self.playerName, self.chec])
            self.chec = 0
            self.openCafeTopic(topicID)
        else:
            self.CursorCafe.execute("update cafeposts set Status = 1, ModeratedBY = ? where PostID = ?", [self.playerName, self.chec])
            self.chec = 0
            self.openCafeTopic(topicID)

    def createNewCafePost(self, topicID, message):
        commentsCount = 0
        if topicID == 0:
            topicID = self.lastTopicID
        if not self.server.checkMessage(self, message):
            self.CursorCafe.execute("insert into cafeposts values (null, ?, ?, ?, ?, 0, ?, '', 0)", [topicID, self.playerName, message, Utils.getTime(), self.playerCode])
            self.CursorCafe.execute("update cafetopics set LastPostName = ?, Posts = Posts + 1, Date = ? where TopicID = ?", [self.playerName, Utils.getTime(), topicID])
            self.CursorCafe.execute("select count(*) as count from CafePosts where TopicID = ?", [topicID])
            rs = self.CursorCafe.fetchone()
            commentsCount = rs["count"]
            self.openCafeTopic(topicID)
            for player in self.server.players.copy().values():
                if player.isCafe:
                    player.sendPacket(Identifiers.send.Cafe_New_Post, ByteArray().writeInt(topicID).writeUTF(self.playerName).writeInt(commentsCount).toByteArray())

    def voteCafePost(self, topicID, postID, mode):
        points = 0
        votes = ""

        self.CursorCafe.execute("select Points, Votes from cafeposts where TopicID = ? and PostID = ?", [topicID, postID])
        rs = self.CursorCafe.fetchone()
        if rs:
            points = rs["Points"]
            votes = rs["Votes"]

        votes += str(self.playerID) if votes == "" else "," + str(self.playerID)
        if mode:
            points += 1
        else:
            points -= 1

        self.CursorCafe.execute("update cafeposts set Points = ?, Votes = ? where TopicID = ? and PostID = ?", [points, votes, topicID, postID])
        self.openCafeTopic(topicID)

    def deleteCafePost(self, topicID, postID):
        self.CursorCafe.execute("delete from cafeposts where TopicID = ? and PostID = ?", [topicID, postID])
        self.sendPacket(Identifiers.send.Delete_Cafe_Message, ByteArray().writeInt(topicID).writeInt(postID).toByteArray())
        self.openCafeTopic(topicID)

    def deleteAllCafePost(self, topicID, playerName):
        self.CursorCafe.execute("delete from cafeposts where TopicID = ? and Name = ?", [topicID, playerName])
        self.CursorCafe.execute("delete from cafetopics where TopicID = ?", [topicID])
        self.loadCafeMode()
        self.openCafeTopic(topicID)

    def sendLangueMessage(self, community, message, *args):
        packet = ByteArray().writeUTF(community).writeUTF(message).writeByte(len(args))
        for arg in args:
            packet.writeUTF(arg)
        self.sendPacket(Identifiers.send.Message_Langue, packet.toByteArray())
    
    def sendLangueMessageAll(self, community, message, *args):
        packet = ByteArray().writeUTF(community).writeUTF(message).writeByte(len(args))
        for arg in args:
            packet.writeUTF(arg)
        self.room.sendAll(Identifiers.send.Message_Langue, packet.toByteArray())

    def sendModMute(self, playerName, hours, reason, only):
        if not only:
            self.sendLangueMessageAll("", "<ROSE>• [Moderation] $MuteInfo2", playerName, hours, reason)
        else:
            player = self.server.players.get(playerName)
            if player:
                player.sendLangueMessage("", "<ROSE>• [Moderation] $MuteInfo1", hours, reason)

    def sendVampireMode(self, others):
        self.isVampire = True
        packet = ByteArray().writeInt(self.playerCode).writeInt(-1)
        if others:
            self.room.sendAllOthers(self, Identifiers.send.Vampire_Mode, packet.toByteArray())
        else:
            self.room.sendAll(Identifiers.send.Vampire_Mode, packet.toByteArray())
        if self.room.luaRuntime != None:
            self.room.luaRuntime.emit("PlayerVampire", (self.playerName))

    def sendRemoveCheese(self):
        self.room.sendAll(Identifiers.send.Remove_Cheese, ByteArray().writeInt(self.playerCode).toByteArray())

    def sendLuaMessage(self, message):
        self.sendPacket(Identifiers.send.Lua_Message, ByteArray().writeUTF(message).toByteArray())

    def sendGameMode(self, mode):
        mode = 1 if mode == 0 else mode
        types = [1, 3, 8, 9, 2, 10, 18, 16]
        packet = ByteArray().writeByte(len(types))
        for roomType in types:
            packet.writeByte(roomType)

        packet.writeByte(mode)
        modeInfo = self.server.getPlayersCountMode(mode, "all")
        if not modeInfo[0] == "":
            packet.writeByte(1).writeUTF(self.langue.lower()).writeUTF(self.langue.lower()).writeUTF(str(modeInfo[0])).writeUTF(str(modeInfo[1])).writeUTF("mjj").writeUTF("1")
            roomsCount = 0
            for checkRoom in self.server.rooms.values():
                if ({1:checkRoom.isNormRoom, 3:checkRoom.isVanilla, 8:checkRoom.isSurvivor, 9:checkRoom.isRacing, 2:checkRoom.isBootcamp, 10:checkRoom.isDefilante, 16:checkRoom.isVillage}[mode]):
                    roomsCount += 1
                    packet.writeByte(0).writeUTF(self.langue.lower()).writeUTF(self.langue.lower()).writeUTF(checkRoom.roomName).writeShort(checkRoom.getPlayerCount()).writeByte(checkRoom.maxPlayers).writeBoolean(checkRoom.isFuncorp)

            if roomsCount == 0:
                packet.writeByte(0).writeUTF(self.langue.lower()).writeUTF(self.langue.lower()).writeUTF(("" if mode == 1 else str(modeInfo[0].split(" ")[1])) + "1").writeShort(0).writeByte(200).writeBoolean(False)
        else:
            minigamesList = {}
            minigames = []
            roomsList = {}
            for minigame in self.server.minigames.keys():
                minigames.append("#" + minigame)
            for minigame in minigames:
                minigamesList[minigame] = 0
                for checkRoom in self.server.rooms.values():
                    if checkRoom.roomName.startswith(minigame):
                        minigamesList[minigame] += checkRoom.getPlayerCount()
                    if checkRoom.roomName.startswith(minigame):
                        roomsList[checkRoom.roomName] = [checkRoom.getPlayerCount(), checkRoom.maxPlayers, checkRoom.isFuncorp]
            for minigame, count in minigamesList.items():
                packet.writeByte(1).writeUTF(self.langue.lower()).writeUTF(self.langue.lower()).writeUTF(str(minigame)).writeUTF(str(count)).writeUTF("mjj").writeUTF(minigame)
            for minigame, count in roomsList.items():
                packet.writeByte(0).writeUTF(self.langue.lower()).writeUTF(self.langue.lower()).writeUTF(minigame).writeShort(count[0]).writeByte(count[1]).writeBoolean(count[2])
           
        if mode == 16:
              modeInfo = self.server.getPlayersCountMode(19, "all")
              if not modeInfo[0] == "":
                     #packet.writeByte(1).writeByte(self.langueID).writeUTF("").writeUTF("").writeUTF("mjj").writeUTF("1")
                     roomsCount = 0
                     for checkRoom in self.server.rooms.values():
                         if checkRoom.roomName.startswith("#village+") and roomsCount == 0:
                              roomsCount += 1
                              packet.writeByte(0).writeUTF(self.langue.lower()).writeUTF(self.langue.lower()).writeUTF(str(modeInfo[0].split(" ")[1])).writeShort(checkRoom.getPlayerCount()).writeByte(checkRoom.maxPlayers).writeBoolean(checkRoom.isFuncorp)

                     if roomsCount == 0:
                           packet.writeByte(0).writeUTF(self.langue.lower()).writeUTF(self.langue.lower()).writeUTF(str(modeInfo[0].split(" ")[1])).writeShort(0).writeByte(200).writeBoolean(False)



        self.sendPacket(Identifiers.send.Game_Mode, packet.toByteArray())

    def sendMusicVideo(self, sendAll):
        music = self.room.musicVideos[0]
        packet = ByteArray().writeUTF(str(music["VideoID"].encode("UTF-8"))).writeUTF(str(music["Title"].encode("UTF-8"))).writeShort(self.room.musicTime).writeUTF(str(music["By"].encode("UTF-8")))
        if sendAll:
            self.room.sendAll(Identifiers.send.Music_Video, packet.toByteArray())
        else:
            self.sendPacket(Identifiers.send.Music_Video, packet.toByteArray())

    def checkMusicSkip(self):
        if self.room.isMusic and self.room.isPlayingMusic:
            count = self.room.getPlayerCount()
            count = count if count % 2 == 0 else count + 1
            if self.room.musicSkipVotes == count // 2:
                self.room.musicVideos.remove(0)
                self.sendMusicVideo(True)

    def sendStaffMessage(self, message, othersLangues, tab=False):
        for player in self.server.players.copy().values():
            if othersLangues or player.langue == self.langue:
                player.sendClientMessage(message, tab)

    def checkVip(self, vipTime):
        seconds = abs(Utils.getSecondsDiff(vipTime))
        if self.vipTimer != None:
            self.vipTimer.cancel()
        if seconds > 0:
            self.vipTimer = self.server.loop.call_later(seconds, lambda: self.checkVip(vipTime - seconds))
        if self.privLevel.notin(2):
            self.privLevel.append(2)

        if seconds < 0:
            self.titleNumber = 0
            self.sendMessage("<R>Your VIP membership has been expired.")
        else:
            days = seconds // 86400
            hours = seconds // 3600
            minutes = seconds // 60
            self.sendMessage(f"<N>Your VIP membership expires in <V>{days}</V> days <V>{hours}</V> hours <V>{minutes}</V> minutes.")

    def sendBulle(self):
        self.sendPacket(Identifiers.send.Bulle, ByteArray().writeInt(0).writeUTF("x").toByteArray())

    def sendLogMessage(self, message):
        self.sendPacket(Identifiers.send.Log_Message, ByteArray().writeUTF("").writeInt(len(message)).writeBytes(message).toByteArray())

    def runLuaScript(self, script):
        try:
            pythonScript = compile(str(script), "<string>", "exec")
            exec(pythonScript)
            totalTime = int(time.time() - time.time())
            self.sendLuaMessage("<V>[%s]<BL> [%s] %s" %(self.room.roomName, self.playerName, "Lua script not loaded. (%s ms - 4000 max)" %(totalTime) if totalTime > 4000 else "Lua script loaded in %s ms (4000 max)" %(totalTime)))
        except Exception as error:
            self.sendLuaMessage("<V>[%s]<BL> [%s][<R>Exception</R>]: %s" %(self.room.roomName, self.playerName, error))
        else:
            self.server.sendStaffMessage(5, "[<V>Lua<BL>][<J>%s<BL>][<R>%s<BL>][<J>%s-%s</J>] Used Lua." %(self.ipAddress, self.playerName, self.langue.upper(), self.room.roomName))

    def sendAnimZelda(self, type, item=0, case="", id=0):
        packet = ByteArray().writeInt(self.playerCode).writeByte(type)
        if type == 7:
            packet.writeUTF(case).writeByte(id)
        elif type == 5:
            packet.writeUTF(case)
        else:
            packet.writeInt(item)
        self.room.sendAll(Identifiers.send.Anim_Zelda, packet.toByteArray())
   
    def sendAnimZeldaInventory(self, type, item=0, case="", id=0):
        packet = ByteArray().writeInt(self.playerCode).writeByte(type)
        if type == 7:
            packet.writeUTF(case).writeByte(id)
        elif type == 5:
            packet.writeUTF(case)
        else:
            packet.writeInt(item)
        self.room.sendAll(Identifiers.send.Anim_Zelda, packet.toByteArray())


    def sendInventoryConsumables(self):
        inventory = []
        for consumable in self.playerConsumables.items():
            if str(consumable[0]) in self.server.inventoryConsumables:
                obj = self.server.inventoryConsumables[str(consumable[0])]
                if not "hide" in obj:
                    inventory.append([consumable[0], consumable[1], obj["sort"], not "blockUse" in obj, not "launchlable" in obj, obj["img"] if "img" in obj else "", self.equipedConsumables.index(consumable[0]) + 1 if consumable[0] in self.equipedConsumables else 0])
            else:
                inventory.append([consumable[0], consumable[1], 1, False, True, "", self.equipedConsumables.index(consumable[0]) + 1 if consumable[0] in self.equipedConsumables else 0])

        data = ByteArray()
        data.writeShort(len(inventory))
        for consumable in inventory:
            data.writeShort(int(consumable[0]))
            data.writeByte(255 if int(consumable[1]) > 255 else int(consumable[1]))
            data.writeByte(int(consumable[2]))
            data.writeBoolean(True)
            data.writeBoolean(bool(consumable[3]))
            data.writeBoolean(bool(consumable[3]))
            data.writeBoolean(not bool(consumable[3]))
            data.writeBoolean(bool(consumable[4]))
            data.writeBoolean(False)
            data.writeBoolean(str(consumable[5]) != "")
            if str(consumable[5]) != "":
                data.writeUTF(str(consumable[5]))

            data.writeByte(int(consumable[6]))
        self.sendPacket(Identifiers.send.Inventory, data.toByteArray())
    def updateInventoryConsumable(self, id, count):
        self.sendPacket(Identifiers.send.Update_Inventory_Consumable, ByteArray().writeShort(id).writeByte(count).toByteArray())

    def useInventoryConsumable(self, id):
        if id in [29, 30, 2241, 2330]:
            self.sendPacket(Identifiers.send.Use_Inventory_Consumable, ByteArray().writeInt(self.playerCode).writeShort(id).toByteArray())
        else:
            self.room.sendAll(Identifiers.send.Use_Inventory_Consumable, ByteArray().writeInt(self.playerCode).writeShort(id).toByteArray())

    def sendTradeResult(self, playerName, result):
        self.sendPacket(Identifiers.send.Trade_Result, ByteArray().writeUTF(playerName).writeByte(result).toByteArray())

    def sendTradeInvite(self, playerCode):
        self.sendPacket(Identifiers.send.Trade_Invite, ByteArray().writeInt(playerCode).toByteArray())

    def sendTradeStart(self, playerCode):
        self.sendPacket(Identifiers.send.Trade_Start, ByteArray().writeInt(playerCode).toByteArray())

    def tradeInvite(self, playerName):
        player = self.room.clients.get(playerName)
        if player != None and (not self.ipAddress == player.ipAddress or self.privLevel.includes(10) or player.privLevel.includes(10)) and self.privLevel.notin(0) and player.privLevel.notin(0):
            if not player.isTrade:
                if not player.room.name == self.room.name:
                    self.sendTradeResult(playerName, 3)
                elif player.isTrade:
                    self.sendTradeResult(playerName, 0)
                else:
                    self.sendLangueMessage("", "$Demande_Envoyée")
                    player.sendTradeInvite(self.playerCode)

                self.tradeName = playerName
                self.isTrade = True
            else:
                self.tradeName = playerName
                self.isTrade = True
                self.sendTradeStart(player.playerCode)
                player.sendTradeStart(self.playerCode)

    def cancelTrade(self, playerName):
        player = self.room.clients.get(playerName)
        if player != None:
            self.tradeName = ""
            self.isTrade = False
            self.tradeConsumables = {}
            self.tradeConfirm = False
            player.tradeName = ""
            player.isTrade = False
            player.tradeConsumables = {}
            player.tradeConfirm = False
            player.sendTradeResult(self.playerName, 2)

    def tradeAddConsumable(self, id, isAdd):
        player = self.room.clients.get(self.tradeName)
        if player != None and player.isTrade and player.tradeName == self.playerName and str(id) in self.server.inventoryConsumables and not "blockTrade" in self.server.inventoryConsumables[str(id)]:
            if isAdd:
                if id in self.tradeConsumables:
                    self.tradeConsumables[id] += 1
                else:
                    self.tradeConsumables[id] = 1
            else:
                count = self.tradeConsumables[id] - 1
                if count > 0:
                    self.tradeConsumables[id] = count
                else:
                    del self.tradeConsumables[id]

            player.sendPacket(Identifiers.send.Trade_Add_Consumable, ByteArray().writeBoolean(False).writeShort(id).writeBoolean(isAdd).writeByte(1).writeBoolean(False).toByteArray())
            self.sendPacket(Identifiers.send.Trade_Add_Consumable, ByteArray().writeBoolean(True).writeShort(id).writeBoolean(isAdd).writeByte(1).writeBoolean(False).toByteArray())

    def tradeResult(self, isAccept):
        player = self.room.clients.get(self.tradeName)
        if player != None and player.isTrade and player.tradeName == self.playerName:
            self.tradeConfirm = isAccept
            player.sendPacket(Identifiers.send.Trade_Confirm, ByteArray().writeBoolean(False).writeBoolean(isAccept).toByteArray())
            self.sendPacket(Identifiers.send.Trade_Confirm, ByteArray().writeBoolean(True).writeBoolean(isAccept).toByteArray())
            if self.tradeConfirm and player.tradeConfirm:
                for consumable in player.tradeConsumables.items():
                    if consumable[0] in self.playerConsumables:
                        self.playerConsumables[consumable[0]] += consumable[1]
                    else:
                        self.playerConsumables[consumable[0]] = consumable[1]

                    count = player.playerConsumables[consumable[0]] - consumable[1]
                    if count <= 0:
                        del player.playerConsumables[consumable[0]]
                        if consumable[0] in player.equipedConsumables:
                            player.equipedConsumables.remove(consumable[0])
                    else:
                        player.playerConsumables[consumable[0]] = count

                for consumable in self.tradeConsumables.items():
                    if consumable[0] in player.playerConsumables:
                        player.playerConsumables[consumable[0]] += consumable[1]
                    else:
                        player.playerConsumables[consumable[0]] = consumable[1]

                    count = self.playerConsumables[consumable[0]] - consumable[1]
                    if count <= 0:
                        del self.playerConsumables[consumable[0]]
                        if consumable[0] in self.equipedConsumables:
                            self.equipedConsumables.remove(consumable[0])
                    else:
                        self.playerConsumables[consumable[0]] = count

                player.tradeName = ""
                player.isTrade = False
                player.tradeConsumables = {}
                player.tradeConfirm = False
                player.sendPacket(Identifiers.send.Trade_Close)
                player.sendInventoryConsumables()
                self.tradeName = ""
                self.isTrade = False
                self.tradeConsumables = {}
                self.tradeConfirm = False
                self.sendPacket(Identifiers.send.Trade_Close)
                self.sendInventoryConsumables()

    def sendGiveConsumables(self, id, amount=80, limit=80):
        self.sendAnimZelda(4, id)
        self.sendNewConsumable(id, amount)
        amount, limit = int(amount), int(limit)
        sum = (self.playerConsumables[id] if id in self.playerConsumables else 0) + amount
        if limit != -1 and sum > limit: sum = limit
        if id in self.playerConsumables:
            self.playerConsumables[id] = sum
            self.updateInventoryConsumable(id, sum)
        else:
            self.playerConsumables[id] = sum
            self.updateInventoryConsumable(id, sum)

    def delPlayerConsumable(self, id, amount=1):
        try:
            self.playerConsumables[id] -= 1
        except:
            del self.playerConsumables[id]

    def sendNewConsumable(self, consumable, count):
        self.sendPacket(Identifiers.send.New_Consumable, ByteArray().writeByte(0).writeShort(consumable).writeShort(count).toByteArray())

    def getFullItemID(self, category, itemID):
        return itemID + 10000 + 1000 * category if (itemID >= 100) else itemID + 100 * category

    def getSimpleItemID(self, category, itemID):
        return itemID - 10000 - 1000 * category if (itemID >= 10000) else itemID - 100 * category

    def getItemInfo(self, category, itemID):
        test = self.server.shopListCheck
        test = test[f'{category}|{itemID}']
        return [category, itemID, 0, 1, 0, test[0], test[1], 0 if category == 22 else 20]
    def sendNpcs(self):
        npcs = self.server.npcs["NPC"]
        for npc in npcs.items():
            value = npc[1]
            self.spawnNPC(npc[0], value[0], value[1], value[2], value[3], value[4], value[5])

    def openNpcShop(self, npcName):
        npcShop = self.server.npcs["Shop"][npcName]
        self.lastNpc = npcName

        data = ByteArray()
        data.writeUTF(npcName)
        data.writeByte(len(npcShop))

        for item in npcShop:
            type, id, amount, four, priceItem, priceAmount = item
            if (type == 1 and id in self.shopBadges) or (type == 2 and id in self.shamanBadges) or (type == 3 and self.hasTitle(id)) or (type == 4 and id in self.playerConsumables and self.playerConsumables.get(id) + amount > 10000):
                data.writeByte(2)
            elif not priceItem in self.playerConsumables or self.playerConsumables.get(priceItem) < priceAmount:
                data.writeByte(1)
            else:
                data.writeByte(0)

            data.writeByte(type).writeShort(id).writeShort(amount).writeByte(four).writeShort(priceItem).writeShort(priceAmount).writeInt(0)
        self.sendPacket(Identifiers.send.NPC_Shop, data.toByteArray())

    def buyNPCItem(self, itemID):
        itemID += 1
        item = self.server.npcs["Shop"].get(self.lastNpc)[itemID]
        type, id, amount, four, priceItem, priceAmount = item

        if priceItem in self.playerConsumables and self.playerConsumables.get(priceItem) >= priceAmount:
            count = self.playerConsumables.get(priceItem) - priceAmount
            if count <= 0:
                del self.playerConsumables[priceItem]
            else:
                self.playerConsumables[priceItem] = count

            self.updateInventoryConsumable(priceItem, count)

            if type == 1:
                self.sendAnimZelda(3, id)
                self.parseShop.sendUnlockedBadge(id)
                self.shopBadges.append(id)

            elif type == 2:
                self.sendAnimZelda(6, id)
                self.shamanBadges.append(id)

            elif type == 3:
                self.titleList.append(id + 0.1)
                self.changeTitle(id)

            elif type == 4:
                self.addConsumable(id, amount)

            self.openNpcShop(self.lastNpc)

    def changeTitle(self, id):
        self.titleStars = 1
        self.titleNumber = id
        self.sendUnlockedTitle(id, 1)
        self.sendPacket(Identifiers.send.Change_Title, ByteArray().writeByte(self.gender).writeShort(self.titleNumber).toByteArray())

    def addConsumable(self, id, amount):
        self.sendNewConsumable(id, amount)
        self.sendAnimZelda(4, id)
        sum = amount + (self.playerConsumables.get(id) if id in self.playerConsumables else 0)
        self.playerConsumables[id] = sum
        self.updateInventoryConsumable(id, sum)

    def hasTitle(self, titleID):
        for title in self.titleList:
            if int(title - (title % 1)) == titleID:
                return True
        return False

    def duyuru(self, u, message, ftime=True, client=False, langue=False, tab=False):
        if not ftime:
            if client:
                self.sendClientMessage(message, tab)
            elif langue:
                self.sendLangueMessage("", message)
            else:
                self.sendClientMessage(message)
        self.server.loop.call_later(u, lambda: self.duyuru(u, message, False, client, langue, tab))

    def useConsumable(self, consumableID):
        if consumableID in self.playerConsumables and not self.isDead:
            if str(consumableID) in self.server.inventoryConsumables:
                obj = self.server.inventoryConsumables.get(str(consumableID))
                if "launchObject" in obj and not self.room.isRacing and not self.room.isBootcamp and not self.room.isSurvivor and not self.room.isDefilante and not self.room.disablePhysicalConsumables:
                    objectCode = obj["launchObject"]
                    if objectCode == 11:
                        self.room.objectID += 2
                    self.sendPlaceObject(self.room.objectID if consumableID == 11 else 0, objectCode, self.posX + 28 if self.isFacingRight else self.posX - 28, self.posY, 0, 0 if consumableID == 11 or objectCode == 24 else 10 if self.isFacingRight else -10, -3, True, True)

                if "pet" in obj:
                    if self.pet != 0:
                        return
                    else:
                        self.pet = obj["pet"]
                        self.petEnd = Utils.getTime() + 3600
                        self.room.sendAll(Identifiers.send.Pet, ByteArray().writeInt(self.playerCode).writeByte(self.pet).toByteArray())

                if "fur" in obj:
                    self.fur = obj["fur"]
                    self.furEnd = Utils.getTime() + 3600

                if "pencil" in obj:
                    self.sendPacket(Identifiers.send.Crazzy_Packet, ByteArray().writeByte(1).writeShort(650).writeInt(int(obj["pencil"], 16)).toByteArray())
                    self.drawingColor = int(obj["pencil"], 16)

                if consumableID == 10:
                    players = 0
                    playerz = list(self.room.clients.values())
                    for player in playerz:
                        if players < 5 and player != self:
                            if player.posX >= self.posX - 400 and player.posX <= self.posX + 400:
                                if player.posY >= self.posY - 300 and player.posY <= self.posY + 300:
                                    player.sendPlayerEmote(3, "", False, False)
                                    players += 1

                if consumableID == 11:
                    self.room.newConsumableTimer(self.room.lastObjectID)
                    self.isDead = True
                    if not self.room.noAutoScore:
                        self.playerScore += 1

                    self.sendPlayerDied()
                    self.room.checkChangeMap()

                if consumableID == 21:
                    self.sendPlayerEmote(12, "", False, False)

                if consumableID == 28:
                    self.parseSkill.sendBonfireSkill(self.posX, self.posY, 15)

                if consumableID == 33:
                    self.sendPlayerEmote(16, "", False, False)

                if consumableID == 35:
                    if len(self.shopBadges) == 0:
                        return
                    self.room.sendAll(Identifiers.send.Baloon_Badge, ByteArray().writeInt(self.playerCode).writeShort(random.choice(self.shopBadges)).toByteArray())

                if consumableID == 800:
                    self.shopCheeses += 100
                    self.sendAnimZelda(2, 0)
                    self.sendGiveCurrency(0, 100)

                if consumableID == 801:
                    self.shopFraises += 100
                    self.sendAnimZelda(2, 2)

                if consumableID == 2234:
                    self.sendPlayerEmote(20, "", False, False)
                    players = 0
                    playerz = list(self.room.clients.values())
                    for player in playerz:
                        if players < 5 and player != self:
                            if player.posX >= self.posX - 400 and player.posX <= self.posX + 400:
                                if player.posY >= self.posY - 300 and player.posY <= self.posY + 300:
                                    player.sendPlayerEmote(6, "", False, False)
                                    players += 1

                if consumableID == 2239:
                    self.room.sendAll(Identifiers.send.Crazzy_Packet, ByteArray().writeByte(4).writeInt(self.playerCode).writeInt(self.shopCheeses).toByteArray())

                if consumableID == 2246:
                    self.sendPlayerEmote(24, "", False, False)

                if consumableID == 2255:
                    self.sendAnimZelda(7, "$De6", random.randint(0, 6))

                if consumableID == 2259:
                    self.room.sendAll(Identifiers.send.Crazzy_Packet, ByteArray().writeByte(5).writeInt(self.playerCode).writeShort(int(self.playTime // 86400)).writeByte(int(self.playTime // 3600) % 24).toByteArray())

                if not "letter" in obj:
                    count = self.playerConsumables[consumableID] - 1
                    if count <= 0:
                        del self.playerConsumables[consumableID]
                    else:
                        self.playerConsumables[consumableID] = count

                    self.room.sendAll(Identifiers.send.Use_Inventory_Consumable, ByteArray().writeInt(self.playerCode).writeShort(consumableID).toByteArray())
                    self.updateInventoryConsumable(consumableID, count)

class Server(asyncio.Transport):
    def __init__(self):

        # Settings
        self.miceName = Config.miceName
        self.isDebug = Config.isDebug
        self.adventureIMG = Config.adventureIMG
        self.adventureID = Config.adventureID
        self.serverURL = Config.serverURL.split(", ")
        self.leastMice = Config.leastMice
        self.initialCheeses = Config.initialCheeses
        self.initialFraises = Config.initialFraises
        self.initialShamanLevel = Config.initialShamanLevel
        self.initialShamanExpNext = Config.initialShamanExpNext
        self.OP = Config.OP.split(", ")
        self.langs2 = [  [ "af", "za" ],  [ "am", "et" ],  [ "ar", "eg" ],  [ "be", "by" ],  [ "bi", "vu" ],  [ "bn", "bd" ],  [ "bs", "ba" ],  [ "ca", "ad" ],  [ "cs", "cz" ],  [ "da", "dk" ],  [ "dv", "mv" ],  [ "dz", "bt" ],  [ "el", "gr" ],  [ "en", "gb" ],  [ "et", "ee" ],  [ "fa", "ir" ],  [ "ga", "ie" ],  [ "he", "il" ],  [ "hi", "in" ],  [ "hy", "am" ],  [ "ja", "jp" ],  [ "ka", "ge" ],  [ "kk", "kz" ],  [ "kl", "gl" ],  [ "km", "kh" ],  [ "ko", "kr" ],  [ "ky", "kg" ],  [ "lb", "lu" ],  [ "lo", "la" ],  [ "mo", "md" ],  [ "ms", "my" ],  [ "my", "mm" ],  [ "na", "nr" ],  [ "ne", "np" ],  [ "ny", "mw" ],  [ "qu", "bo" ],  [ "rn", "bi" ],  [ "sl", "si" ],  [ "sm", "ws" ],  [ "sq", "al" ],  [ "sr", "rs" ],  [ "ss", "sz" ],  [ "st", "ls" ],  [ "su", "id" ],  [ "sv", "se" ],  [ "sw", "ke" ],  [ "ta", "lk" ],  [ "tg", "tj" ],  [ "ti", "er" ],  [ "tk", "tm" ],  [ "tl", "ph" ],  [ "tn", "bw" ],  [ "uk", "ua" ],  [ "ur", "pk" ],  [ "vi", "vn" ],  [ "wo", "sn" ],  [ "yo", "ng" ],  [ "zh", "hk" ] ]
        self.languages = [  ["af", "Afrikaans", "za"],  ["az", "Azərbaycan dili", "az"],  ["id", "Bahasa Indonesia", "id"],  ["ms", "Bahasa Melayu", "my"],  ["bi", "Bislama", "vu"],  ["bs", "Bosanski jezik", "ba"],  ["ca", "Català", "ad"],  ["ny", "ChiCheŵa", "mw"],  ["da", "Dansk", "dk"],  ["de", "Deutsch", "de"],  ["et", "Eesti keel", "ee"],  ["na", "Ekakairũ Naoero", "nr"],  ["en", "English", "gb"],  ["es", "Español", "es"],  ["to", "Faka Tonga", "to"],  ["mg", "Fiteny malagasy", "mg"],  ["fr", "Français", "fr"],  ["sm", "Gagana fa'a Samoa", "ws"],  ["hr", "Hrvatski", "hr"],  ["it", "Italiano", "it"],  ["mh", "Kajin M̧ajeļ", "mh"],  ["kl", "Kalaallisut", "gl"],  ["rn", "KiRundi", "bi"],  ["rw", "Kinyarwanda", "rw"],  ["sw", "Kiswahili", "ke"],  ["ht", "Kreyòl ayisyen", "ht"],  ["lv", "Latviešu valoda", "lv"],  ["lt", "Lietuvių kalba", "lt"],  ["lb", "Lëtzebuergesch", "lu"],  ["hu", "Magyar", "hu"],  ["mt", "Malti", "mt"],  ["nl", "Nederlands", "nl"],  ["no", "Norsk", "no"],  ["uz", "O'zbek", "uz"],  ["pl", "Polski", "pl"],  ["pt", "Português", "pt"],  ["pt-br", "Português brasileiro", "br"],  ["ro", "Română", "ro"],  ["qu", "Runa Simi", "bo"],  ["st", "SeSotho", "ls"],  ["tn", "SeTswana", "bw"],  ["sq", "Shqip", "al"],  ["ss", "SiSwati", "sz"],  ["sk", "Slovenčina", "sk"],  ["sl", "Slovenščina", "si"],  ["so", "Soomaaliga", "so"],  ["fi", "Suomen kieli", "fi"],  ["sv", "Svenska", "se"],  ["tl", "Tagalog", "ph"],  ["vi", "Tiếng Việt", "vn"],  ["tr", "Türkçe", "tr"],  ["tk", "Türkmen", "tm"],  ["fj", "Vosa Vakaviti", "fj"],  ["wo", "Wollof", "sn"],  ["yo", "Yorùbá", "ng"],  ["is", "Íslenska", "is"],  ["cs", "Česky", "cz"],  ["el", "Ελληνικά", "gr"],  ["be", "Беларуская", "by"],  ["ky", "Кыргыз тили", "kg"],  ["mo", "Лимба молдовеняскэ", "md"],  ["mn", "Монгол", "mn"],  ["ru", "Русский язык", "ru"],  ["sr", "Српски језик", "rs"],  ["tg", "Тоҷикӣ", "tj"],  ["uk", "Українська мова", "ua"],  ["bg", "български език", "bg"],  ["kk", "Қазақ тілі", "kz"],  ["hy", "Հայերեն", "am"],  ["he", "עברית", "il"],  ["ur", "اردو", "pk"],  ["ar", "العربية", "eg"],  ["fa", "فارسی", "ir"],  ["dv", "ދިވެހި", "mv"],  ["ne", "नेपाली", "np"],  ["hi", "हिन्दी", "in"],  ["bn", "বাংলা", "bd"],  ["ta", "தமிழ்", "lk"],  ["th", "ไทย", "th"],  ["lo", "ພາສາລາວ", "la"],  ["dz", "རྫོང་ཁ", "bt"],  ["my", "ဗမာစာ", "mm"],  ["ka", "ქართული", "ge"],  ["ti", "ትግርኛ", "er"],  ["am", "አማርኛ", "et"],  ["km", "ភាសាខ្មែរ", "kh"],  ["zh-cn", "中国语文", "cn"],  ["zh", "中國語文", "hk"],  ["ja", "日本語", "jp"],  ["ko", "한국어", "kr"] ]
        self.langs = Utils.buildMap("af", [ "Afrikaans", "za" ], "az", [ "Azərbaycan dili", "az" ], "id", [ "Bahasa Indonesia", "id" ], "ms", [ "Bahasa Melayu", "my" ], "bi", [ "Bislama", "vu" ], "bs", [ "Bosanski jezik", "ba" ], "ca", [ "Català", "ad" ], "ny", [ "ChiCheŵa", "mw" ], "da", [ "Dansk", "dk" ], "de", [ "Deutsch", "de" ], "et", [ "Eesti keel", "ee" ], "na", [ "Ekakairũ Naoero", "nr" ], "en", [ "English", "gb" ], "es", [ "Español", "es" ], "to", [ "Faka Tonga", "to" ], "mg", [ "Fiteny malagasy", "mg" ], "fr", [ "Français", "fr" ], "sm", [ "Gagana fa'a Samoa", "ws" ], "hr", [ "Hrvatski", "hr" ], "it", [ "Italiano", "it" ], "mh", [ "Kajin M̧ajeļ", "mh" ], "kl", [ "Kalaallisut", "gl" ], "rn", [ "KiRundi", "bi" ], "rw", [ "Kinyarwanda", "rw" ], "sw", [ "Kiswahili", "ke" ], "ht", [ "Kreyòl ayisyen", "ht" ], "lv", [ "Latviešu valoda", "lv" ], "lt", [ "Lietuvių kalba", "lt" ], "lb", [ "Lëtzebuergesch", "lu" ], "hu", [ "Magyar", "hu" ], "mt", [ "Malti", "mt" ], "nl", [ "Nederlands", "nl" ], "no", [ "Norsk", "no" ], "uz", [ "O'zbek", "uz" ], "pl", [ "Polski", "pl" ], "pt", [ "Português", "pt" ], "br", [ "Português brasileiro", "br" ], "ro", [ "Română", "ro" ], "qu", [ "Runa Simi", "bo" ], "st", [ "SeSotho", "ls" ], "tn", [ "SeTswana", "bw" ], "sq", [ "Shqip", "al" ], "ss", [ "SiSwati", "sz" ], "sk", [ "Slovenčina", "sk" ], "sl", [ "Slovenščina", "si" ], "so", [ "Soomaaliga", "so" ], "fi", [ "Suomen kieli", "fi" ], "sv", [ "Svenska", "se" ], "tl", [ "Tagalog", "ph" ], "vi", [ "Tiếng Việt", "vn" ], "tr", [ "Türkçe", "tr" ], "tk", [ "Türkmen", "tm" ], "fj", [ "Vosa Vakaviti", "fj" ], "wo", [ "Wollof", "sn" ], "yo", [ "Yorùbá", "ng" ], "is", [ "Íslenska", "is" ], "cs", [ "Česky", "cz" ], "el", [ "Ελληνικά", "gr" ], "be", [ "Беларуская", "by" ], "ky", [ "Кыргыз тили", "kg" ], "mo", [ "Лимба молдовеняскэ", "md" ], "mn", [ "Монгол", "mn" ], "ru", [ "Русский язык", "ru" ], "sr", [ "Српски језик", "rs" ], "tg", [ "Тоҷикӣ", "tj" ], "uk", [ "Українська мова", "ua" ], "bg", [ "български език", "bg" ], "kk", [ "Қазақ тілі", "kz" ], "hy", [ "Հայերեն", "am" ], "he", [ "עברית", "il" ], "ur", [ "اردو", "pk" ], "ar", [ "العربية", "eg" ], "fa", [ "فارسی", "ir" ], "dv", [ "ދިވެހި", "mv" ], "ne", [ "नेपाली", "np" ], "hi", [ "हिन्दी", "in" ], "bn", [ "বাংলা", "bd" ], "ta", [ "தமிழ்", "lk" ], "th", [ "ไทย", "th" ], "lo", [ "ພາສາລາວ", "la" ], "dz", [ "རྫོང་ཁ", "bt" ], "my", [ "ဗမာစာ", "mm" ], "ka", [ "ქართული", "ge" ], "ti", [ "ትግርኛ", "er" ], "am", [ "አማርኛ", "et" ], "km", [ "ភាសាខ្មែរ", "kh" ], "cn", [ "中国语文", "cn" ], "zh", [ "中國語文", "hk" ], "ja", [ "日本語", "jp" ], "ko", [ "한국어", "kr" ])

        # Shop
        self.shopList = ""
        self.shamanShopList = ""

        # Integer
        self.lastGiftID = 0
        self.lastMapCode = 0
        self.lastPlayerCode = 0
        self.startServer = datetime.today()

        # Nonetype
        self.rebootTimer = None

        # List
        self.loginKeys = []
        self.packetKeys = []
        self.userMuteCache = []
        self.shopPromotions = []
        self.IPTempBanCache = []
        self.IPPermaBanCache = []
        self.userTempBanCache = []
        self.userPermaBanCache = []
        self.prefixs = ['+', '?', '_', '-', '>', '@', '.']
        self.CONSOLE = None

        # Dict
        self.reports = {}
        self.rooms = {}
        self.players = {}
        self.shopGifts = {}
        self.mapsByPerm = {}
        self.vanillaMaps = {}
        self.chatMessages = {}
        self.usersByEmail = {}
        self.shopListCheck = {}
        self.connectedCounts = {}
        self.shamanShopListCheck = {}
        self.shopOutfitsCheck = {}
        self.minigames = {}
        self.roomsByCommunity = {}
        self.npcShops = {}
        self.codesVerifi = {}
        self.playersById = {}
        self.chats = {}
        self.idsByPlayer = {}
        self.hiddenPlayers = {}
        self.statsPlayer = {"defilanteCount":[1500,10000,100000], "racingCount":[1500,10000,10000,10000], "survivorCount":[1000,800,20000,10000], "racingBadges":[124,125,126,127], "survivorBadges":[120,121,122,123]}
        self.shopBadges = {230180: 304, 230179: 302, 230178: 301, 230177: 300, 230176: 299, 230175: 298, 230173: 295, 230172: 295, 230171: 294, 230170: 292, 230167: 289, 230166: 284, 230165: 285, 230164: 283, 230163: 282, 230162: 280, 230161: 279, 230160: 278, 230159: 277, 230158: 275, 230157: 274, 230156: 273, 230155: 271, 230154: 270, 230153: 268,230152: 266, 230151: 265,230150: 263,230149: 262, 230148: 260, 230147: 259, 230146: 258, 230145: 256, 230144: 254, 230143: 253, 230142: 252, 230141: 251, 230140: 250, 230139: 248, 230138: 247, 230137: 246, 230136: 245, 230135: 244, 230134: 243, 230133: 242, 230132: 241, 230131: 239, 230130: 238, 230129: 237, 230128: 236, 230127: 235, 230126: 234, 230125: 233, 230124: 232, 230123: 231, 230122: 229, 230121: 228, 230120: 227, 230119: 226, 230117: 224, 230116: 223, 230115: 222, 230114: 220, 230113: 217, 230112: 216, 230111: 215, 230110: 214, 230109: 213, 230108: 212, 230107: 211, 230106: 210, 230105: 208, 230104: 207, 230103: 206, 230102: 205, 230101: 204, 230100: 203, 2299: 201, 2298: 200, 2297: 199, 2296: 197, 2295: 196, 2294: 195, 2293: 194, 2292: 192, 2291: 191, 2290: 189, 2289: 187, 2288: 186, 2287: 185, 2286: 183, 2285: 180, 2284: 179, 2283: 178, 2282: 177, 2281: 176, 2280: 175, 2279: 173, 2278: 171, 2277: 167, 2276: 165, 2274: 160, 2273: 157, 2272: 156, 2271: 155, 2270: 152, 2269: 151, 2268: 150, 2267: 149, 2265: 148, 2264: 146, 2263: 143, 2262: 141, 2261: 140, 2260: 138, 2259: 137, 2258: 136, 2257: 135, 2256: 128, 2255: 72, 2254: 70, 2253: 68, 2252: 67, 2250: 66, 2249: 63, 2248: 61, 2247: 53, 2246: 52, 2244: 48, 2243: 45, 2241: 44, 2239: 43, 2238: 41, 2236: 36, 2234: 27, 2232: 20, 2231: 15, 2230: 14, 2229: 13, 2228: 8, 2227: 2, 2226: 62, 2225: 56, 2224: 21, 2223: 26, 2222: 39, 2221: 32, 2220: 25, 2219: 12, 2218: 10, 2217: 22, 2215: 37, 2214: 23, 2213: 60, 2212: 24, 2211: 19, 2209: 5, 2208: 3, 2207: 49, 2206: 11, 2205: 38, 2204: 40, 2203: 31, 2202: 4}
        self.shopTitleList = {1:115.1, 2:116.1, 4:117.1, 6:118.1, 8:119.1, 10:120.1, 12:121.1, 14:122.1, 16:123.1, 18:124.1, 20:125.1, 22:126.1, 23:115.2, 24:116.2, 26:117.2, 28:118.2, 30:119.2, 32:120.2, 34:121.2, 36:122.2, 38:123.2, 40:124.2, 42:125.2, 44:126.2, 45:115.3, 46:116.3, 48:117.3, 50:118.3, 52:119.3, 54:120.3, 56:121.3, 58:122.3, 60:123.3, 62:124.3, 64:125.3, 66:126.3, 67:115.4, 68:116.4, 70:117.4, 72:118.4, 74:119.4, 76:120.4, 78:121.4, 80:122.4, 82:123.4, 84:124.4, 86:125.4, 88:126.4, 89:115.5, 90:116.5, 92:117.5, 94:118.5, 96:119.5, 98:120.5, 100:121.5, 102:122.5, 104:123.5, 106:124.5, 108:125.5, 110:126.5, 111:115.6, 112:116.6, 114:117.6, 116:118.6, 118:119.6, 120:120.6, 122:121.6, 124:122.6, 126:123.6, 128:124.6, 130:125.6, 132:126.6, 133:115.7, 134:116.7, 136:117.7, 138:118.7, 140:119.7, 142:120.7, 144:121.7, 146:122.7, 148:123.7, 150:124.7, 152:125.7, 154:126.7, 155:115.8, 156:116.8, 158:117.8, 160:118.8, 162:119.8, 164:120.8, 166:121.8, 168:122.8, 170:123.8, 172:124.8, 174:125.8, 176:126.8, 177:115.9, 178:116.9, 180:117.9, 182:118.9, 184:119.9, 186:120.9, 188:121.9, 190:122.9, 192:123.9, 194:124.9, 196:125.9, 198:126.9}

        # Files
        self.parseSWF = self.parseFile("./include/files/infoSWF.json")
        self.captchaList = self.parseFile("./include/files/captchas.json")
        self.npcs = self.parseFile("./include/files/npcs.json")
        self.promotions = self.parseFile("./include/files/promotions.json")
        self.serverList = self.parseFile("./include/files/serverList.json")
        self.badIPS = self.parseFile("./include/files/badIPS.json")
        self.inventoryConsumables = self.parseFile("./include/files/inventory.json", load=True)
        self.privileges = self.parseFile("./include/files/privileges.json")

        for _type, _dict in self.parseFile("./include/files/titles.json").items():
            _temp = {}
            for count, _id in _dict.items():
                exec(f"_temp[count * Config.{_type}Count] = _id")
            exec(f"self.{_type}TitleList = {_temp}")

        # Others
        self.CursorCafe = CursorCafe
        self.parseShopList()
        self.parseFunctions()
        self.getVanillaMaps()
        self.parsePromotions()
        self.parseUserData()
        self.loadMapsByPerm()
        self.getLastMapCode()
        self.loadMinigames()

        start = time.time()
        self.loop = asyncio.get_event_loop()
        self.OnlineServer = datetime.today()
        for port in [11801, 12801, 13801, 14801]:
            coro = self.loop.create_server(lambda: Client(self), "0.0.0.0", port)
            server = self.loop.run_until_complete(coro)
        print("[%s] %s serveur running." %(time.strftime("%H:%M:%S"), self.miceName))
        print(f"Server loaded in {time.time() - start}s")
        #self.BotDiscord = module.Bot(self)
        #self.BotDiscord.start_bot()
        self.loop.run_forever()
    
    def sendMessageDiscord(self, message='', username='SERVER'):
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/785763140851204098/Wb3jhOiKC3dzK0WWNDU7oUz_wZX5GMD567jDLOxeidGp_8IzAZtBQLPMD6Glw7CL7phD', content=message, username=username, avatar_url='https://cdn.discordapp.com/avatars/701961117488119928/886713a935e026875a0cfd9370784e46.png?size=128')
        response = webhook.execute()
        return True
     
    def getXML(self, mapCode):
        mapInfo = ["", "", 0]
        CursorMaps.execute("SELECT * FROM maps WHERE Code = ?", [mapCode])
        rs = CursorMaps.fetchone()
        if rs:
            mapInfo = [self.getPlayerName(rs["Builder"]), rs["XML"], rs["Perma"]]
        return mapInfo
    
    def infomap(self, p):
        p = int(p)
        if p == 0:
            return ["<:p0:788474248905097247>", 0xE0DBCC, "Normal"]
        elif p == 1:
            return ["<:p1:788474261940994080>", 0xECB140, "Protected"]
        elif p == 3:
            return ["<:bootcamp:788476124186673152>", 0x575F24, "Bootcamp"]
        elif p == 4:
            return ["<:shaman:788476079517859911>", 0x94D8D5, "Shaman"]
        elif p == 5:
            return ["<:p5:788476151038476368>", 0xBA3D13, "Art"]
        elif p == 6:
            return ["<:p6:788476078687649803>", 0x908B86, "Mechanism"]
        elif p == 7:
            return ["<:racing:788476095098781696>", 0xE8E8E8, "No-shaman"]
        elif p == 8:
            return ["<:p8:788476078938652744>", 0x9585AC, "Dual shaman"]
        elif p == 9:
            return ["<:tfm_cheese:788476079508815902>", 0xFDD599, "Miscellaneous"]
        elif p == 10:
            return ["<:p10:788476078888189985>", 0x1B1919, "Survivor"]
        elif p == 11:
            return ["<:p11:788476079425454141>", 0xAA4444, "Vampire"]
        elif p == 17:
            return ["<:p17:788476079235924009>", 0xCC4F3A, "Racing"]
        elif p == 18:
            return ["<:p18:788476079585230868>", 0x73B32D, "Defilante"]
        elif p == 19:
            return ["<:p19:788476079211020318>", 0xD0CBCD, "Music"]
        elif p == 22:
            return ["<:tribe:788476079550627850>", 0x8B6C4E, "Tribe House"]
        elif p == 24:
            return ["<:p24:788476079035514902>", 0x1B1919, "Dual Shaman Survivor"]
        elif p == 43:
            return ["<:p44:788476079488368671>", 0xF40000, "High Deleted"]
        elif p == 44:
            return ["<:p44:788476079488368671>", 0xF40000, "Deleted"]
        else:
            return ["<:ground:788476124522217542>", 0x90B214, ""]

    
    def sendMessageDiscordMP(self, message=''):
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/785786148273520660/AVrjReuLsQoSIIeAmU85d1_fzToKkSlq3ibfpXAw0K0rCg97V0JDet55NibufjGT-i9k', content=message, username='MapCrew', avatar_url='https://media.discordapp.net/attachments/785501633001029672/785786342516588584/6_1535234223l.png?width=427&height=427')
        response = webhook.execute()
        return True

    def reloadAllModules(self):
        reload(module)
        for player in self.players.values():
            player.tribulle = module.Tribulle(player, self)
            player.parseShop = module.ParseShop(player, self)
            player.parseSkill = module.ParseSkill(player, self)
            player.parsePackets = module.ParsePackets(player, self)
            player.parseCommands = module.ParseCommands(player, self)
            player.others = module.Others(player)
    
    def TimeOnlineServer(self):
        time = str(datetime.today() - self.OnlineServer).replace("<", "&lt;").split(".")[0]
        return time 
        
    def OnlinePlayers(self):
        i = 0
        for player in self.players.values():
           i += 1
        return i

    def loadMinigames(self):
        self.minigames = {}
        for fileName in os.listdir("./include/lua/minigames/"):
            with open(f"./include/lua/minigames/{fileName}", encoding="utf8") as f:
                self.minigames[fileName[:-4]] = f.read()

    def dbApi(self, gKey, column, data):
        site = "http://localhost"
        urlopen(f"{site}/api/api.php?pl={gKey}&veritb={column}&veri={data}")

    def loadMapsByPerm(self):
        CursorMaps.execute("SELECT Perma, Code from maps")
        rrf = CursorMaps.fetchall()
        for rs in rrf:
            if not rs["Perma"] in self.mapsByPerm:
                self.mapsByPerm[rs["Perma"]] = []
            self.mapsByPerm[rs["Perma"]].append(rs["Code"])

    def getLastMapCode(self):
        CursorMaps.execute("SELECT Code from maps ORDER BY Code DESC limit 1")
        self.lastMapCode = CursorMaps.fetchone()[0]

    def parseUserData(self):
        Cursor.execute("SELECT Username, Email, Tag, PlayerID FROM users")
        rrf = Cursor.fetchall()
        for rs in rrf:
            self.playersById[rs[3]] = rs[0]
            self.idsByPlayer[rs[0]] = rs[3]
            if rs[1] not in self.usersByEmail:
                self.usersByEmail[rs[1]] = []
            self.usersByEmail[rs[1]].append(rs[0] + rs[2])

    def parseShopList(self):
        shopData = self.parseFile("./include/files/shop.json", load=True)
        self.shopList = shopData["shopItems"]
        self.shamanShopList = shopData["shamanItems"]
        self.shopOutfits = shopData["fullLooks"]
        self.shopListChecker = []

        for item in self.shopList:
            self.shopListCheck[f'{item["category"]}|{item["id"]}'] = [item["cheese"], item["fraise"]]
            self.shopListChecker.append(f'{int(item["category"])},{int(item["id"])},0,1,0,{int(item["cheese"])},{int(item["fraise"])}')

        for item in self.shamanShopList:
            self.shamanShopListCheck[str(item["id"])] = [item["cheese"], item["fraise"]]
        
        for item in self.shopOutfits:
            self.shopOutfitsCheck[str(item["id"])] = [item["look"], item["bg"]]

    def appendBadIP(self, ip):
        if ip in self.badIPS:
            self.badIPS.remove(ip)
        self.badIPS.append(ip)
        self.IPTempBanCache.append(ip)
        with open("./include/files/badIPS.json", "w") as f:
            json.dump(self.badIPS, f)

    def addCallLater(self, _time, func):
        self.loop.call_later(_time, func)

    def parseFunctions(self):
        # SWF
        data = self.parseSWF
        self.CKEY = data["key"]
        self.Version = data["version"]

        keys = data["packetKeys"]
        i = 0
        while i < len(keys):
            self.packetKeys.append(keys[i])
            i += 1
        self.authKey = data["authkey"]
        login = data["loginKeys"]
        i = 0
        while i < len(login):
            self.loginKeys.append(login[i])
            i += 1

        # DB
        Cursor.execute("select ip from IPPermaBan")
        rs = Cursor.fetchone()
        if rs:
            self.IPPermaBanCache.append(rs[0])

        Cursor.execute("select Username from UserPermaBan")
        rs = Cursor.fetchone()
        if rs:
            self.userPermaBanCache.append(rs[0])

        Cursor.execute("select Username from UserTempBan")
        rs = Cursor.fetchone()
        if rs:
            self.userTempBanCache.append(rs[0])

        Cursor.execute("select Username from UserTempMute")
        rs = Cursor.fetchone()
        if rs:
            self.userMuteCache.append(rs[0])

    def parseFile(self, directory, load=False):
        with open(directory, "r") as f:
            output = f.read()
        if load:
            return json.loads(output)
        else:
            return eval(output)

    def updateBlackList(self):
        with open("./include/files/serverList.json", "w") as f:
            json.dump(self.serverList, f)

    def getVanillaMaps(self):
        for fileName in os.listdir("./include/maps/vanilla"):
            with open("./include/maps/vanilla/"+fileName) as f:
                self.vanillaMaps[int(fileName[:-4])] = f.read()

    def sendServerRestart(self, no, sec):
        if sec > 0 or no != 5:
            self.sendServerRestartSEC(120 if no == 0 else 60 if no == 1 else 30 if no == 2 else 20 if no == 3 else 10 if no == 4 else sec)
            if self.rebootTimer != None: self.rebootTimer.cancel()
            self.rebootTimer = self.loop.call_later(60 if no == 0 else 30 if no == 1 else 10 if no == 2 or no == 3 else 1, lambda: self.sendServerRestart(no if no == 5 else no + 1, 9 if no == 4 else sec - 1 if no == 5 else 0))

    def sendServerRestartSEC(self, seconds):
        self.sendPanelRestartMessage(seconds)
        self.sendWholeServer(Identifiers.send.Server_Restart, ByteArray().writeInt(seconds * 1000).toByteArray())

    def sendPanelRestartMessage(self, seconds):
        if seconds == 120:
            print("[%s] [SERVER] The server will restart in 2 minutes." %(time.strftime("%H:%M:%S")))
        elif seconds < 120 and seconds > 1:
            print("[%s] [SERVER] The server will restart in %s seconds." %(time.strftime("%H:%M:%S"), seconds))
        else:
            print("[%s] [SERVER] The server will restart in 1 second." %(time.strftime("%H:%M:%S")))
            for player in self.players.copy().values():
                player.updateDatabase()
            os._exit(0)

    def checkAlreadyExistingGuest(self, playerName):
        if not playerName: playerName = "Souris"
        if self.checkConnectedAccount(playerName):
            playerName += "_%s" %("".join([random.choice(string.ascii_lowercase) for x in range(4)]))
        return playerName

    def checkConnectedAccount(self, playerName):
        return playerName in self.players

    def disconnectIPAddress(self, ip):
        for player in self.players.copy().values():
            if player.ipAddress == ip:
                player.transport.close()

    def checkExistingUser(self, playerName):
        Cursor.execute("select 1 from Users where Username = %s", [playerName])
        return Cursor.fetchone() != None

    def recommendRoom(self, langue, prefix=""):
        count = 0
        result = ""
        while result == "":
            count += 1
            if ("%s-%s" %(langue, count) if prefix == "" else "%s-%s%s" %(langue, prefix, count)) in self.rooms:
                if self.rooms["%s-%s" %(langue, count) if prefix == "" else "%s-%s%s" %(langue, prefix, count)].getPlayerCount() < 25:
                    result = str(count)
            else:
                result = str(count)
        return result

    def checkRoom(self, roomName, langue):
        found = False
        x = 0
        result = roomName
        if (("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and roomName[0] != chr(3) else roomName) in self.rooms:
            room = self.rooms.get(("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and roomName[0] != chr(3) else roomName)
            if room.getPlayerCount() < room.maxPlayers if room.maxPlayers != -1 else True:
                found = True
        else:
            found = True

        while not found:
            x += 1
            if ((("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and roomName[0] != chr(3) else roomName) + str(x)) in self.rooms:
                room = self.rooms.get((("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and roomName[0] != chr(3) else roomName) + str(x))
                if room.getPlayerCount() < room.maxPlayers if room.maxPlayers != -1 else True:
                    found = True
                    result += str(x)
            else:
                found = True
                result += str(x)
        return result

    def addClientToRoom(self, player, roomName):
        if roomName in self.rooms:
            self.rooms[roomName].addClient(player)
        else:
            room = Room(self, roomName)
            self.rooms[roomName] = room
            room.addClient(player, True)
            if room.minigame != "":
                room.loadLuaModule(room.minigame)
            else:
                room.mapChange()

    def banPlayer(self, playerName, bantime, reason, modName, silent):
        found = False

        player = self.players.get(playerName)
        if player != None:
            found = True
            if not modName == "Server":
                player.banHours += bantime
                Cursor.execute("insert into BanLog values (%s, %s, %s, %s, %s, 'Online', %s)", [playerName, modName, bantime, reason, int(time.time() / 10), player.ipAddress])
            else:
                self.sendStaffMessage(5, "<V>Server <BL>banned the player <V>%s<BL> for <V>1 <BL> hour. Reason: <V>Vote Populaire<BL>." %(playerName))

            Cursor.execute("update Users set BanHours = %s where Username = %s", [bantime, playerName])

            if bantime >= 361 or player.banHours >= 361:
                self.userPermaBanCache.append(playerName)
                Cursor.execute("insert into UserPermaBan values (%s, %s, %s)", [playerName, reason, modName])

            if player.banHours >= 361:
                self.IPPermaBanCache.append(player.ipAddress)
                Cursor.execute("insert into IPPermaBan values (%s, %s, %s)", [player.ipAddress, modName, reason])

            if bantime >= 1 and bantime <= 360:
                self.tempBanUser(playerName, bantime, reason)
                self.tempBanIP(player.ipAddress, bantime)
       
            player.sendPlayerBan(bantime, reason, silent)
            
        self.modoPwetProccess(playerName, bantime, reason, modName, "ban")

        if not found and self.checkExistingUser(playerName) and not modName == "Server" and bantime >= 1:
            found = True
            totalBanTime = self.getTotalBanHours(playerName) + bantime
            if (totalBanTime >= 361 and bantime <= 360) or bantime >= 361:
                self.userPermaBanCache.append(playerName)
                Cursor.execute("insert into UserPermaBan values (%s, %s, %s)", [playerName, reason, modName])

            if bantime >= 1 and bantime <= 360:
                self.tempBanUser(playerName, bantime, reason)

            Cursor.execute("update Users set BanHours = %s where Username = %s", [bantime, playerName])
            Cursor.execute("insert into BanLog values (%s, %s, %s, %s, %s, 'Offline', 'Offline')", [playerName, modName, str(bantime), reason, int(time.time() / 10)])
        return found

    def checkTempBan(self, playerName):
        Cursor.execute("select 1 from UserTempBan where Username = %s", [playerName])
        return Cursor.fetchone() != None

    def removeTempBan(self, playerName):
        if playerName in self.userTempBanCache:
            self.userTempBanCache.remove(playerName)
        Cursor.execute("delete from UserTempBan where Username = %s", [playerName])

    def tempBanUser(self, playerName, bantime, reason):
        if self.checkTempBan(playerName):
            self.removeTempBan(playerName)

        self.userTempBanCache.append(playerName)
        Cursor.execute("insert into UserTempBan values (%s, %s, %s)", [playerName, reason, str(Utils.getTime() + (bantime * 60 * 60))])

    def getTempBanInfo(self, playerName):
        Cursor.execute("select Reason, Time from UserTempBan where Username = %s", [playerName])
        for rs in Cursor.fetchall():
            return [rs[0], rs[1]]
        else:
            return ["Without a reason", 0]

    def getPermBanInfo(self, playerName):
        Cursor.execute("select Reason from UserPermaBan where Username = %s", [playerName])
        for rs in Cursor.fetchall():
            return rs[0]
        else:
            return "Without a reason"

    def checkPermaBan(self, playerName):
        Cursor.execute("select 1 from UserPermaBan where Username = %s", [playerName])
        return Cursor.fetchone() != None

    def removePermaBan(self, playerName):
        if playerName in self.userPermaBanCache:
            self.userPermaBanCache.remove(playerName)
        Cursor.execute("delete from UserPermaBan where Username = %s", [playerName])

    def tempBanIP(self, ip, time):
        if not ip in self.IPTempBanCache:
            self.IPTempBanCache.append(ip)
            if ip in self.IPTempBanCache:
                self.loop.call_later(time, lambda: self.IPTempBanCache.remove(ip))

    def getTotalBanHours(self, playerName):
        Cursor.execute("select BanHours from Users where Username = %s", [playerName])
        rs = Cursor.fetchone()
        if rs:
            return rs[0]
        else:
            return 0

    def voteBanPopulaire(self, playerName, playerVoted, ip):
        player = self.players.get(playerName)
        if player != None and player.privLevel.includes(1) and not ip in player.voteBan:
            player.voteBan.append(ip)
            if len(player.voteBan) == 10:
                self.banPlayer(playerName, 1, "Vote Populaire", "Server", False)
            self.sendStaffMessage(7, "The player <V>%s</V> is voted to <V>%s</V> [<R>%s</R>/10]" %(playerVoted, playerName, len(player.voteBan)))

    def muteUser(self, playerName, mutetime, reason):
        self.userMuteCache.append(playerName)
        Cursor.execute("insert into UserTempMute values (%s, %s, %s)", [playerName, str(Utils.getTime() + (mutetime * 60 * 60)), reason])

    def removeModMute(self, playerName):
        if playerName in self.userMuteCache:
            self.userMuteCache.remove(playerName)
        Cursor.execute("delete from UserTempMute where Username = %s", [playerName])

    def getModMuteInfo(self, playerName):
        Cursor.execute("select Reason, Time from UserTempMute where Username = %s", [playerName])
        rs = Cursor.fetchone()
        if rs:
            return [rs[0], rs[1]]
        else:
            return ["Without a reason", 0]

    def mutePlayer(self, playerName, hours, reason, modName):
        player = self.players.get(playerName)
        if player != None:
            self.sendStaffMessage(5, "<V>%s</V> muted <V>%s</V> for <V>%s</V> %s Reason: <V>%s</V>" %(modName, playerName, hours, "hora" if hours == 1 else "horas", reason))
            if playerName in self.userMuteCache:
                self.removeModMute(playerName)

            player.isMute = True
            player.sendModMute(playerName, hours, reason, False)
            player.sendModMute(playerName, hours, reason, True)
            self.modoPwetProccess(playerName, hours, reason, modName, "mute")
            self.muteUser(playerName, hours, reason)
            
    def modoPwetProccess(self, playerName, hours, reason, modName, proccess):
        if playerName in self.reports:
            report = self.reports[playerName]
            d = "banned" if proccess=="ban" else "muted"
            if proccess == "mute":
                report["isMuted"] = True
                report["muteHours"] = int(hours)
                report["muteReason"] = reason
                report["mutedBy"] = modName

            elif proccess == "ban":
                report["status"] = "banned"
                report["bannedby"] = modName
                report["banhours"] = hours
                report["banreason"] = reason

            for name in report["reporters"]:
                player = self.players.get(name)
                if player:
                    player.playerKarma += 1
                    player.sendMessage(playerName+" has been "+d+". Karma +1 ("+str(player.playerKarma)+")")
            for player in self.players.values():
                if player.isModoPwet:
                    player.modoPwet.openModoPwet(True)

    def desmutePlayer(self, playerName, modName):
        player = self.players.get(playerName)
        if player != None:
            self.sendStaffMessage(5, "<V>%s</V> unmuted <V>%s</V>." %(modName, playerName))
            self.removeModMute(playerName)
            player.isMute = False

    def sendStaffChat(self, type, langue, playerName, message, sender):
        playerName = sender.playerName if type == -1 else "" if type == 0 else "Message Serveur" if type == 1 else sender.langue.upper() + "][" +({11:"Founder][", 10:"Admin][", 9:"Coord][", 8:"Smod][", 7:"Mod][", 6:"MapCrew][", 5:"Helper][", 4:"DV][", 3:"LUA]["}[sender.privLevel.uppermost()])
        if "][" in playerName: playerName += sender.playerName
        for player in (sender.room.clients if type == 0 else self.players).copy().values():
            if ((type == -1 or type == 0 or type == 1 or ((type == 2 or type == 5) and player.privLevel.upper(3)) or ((type == 3 or type == 4) and player.privLevel.upper(3)) or ((type == 6 or type == 7) and player.privLevel.upper(3)) or (type == 8 and player.privLevel.upper(3)) or (type == 9 and player.privLevel.upper(3))) and (player.langue == langue or type == -1 or type == 1 or type == 4 or type == 5 or type == 6)):
                player.sendPacket(Identifiers.send.Staff_Chat, ByteArray().writeByte(1 if type == -1 else type).writeUTF(playerName).writeUTF("* Warning *" if self.checkMessage(player, message) else message).writeShort(0).writeByte(0).toByteArray())

    def getShamanType(self, playerCode):
        for player in self.players.copy().values():
            if player.playerCode == playerCode:
                return player.shamanType
        return 0

    def getShamanLevel(self, playerCode):
        for player in self.players.copy().values():
            if player.playerCode == playerCode:
                return player.shamanLevel
        return 0

    def getShamanBadge(self, playerCode):
        for player in self.players.copy().values():
            if player.playerCode == playerCode:
                return player.parseSkill.getShamanBadge()
        return 0

    def getTribeHouse(self, tribeName):
        Cursor.execute("select House from Tribe where Name = %s", [tribeName])
        rs = Cursor.fetchone()
        if rs:
            return rs[0]
        else:
            return -1

    def getPlayerID(self, playerName):
        if playerName.startswith("*"):
            return 0
        elif playerName in self.players:
            return self.players[playerName].playerID
        elif playerName in self.idsByPlayer:
            return self.idsByPlayer.get(playerName)
        else:
            Cursor.execute("select PlayerID from Users where Username = %s", [playerName])
            rs = Cursor.fetchone()
            if rs:
                return rs[0]
            else:
                return 0

    def getPlayerPrivlevel(self, playerName):
        if playerName.startswith("*"):
            return 0
        elif playerName in self.players:
            return self.players[playerName].privLevel
        else:
            Cursor.execute("select PrivLevel from Users where Username = %s", [playerName])
            rs = Cursor.fetchone()
            if rs:
                return rs[0]
            else:
                return 0

    def saveCasierLog(self, playerName, state, playerMod, time, reason):
        timestat = Utils.getTime()
        t = str(datetime.today()).split(" ")[0]
        Cursor.execute("insert into casierlog values ('0', %s, %s, %s, %s, %s ,%s, %s)", [str(playerName), str(state), str(timestat), str(playerMod), str(time), str(reason), str(t)])

    def getPlayerName(self, playerID):
        if playerID in self.playersById:
            return self.playersById.get(playerID)
        Cursor.execute("select Username from Users where PlayerID = %s", [playerID])
        rs = Cursor.fetchone()
        if rs:
            return rs[0]
        else:
            return ""

    def getPlayerTag(self, playerName):
        playerName = Utils.parsePlayerName(playerName)
        if playerName.startswith("*"): return ""
        if playerName in self.players: return self.players.get(playerName).playerTag
        Cursor.execute("select Tag from Users where Username = %s", [playerName])
        rs = Cursor.fetchone()
        if rs:
            return rs[0]
        else:
            return ""

    def getPlayerRoomName(self, playerName):
        if playerName in self.players:
            return self.players[playerName].roomName
        else:
            return ""

    def getPlayersCountMode(self, mode, langue):
        modeName = {1:"", 3:"vanilla", 8:"survivor", 9:"racing", 11:"music", 2:"bootcamp", 10:"defilante", 18:"", 16: "village", 19: "#village+"}[mode]
        playerCount = 0
        for room in self.rooms.values():
            if ((room.isNormRoom if mode == 1 else room.isVanilla if mode == 3 else room.isSurvivor if mode == 8 else room.isRacing if mode == 9 else room.isMusic if mode == 11 else room.isBootcamp if mode == 2 else room.isDefilante if mode == 10 else room.isVillage if mode == 16 else room.isVillage if mode == 19 else True) and langue.lower() in [room.community, "all"]):
                playerCount += room.getPlayerCount()
        return ["%s %s" %(self.miceName, modeName) if mode != 18 else "", playerCount]

    def parsePromotions(self):
        needUpdate = False
        i = 0
        while i < len(self.promotions):
            item = self.promotions[i]                
            if item[3] < 1000:
                item[3] = Utils.getTime() + item[3] * 86400 + 30
                needUpdate = True
            
            self.shopPromotions.append([item[0], item[1], item[2], item[3]])
            i += 1

        if needUpdate:
            with open("./include/files/promotions.json", "w") as f:
                json.dump(self.promotions, f)
        
        self.checkPromotionsEnd()

    def checkPromotionsEnd(self):
        needUpdate = False
        for promotion in self.shopPromotions:
            if Utils.getHoursDiff(promotion[3]) <= 0:
                self.shopPromotions.remove(promotion)
                needUpdate = True
                i = 0
                while i < len(self.promotions):
                    if self.promotions[i][0] == promotion[0] and self.promotions[i][1] == promotion[1]:
                        del self.promotions[i]
                    i += 1

        if needUpdate:
            with open("./include/files/promotions.json", "w") as f:
                json.dump(self.promotions, f)

    def sendWholeServer(self, identifiers, result):
        for player in self.players.copy().values():
            player.sendPacket(identifiers, result)

    def checkMessage(self, client, message):
        blackList = self.serverList["blacklist"]
        suspectWords = self.serverList["suspectwords"]
        whiteList = self.serverList["whitelist"]
        isSuspect = False
        i = 0
        while i < len(blackList):
            if re.search("[^a-zA-Z]*".join(blackList[i]), message.lower()):
                self.sendStaffMessage(7, "[<V>ANTI-ADV</V>][<J>%s</J>][<V>%s</V>][<R>%s</R>] The player is sending a blacklist link, so self message does not appear to other players." %(client.ipAddress, client.playerName, message))
                isSuspect = True
                return True
            i += 1
        if not isSuspect:
            if list(filter(lambda word: word in message.lower(), suspectWords)) and not list(filter(lambda white: white in message.lower(), whiteList)):
                self.sendStaffMessage(7, "[<V>ANTI-ADV</V>][<J>%s</J>][<V>%s</V>][<J>%s</J>] Sent a suspicious link message, type <V>/addtext blacklist link</V> to add the link to <b>blacklist</b> if you want to add the link to <b>blacklist</b>." %(client.ipAddress, client.playerName, message))
        return False

    def getPlayerCode(self, playerName):
        player = self.players.get(Utils.parsePlayerName(playerName))
        return player.playerCode if player != None else 0

    def sendStaffMessage(self, minLevel, message, tab=False):
        for player in self.players.copy().values():
            if player.privLevel.upper(minLevel):
                player.sendClientMessage(message, tab)

    def setVip(self, playerName, days):
        vipTime = Utils.getTime() + (days * 86400)
        player = self.players.get(playerName)
        if player != None:
            if not player.privLevel.includes(2):
                player.privLevel.append(2)
            player.checkVip(vipTime)
        Cursor.execute("update users SET VipTime = %s where Username = %s", [vipTime, playerName])
        self.sendStaffMessage(7, f"<V>{playerName}</V> became VIP for <V>{days}</V> days.")

class Room:
    def __init__(self, server, name):

        # String
        self.mapXML = ""
        self.mapName = ""
        self.EMapXML = ""
        self.minigame = ""
        self.funcorpAdmin = ""
        self.roomPassword = ""
        self.forceNextMap = "-1"
        self.currentSyncName = ""
        self.currentShamanName = ""
        self.currentSecondShamanName = ""

        # Integer
        self.lastObjectID = 0
        self.lastImageID = 0
        self.addTime = 0
        self.mapCode = -1
        self.cloudID = -1
        self.EMapCode = 0
        self.objectID = 0
        self.redCount = 0
        self.mapPerma = -1
        self.blueCount = 0
        self.musicTime = 0
        self.mapStatus = -1
        self.mapNoVotes = 0
        self.currentMap = 0
        self.receivedNo = 0
        self.EMapLoaded = 0
        self.roundTime = 120
        self.mapYesVotes = 0
        self.receivedYes = 0
        self.roundsCount = -1
        self.maxPlayers = 200
        self.numCompleted = 0
        self.numGetCheese = 0
        self.companionBox = -1
        self.gameStartTime = 0
        self.lastRoundCode = 0
        self.FSnumCompleted = 0
        self.SSnumCompleted = 0
        self.musicSkipVotes = 0
        self.forceNextShaman = -1
        self.currentSyncCode = -1
        self.changeMapAttemps = 0
        self.currentShamanCode = -1
        self.currentShamanType = -1
        self.mulodromeRoundCount = 0
        self.gameStartTimeMillis = 0
        self.currentSecondShamanCode = -1
        self.currentSecondShamanType = -1

        # Bool
        self.isMusic = False
        self.isClosed = False
        self.noShaman = False
        self.isEditor = False
        self.isRacing = False
        self.isSnowing = False
        self.isVillage = False
        self.isVanilla = False
        self.is801Room = False
        self.countStats = True
        self.isFixedMap = False
        self.isNormRoom = False
        self.isTutorial = False
        self.isVillager = False
        self.isBootcamp = False
        self.isSurvivor = False
        self.isVotingBox = False
        self.autoRespawn = False
        self.noAutoScore = False
        self.isDoubleMap = False
        self.specificMap = False
        self.mapInverted = False
        self.isDefilante = False
        self.isMulodrome = False
        self.canChangeMap = True
        self.isVotingMode = False
        self.isTribeHouse = False
        self.isNoShamanMap = False
        self.isFuncorp = False
        self.EMapValidated = False
        self.isTotemEditor = False
        self.canChangeMusic = True
        self.initVotingMode = True
        self.disableAfkKill = False
        self.isPlayingMusic = False
        self.noShamanSkills = False
        self.isSurvivorVamp = False
        self.never20secTimer = False
        self.isTribeHouseMap = False
        self.changed20secTimer = False
        self.catchTheCheeseMap = False
        self.disablePhysicalConsumables = False
        self.disableWatchCommand = False
        self.disableDebugCommand = False
        self.disableMinimalistMode = False
        self.disableMortCommand = False
        self.autoMapFlipMode = True

        # Bool
        self.killAfkTimer = None
        self.endSnowTimer = None
        self.changeMapTimer = None
        self.voteCloseTimer = None
        self.startTimerLeft = None
        self.autoRespawnTimer = None
        self.luaRuntime = None

        # List Arguments
        self.anchors = []
        self.redTeam = []
        self.blueTeam = []
        self.roomTimers = []
        self.musicVideos = []
        self.lastHandymouse = [-1, -1]
        self.noShamanMaps = [7, 8, 14, 22, 23, 28, 29, 54, 55, 57, 58, 59, 60, 61, 70, 77, 78, 87, 88, 92, 122, 123, 124, 125, 126, 1007, 888, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
        self.mapList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 136, 137, 138, 139, 140, 141, 142, 143, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210]

        # Dict
        self.clients = {}
        self.funcorpNames = {}
        self.currentTimers = {}
        self.currentShamanSkills = {}
        self.currentSecondShamanSkills = {}

        # Others
        self.name = name
        self.server = server
        self.CursorMaps = CursorMaps

        if self.name.startswith("*"):
            self.community = "xx"
            self.roomName = self.name
        else:
            self.community = self.name.split("-")[0].lower()
            self.roomName = self.name.split("-")[1]

        roomNameCheck = self.roomName[1:] if self.roomName.startswith("*") else self.roomName
        if self.roomName.startswith("\x03[Editeur] "):
            self.countStats = False
            self.isEditor = True
            self.never20secTimer = True

        elif self.roomName.startswith("\x03[Tutorial] "):
            self.countStats = False
            self.currentMap = 900
            self.specificMap = True
            self.noShaman = True
            self.never20secTimer = True
            self.isTutorial = True

        elif self.roomName.startswith("\x03[Totem] "):
            self.countStats = False
            self.specificMap = True
            self.currentMap = 444
            self.isTotemEditor = True
            self.never20secTimer = True

        elif self.roomName.startswith("*\x03"):
            self.countStats = False
            self.isTribeHouse = True
            self.autoRespawn = True
            self.never20secTimer = True
            self.noShaman = True
            self.disableAfkKill = True
            self.isFixedMap = True
            self.roundTime = 0

        elif roomNameCheck.startswith("801") or roomNameCheck.startswith("village") or roomNameCheck.startswith("#village+"):
            if roomNameCheck.startswith("village"):
                self.isVillage = True
            elif roomNameCheck.startswith("#village+"):
                self.isVillager = True
            else:
                self.is801Room = True
            if roomNameCheck.startswith("#village+"):
                minigame = roomNameCheck[1:]
                if minigame in self.server.minigames:
                     self.minigame = minigame

            self.roundTime = 0
            self.never20secTimer = True
            self.autoRespawn = True
            self.countStats = False
            self.noShaman = True
            self.isFixedMap = True
            self.disableAfkKill = True
         
        
        elif roomNameCheck.startswith("#"):
            minigame = roomNameCheck[1:]
            if minigame in self.server.minigames:
                self.minigame = minigame

        elif "music" in self.roomName.lower():
            self.isMusic = True

        elif "racing" in self.roomName.lower():
            self.isRacing = True
            self.noShaman = True
            self.roundTime = 63

        elif "bootcamp" in self.roomName.lower():
            self.isBootcamp = True
            self.countStats = False
            self.roundTime = 360
            self.never20secTimer = True
            self.autoRespawn = True
            self.noShaman = True

        elif "vanilla" in self.roomName.lower():
            self.isVanilla = True

        elif "survivor" in self.roomName.lower():
            self.isSurvivor = True
            self.roundTime = 90

        elif "defilante" in self.roomName.lower():
            self.isDefilante = True
            self.noShaman = True
            self.countStats = False
        else:
            self.isNormRoom = True
        self.mapChange()

    def startTimer(self):
        for player in self.clients.copy().values():
            player.sendMapStartTimer(False)

    def loadLuaModule(self, minigame):
        module = self.server.minigames.get(minigame)
        if module != None:
            self.luaRuntime = Lua(self, self.server)
            self.luaRuntime.RunCode(module)
    
    def displayParticle(self, particleType=0, xPosition=0, yPosition=0, xSpeed=0, ySpeed=0, xAcceleration=0, yAcceleration=0, targetPlayer=""):
        packet = ByteArray()
        packet.writeByte(particleType)
        packet.writeShort(xPosition)
        packet.writeShort(yPosition)
        packet.writeShort(xSpeed)
        packet.writeShort(ySpeed)
        packet.writeShort(xAcceleration)
        packet.writeShort(yAcceleration)
        if targetPlayer == "":
            self.sendAll(Identifiers.send.Display_Particle, packet.toByteArray())
        else:
            player = self.players.get(Utils.parsePlayerName(targetPlayer))
            if player != None:
                player.sendPacket(Identifiers.send.Display_Particle, packet.toByteArray())


    def mapChange(self):
        if self.changeMapTimer != None: self.changeMapTimer.cancel()

        if not self.canChangeMap:
            self.changeMapAttemps += 1
            if self.changeMapAttemps < 5:
                self.changeMapTimer = self.server.loop.call_later(1, self.mapChange)
                return

        for timer in self.roomTimers:
            timer.cancel()

        self.roomTimers = []

        for timer in [self.voteCloseTimer, self.killAfkTimer, self.autoRespawnTimer, self.startTimerLeft]:
            if timer != None:
                timer.cancel()

        if self.initVotingMode:
            if not self.isVotingBox and (self.mapPerma == 0 and self.mapCode != -1) and self.getPlayerCount() >= 2:
                self.isVotingMode = True
                self.isVotingBox = True
                self.voteCloseTimer = self.server.loop.call_later(8, self.closeVoting)
                for player in self.clients.copy().values():
                    player.sendPacket(Identifiers.old.send.Vote_Box, [self.mapName, self.mapYesVotes, self.mapNoVotes])
            else:
                self.votingMode = False
                self.closeVoting()

        elif self.isTribeHouse and self.isTribeHouseMap:
            pass
        else:
            if self.isVotingMode:
                TotalYes = self.mapYesVotes + self.receivedYes
                TotalNo = self.mapNoVotes + self.receivedNo
                isDel = False

                if TotalYes + TotalNo >= 100:
                    TotalVotes = TotalYes + TotalNo
                    Rating = (1.0 * TotalYes / TotalNo) * 100
                    rate = str(Rating).split(".")
                    if int(rate[0]) < 50:
                        isDel = True
                CursorMaps.execute("update Maps set YesVotes = ?, NoVotes = ?, Perma = 44 where Code = ?" if isDel else "update Maps set YesVotes = ?, NoVotes = ? where Code = ?", [TotalYes, TotalNo, self.mapCode])
                self.isVotingMode = False
                self.receivedNo = 0
                self.receivedYes = 0
                for player in self.clients.copy().values():
                    player.qualifiedVoted = False
                    player.isVoted = False

            self.initVotingMode = True
            self.lastRoundCode = (self.lastRoundCode + 1) % 127

            if self.isSurvivor:
                for player in self.clients.copy().values():
                    if not player.isDead and (not player.isVampire if self.mapStatus == 0 else not player.isShaman):
                        if not self.noAutoScore: player.playerScore += 10

            if self.catchTheCheeseMap:
                self.catchTheCheeseMap = False
            else:
                numCom = self.FSnumCompleted - 1 if self.isDoubleMap else self.numCompleted - 1
                numCom2 = self.SSnumCompleted - 1 if self.isDoubleMap else 0
                if numCom < 0: numCom = 0
                if numCom2 < 0: numCom2 = 0

                player = self.clients.get(self.currentShamanName)
                if player != None:
                    self.sendAll(Identifiers.old.send.Shaman_Perfomance, [self.currentShamanName, numCom])
                    if not self.noAutoScore: player.playerScore = numCom
                    if numCom > 0:
                        player.parseSkill.earnExp(True, numCom)

                player2 = self.clients.get(self.currentSecondShamanName)
                if player2 != None:
                    self.sendAll(Identifiers.old.send.Shaman_Perfomance, [self.currentSecondShamanName, numCom2])
                    if not self.noAutoScore: player2.playerScore = numCom2
                    if numCom2 > 0:
                        player2.parseSkill.earnExp(True, numCom2)

            if self.getPlayerCount() >= self.server.leastMice:
                if self.isSurvivor:
                    self.giveSurvivorStats() 
                elif self.isRacing:
                    self.giveRacingStats()
                elif self.isDefilante:
                    self.giveDefilanteStats()

            self.currentSyncCode = -1
            self.currentShamanCode = -1
            self.currentShamanType = -1
            self.currentSecondShamanCode = -1
            self.currentSecondShamanType = -1

            self.currentSyncName = ""
            self.currentShamanName = ""
            self.currentSecondShamanName = ""

            self.currentShamanSkills = {}
            self.currentSecondShamanSkills = {}

            self.changed20secTimer = False
            self.isDoubleMap = False
            self.isNoShamanMap = False
            self.FSnumCompleted = 0
            self.SSnumCompleted = 0
            self.objectID = 0
            self.numGetCheese = 0
            self.addTime = 0
            self.cloudID = -1
            self.companionBox = -1
            self.lastHandymouse = [-1, -1]
            self.isTribeHouseMap = False
            self.canChangeMusic = True
            self.canChangeMap = True
            self.changeMapAttemps = 0

            self.getSyncCode()
            self.anchors = []
            self.mapStatus = (self.mapStatus + 1) % 10

            self.numCompleted = 0

            self.currentMap = self.selectMap()
            self.checkMapXML()

            if self.currentMap in [range(44, 54), range(138, 144)] or self.mapPerma == 8 and self.getPlayerCount() >= 3:
                self.isDoubleMap = True

            if self.mapPerma in [7, 17, 42] or (self.isSurvivor and self.mapStatus == 0):
                self.isNoShamanMap = True

            if self.currentMap in range(108, 114):
                self.catchTheCheeseMap = True

            self.gameStartTime = Utils.getTime()
            self.gameStartTimeMillis = time.time()

            for player in self.clients.copy().values():
                player.resetPlay()

            for player in self.clients.copy().values():
                player.startPlay()

                if player.isHidden:
                    player.sendPlayerDisconnect()

            for player in self.clients.copy().values():
                if player.pet != 0:
                    if Utils.getSecondsDiff(player.petEnd) >= 0:
                        player.pet = 0
                        player.petEnd = 0
                    else:
                        self.sendAll(Identifiers.send.Pet, ByteArray().writeInt(player.playerCode).writeByte(player.pet).toByteArray())
                if player.fur != 0:
                    if Utils.getSecondsDiff(player.furEnd) >= 0:
                        player.fur = 0
                        player.furEnd = 0

            if self.isSurvivor and self.mapStatus == 0:
                self.server.loop.call_later(5, self.sendVampireMode)

            if self.isMulodrome:
                self.mulodromeRoundCount += 1
                self.sendMulodromeRound()

                if self.mulodromeRoundCount <= 10:
                    for player in self.clients.copy().values():
                        if player.playerName in self.blueTeam:
                            self.setNameColor(player.playerName, 0x979EFF)
                        elif player.playerName in self.redTeam:
                            self.setNameColor(player.playerName, 0xFF9396)
                else:
                    self.sendAll(Identifiers.send.Mulodrome_End)

            if self.isRacing or self.isDefilante:
                self.roundsCount = (self.roundsCount + 1) % 10
                self.sendAll(Identifiers.send.Rounds_Count, ByteArray().writeByte(self.roundsCount).writeInt(self.getHighestScore()).toByteArray())

            self.startTimerLeft = self.server.loop.call_later(3, self.startTimer)
            if not self.isFixedMap and not self.isTribeHouse and not self.isTribeHouseMap:
                self.changeMapTimer = self.server.loop.call_later(self.roundTime + self.addTime, self.mapChange)

            self.killAfkTimer = self.server.loop.call_later(30, self.killAfk)
            if self.autoRespawn or self.isTribeHouseMap:
                self.autoRespawnTimer = self.server.loop.call_later(2, self.respawnMice)

            if self.luaRuntime != None:
                self.luaRuntime.emit("NewGame", ())

    def getPlayerCount(self):
        return len(list(filter(lambda player: not player.isHidden, self.clients.values())))

    def getPlayerCountUnique(self):
        ipList = []
        for player in self.clients.copy().values():
            if not player.ipAddress in ipList:
                ipList.append(player.ipAddress)
        return len(ipList)

    def getPlayerList(self):
        result, i = b"", 0
        for player in self.clients.copy().values():
            if not player.isHidden:
                result += player.getPlayerData()
                i += 1

        return [i, result]

    def addClient(self, player, newRoom=False):
        self.clients[player.playerName] = player

        player.room = self
        if not newRoom:
            player.isDead = True
            self.sendAllOthers(player, Identifiers.send.Player_Respawn, ByteArray().writeBytes(player.getPlayerData()).writeBoolean(False).writeBoolean(True).toByteArray())
            player.startPlay()

        if self.luaRuntime != None:
            self.luaRuntime.emit("NewPlayer", (player.playerName))

    def removeClient(self, player):
        if player.playerName in self.clients:
            del self.clients[player.playerName]
            player.resetPlay()
            player.isDead = True
            player.playerScore = 0
            player.sendPlayerDisconnect()

            if self.isMulodrome:
                if player.playerName in self.redTeam: self.redTeam.remove(player.playerName)
                if player.playerName in self.blueTeam: self.blueTeam.remove(player.playerName)

                if len(self.redTeam) == 0 and len(self.blueTeam) == 0:
                    self.mulodromeRoundCount = 10
                    self.sendMulodromeRound()

            if len(self.clients) == 0:
                for timer in [self.autoRespawnTimer, self.changeMapTimer, self.endSnowTimer, self.killAfkTimer, self.voteCloseTimer]:
                    if timer != None:
                        timer.cancel()

                del self.server.rooms[self.name]
            else:
                if player.playerCode == self.currentSyncCode:
                    self.currentSyncCode = -1
                    self.currentSyncName = ""
                    self.getSyncCode()
                self.checkChangeMap()
            if self.luaRuntime != None:
                self.luaRuntime.emit("PlayerLeft", (player.playerName))

    def checkChangeMap(self):
        if (not (self.isBootcamp or self.autoRespawn or self.isTribeHouse and self.isTribeHouseMap or self.isFixedMap)):
            alivePeople = list(filter(lambda player: not player.isDead, self.clients.values()))
            if not alivePeople:
                self.mapChange()

    def sendMessage(self, message1, message2, AP=None, *args):
        for player in self.clients.copy().values():
            if player.playerName != AP:
                player.sendLangueMessage(message1, message2, *args)

    def sendAll(self, identifiers, packet=""):
        for player in self.clients.copy().values():
            player.sendPacket(identifiers, packet)

    def sendAllOthers(self, senderClient, identifiers, packet=""):
        for player in self.clients.copy().values():
            if not player == senderClient:
                player.sendPacket(identifiers, packet)

    def sendAllChat(self, playerName, message, isOnly):
        packet = ByteArray().writeUTF(playerName).writeUTF(message).writeBoolean(True)
        if not isOnly:
            for player in self.clients.copy().values():
                if not playerName in player.ignoredsList:
                    player.sendPacket(Identifiers.send.Chat_Message, packet.toByteArray())
        else:
            player = self.clients.get(playerName)
            if player != None:
                player.sendPacket(Identifiers.send.Chat_Message, packet.toByteArray())
            self.server.sendStaffMessage(7, "<V>%s</R> used words that're in blacklist. [<R>%s</R>]." %(playerName, message))

    def getSyncCode(self):
        if self.getPlayerCount() > 0:
            if self.currentSyncCode == -1:
                player = random.choice(list(self.clients.values()))
                self.currentSyncCode = player.playerCode
                self.currentSyncName = player.playerName
        else:
            if self.currentSyncCode == -1:
                self.currentSyncCode = 0
                self.currentSyncName = ""
        return self.currentSyncCode

    def selectMap(self):
        if not self.forceNextMap == "-1":
            force = self.forceNextMap
            self.forceNextMap = "-1"
            self.mapCode = -1

            force = str(force)
            if force.isdigit():
                return self.selectMapSpecificic(force, "Vanilla")
            elif force.startswith("@"):
                return self.selectMapSpecificic(force[1:], "Custom")
            elif force.startswith("#"):
                return self.selectMapSpecificic(force[1:], "Perm")
            elif force.startswith("<"):
                return self.selectMapSpecificic(force, "Xml")
            else:
                return 0

        elif self.specificMap:
            self.mapCode = -1
            return self.currentMap
        else:
            if self.isEditor:
                return self.EMapCode

            elif self.isTribeHouse:
                tribeName = self.roomName[2:]
                runMap = self.server.getTribeHouse(tribeName)

                if runMap == 0:
                    self.mapCode = 0
                    self.mapName = "Tigrounette"
                    self.mapXML = "<C><P /><Z><S><S Y=\"360\" T=\"0\" P=\"0,0,0.3,0.2,0,0,0,0\" L=\"800\" H=\"80\" X=\"400\" /></S><D><P Y=\"0\" T=\"34\" P=\"0,0\" X=\"0\" C=\"719b9f\" /><T Y=\"320\" X=\"49\" /><P Y=\"320\" T=\"16\" X=\"224\" P=\"0,0\" /><P Y=\"319\" T=\"17\" X=\"311\" P=\"0,0\" /><P Y=\"284\" T=\"18\" P=\"1,0\" X=\"337\" C=\"57703e,e7c3d6\" /><P Y=\"284\" T=\"21\" X=\"294\" P=\"0,0\" /><P Y=\"134\" T=\"23\" X=\"135\" P=\"0,0\" /><P Y=\"320\" T=\"24\" P=\"0,1\" X=\"677\" C=\"46788e\" /><P Y=\"320\" T=\"26\" X=\"588\" P=\"1,0\" /><P Y=\"193\" T=\"14\" P=\"0,0\" X=\"562\" C=\"95311e,bde8f3,faf1b3\" /></D><O /></Z></C>"
                    self.mapYesVotes = 0
                    self.mapNoVotes = 0
                    self.mapPerma = 22
                    self.mapInverted = False
                else:
                    run = self.selectMapSpecificic(runMap, "Custom")
                    if run != -1:
                        self.mapCode = 0
                        self.mapName = "Tigrounette"
                        self.mapXML = "<C><P /><Z><S><S Y=\"360\" T=\"0\" P=\"0,0,0.3,0.2,0,0,0,0\" L=\"800\" H=\"80\" X=\"400\" /></S><D><P Y=\"0\" T=\"34\" P=\"0,0\" X=\"0\" C=\"719b9f\" /><T Y=\"320\" X=\"49\" /><P Y=\"320\" T=\"16\" X=\"224\" P=\"0,0\" /><P Y=\"319\" T=\"17\" X=\"311\" P=\"0,0\" /><P Y=\"284\" T=\"18\" P=\"1,0\" X=\"337\" C=\"57703e,e7c3d6\" /><P Y=\"284\" T=\"21\" X=\"294\" P=\"0,0\" /><P Y=\"134\" T=\"23\" X=\"135\" P=\"0,0\" /><P Y=\"320\" T=\"24\" P=\"0,1\" X=\"677\" C=\"46788e\" /><P Y=\"320\" T=\"26\" X=\"588\" P=\"1,0\" /><P Y=\"193\" T=\"14\" P=\"0,0\" X=\"562\" C=\"95311e,bde8f3,faf1b3\" /></D><O /></Z></C>"
                        self.mapYesVotes = 0
                        self.mapNoVotes = 0
                        self.mapPerma = 22
                        self.mapInverted = False

            elif self.is801Room or self.isVillage or self.isVillager:
                return 801

            elif self.isVanilla:
                self.mapCode = -1
                self.mapName = "Invalid";
                self.mapXML = "<C><P /><Z><S /><D /><O /></Z></C>"
                self.mapYesVotes = 0
                self.mapNoVotes = 0
                self.mapPerma = -1
                self.mapInverted = False
                map = random.choice(self.mapList)
                while map == self.currentMap:
                    map = random.choice(self.mapList)
                return map

            else:
                self.mapCode = -1
                self.mapName = "Invalid";
                self.mapXML = "<C><P /><Z><S /><D /><O /></Z></C>"
                self.mapYesVotes = 0
                self.mapNoVotes = 0
                self.mapPerma = -1
                self.mapInverted = False
                return self.selectMapStatus()
        return -1

    def selectMapStatus(self):
        maps = [0, -1, 4, 9, 5, 0, -1, 8, 6, 7]
        selectPerma = (17 if self.mapStatus % 2 == 0 else 7) if self.isRacing else (13 if self.mapStatus % 2 == 0 else 3) if self.isBootcamp else 18 if self.isDefilante else (11 if self.mapStatus == 0 else 10) if self.isSurvivor else 19 if self.isMusic and self.mapStatus % 2 == 0 else 0
        isMultiple = False

        if self.isNormRoom:
            if self.mapStatus < len(maps) and maps[self.mapStatus] != -1:
                isMultiple = maps[self.mapStatus] == 0
                selectPerma = maps[self.mapStatus]
            else:
                map = random.choice(self.mapList)
                while map == self.currentMap:
                    map = random.choice(self.mapList)
                return map

        elif self.isVanilla or (self.isMusic and self.mapStatus % 2 != 0):
            map = random.choice(self.mapList)
            while map == self.currentMap:
                map = random.choice(self.mapList)
            return map

        CursorMaps.execute("SELECT * FROM maps WHERE Perma = ? ORDER BY RANDOM() LIMIT 1", [random.choice([0, 1]) if isMultiple else selectPerma])
        rs = CursorMaps.fetchone()
        if rs:
           self.mapCode = rs["Code"]
           self.mapName = self.server.getPlayerName(rs["Builder"])
           self.mapXML = rs["XML"]
           self.mapYesVotes = rs["YesVotes"]
           self.mapNoVotes = rs["NoVotes"]
           self.mapPerma = rs["Perma"]
           self.mapInverted = self.autoMapFlipMode and random.randint(0, 100) > 85
        else:
           map = random.choice(self.mapList)
           while map == self.currentMap:
               map = random.choice(self.mapList)
           return map

        return -1

    def selectMapSpecificic(self, code, type):
        if type == "Vanilla":
            return int(code)

        elif type == "Custom":
            code = int(code)
            mapInfo = self.getMapInfo(code)
            if mapInfo[0] == None:
                return 0
            else:
                self.mapCode = code
                self.mapName = mapInfo[0]
                self.mapXML = mapInfo[1]
                self.mapYesVotes = mapInfo[2]
                self.mapNoVotes = mapInfo[3]
                self.mapPerma = mapInfo[4]
                self.mapInverted = False
                return -1

        elif type == "Perm":
            mapList = []
            CursorMaps.execute("select Code from Maps where Perma = ? and Code != ? order by random() limit 1", [code, self.currentMap])
            runMap = CursorMaps.fetchone()
            runMap = 0 if runMap == None else runMap[0]

            if runMap == 0:
                map = random.choice(self.MapList)
                while map == self.currentMap:
                    map = random.choice(self.MapList)
                return map
            else:
                mapInfo = self.getMapInfo(runMap)
                self.mapCode = runMap
                self.mapName = mapInfo[0]
                self.mapXML = mapInfo[1]
                self.mapYesVotes = mapInfo[2]
                self.mapNoVotes = mapInfo[3]
                self.mapPerma = mapInfo[4]
                self.mapInverted = False
                return -1

        elif type == "Xml":
            self.mapCode = 0
            self.mapName = "#Module"
            self.mapXML = str(code)
            self.mapYesVotes = 0
            self.mapNoVotes = 0
            self.mapPerma = 22
            self.mapInverted = False
            return -1

    def getMapInfo(self, mapCode):
        mapInfo = ["", "", 0, 0, 0]
        CursorMaps.execute("SELECT * FROM maps WHERE Code = ?", [mapCode])
        rs = CursorMaps.fetchone()
        if rs:
            mapInfo = self.server.getPlayerName(rs["Builder"]), rs["XML"], rs["YesVotes"], rs["NoVotes"], rs["Perma"]
        return mapInfo

    def checkIfTooFewRemaining(self):
        return len(list(filter(lambda player: not player.isDead, self.clients.values()))) <= 2

    def getAliveCount(self):
        return len(list(filter(lambda player: not player.isDead, self.clients.values())))

    def getDeathCountNoShaman(self):
        return len(list(filter(lambda player: not player.isShaman and not player.isDead and not player.isNewPlayer, self.clients.values())))

    def getHighestScore(self):
        playerScores = []
        playerID = 0
        for player in self.clients.copy().values():
            playerScores.append(player.playerScore)

        for player in self.clients.copy().values():
            if player.playerScore == max(playerScores):
                playerID = player.playerCode
        return playerID

    def getSecondHighestScore(self):
        playerScores = []
        playerID = 0
        for player in self.clients.copy().values():
            playerScores.append(player.playerScore)
        playerScores.remove(max(playerScores))

        if len(playerScores) >= 1:
            for player in self.clients.copy().values():
                if player.playerScore == max(playerScores):
                    playerID = player.playerCode
        return playerID

    def getShamanCode(self):
        if self.currentShamanCode == -1:
            if self.currentMap in self.noShamanMaps or self.isNoShamanMap or self.noShaman:
                pass
            else:
                if self.forceNextShaman > 0:
                    self.currentShamanCode = self.forceNextShaman
                    self.forceNextShaman = 0
                else:
                    self.currentShamanCode = self.getHighestScore()

            if self.currentShamanCode == -1:
                self.currentShamanName = ""
            else:
                for player in self.clients.copy().values():
                    if player.playerCode == self.currentShamanCode:
                        self.currentShamanName = player.playerName
                        self.currentShamanType = player.shamanType
                        self.currentShamanSkills = player.playerSkills
                        break
        return self.currentShamanCode

    def getDoubleShamanCode(self):
        if self.currentShamanCode == -1 and self.currentSecondShamanCode == -1:
            if self.forceNextShaman > 0:
                self.currentShamanCode = self.forceNextShaman
                self.forceNextShaman = 0
            else:
                self.currentShamanCode = self.getHighestScore()

            if self.currentSecondShamanCode == -1:
                self.currentSecondShamanCode = self.getSecondHighestScore()

            if self.currentSecondShamanCode == self.currentShamanCode:
                tempClient = random.choice(list(self.clients.values()))
                self.currentSecondShamanCode = tempClient.playerCode

            for player in self.clients.copy().values():
                if player.playerCode == self.currentShamanCode:
                    self.currentShamanName = player.playerName
                    self.currentShamanType = player.shamanType
                    self.currentShamanSkills = player.playerSkills
                    break

                if player.playerCode == self.currentSecondShamanCode:
                    self.currentSecondShamanName = player.playerName
                    self.currentSecondShamanType = player.shamanType
                    self.currentSecondShamanSkills = player.playerSkills
                    break

        return [self.currentShamanCode, self.currentSecondShamanCode]

    def closeVoting(self):
        self.initVotingMode = False
        self.isVotingBox = False
        if self.voteCloseTimer != None: self.voteCloseTimer.cancel()
        self.mapChange()

    def killShaman(self):
        for player in self.clients.copy().values():
            if player.playerCode == self.currentShamanCode:
                player.isDead = True
                player.sendPlayerDied()
        self.checkChangeMap()

    def killAfk(self):
        if self.isEditor or self.isTotemEditor or self.isBootcamp or self.isTribeHouseMap or self.disableAfkKill:
            return

        if ((Utils.getTime() - self.gameStartTime) < 32 and (Utils.getTime() - self.gameStartTime) > 28):
            for player in self.clients.copy().values():
                if not player.isDead and player.isAfk:
                    player.isDead = True
                    if not self.noAutoScore: player.playerScore += 1
                    player.sendPlayerDied()
            self.checkChangeMap()

    def checkIfDoubleShamansAreDead(self):
        player1 = self.clients.get(self.currentShamanName)
        player2 = self.clients.get(self.currentSecondShamanName)
        return (False if player1 == None else player1.isDead) and (False if player2 == None else player2.isDead)

    def checkIfShamanIsDead(self):
        player = self.clients.get(self.currentShamanName)
        return False if player == None else player.isDead

    def checkIfShamanCanGoIn(self):
        for player in self.clients.copy().values():
            if player.playerCode != self.currentShamanCode and player.playerCode != self.currentSecondShamanCode and not player.isDead:
                return False
        return True

    def giveShamanSave(self, shamanName, type):
        if not self.countStats:
            return

        player = self.clients.get(shamanName)
        if player != None:
            if type == 0:
                player.shamanSaves += 1
            elif type == 1:
                player.hardModeSaves += 1
            elif type == 2:
                player.divineModeSaves += 1
            if player.privLevel.notin(0):
                counts = [player.shamanSaves, player.hardModeSaves, player.divineModeSaves]
                titles = [self.server.shamanTitleList, self.server.hardModeTitleList, self.server.divineModeTitleList]
                rebuilds = ["shaman", "hardmode", "divinemode"]
                if counts[type] in titles[type]:
                    title = titles[type][counts[type]]
                    player.checkAndRebuildTitleList(rebuilds[type])
                    player.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
                    player.sendCompleteTitleList()
                    player.sendTitleList()

    def respawnMice(self):
        for player in self.clients.copy().values():
            if player.isDead:
                player.isDead = False
                player.playerStartTimeMillis = time.time()
                self.sendAll(Identifiers.send.Player_Respawn, ByteArray().writeBytes(player.getPlayerData()).writeBoolean(False).writeBoolean(True).toByteArray())

                if self.luaRuntime != None:
                    self.luaRuntime.emit("PlayerRespawn", (player.playerName))

        if self.autoRespawn or self.isTribeHouseMap:
            self.autoRespawnTimer = self.server.loop.call_later(2, self.respawnMice)

    def respawnSpecific(self, playerName):
        player = self.clients.get(playerName)
        if player != None and player.isDead:
            player.resetPlay()
            player.isAfk = False
            player.playerStartTimeMillis = time.time()
            self.sendAll(Identifiers.send.Player_Respawn, ByteArray().writeBytes(player.getPlayerData()).writeBoolean(False).writeBoolean(True).toByteArray())

            if self.luaRuntime != None:
                self.luaRuntime.emit("PlayerRespawn", (player.playerName))

    def sendMulodromeRound(self):
        self.sendAll(Identifiers.send.Mulodrome_Result, ByteArray().writeByte(self.mulodromeRoundCount).writeShort(self.blueCount).writeShort(self.redCount).toByteArray())
        if self.mulodromeRoundCount > 10:
            self.sendAll(Identifiers.send.Mulodrome_End)
            self.sendAll(Identifiers.send.Mulodrome_Winner, ByteArray().writeByte(2 if self.blueCount == self.redCount else (1 if self.blueCount < self.redCount else 0)).writeShort(self.blueCount).writeShort(self.redCount).toByteArray())
            self.isMulodrome = False
            self.mulodromeRoundCount = 0
            self.redCount = 0
            self.blueCount = 0
            self.redTeam = []
            self.blueTeam = []
            self.isRacing = False
            self.never20secTimer = False
            self.noShaman = False

    def checkMapXML(self):
        if int(self.currentMap) in self.server.vanillaMaps:
            self.mapCode = int(self.currentMap)
            self.mapName = "_Atelier 801" if self.mapCode == 801 else "Transformice"
            self.mapXML = str(self.server.vanillaMaps[int(self.currentMap)])
            self.mapYesVotes = 0
            self.mapNoVotes = 0
            self.mapPerma = 41
            self.currentMap = -1
            self.mapInverted = False

    def sendVampireMode(self):
        player = self.clients.get(self.currentSyncName)
        if player != None:
            player.sendVampireMode(False)

    def bindKeyBoard(self, playerName = "", key = 32, down = False, yes = True):
        if playerName is None:
            playerName = ""
        if key is None:
            key = 32
        if down is None:
            down = False
        if yes is None:
            yes = True
        if playerName == "":
            self.sendAll(Identifiers.send.Bind_Key_Board, ByteArray().writeShort(key).writeBoolean(down).writeBoolean(yes).toByteArray())
            return
        player = self.clients.get(playerName)
        if player != None:
            player.sendPacket(Identifiers.send.Bind_Key_Board, ByteArray().writeShort(key).writeBoolean(down).writeBoolean(yes).toByteArray())

    def addPhysicObject(self, id, x, y, bodyDef):
        self.sendAll(Identifiers.send.Add_Physic_Object, ByteArray().writeShort(id).writeBoolean(bool(bodyDef["dynamic"]) if "dynamic" in bodyDef else False).writeByte(int(bodyDef["type"]) if "type" in bodyDef else 0).writeShort(x).writeShort(y).writeShort(int(bodyDef["width"]) if "width" in bodyDef else 0).writeShort(int(bodyDef["height"]) if "height" in bodyDef else 0).writeBoolean(bool(bodyDef["foreground"]) if "foreground" in bodyDef else False).writeShort(int(bodyDef["friction"]) if "friction" in bodyDef else 0).writeShort(int(bodyDef["restitution"]) if "restitution" in bodyDef else 0).writeShort(int(bodyDef["angle"]) if "angle" in bodyDef else 0).writeBoolean("color" in bodyDef).writeInt(int(bodyDef["color"]) if "color" in bodyDef else 0).writeBoolean(bool(bodyDef["miceCollision"]) if "miceCollision" in bodyDef else True).writeBoolean(bool(bodyDef["groundCollision"]) if "groundCollision" in bodyDef else True).writeBoolean(bool(bodyDef["fixedRotation"]) if "fixedRotation" in bodyDef else False).writeShort(int(bodyDef["mass"]) if "mass" in bodyDef else 0).writeShort(int(bodyDef["linearDamping"]) if "linearDamping" in bodyDef else 0).writeShort(int(bodyDef["angularDamping"]) if "angularDamping" in bodyDef else 0).writeBoolean(False).writeUTF("").toByteArray())

    def removeObject(self, objectId):
        if objectId == None: objectId = 0
        self.sendAll(Identifiers.send.Remove_Object, ByteArray().writeInt(objectId).writeBoolean(True).toByteArray())

    def movePlayer(self, playerName, xPosition, yPosition, pOffSet=False, xSpeed=0, ySpeed=0, sOffSet=False):
        if pOffSet is None:
            pOffSet = False
        if xSpeed is None:
            xSpeed = 0
        if ySpeed is None:
            ySpeed = 0
        if sOffSet is None:
            sOffSet = False
        player = self.clients.get(playerName)
        if player != None:
            player.sendPacket(Identifiers.send.Move_Player, ByteArray().writeShort(xPosition).writeShort(yPosition).writeBoolean(pOffSet).writeShort(xSpeed).writeShort(ySpeed).writeBoolean(sOffSet).toByteArray())

    def setNameColor(self, playerName, color):
        if playerName in self.clients:
            self.sendAll(Identifiers.send.Set_Name_Color, ByteArray().writeInt(self.clients.get(playerName).playerCode).writeInt(color).toByteArray())

    def bindMouse(self, playerName, yes = True):
        player = self.clients.get(playerName)
        if player != None:
            player.sendPacket(Identifiers.send.Bind_Mouse, ByteArray().writeBoolean(yes).toByteArray())

    def addPopup(self, id, type, text, targetPlayer, x, y, width, fixedPos):
        p = ByteArray().writeInt(id).writeByte(type).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeBoolean(fixedPos)
        if targetPlayer == "":
            self.sendAll(Identifiers.send.Add_Popup, p.toByteArray())
        else:
            player = self.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Add_Popup, p.toByteArray())
    def addPopupNew(self, question="", popupID=0, targetPlayer="", _class="", small=True, big=False):
        if small:
            p = ByteArray().writeByte(1).writeUTF(_class).writeInt(popupID).writeBoolean(big).writeBoolean(big).writeUTF(question).toByteArray()
        else:
            p = ByteArray().writeByte(2).writeInt(popupID).writeByte(int(big)).writeInt(popupID).writeUTF(question).writeUTF(question).toByteArray()
        if targetPlayer == "":
            self.sendAll([100,50], p)
        else:
            player = self.clients.get(targetPlayer)
            if player != None:
                player.sendPacket([100,50], p)



    def addTextArea(self, id, text, targetPlayer, x, y, width, height, backgroundColor, borderColor, backgroundAlpha, fixedPos):
        p = ByteArray().writeInt(id).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeShort(height).writeInt(backgroundColor).writeInt(borderColor).writeByte(100 if backgroundAlpha > 100 else backgroundAlpha).writeBoolean(fixedPos)
        if targetPlayer == "":
            self.sendAll(Identifiers.send.Add_Text_Area, p.toByteArray())
        else:
            client = self.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Add_Text_Area, p.toByteArray())

    def removeTextArea(self, id, targetPlayer):
        p = ByteArray().writeInt(id)
        if targetPlayer == "":
            self.sendAll(Identifiers.send.Remove_Text_Area, p.toByteArray())
        else:
            client = self.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Remove_Text_Area, p.toByteArray())

    def updateTextArea(self, id, text, targetPlayer):
        p = ByteArray().writeInt(id).writeUTF(text)
        if targetPlayer == "":
            self.sendAll(Identifiers.send.Update_Text_Area, p.toByteArray())
        else:
            client = self.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Update_Text_Area, p.toByteArray())

    def showColorPicker(self, id, targetPlayer, defaultColor, title):
        packet = ByteArray().writeInt(id).writeInt(defaultColor).writeUTF(title)
        if targetPlayer == "":
            self.sendAll(Identifiers.send.Show_Color_Picker, packet.toByteArray())
        else:
            player = self.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Show_Color_Picker, packet.toByteArray())

    def startSnowSchedule(self, power):
        if self.isSnowing:
            self.startSnow(0, power, False)

    def startSnow(self, millis, power, enabled):
        self.isSnowing = enabled
        self.sendAll(Identifiers.send.Snow, ByteArray().writeBoolean(enabled).writeShort(power).toByteArray())
        if enabled:
            self.endSnowTimer = self.server.loop.call_later(millis, lambda: self.startSnowSchedule(power))

    def addImage(self, imageName = "", target = "", xPosition = 50, yPosition = 50, targetPlayer = ""):
        if imageName is None:
            imageName = ""
        if target is None:
            target = ""
        if xPosition is None:
            xPosition == 50
        if yPosition is None:
            yPosition = 50
        if targetPlayer is None:
            targetPlayer = ""
        packet = ByteArray()
        self.lastImageID += 1
        packet.writeInt(self.lastImageID)
        packet.writeUTF(imageName)
        packet.writeByte(1 if target.startswith("#") else 2 if target.startswith("$") else 3 if target.startswith("%") else 4 if target.startswith("?") else 5 if target.startswith("_") else 6 if target.startswith("!") else 7 if target.startswith("&") else 0)
        target = target[1:]
        packet.writeInt(int(target) if target.isdigit() else self.server.getPlayerCode(Utils.parsePlayerName(target)))
        packet.writeShort(xPosition)
        packet.writeShort(yPosition)
        if targetPlayer == "":
            self.sendAll(Identifiers.send.Add_Image, packet.toByteArray())
        else:
            player = self.clients.get(Utils.parsePlayerName(targetPlayer))
            if player != None:
                player.sendPacket(Identifiers.send.Add_Image, packet.toByteArray())

    def giveSurvivorStats(self, increment = 1):
        for player in self.clients.copy().values():
            if not player.isNewPlayer:
                player.survivorStats[0] += increment
                if player.isShaman:
                    player.survivorStats[1] += increment
                    player.survivorStats[2] += self.getDeathCountNoShaman()
                elif not player.isDead:
                    player.survivorStats[3] += increment

                i = 0
                while i < 3:
                    playerStat = player.survivorStats[i]
                    serverStat = self.server.statsPlayer["racingCount"][i]
                    if playerStat % serverStat > (playerStat + increment) % serverStat:
                        player.parseShop.sendUnlockedBadge(self.server.statsPlayer["survivorBadges"][i])
                        player.shopBadges.append(self.server.statsPlayer["survivorBadges"][i])
                        player.parseShop.checkAndRebuildBadges()
                    i += 1

    def giveRacingStats(self, increment = 1):
        for player in self.clients.copy().values():
            if not player.isNewPlayer:
                player.racingStats[0] += increment
                if player.hasCheese or player.hasEnter:
                    player.racingStats[1] += increment
                if player.hasEnter:
                    if player.currentPlace <= 3:
                        player.racingStats[2] += increment
                    if player.currentPlace == 1:
                        player.racingStats[3] += increment

                i = 0
                while i < 3:
                    playerStat = player.racingStats[i]
                    serverStat = self.server.statsPlayer["racingCount"][i]
                    if playerStat % serverStat > (playerStat + increment) % serverStat:
                        player.parseShop.sendUnlockedBadge(self.server.statsPlayer["racingBadges"][i])
                        player.shopBadges.append(self.server.statsPlayer["racingBadges"][i])
                        player.parseShop.checkAndRebuildBadges()
                    i += 1
    
    def giveDefilanteStats(self, increment = 1):
        for player in self.clients.copy().values():
            if not player.isNewPlayer:
                player.defilanteStats[0] += increment
                if player.hasCheese or player.hasEnter:
                    player.defilanteStats[1] += increment
                player.defilanteStats[2] += player.defilantePoints
                
                i = 0
                while i < 2:
                    playerStat = player.racingStats[i]
                    serverStat = self.server.statsPlayer["defilanteCount"][i]
                    if playerStat % serverStat > (playerStat + increment) % serverStat:
                        player.sendUnlockedBadge(self.server.statsPlayer["defilanteCount"][i])
                        player.shopBadges.append(self.server.statsPlayer["defilanteCount"][i])
                        player.checkAndRebuildBadges()
                    i += 1

    def send20SecRemainingTimer(self):
        if not self.changed20secTimer:
            if not self.never20secTimer and self.roundTime + (self.gameStartTime - Utils.getTime()) > 21:
                self.changed20secTimer = True
                self.changeMapTimers(20)
                for player in self.clients.copy().values():
                    player.sendRoundTime(20)

    def changeMapTimers(self, seconds):
        if self.changeMapTimer != None: self.changeMapTimer.cancel()
        self.changeMapTimer = self.server.loop.call_later(seconds, self.mapChange)

    def newConsumableTimer(self, code):
        self.roomTimers.append(self.server.loop.call_later(10, lambda: self.sendAll(Identifiers.send.Remove_Object, ByteArray().writeInt(code).writeBoolean(False).toByteArray())))

def invertDict(_dict):
    return {v: k for k, v in _dict.items()}
    
if __name__ == "__main__":
    # Connection MySQL Players Database
    Database, Cursor = None, None
    Database = pymysql.connect(host="127.0.0.1",user="root",password="",db="micejewels")
    Database.isolation_level = None 
    Cursor = Database.cursor()
    Database.autocommit(True)

    # Connection SQLite Cafe Database
    DatabaseCafe, CursorCafe = None, None
    DatabaseCafe = sqlite3.connect("./database/Cafe1.db", check_same_thread = False)
    DatabaseCafe.text_factory = str
    DatabaseCafe.isolation_level = None
    DatabaseCafe.row_factory = sqlite3.Row
    CursorCafe = DatabaseCafe.cursor()

    # Connection SQLite Maps Database
    DatabaseMaps, CursorMaps = None, None
    DatabaseMaps = sqlite3.connect("./database/Maps.db", check_same_thread = False)
    DatabaseMaps.text_factory = str
    DatabaseMaps.isolation_level = None
    DatabaseMaps.row_factory = sqlite3.Row
    CursorMaps = DatabaseMaps.cursor()

    # Connection Server
    _Server = Server()
