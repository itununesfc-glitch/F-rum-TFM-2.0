from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers
import math

class ModoPwet:

    def __init__(this, player, server):
        this.client = player
        this.server = player.server

    def checkReport(this, array, playerName):
        return playerName in array

    def makeReport(this, playerName, type, comments):
        playerName = Utils.parsePlayerName(playerName)
        reporter = this.client.playerName
        this.server.sendStaffMessage(5, "[REPORT] [<V>%s</V>] -> <V>%s</V>" % (this.client.playerName,playerName))

        if this.server.players.get(playerName):
            if playerName in this.server.reports:
                if reporter in this.server.reports[playerName]["reporters"]:
                    r = this.server.reports[playerName]["reporters"][reporter]
                    if r[0] != type:
                        this.server.reports[playerName]["reporters"][reporter]=[type, comments, Utils.getTime()]
                else:
                    this.server.reports[playerName]["reporters"][reporter] = [type, comments, Utils.getTime()]
                this.server.reports[playerName]["status"] = "online" if this.server.checkConnectedAccount(playerName) else "disconnected"
            else:
                this.server.reports[playerName] = {}
                this.server.reports[playerName]["reporters"] = {reporter: [type, comments, Utils.getTime()]}
                this.server.reports[playerName]["status"] = "online" if this.server.checkConnectedAccount(playerName) else "disconnected"
                this.server.reports[playerName]["language"] = this.getModopwetLanguage(playerName)
                this.server.reports[playerName]["isMuted"] = False
            this.updateModoPwet()
            this.client.sendBanConsideration()

    def getModopwetLanguage(this, playerName):
        player = this.server.players.get(playerName)
        if player != None:
            return player.langue
        else:
            return "EN"

    def updateModoPwet(this):
        for player in this.server.players.values():
            if player.isModoPwet and player.privLevel.uppermost() >= 5:
                player.modoPwet.openModoPwet(True)

    def getPlayerRoomName(this, playerName):
        player = this.server.players.get(playerName)
        if player != None:
            return player.roomName
        else:
            return "0"

    def getRoomMods(this, room):
        s = []
        i = ""
        for player in this.server.players.values():
            if player.roomName == room and player.privLevel.uppermost() >= 5:
                s.append(player.playerName)

        if len(s) == 1:
            return s[0]
        else:
            for name in s:
                i = i+name+", "
        return i

    def getPlayerKarma(this, playerName):
        player = this.server.players.get(playerName)
        if player:
            return player.playerKarma
        else:
            return 0

    def banHack(this, playerName, iban):
        if this.server.banPlayer(playerName, 360, "Hack (last warning before account deletion)", this.client.playerName, iban):
            this.server.sendStaffMessage(5, "<V>%s<BL> banned <V>%s<BL> for <V>360 <BL>hours. Reason: <V>Hack (last warning before account deletion)<BL>." %(this.client.playerName, playerName))
        this.updateModoPwet()

    def deleteReport(this, playerName, handled):
        if handled == 0:
            this.server.reports[playerName]["status"] = "deleted"
            this.server.reports[playerName]["deletedby"] = this.client.playerName
        else:
            if playerName in this.server.reports:
                del this.server.reports[playerName]

        this.updateModoPwet()

    def sort(this, given):
        for i in given[1]["reporters"]:
            return given[1]["reporters"][i][2]

    def sortReports(this, reports, sort):
        if sort:
            return sorted(reports.items(), key=this.sort,reverse=True)
        else:
            return sorted(reports.items(), key=lambda x: len(x[1]["reporters"]),reverse=True)

    def openModoPwet(this, isOpen=False, modopwetOnlyPlayerReports=False, sortBy=False):
        if isOpen:
            if len(this.server.reports) <= 0:
                this.client.sendPacket(Identifiers.send.Modopwet_Open, 0)
            else:
                this.client.sendPacket(Identifiers.send.Modopwet_Open, 0)
                reports, bannedList, deletedList, disconnectList = this.sortReports(this.server.reports, sortBy), {}, {}, []
                count = 0
                p = ByteArray()
                for i in reports:
                    name = i[0]
                    report = this.server.reports[name]
                    if this.client.modoPwetLanguage == "ALL" or report["language"] == this.client.modoPwetLanguage:
                        player = this.server.players.get(name)
                        hours = math.floor(player.playTime/3600) if player else 0
                        roomName = player.roomName if player else "0"
                        count += 1
                        this.client.lastReportID += 1
                        if count >= 255:
                            break
                        p.writeByte(count)
                        p.writeShort(this.client.lastReportID)
                        p.writeUTF(report["language"])
                        p.writeUTF(name)
                        p.writeUTF(roomName)
                        p.writeByte(1)
                        p.writeUTF(this.getRoomMods(roomName))
                        p.writeInt(hours)
                        p.writeByte(int(len(report["reporters"])))
                        for name in report["reporters"]:
                            r = report["reporters"][name]
                            p.writeUTF(name)
                            p.writeShort(this.getPlayerKarma(name)) #karma
                            p.writeUTF(r[1])
                            p.writeByte(r[0])
                            p.writeShort(int(Utils.getSecondsDiff(r[2])/60)) #report period

                        mute = report["isMuted"]
                        p.writeBoolean(mute) #isMute
                        if mute:
                            p.writeUTF(report["mutedBy"])
                            p.writeShort(report["muteHours"])
                            p.writeUTF(report["muteReason"])

                        if report["status"] == "banned":
                            x = {}
                            x["banhours"] = report["banhours"]
                            x["banreason"] = report["banreason"]
                            x["bannedby"] = report["bannedby"]
                            bannedList[name] = x
                        if report["status"] == "deleted":
                            x = {}
                            x["deletedby"] = report["deletedby"]
                            deletedList[name] = x
                        if report["status"] == "disconnected":
                            disconnectList.append(name)

                this.client.sendPacket(Identifiers.send.Modopwet_Open, ByteArray().writeByte(int(len(reports))).writeBytes(p.toByteArray()).toByteArray())
                for user in disconnectList:
                    this.changeReportStatusDisconnect(user)

                for user in deletedList.keys():
                    this.changeReportStatusDeleted(user, deletedList[user]["deletedby"])

                for user in bannedList.keys():
                    this.changeReportStatusBanned(user, bannedList[user]["banhours"], bannedList[user]["banreason"], bannedList[user]["bannedby"])

    def changeReportStatusDisconnect(this, playerName):
        this.client.sendPacket(Identifiers.send.Modopwet_Disconnected, ByteArray().writeUTF(playerName).toByteArray())

    def changeReportStatusDeleted(this, playerName, deletedby):
        this.client.sendPacket(Identifiers.send.Modopwet_Deleted, ByteArray().writeUTF(playerName).writeUTF(deletedby).toByteArray())

    def changeReportStatusBanned(this, playerName, banhours, banreason, bannedby):
        this.client.sendPacket(Identifiers.send.Modopwet_Banned, ByteArray().writeUTF(playerName).writeUTF(bannedby).writeInt(int(banhours)).writeUTF(banreason).toByteArray())

    def openChatLog(this, playerName):
        if playerName in this.server.chatMessages:
            packet = ByteArray().writeUTF(playerName).writeByte(len(this.server.chatMessages[playerName]))
            for message in this.server.chatMessages[playerName]:
                packet.writeUTF(message[1]).writeUTF(message[0])
            packet.writeUTF(this.server.chatMessages[playerName][len(this.server.chatMessages[playerName])-1][1])
            packet.writeUTF(this.server.chatMessages[playerName][len(this.server.chatMessages[playerName])-1][0])
            this.client.sendPacket(Identifiers.send.Modopwet_Chatlog, packet.toByteArray())
    
    def openChatLogAll(this):
        packet = ByteArray().writeUTF("All").writeByte(len(this.server.chatMessages))
        for playerName in this.server.chatMessages:
            for message in this.server.chatMessages[playerName]:
                packet.writeUTF(message[1]).writeUTF(message[0])
            packet.writeUTF(this.server.chatMessages[playerName][len(this.server.chatMessages[playerName])-1][1])
            packet.writeUTF(this.server.chatMessages[playerName][len(this.server.chatMessages[playerName])-1][0])
        this.client.sendPacket(Identifiers.send.Modopwet_Chatlog, packet.toByteArray())

