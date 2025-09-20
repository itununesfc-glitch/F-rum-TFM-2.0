#coding: utf-8
import re

# Modules
from ByteArray import ByteArray
from Identifiers import Identifiers

# Utils
from utils import *
from Exceptions import *

from datetime import datetime

class ParseCommands:
    def __init__(self, client, server):
        self.client = client
        self.server = client.server
        self.Cursor = client.Cursor
        self.currentArgsCount = 0

    def requireLevel(self, level=0, inPrivs=False, can=None):
        if (can != None and not can) or self.client.privLevel.lower(level, False):
            raise UserWarning("Not enough authorithy")

    def requireVip(self):
        if self.client.vipTime < 1 and not self.client.privLevel.uppermost() > 2:
            raise UserWarning("Only VIP players can use this command.")

    def requireNoGuest(self, playerName):
        if playerName.startswith("*"):
            raise UserWarning("Target player is guest.")

    def requireArgs(self, argsCount):
        if self.currentArgsCount < argsCount:
            raise UserWarning("Not enough arguments")

    def requireTribe(self, canUse=False, tribePerm=8, minLevel=8):
        if (not (not(not self.client.tribeName == "" and self.client.room.isTribeHouse and tribePerm != -1 and self.client.tribeRanks[self.client.tribeRank].split("|")[2].split(",")[tribePerm] == "1"))) and self.client.privLevel.lower(minLevel):
            raise UserWarning("Not enough tribe permitions")

    def parseCommand(self, command):
        values = command.split(" ")
        command = values[0].lower()
        args = values[1:]
        argsCount = len(args)
        argsNotSplited = " ".join(args)
        self.currentArgsCount = argsCount

        if command in ["profil", "perfil", "profile"]:
            self.client.sendProfile(self.client.playerName if argsCount == 0 else Utils.parsePlayerName(args[0]))

        elif command in ["editeur"]:
            self.client.enterRoom("\x03[Editeur] " + self.client.playerName)
            self.client.sendPacket(Identifiers.old.send.Map_Editor, [])
            self.client.sendPacket(Identifiers.send.Room_Type, b"\x01")
        
        elif command in ["profilecolortemp"]:
             self.requireLevel(10)
             self.client.colorProfileCC = args[0]
        
        elif command in ["verification"]:
             self.requireNoGuest(self.client.playerName)
             if self.client.verifed:
                 self.client.sendMessage("Aleardy verifed!")
                 return
             argser = ["a", "b", "c", "d", "f", "g", "e","A","B","C","D","E","F","G","h","H","i","I","K","k","O","o"]
             code = ""
             x = 0
             while x < 20:
                  code += random.choice(argser)
                  x +=1
             code = str(code)
             self.server.codesVerifi[code] = self.client.playerName + self.client.playerTag
             self.client.sendMessage(f"Please go discord server and use this command: <BG>!verify {code}</BG>")
             self.client.verifed = True
        
        elif command in ["rmverifcationere"]:
             self.client.verifed = False

        elif command in ["smc"]:
            self.requireLevel(10)
            for player in self.server.players.copy().values():
                player.sendMessage("<VP>[%s] [%s] %s" % (self.client.langue, self.client.playerName, argsNotSplited))

        elif command in ["mfc"]:
            if self.client.privLevel.includes(5) and self.client.room.isFuncorp:
                for player in self.client.room.clients.copy().values():
                    player.sendMessage("<FC>[%s] [%s] %s" % ("FunCorp", self.client.playerName, argsNotSplited))
        
        elif command in ["shop"]:
            self.client.shopPanel.openPanel()

        elif command in ["inv"]:
            self.requireArgs(1)
            if self.client.room.isTribeHouse:
                playerName = Utils.parsePlayerName(args[0])
                player = self.server.players.get(playerName)
                if player and player.tribeName != self.client.tribeName: 
                    player = self.server.players.get(playerName)
                    player.invitedTribeHouses.append(self.client.tribeName)
                    player.sendPacket(Identifiers.send.Tribe_Invite, ByteArray().writeUTF(self.client.playerName).writeUTF(self.client.tribeName).toByteArray())
                    self.client.sendLangueMessage("", f"$InvTribu_InvitationEnvoyee",  f"<V>{playerName}</V>")

        elif command in ["invkick"]:
            self.requireArgs(1)
            if self.client.room.isTribeHouse and self.client.tribeCode != 0:
                playerName = Utils.parsePlayerName(args[0])
                if self.server.checkConnectedAccount(playerName):
                    player = self.server.players.get(playerName)
                    if player and self.client.tribeName in player.invitedTribeHouses:
                        player.invitedTribeHouses.remove(self.client.tribeName)
                        self.client.sendLangueMessage("", "$InvTribu_AnnulationEnvoyee", f"<V>{player.playerName}</V>")
                        player.sendLangueMessage("", "$InvTribu_AnnulationRecue", f"<V>{self.client.tribeName}</V>")
                        if player.roomName == "*\x03%s" %(self.client.tribeName):
                            player.enterRoom(self.server.recommendRoom(self.client.langue))

        elif command in ["mapname"]:
            if argsCount == 1:
                self.requireLevel(11)
                playerName = Utils.parsePlayerName(args[0])
                self.client.room.CursorMaps.execute("update Maps set Name = ?", [playerName])
                self.server.sendStaffMessage(6, f"[MAP] <J>All</J> maps' new owner is <V>{playerName}</V> from now on.")
            if argsCount == 2:
                if self.client.privLevel.includes(5):
                    mapCode = int(args[0])
                    playerName = Utils.parsePlayerName(args[0])
                    if mapCode.isdigit():
                        mapInfo = self.client.room.getMapInfo(int(mapCode[1:]))
                        if mapInfo[0] == None:
                            self.client.sendLangueMessage("", "$CarteIntrouvable")
                        else:
                            self.client.room.CursorMaps.execute("update Maps set Name = ? where Code = ?", [playerName, mapCode])
                            self.server.sendStaffMessage(6, f"[MAP] The map <J>@{mapCode}</J>' new owner is <V>{playerName}</V> from now on.")

        elif command in ["msg"]:
            self.requireLevel(8)
            self.client.room.sendMessage("", f"<ROSE>[$Moderation] {argsNotSplited}")

        elif command in ["rank"]:
            self.requireLevel(10)
            self.client.others.modules["privPanel"].openPanel()

        elif command in ["chatlog"]:
            if self.client.privLevel.upper(3):
                self.client.modoPwet.openChatLog(Utils.parsePlayerName(args[0]))

        elif command in ["totem"]:
            self.requireLevel(1)
            if self.client.shamanSaves >= 500:
                self.client.enterRoom(chr(3) + "[Totem] " + self.client.playerName)

        elif command in ["luaadmin"]:
            self.requireLevel(11)
            self.client.luaadmin = not self.client.luaadmin
            self.client.sendMessage(f"You're {'no longer ' if not self.client.luaadmin else ''}running python scrips in lua.")

        elif command in ["sauvertotem"]:
            if self.client.room.isTotemEditor:
                self.client.totem[0] = self.client.tempTotem[0]
                self.client.totem[1] = self.client.tempTotem[1]
                self.client.sendPlayerDied()
                self.client.enterRoom(self.server.recommendRoom(self.client.langue))

        elif command in ["mgive", "reward"]:
            self.requireLevel(8)
            self.requireLevel(2)
            if argsCount == 2:
                self.client.addConsumable(*map(int, args))
            else:
                playerName = Utils.parsePlayerName(args[0])
                args = args[1:]
                player = self.server.players.get(playerName)
                if player:
                    player.addConsumable(*map(int, args))
                    if command == "mgive":
                        player.sendMessage(f"<r>{self.client.playerName} <v>gave you consumables.")
        
        elif command in ["giveplus"]:
            self.requireArgs(1)
            self.requireLevel(10)
            player = self.server.players.get(args[0])
            if "+" in args[0]:
                 return
            if player != None:
                 player.shopPanel.buyPlus("yes")
            else:
                 playerName = args[0]
                 self.Cursor.execute("update users set playername = %s where playername = %s", ["+" + playerName, playerName])
            self.client.sendMessage("Done!")

        elif command in ["unlocktlt"]:
            self.requireArgs(1)
            self.requireLevel(10)
            if argsCount == 1:
                title = int(args[0])
                if title + 0.1 in self.client.titleList:
                    self.client.sendMessage("You Aleardy have this title!")
                    return
                self.client.titleList.append(title + 0.1)
                self.client.specialTitleList = self.client.specialTitleList + [title + 0.1]
                self.client.sendUnlockedTitle(title, 1)
            else:
                playerName = Utils.parsePlayerName(args[0])
                title = int(args[1])
                if playerName == "*":
                    for player in self.client.room.clients.copy().values():
                        if title + 0.1 in player.titleList:
                             #self.client.sendMessage("Player aleardy have this title!")
                             t = 1
                        else:
                             player.titleList.append(title + 0.1)
                             player.specialTitleList = player.specialTitleList + [title + 0.1]
                             player.sendUnlockedTitle(title, 1)
                             player.sendMessage(f"<font color='#ff0000'>EVENT</font> gived you a free title :D")
                    return

                if self.server.checkConnectedAccount(playerName):
                    player = self.server.players.get(playerName)
                    if title + 0.1 in player.titleList:
                        self.client.sendMessage("Player aleardy have this title!")
                        return
                    player.titleList.append(title + 0.1)
                    player.specialTitleList = player.specialTitleList + [title + 0.1]
                    player.sendUnlockedTitle(title, 1)
                    player.sendMessage(f"{self.client.playerName} gived you a free title :D")
        
        elif command in ["removetl"]:
            self.requireArgs(1)
            self.requireLevel(10)
            if argsCount == 1:
                title = int(args[0])
                if not title + 0.1 in self.client.specialTitleList:
                    self.client.sendMessage("You not have the title!")
                    return
                self.client.titleList.remove(title + 0.1)
                self.client.specialTitleList.remove(title + 0.1)
                #self.client.sendUnlockedTitle(title, 1)
                self.client.sendMessage(f"Removed you title $T_{title} :D")

            else:
                playerName = Utils.parsePlayerName(args[0])
                title = int(args[1])
                if self.server.checkConnectedAccount(playerName):
                    player = self.server.players.get(playerName)
                    if not title + 0.1 in player.specialTitleList:
                        self.client.sendMessage("Player not have the title!")
                        return
                    player.titleList.remove(title + 0.1)
                    player.specialTitleList.remove(title + 0.1)
                    #player.sendUnlockedTitle(title, 1)
                    player.sendMessage(f"{self.client.playerName} removed you title $T_{title} :D")
                else: self.client.sendMessage("Player not online!")


        elif command in ["resettotem"]:
            if self.client.room.isTotemEditor:
                self.client.totem = [0 , ""]
                self.client.tempTotem = [0 , ""]
                self.client.resetTotem = True
                self.client.isDead = True
                self.client.sendPlayerDied()
                self.client.room.checkChangeMap()

        elif command in ["tag"]:
            self.requireLevel(1)
            if argsCount == 0:
                tag = ""
            else:
                tag = argsNotSplited
                isVip = self.client.vipTime > 0
                if tag.startswith("#"):
                    tag = tag[1:]
                if not tag.isdigit() and not isVip:
                    self.client.sendMessage("You can only use numbers in your tag.")
                    return
                if len(tag) > 4 and not isVip:
                    self.client.sendMessage("You can only use 4 numbers for your tag.")
                    return
                elif isVip and len(tag) > 20:
                    self.client.sendMessage("You can only use 20 characters for your tag.")
                    return
                tag = "#" + tag

            if "'" in tag or '"' in tag:
                self.client.sendMessage("Tag includes invalid characters (<r>%s</r>)" % ("'" if "'" in tag else '"'))
                return

            if tag == "#":
                tag = ""
                args = []
            if tag == self.client.cacheTag:
                self.client.sendMessage(f"Your tag is already <r>{tag}")
                return

            self.client.cacheTag = tag
            self.client.sendMessage({True: "Your tag has been removed successfully. Please re-login.", False: f"Your tag has changed. New tag: <r>{tag}</r>. Please re-login."}[argsCount == 0])

        elif command in ["setvip"]:
            self.requireLevel(8)
            self.requireArgs(2)
            playerName, days = Utils.parsePlayerName(args[0]), args[1]
            if not args[1].isdigit():
                self.client.sendMessage("Argument 1 must be a number")
            else:
                days = int(days)
                self.server.setVip(playerName, days)

        elif command in ["changetag"]:
            self.requireLevel(8)
            self.requireArgs(1)
            if argsCount == 1:
                playerName = args[0]
                tag = ""
            else:
                playerName, tag = argsNotSplited.split(" ", 1)
                if tag.startswith("#"):
                    tag = tag[1:]
                if len(tag) > 20:
                    self.client.sendMessage("Max. character length for tags is <r>20</r>.")
                    return
                tag = "#" + tag

            if tag == "#":
                tag = ""
                args = []
            playerName = Utils.parsePlayerName(playerName)
            player = self.server.players.get(playerName)
            if player != None:
                if player.cacheTag == tag:
                    self.client.sendMessage(f"Target's tag is already <r>{tag}")
                    return
                player.cacheTag = tag
                player.sendMessage({True: f"Your tag has been removed by <r>{self.client.playerName}</r>. Please re-login.", False: f"Your tag has changed by {self.client.playerName}. New tag: <r>{tag}</r>. Please re-login."}[argsCount == 1])

            self.client.sendMessage(f"The tag of the target player has been changed. New tag: <r>{tag}")

        elif command in ["ping"]:
            if argsCount == 0:
                self.requireLevel(1)
                self.client.sendClientMessage('ping ~'+str(self.client.PInfo[2]))
            elif argsCount == 1:
                self.requireLevel(8)
                playerName = Utils.parsePlayerName(args[0])
                player = self.server.players.get(playerName)
                if player != None:
                    self.client.sendClientMessage("<V>%s</V>' ping~ %s" %(playerName, player.PInfo[2]))
                else:
                    self.client.sendClientMessage("The player [<V>%s</V>] does not exists." % playerName)

        elif command in ["loginlog"]:
            self.requireLevel(8)
            self.requireArgs(1)
            if "." in args[0]:
                ipAdres = args[0]
                self.Cursor.execute("select * from loginlog where ip = %s order by Timestamp asc limit 0, 200", [ipAdres])
                rs = self.Cursor.fetchall()
                if rs:
                    msg = f"<p align='center'>Connection logs for ip<N2> {ipAdres}</N2>\n</p>"
                    for a in rs:
                        name, ip, text = a[0], a[1], a[2]
                        msg = msg + text
                    self.client.sendLogMessage(msg)
            else:
                playerName = Utils.parsePlayerName(args[0])
                self.Cursor.execute("select * from loginlog where username = %s order by Timestamp asc limit 0, 200", [playerName])
                rs = self.Cursor.fetchall()
                if rs:
                    msg = f"<p align='center'>Connection logs for player<N2> {playerName}</N2>\n</p>"
                    for a in rs:
                        name, ip, text = a[0], a[1], a[2]
                        msg = msg + text
                    self.client.sendLogMessage(msg)

        elif command in ["time", "temps"]:
            self.requireLevel(1)
            self.client.playTime += abs(Utils.getSecondsDiff(self.client.loginTime))
            self.client.loginTime = Utils.getTime()
            temps = map(int, [self.client.playTime // 86400, self.client.playTime // 3600 % 24, self.client.playTime // 60 % 60, self.client.playTime % 60])
            self.client.sendLangueMessage("", "$TempsDeJeu", *temps)

        elif command in ["ban", "iban"]:
            self.requireLevel(1)
            self.requireArgs(1)
            if self.client.privLevel.includes(3):
                playerName = Utils.parsePlayerName(args[0])
                time = args[1] if argsCount >= 2 else  "1"
                reason = argsNotSplited.split(" ", 2)[2] if argsCount >= 3 else ""
                silent = command == "iban"
                hours = int(time) if time.isdigit() else 1
                hours = 100000 if hours > 100000 else hours
                hours = 24 if (self.client.privLevel.upper(6) and hours > 24) else hours
                if playerName in self.server.OP:
                    return
                if self.server.banPlayer(playerName, hours, reason, self.client.playerID, silent):
                    self.server.sendStaffMessage(5, f"<V>{self.client.playerName}<BL> banned <V>{playerName}<BL> for <V>{hours}<BL> hours, reason: <V>{reason}<BL>.")
                    self.server.sendMessageDiscord(f"```{self.client.playerName} banned {playerName} for {hours} hours, reason: {reason}```")
                    self.server.saveCasierLog(playerName, "BAN", self.client.playerName, time, reason)
                else:
                    self.client.sendClientMessage(f"The player [{playerName}] does not exists.")
            else:
                playerName = Utils.parsePlayerName(args[0])
                self.server.voteBanPopulaire(playerName, self.client.playerName, self.client.ipAddress)
                self.server.sendMessageDiscord(f"```{self.client.playerName} voted {playerName} for ban```")
                self.client.sendBanConsideration()

        elif command in ["unbanip"]:
            if self.client.privLevel.includes(3):
                ip = args[0]
                if ip in self.server.IPPermaBanCache:
                    self.server.IPPermaBanCache.remove(ip)
                    self.Cursor.execute("delete from IPPermaBan where IP = %s", [ip])
                    self.server.sendStaffMessage(7, "<V>%s</V> unbanned the IP <V>%s</V>." %(self.client.playerName, ip))
                    self.server.sendMessageDiscord(f"```{self.client.playerName} unbanned the IP {ip}```")
                else:
                    self.client.sendClientMessage("self IP is not banned.")

        elif command in ["unban"]:
            if self.client.privLevel.includes(3):
                playerName = Utils.parsePlayerName(args[0])
                self.requireNoGuest(playerName)
                found = False
                if self.server.checkExistingUser(playerName):
                    if self.server.checkTempBan(playerName):
                        self.server.removeTempBan(playerName)
                        found = True
                    if self.server.checkPermaBan(playerName):
                        self.server.removePermaBan(playerName)
                        found = True
                    if found:
                        self.Cursor.execute("update Users set BanHours = %s where Username = %s", [0, playerName])
                        #self.Cursor.execute("insert into BanLog (Username, BannedBy, Time, Reason, Date, Status, IP) values (%s, %s, %s, %s, %s, %s, %s)", [playerName, self.client.playerName, "", "", "", "Unban", ""])
                        self.Cursor.execute("delete from BanLog where Username = %s", [playerName])
                        self.Cursor.execute("delete from userpermaban where Username = %s", [playerName])
                        self.Cursor.execute("delete from usertempban where Username = %s", [playerName])
                        if playerName in self.server.userPermaBanCache:
                             self.server.userPermaBanCache.remove(playerName)
                        self.server.saveCasierLog(playerName, "UNBAN", self.client.playerName, "", "")
                        self.server.sendStaffMessage(5, f"<V>{self.client.playerName}<N> unbanned the player <V>{playerName}<BL>.")
                        self.server.sendMessageDiscord(f"```{self.client.playerName} unbanned the player {playerName}```")

        elif command in ["casier", "log"]:
            if self.client.privLevel.upper(8) or self.client.privLevel.includes(3):
                playerName = Utils.parsePlayerName(args[0]) if argsCount > 0 else ""

                if playerName != "":
                    text = "<p align='center'><V>" + playerName + "</V>'s Sanction Logs\n\n"
                    self.Cursor.execute("select * from casierlog where Name = %s order by Timestamp desc limit 0, 200", [playerName])
                else:
                    text = "<p align='center'>Sanction Logs\n\n"
                    self.Cursor.execute("select * from casierlog order by Timestamp desc limit 0, 200")

                for rs in self.Cursor.fetchall():
                    name, state, timestamp, bannedBy, time, reason = rs[1], rs[2], rs[3], rs[4], rs[5], rs[6]
                    if not state.startswith("UN"):
                        if 'h' in timestamp:
                             timestamp.replace('h', '')
                       
                        startTime = str(datetime.fromtimestamp(float(int(timestamp))))
                        endTime = str(datetime.fromtimestamp(float(int(timestamp) + (int(time) * 60 * 60))))
                        try:bannedBy = self.server.getPlayerName(int(bannedBy))
                        except:pass
                        text += "<font size='12'><p align='left'>" + ("<J>" + name + "</J>" if playerName == "" else "") + " - <b><V>" + state + " "+time+"h by " + bannedBy + " : <BL>" + reason + "</BL>\n"
                        text += "<p align='left'><font size='9'><N2>    " + startTime + " -> " + endTime + " </N2>\n\n"
                    elif state.startswith("UN"):
                        text += "<font size='12'><p align='left'>" + ("<J>" + name + "</J>" if playerName == "" else "") + " - <b><V>" + state + " by " + bannedBy + "\n<br>"
                self.client.sendLogMessage(text)

        elif command in ["mute"]:
            if self.client.privLevel.includes(3) or self.client.privLevel.upper(8):
                playerName = Utils.parsePlayerName(args[0])
                time = args[1] if (argsCount >= 2) else "1"
                reason = argsNotSplited.split(" ", 2)[2] if (argsCount >= 3) else ""
                hours = int(time) if (time.isdigit()) else 1
                self.requireNoGuest(playerName)
                hours = 500 if (hours > 500) else hours
                hours = 24 if (self.client.privLevel.lower(7) and hours > 24) else hours
                hours = int(hours)
                self.server.mutePlayer(playerName, hours, reason, self.client.playerName)
                self.server.sendMessageDiscord(f"```{self.client.playerName} muted {playerName} for {hours} hours Reason: {reason}```")
                self.server.saveCasierLog(playerName, "MUTE", self.client.playerName, time, reason)
                if hours == 0:
                    self.server.removeModMute(playerName)

        elif command in ["unmute"]:
            if self.client.privLevel.includes(3):
                playerName = Utils.parsePlayerName(args[0])
                self.requireNoGuest(playerName)
                self.server.desmutePlayer(playerName, self.client.playerName)
                self.server.sendStaffMessage(5, "<V>%s</V> unmuted <V>%s</V>." %(self.client.playerName, playerName))
                self.server.sendMessageDiscord(f"```{self.client.playerName} unmuted {playerName}```")
                self.server.saveCasierLog(playerName, "UNMUTE", self.client.playerName, "", "")
                self.server.removeModMute(playerName)

        elif command in ["mousecolor"]:
            self.requireLevel(1)
            self.client.room.showColorPicker(10001, self.client.playerName, int(self.client.mouseColor, 16), "Select a color for your mouse body.")

        elif command in ["namecolor"]:
            if argsCount == 0:
                self.client.room.showColorPicker(10000, self.client.playerName, int(self.client.nameColor, 16) if not self.client.nameColor == "" else 0xc2c2da, "Select a color for your name.")
            if argsCount == 1:
                renk = args[0]
                if not renk.startswith("#"):
                    self.client.sendMessage("<V>[•]</V> Use hex code (#000000)")
                else:
                    self.client.nameColor = renk[1:7] ; self.client.sendMessage("<V>[•]</V> <font color='%s'>%s</font>" % (renk, "İsminizin rengini başarıyla değiştirdiniz. Yeni renk için sonraki turu bekleyin." if self.client.langue.lower() == "tr" else "You've changed color of your nickname successfully.\nWait next round for new color."))

        elif command in ["cc"]:
            self.requireLevel(8)
            if argsCount <= 1:
                dil = args[0].upper()
                dilid = Utils.getLangueID(dil)
                if dilid != None:
                    self.client.langue = dil
                    self.client.langueID = dilid
                    self.client.enterRoom(self.server.recommendRoom(dilid))
            else:
                playerName = Utils.parsePlayerName(args[0])
                player = self.server.players.get(playerName)
                if player != None:
                    dil = args[1].upper()
                    dilid = Utils.getLangueID(dil)
                    if dilid != None:
                        player.langue = dil
                        player.langueID = dilid
                        player.enterRoom(self.server.recommendRoom(dilid))

        elif command in ["pw"]:
            if self.client.room.roomName.startswith("*" + self.client.playerName) or self.client.room.roomName.startswith(self.client.playerName):
                if argsCount == 0:
                    self.client.room.roomPassword = ""
                    self.client.sendLangueMessage("", "$MDP_Desactive")
                else:
                    password = args[0]
                    self.client.room.roomPassword = password
                    self.client.sendLangueMessage("", "$Mot_De_Passe : " + password)

        elif command in ["hide"]:
            if self.client.isHidden == True:
                self.client.sendClientMessage("You're already hidden.")
            else:
                self.requireLevel(8)
                self.client.sendPlayerDisconnect()
                self.client.sendClientMessage("You're invisible.")
                self.client.isHidden = True
                self.server.hiddenPlayers[self.client.playerName] = self.client
                del self.server.players[self.client.playerName]

        elif command in ["unhide"]:
            self.requireLevel(8)
            if self.client.isHidden:
                del self.server.hiddenPlayers[self.client.playerName]
                self.server.players[self.client.playerName] = self.client
                self.client.sendClientMessage("You're no longer invisible.")
                self.client.isHidden = False
                self.client.enterRoom(self.client.room.name)

        elif command in ["reboot", "shutdown"]:
            self.requireLevel(11)
            self.server.sendServerRestart(0, 0)
            self.server.sendMessageDiscord(f":warning: The server will restart in 2 minutes.")

        elif command in ["updatesql"]:
            self.requireLevel(11)
            for client in self.client.room.clients.copy().values():
                if not client.isGuest:
                    client.updateDatabase()
            self.server.sendStaffMessage(7, f"Server database successfully updated by <ROSE>{self.client.playerName}</ROSE>.")

        elif command in ["kill", "suicide", "mort", "die"]:
            if not self.client.isDead and not self.client.room.disableMortCommand:
                self.client.isDead = True
                if not self.client.room.noAutoScore:
                    self.client.playerScore += 1
                self.client.sendPlayerDied()
                self.client.room.checkChangeMap()

        elif command in ["myip"]:
            self.client.sendClientMessage(f"Your IP address: {self.client.ipAddress}")

        elif command in ["sy?"]:
            self.requireLevel(5)
            self.client.sendLangueMessage("", "$SyncEnCours : [" + self.client.room.currentSyncName + "]")

        elif re.match("p\\d+(\\.\\d+)?", command):
            if self.client.privLevel.includes(7):
                mapCode = self.client.room.mapCode
                mapName = self.client.room.mapName
                currentCategory = self.client.room.mapPerma
                if mapCode != -1:
                    category = int(command[1:])
                    if category in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17, 18, 19, 22, 31, 41, 42, 44]:
                        self.server.sendStaffMessage(7, "[%s] @%s : %s -> %s" %(self.client.playerName, mapCode, currentCategory, category))
                        self.server.sendMessageDiscordMP("``` [%s] @%s : P%s -> P%s ```" %(self.client.playerName, mapCode, currentCategory, category))
                        self.client.room.CursorMaps.execute("update Maps set Perma = ? where Code = ?", [category, mapCode])

        elif re.match("lsp\\d+(\\.\\d+)?", command):
            if self.client.privLevel.includes(7):
                category = int(command[3:])
                if category in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17, 18, 19, 22, 31, 41, 42, 44]:
                    mapList = ""
                    mapCount = 0
                    self.client.room.CursorMaps.execute("select * from Maps where Perma = ? ORDER BY CODE ASC", [category])
                    for rs in self.client.room.CursorMaps.fetchall():
                        mapCount += 1
                        yesVotes = rs["YesVotes"]
                        noVotes = rs["NoVotes"]
                        totalVotes = yesVotes + noVotes
                        if totalVotes < 1: totalVotes = 1
                        rating = (1.0 * yesVotes // totalVotes) * 100
                        mapList += "\n<N>%s</N> - @%s - %s - %s%s - P%s" %(rs["Name"], rs["Code"], totalVotes, str(rating).split(".")[0], "%", rs["Perma"])

                    try: self.client.sendLogMessage("<font size=\"12\"><N>There is</N> <BV>%s</BV> <N>maps</N> <V>P%s %s</V></font>" %(mapCount, category, mapList))
                    except: self.client.sendClientMessage("<R>Too many maps.</R>")

        elif command in ["re", "respawn"]:
            if argsCount == 0:
                self.requireVip()
                if not self.client.canRespawn:
                    self.client.room.respawnSpecific(self.client.playerName)
                    self.client.canRespawn = True
                return

            self.requireLevel(8)
            playerName = Utils.parsePlayerName(args[0])
            if playerName in self.client.room.clients:
                self.client.room.respawnSpecific(playerName)

        elif command in ["clone"]:
            self.requireLevel(12)
            self.requireArgs(1)
            playerName = Utils.parsePlayerName(args[0])
            player = self.server.players.get(playerName)
            if player != None:
                player.isDead = True
                player.cloneData = [player.posX, player.posY]
                self.client.room.respawnSpecific(playerName)
                self.client.room.movePlayer(player.playerName, player.cloneData[0], player.cloneData[1], False, 0, 0, False)

        elif command in ["music", "musique"]:
            self.requireLevel(12)
           # self.requireTribe(True)
            if argsCount == 0:
                self.client.room.sendAll(Identifiers.old.send.Music, [])
            else:
                self.client.room.sendAll(Identifiers.old.send.Music, [args[0]])

        elif command in ["neige", "startsnow", "stopsnow"]:
            self.requireLevel(10)
            self.client.room.startSnow(1000, 60, not self.client.room.isSnowing)

        elif command in ["info"]:
            self.requireLevel(1)
            if self.client.room.mapCode != -1:
                totalVotes = self.client.room.mapYesVotes + self.client.room.mapNoVotes
                if totalVotes < 1:
                    totalVotes += 1
                rating = (1.0 * self.client.room.mapYesVotes // totalVotes) * 100
                self.client.sendClientMessage("<V>[•]</V> <V>" + self.client.room.mapName + "<BL> - <V>@" + str(self.client.room.mapCode) + "<BL> - <V>" + str(int(rating)) + "%<BL> - <V>P" + str(self.client.room.mapPerma))

        elif command in ["clearreports"]:
                self.requireLevel(10)
                self.server.reports = {"names": []}
                self.server.sendStaffMessage(7, "<V>%s</V> cleared all modopwet reports." %(self.client.playerName))

        elif command in ["clearcache"]:
            self.requireLevel(10)
            self.server.IPPermaBanCache = []
            self.server.sendStaffMessage(7, "<V>%s</V> cleared server cache." %(self.client.playerName))

        elif command in ["cleariptempban"]:
            self.requireLevel(10)
            self.server.IPTempBanCache = []
            self.server.sendStaffMessage(7, "<V>%s</V> cleared all ip temporary bans." %(self.client.playerName))

        elif command in ["clearlog"]:
            self.requireLevel(10)
            self.Cursor.execute("DELETE from banlog")
            self.client.sendClientMessage("<ROSE>Ban log successfully cleared.")

        elif command in ["log"]:
            self.requireLevel(8)
            playerName = Utils.parsePlayerName(args[0]) if argsCount > 0 else ""
            logList = []
            self.Cursor.execute("select * from BanLog order by Date desc limit 0, 200") if playerName == "" else self.Cursor.execute("select * from BanLog where Name = %s order by Date desc limit 0, 200", [playerName])
            r = self.Cursor.fetchall()
            for rs in r:
                if rs[5] == "Unban":
                    logList += rs[0], "", rs[1], "", "", rs[4].ljust(13, "0")
                else:
                    logList += rs[0], rs[7], rs[1], rs[2], rs[3], rs[4].ljust(13, "0")
            self.client.sendPacket(Identifiers.old.send.Log, logList)

        elif command in ["mod", "mapcrew"]:
                staff = {}
                staffList = "$ModoPasEnLigne" if command == "mod" else "$MapcrewPasEnLigne"
                control = [7] if command == "mapcrew" else [8,9]
                for player in self.server.players.copy().values():
                    if player.privLevel.uppermost() in control:
                        langue = player.langue.lower()
                        if langue in staff:
                            staff[langue].append(player.playerName)
                        else:
                            staff[langue] = []
                            staff[langue].append(player.playerName)
                            
                if len(staff) >= 1:
                    staffList = "$ModoEnLigne" if command == "mod" else "$MapcrewEnLigne"
                    for langue,names in staff.items():
                        staffList += "\n<BL>[%s]<BV> " % (langue)
                        staffList += "%s" %(("<BL>, <BV>").join(names))
                self.client.sendLangueMessage("", staffList)

        elif command in ["ls"]:
            self.requireLevel(7)
            data = []
            rooms = self.server.rooms.values()
            for room in rooms:
                if room.name.startswith("*") and not room.name.startswith("*" + chr(3)):
                    data.append(["ALL", room.name, room.getPlayerCount()])
                elif room.name.startswith(str(chr(3))) or room.name.startswith("*" + chr(3)):
                    if room.name.startswith(("*" + chr(3))):
                        data.append(["TRIBE", room.name, room.getPlayerCount()])
                    else:
                        data.append(["PRIVATE", room.name, room.getPlayerCount()])
                else:
                    data.append([room.community.upper(), room.roomName, room.getPlayerCount()])
            result = "\n"
            for roomInfo in data:
                result += "<BL>[%s]</BL> <b>%s</b> : %s\n" %(roomInfo[0], roomInfo[1], roomInfo[2])
            result += "<j>Total players/rooms: </J><R>%s<N>/</N><R>%s</R>" %(len(self.server.players), len(self.server.rooms))
            self.client.sendLogMessage(result)

        elif command in ["lsc"]:
            self.requireLevel(7)
            result = {}
            rooms = self.server.rooms.values()
            for room in rooms:
                if room.community in result:
                    result[room.community] = result[room.community] + room.getPlayerCount()
                else:
                    result[room.community] = room.getPlayerCount()

            message = "\n"
            for community, count in result.items():
                message += "<BL>%s<BL> : <V>%s\n" %(community.upper(), count)
            message += "<J>Total players<J>: <R>%s" %(sum(result.values()))
            self.client.sendLogMessage(message)

        elif command in ["maxplayers"]:
            self.requireLevel(8)
            maxPlayers = int(args[0])
            if maxPlayers < 1: maxPlayers = 1
            self.client.room.maxPlayers = maxPlayers
            self.client.sendClientMessage("Maximum players of the map: <V>" +str(maxPlayers))

        elif command in ["clearchat"]:
            self.requireLevel(8)
            self.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("\n" * 100).toByteArray())

        elif command in ["vamp"]:
            self.requireVip()
            if argsCount == 0:
                if self.client.room.numCompleted > 1:
                    self.client.sendVampireMode(False)
                return

            self.requireLevel(8)
            playerName = Utils.parsePlayerName(args[0])
            client = self.server.players.get(playerName)
            if client != None:
                client.sendVampireMode(False)

        elif command in ["meep"]:
            self.requireVip()
            if argsCount == 0:
                if self.client.room.numCompleted > 1:
                    self.client.sendPacket(Identifiers.send.Can_Meep, 1)
                return

            self.requireLevel(8)
            playerName = Utils.parsePlayerName(args[0])
            if playerName == "*":
                for client in self.client.room.clients.copy().values():
                    client.sendPacket(Identifiers.send.Can_Meep, 1)
            else:
                client = self.server.players.get(playerName)
                if client != None:
                    client.sendPacket(Identifiers.send.Can_Meep, 1)

        elif command in ["don"]:
            self.requireVip()
            self.client.sendMessage("Not working!")
            #self.client.room.sendAll(Identifiers.send.Don, ByteArray().writeInt(self.client.playerCode).toByteArray())

        elif command in ["vsha"]:
            self.requireLevel(7)
            self.client.isShaman = True
            for client in self.client.room.clients.copy().values():
                client.sendShamanCode(self.client.playerCode, 0)

        elif command in ["mymaps"]:
            self.requireLevel(1)
            result = ""
            mapList = ""
            mapCount = 0

            self.client.room.CursorMaps.execute("select * from Maps where Builder = ?", [self.server.getPlayerID(self.client.playerName)])
            for rs in self.client.room.CursorMaps.fetchall():
                mapCount += 1
                yesVotes = rs["YesVotes"]
                noVotes = rs["NoVotes"]
                totalVotes = yesVotes + noVotes
                if totalVotes < 1: totalVotes = 1
                Rating = (1.0 * yesVotes // totalVotes) * 100
                rate = str(Rating).split(".")[0]
                if rate == "Nan": rate = "0"
                mapList += f"<br><N>{self.client.playerName} - @{rs['Code']} - {totalVotes} - {rate}% - P{rs['Perma']}"

            if len(mapList) != 0:
                result = str(mapList)

            try: self.client.sendLogMessage(f"<font size= \"12\"><V>f{self.client.playerName}<N>'s maps: <BV>{mapCount} {result}</font>")
            except: pass

        elif command in ["settime"]:
            self.requireLevel(7)
            time = args[0]
            if time.isdigit():
                iTime = int(time)
                iTime = 2 if iTime < 2 else (32767 if iTime > 32767 else iTime)
                for client in self.client.room.clients.copy().values():
                    client.sendRoundTime(iTime)
                self.client.room.changeMapTimers(iTime)

        elif command in ["np", "npp"]:
            self.requireLevel(7)
        #    self.requireTribe(True)
            if argsCount == 0:
                self.client.room.mapChange()
                return

            if self.client.room.isVotingMode:
                return

            code = args[0]
            if code.startswith("@"):
                if len(code[1:]) < 1 or not code[1:].isdigit():
                    self.client.sendLangueMessage("", "$CarteIntrouvable")
                    return
                mapInfo = self.client.room.getMapInfo(int(code[1:]))
                if mapInfo[0] == None:
                    self.client.sendLangueMessage("", "$CarteIntrouvable")
                    return

                self.client.room.forceNextMap = code
                if command == "np":
                    if self.client.room.changeMapTimer != None:
                        try:self.client.room.changeMapTimer.cancel()
                        except:self.client.room.changeMapTimer = None
                    self.client.room.mapChange()
                    return
                self.client.sendLangueMessage("", f"$ProchaineCarte {code}")
                return

            elif code.isdigit():
                self.client.room.forceNextMap = f"@{code}"
                if command == "np":
                    if self.client.room.changeMapTimer != None:
                        try:self.client.room.changeMapTimer.cancel()
                        except:self.client.room.changeMapTimer = None
                    self.client.room.mapChange()
                    return
                self.client.sendLangueMessage("", f"$ProchaineCarte {code}")

        elif command in ["reload"]:
            self.requireLevel(10)
            self.requireArgs(1)
            target = args[0].lower()
            if target in ["minigame", "minigames"]:
                self.server.loadMinigames()
            elif target in ["shop", "shoplist"]:
                self.server.parseShopList()
            elif target in ["config", "configure"]:
                self.server.parseConfig()
            elif target in ["module", "modules"]:
                self.server.reloadAllModules()
            elif target in ["village"]:
                with open("./include/files/village.lua") as f:
                    self.server.npcs = f.read()
            else:
                self.client.sendClientMessage(f"<R>{target.capitalize()} <V>not found.")
                return
            self.client.sendClientMessage(f"<R>{target.capitalize()} <V>has been reloaded successfully.")

        elif command in ["mjj"]:
            roomName = args[0]
            if roomName.startswith("#"):
                if roomName[1:] in self.server.minigames:
                    langue = "en"
                    lang = langue.lower()
                    self.client.enterRoom(f"{lang}-{roomName}")
                    return
            self.client.enterRoom(("" if self.client.lastGameMode == 1 else "vanilla" if self.client.lastGameMode == 3 else "survivor" if self.client.lastGameMode == 8 else "racing" if self.client.lastGameMode == 9 else "music" if self.client.lastGameMode == 11 else "bootcamp" if self.client.lastGameMode == 2 else "defilante" if self.client.lastGameMode == 10 else "village") + roomName)

        elif command in ["title", "titulo", "titre"]:
            self.requireLevel(1)
            if argsCount == 0:
                p = ByteArray()
                p2 = ByteArray()
                titlesCount = 0
                starTitlesCount = 0

                for title in self.client.titleList:
                    titleInfo = str(title).split(".")
                    titleNumber = int(titleInfo[0])
                    titleStars = int(titleInfo[1])
                    if titleStars > 1:
                        p.writeShort(titleNumber).writeByte(titleStars)
                        starTitlesCount += 1
                    else:
                        p2.writeShort(titleNumber)
                        titlesCount += 1
                self.client.sendPacket(Identifiers.send.Titles_List, ByteArray().writeShort(titlesCount).writeBytes(p2.toByteArray()).writeShort(starTitlesCount).writeBytes(p.toByteArray()).toByteArray())
                return

            titleID = args[0]
            found = False
            for title in self.client.titleList:
                if str(title).split(".")[0] == titleID:
                    found = True

            if found:
                self.client.titleNumber = int(titleID)
                for title in self.client.titleList:
                    if str(title).split(".")[0] == titleID:
                        self.client.titleStars = int(str(title).split(".")[1])
                self.client.sendPacket(Identifiers.send.Change_Title, ByteArray().writeByte(self.client.gender).writeShort(titleID).toByteArray())

        elif command in ["sy"]:
            self.requireLevel(8)
            playerName = Utils.parsePlayerName(args[0])
            client = self.server.players.get(playerName)
            if client == None:
                return
            client.isSync = True
            self.client.room.currentSyncCode = client.playerCode
            self.client.room.currentSyncName = client.playerName
            if self.client.room.mapCode != -1 or self.client.room.EMapCode != 0:
                self.client.room.sendAll(Identifiers.old.send.Sync, [client.playerCode, ""])
            else:
                self.client.room.sendAll(Identifiers.old.send.Sync, [client.playerCode])

            self.client.sendLangueMessage("", "$NouveauSync <V>" + playerName)

        elif command in ["clearban"]:
            self.requireLevel(8)
            playerName = Utils.parsePlayerName(args[0])
            client = self.server.players.get(playerName)
            if client == None: return
            client.voteBan = []
            self.server.sendStaffMessage(7, "<V>"+self.client.playerName+"<BL> cleared reports/bans of the player <V>"+playerName+"<BL>.")

        elif command in ["ip"]:
            self.requireLevel(11)
            playerName = Utils.parsePlayerName(args[0])
            client = self.server.players.get(playerName)
            if client != None:
                self.client.sendClientMessage("IP of the player <V>"+playerName+"<BL>: <V>"+client.ipAddress+"<BL>.")
            else:
                self.client.sendClientMessage("The player ["+playerName+"] is offline.")

        elif command in ["kick"]:
            self.requireLevel(8)
            playerName = Utils.parsePlayerName(args[0])
            client = self.server.players.get(playerName)
            if client == None:
                self.client.sendClientMessage("The player <V>"+playerName+"<BL> is offline.")
                return
            client.room.removeClient(client)
            client.transport.close()
            self.server.sendStaffMessage(6, "<V>"+self.client.playerName+"<BL> kicked the player <V>"+playerName+" <BL>from server.")
            self.server.sendMessageDiscord("```"+self.client.playerName+" kicked the player "+playerName+" from server```")

        elif command in ["search", "find"]:
            self.requireLevel(6)
            playerName = Utils.parsePlayerName(args[0])
            result = ""
            for client in self.client.room.clients.copy().values():
                if playerName in client.playerName:
                    result += "<br><V>"+client.playerName+"<BL> -> <V>"+client.room.name
            self.client.sendClientMessage(result)

        elif command in ["join"]:
                self.requireLevel(8)
                playerName = Utils.parsePlayerName(args[0])
                player = self.server.players.get(playerName)
                if player != None:
                    self.client.enterRoom(player.roomName)

        elif command in ["smn"]:
            self.requireLevel(6)
            self.server.sendStaffChat(-1, self.client.langue, self.client.playerName, argsNotSplited, self.client)

        elif command in ["mm"]:
            self.requireLevel(8)
            if self.client.isMute:
                muteInfo = self.server.getModMuteInfo(self.client.playerName)
                timeCalc = Utils.getHoursDiff(int(muteInfo[0]))
                if timeCalc <= 0:
                    self.client.isMute = False
                    self.server.removeModMute(self.client.playerName)
                    self.client.room.sendAllChat(self.client.playerCode, self.client.playerName if self.client.mouseName == "" else self.client.mouseName, message, self.client.langueByte, isSuspect)
                else:
                    self.client.sendLangueMessage("", "<ROSE>$MuteInfo1", str(abs(timeCalc)), (muteInfo[1]))
            else:
                self.client.room.sendAll(Identifiers.send.Staff_Chat, ByteArray().writeByte(0).writeUTF("").writeUTF(argsNotSplited).writeShort(0).writeByte(0).toByteArray())

        elif command in ["pink"]:
            self.requireVip()
            self.client.room.sendAll(Identifiers.send.Player_Damanged, ByteArray().writeInt(self.client.playerCode).toByteArray())

        elif command in ["transformation"]:
            self.requireVip()
            if argsCount == 0:
                if self.client.room.numCompleted > 1:
                    self.client.sendPacket(Identifiers.send.Can_Transformation, 1)
                    return

            self.requireLevel(8)
            playerName = Utils.parsePlayerName(args[0])
            if playerName == "*":
                for client in self.client.room.clients.copy().values():
                    client.sendPacket(Identifiers.send.Can_Transformation, 1)
                return
            client = self.server.players.get(playerName)
            if client != None:
                client.sendPacket(Identifiers.send.Can_Transformation, 1)

        elif command in ["resetprofile", "reset"]:
            self.requireLevel(10)
            playerName = Utils.parsePlayerName(args[0])
            self.requireNoGuest(playerName)
            if not self.server.checkExistingUser(playerName):
                self.client.sendClientMessage("User not found: <V>%s</V>." %(playerName))
                return

            client = self.server.players.get(playerName)
            if client != None:
                client.room.removeClient(client)
                client.transport.close()
            self.Cursor.execute("update Users set FirstCount = 0, CheeseCount = 0, ShamanSaves = 0, HardModeSaves = 0, DivineModeSaves = 0, BootcampCount = 0, ShamanCheeses = 0, racingStats = '0,0,0,0', survivorStats = '0,0,0,0' where Username = %s", [playerName])
            self.server.sendStaffMessage(7, "<V>%s</V> reset the profile of the player <V>%s</V>." %(playerName, self.client.playerName))

        elif command in ["move"]:
            self.requireLevel(8)
            for player in self.client.room.clients.copy().values():
                player.enterRoom(argsNotSplited)

        elif command in ["lsmap", "lsmaps"]:
            self.requireLevel(1 if argsCount == 0 else 7)
            playerName = self.client.playerName if argsCount == 0 else Utils.parsePlayerName(args[0])
            mapList = ""
            mapCount = 0

            self.client.room.CursorMaps.execute("select * from Maps where Builder = ?", [self.server.getPlayerID(playerName)])
            rrf = self.client.room.CursorMaps.fetchall()
            for rs in rrf:
                mapCount += 1
                yesVotes = rs["YesVotes"]
                noVotes = rs["NoVotes"]
                totalVotes = yesVotes + noVotes
                if totalVotes < 1: totalVotes = 1
                rating = (1.0 * yesVotes // totalVotes) * 100
                mapList += "\n<N>%s</N> - @%s - %s - %s%s - P%s" %(self.server.getPlayerID(playerName), rs["Code"], totalVotes, str(rating).split(".")[0], "%", rs["Perma"])

            try: self.client.sendLogMessage("<font size= \"12\"><V>%s<N>'s maps: <BV>%s %s</font>" %(playerName, mapCount, mapList))
            except: self.client.sendClientMessage("<R>Too many maps.</R>")

        elif command in ["addtext", "removetext"]:
            self.requireLevel(10)
            self.requireArgs(2)
            type, link = args[0], args[1]
            if not type in ["blacklist", "whitelist", "suspectwords"]:
                self.client.sendClientMessage("Unknown type. Types: [<V>blacklist, whitelist, suspectwords</V>].")
                return

            link = link.replace("https://", "").replace("http://", "").replace("www.", "") if type != "suspectwords" else link
            if link in self.server.serverList[type] if command == "addtext" else not link in self.server.serverList[type]:
                self.client.sendClientMessage("The link <V>%s</V> is already in the list." %(link) if command == "addtext" else "The link <V>%s</V> is not in the list, you can't remove it." %(link))
                return

            self.server.serverList[type].append(link.lower()) if command == "addtext" else self.server.serverList[type].remove(link.lower())
            self.client.sendClientMessage(("Added" if command == "addtext" else "Removed") + " successfully. [<V>%s</V> -> [<VP>%s</VP>]." %(link, type))
            self.server.updateBlackList()

        elif command in ["ch"]:
            self.requireLevel(8)
            playerName = Utils.parsePlayerName(args[0])
            client = self.server.players.get(playerName)
            if client != None and client.roomName == self.client.roomName:
                self.client.sendLangueMessage("", "$ProchaineChamane", client.playerName)
                self.client.room.forceNextShaman = client.playerCode
            else:
                self.client.sendClientMessage("Player not found.")

        elif command in ["moveplayer", "mjoin"]:
            self.requireLevel(9)
            self.requireArgs(2)
            playerName = Utils.parsePlayerName(args[0])
            roomName = argsNotSplited.split(" ", 1)[1]
            client = self.server.players.get(playerName)
            if client != None:
                client.enterRoom(roomName)

        elif command in ["funcorp"]:
            if self.client.privLevel.includes(5):
                self.client.room.isFuncorp = not self.client.room.isFuncorp
                if not self.client.room.isFuncorp:
                    self.client.room.funcorpNames.clear()
                    self.client.room.funcorpAdmin = ""
                    for player in self.client.room.clients.copy().values():
                        player.sendLangueMessage("", "<FC>$FunCorpDesactive</FC>")
                        player.tempMouseColor = ""
                else:
                    self.client.room.funcorpAdmin = self.client.playerName
                    for player in self.client.room.clients.copy().values():
                        player.sendLangueMessage("", "<FC>$FunCorpActive</FC>")

        elif command in ["changename"]:
            self.requireArgs(1)
            if self.client.privLevel.upper(9) and not self.client.room.isFuncorp:
                playerName = Utils.parsePlayerName(args[0])
                player = self.server.players.get(playerName)
                if player != None:
                    player.mouseName = argsNotSplited.split(" ", 1)[1] if argsCount > 1 else ""
            else:
                self.requireLevel(self.client.privLevel.upper(9) or self.client.privLevel.includes(5))
                playerName = Utils.parsePlayerName(args[0])
                if playerName in self.client.room.clients:
                    self.client.room.funcorpNames[playerName] = argsNotSplited.split(" ", 1)[1] if argsCount > 1 else ""

        elif command in ["changesize"]:
            self.requireLevel(can=self.client.privLevel.upper(9) or self.client.privLevel.includes(5))
            self.requireArgs(2)
            playerName = Utils.parsePlayerName(args[0])
            if args[1].isdigit():
                size = float(args[1])
                size = 5.0 if size > 5.0 else size
                size = int(size * 100)
                if playerName == "*":
                    for player in self.client.room.clients.copy().values():
                        self.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeShort(size).writeBoolean(False).toByteArray())
                else:
                    player = self.server.players.get(playerName)
                    if player != None:
                        self.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeShort(size).writeBoolean(False).toByteArray())

        elif command in ["image"]:
            self.requireLevel(can=self.client.privLevel.upper(9) or self.client.privLevel.includes(5))
            self.requireArgs(4)
            imageName = args[0]
            target = args[1]
            xPosition = int(args[2]) if args[2].isdigit() else 0
            yPosition = int(args[3]) if args[3].isdigit() else 0

            if target.lower() in ["$all", "%all"]:
                for player in self.client.room.clientsvalues():
                    self.client.room.addImage(imageName, target[0] + player.playerName, xPosition, yPosition, "")
            else:
                self.client.room.addImage(imageName, target, xPosition, yPosition, "")

        elif command in ["soulmate"]:
            self.requireLevel(can=self.client.privLevel.upper(9) or self.client.privLevel.includes(5))
            self.requireArgs(2)
            playerName = Utils.parsePlayerName(args[0])
            playerName2 = Utils.parsePlayerName(args[1])
            player = self.client.room.clients.get(playerName)
            if player != None:
                if playerName2 == "*":
                    for player2 in self.client.room.clientsvalues():
                        self.client.room.sendAll(Identifiers.send.Soulmate, ByteArray().writeBoolean(True).writeInt(player.playerCode).writeInt(player2.playerCode).toByteArray())
                else:
                    player2 = self.client.room.clients.get(playerName2)
                    if player2 != None:
                        self.client.room.sendAll(Identifiers.send.Soulmate, ByteArray().writeBoolean(True).writeInt(player.playerCode).writeInt(player2.playerCode).toByteArray())

        elif command in ["removesoulmate"]:
            self.requireLevel(can=self.client.privLevel.upper(9) or self.client.privLevel.includes(5))
            self.requireArgs(1)
            playerName = Utils.parsePlayerName(args[0])
            player = self.client.room.clients.get(playerName)
            if player != None:
                self.client.room.sendAll(Identifiers.send.Soulmate, ByteArray().writeBoolean(False).writeInt(player.playerCode).toByteArray())

        elif command in ["anim"]:
            self.requireLevel(9)
            self.requireArgs(3)
            playerName = Utils.parsePlayerName(args[0])
            anim = args[1]
            frame = int(args[2]) if args[2].isdigit() else 0
            player = self.client.room.clients.get(playerName)
            if player != None:
                self.client.room.sendAll(Identifiers.send.Add_Anim, ByteArray().writeInt(player.playerCode).writeUTF(anim).writeShort(frame).toByteArray())

        elif command in ["frame"]:
            self.requireLevel(9)
            self.requireArgs(4)
            playerName = Utils.parsePlayerName(args[0])
            frame = args[1]
            xPosition = int(args[2]) if args[2].isdigit() else 0
            yPosition = int(args[3]) if args[3].isdigit() else 0
            player = self.client.room.clients.get(playerName)
            if player != None:
                self.client.room.sendAll(Identifiers.send.Add_Frame, ByteArray().writeInt(player.playerCode).writeUTF(frame).writeInt(xPosition).writeInt(yPosition).toByteArray())

        elif command in ["gravity"]:
            self.requireLevel(9)
            self.requireArgs(2)
            wind = int(args[0]) if args[0].isdigit() else 10
            gravity = int(args[0]) if args[0].isdigit() else 0
            self.client.room.sendAll(Identifiers.old.send.Gravity, [wind, gravity])

        else:
            self.client.sendMessage("Unknow Command!")

