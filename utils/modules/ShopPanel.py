#coding: utf-8
import time, random
from ByteArray import ByteArray
from Identifiers import Identifiers
from datetime import datetime

from utils import Utils

class ShopPanel:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        this.room = client.room
        this.Cursor = client.Cursor

        # Integers
        this.lastAreaID = 0


        # NoneType
        this.vipTimer = None

        # DL
        this.buyTime = None # düşünemedim daha yarram
        this.buyTAGL = []
        this.buyVIPL = []
        this.buyCTL = []

    def addPU(this, id, type, text, x, y, w, f):
        if type == 1:
            this.client.room.addPopupNew(text, id, this.client.playerName)
        else:
            this.client.room.addPopup(id, type, text, this.client.playerName, x, y, w, f)

    def addTA(this, txt, x, y, w, h, bgc, bdc, o = 0, f = False, LAID = None):
        if LAID == None:
            this.lastAreaID += 10
            LAID = this.lastAreaID
        this.client.room.addTextArea(LAID, txt, this.client.playerName, x, y, w, h, bgc, bdc, o, f)


    def updateTA(this, id, text):
        this.client.room.updateTextArea(id, text, this.client.playerName)

    def removeTA(this, id):
        this.client.room.removeTextArea(id, this.client.playerName)

    def textACback(this, textID, x):
        if x == "buyVIP":
            if 4 >= this.client.hazelnuts:
                this.addPU(102, 0, "<font color='#D1D1D1'>Buy Hazlenut</font>", 330, 160, 145, False)
                return
            this.addPU(101, 1, "<p align='center'>Do you want to buy a VIP?", 310-20, 160, 200, False)
        elif x == "buyPlus":
            if 4 >= this.client.hazelnuts:
                this.addPU(102, 0, "<font color='#D1D1D1'>Buy Hazlenut</font>", 330, 160, 145, False)
                return
            this.addPU(105, 1, "<p align='center'>Do you want to buy a Plus?", 310-20, 160, 200, False)
        elif x == "buyTag":
            if 4 >= this.client.hazelnuts:
                this.addPU(102, 0, "<font color='#D1D1D1'>Buy Hazlenut</font>", 330, 160, 145, False)
                return
            this.addPU(100, 2, "<font color ='#D1D1D1'>Write Tag</font>", 330, 160, 145, False)
        elif x == "buyCT":
            #this.addPU(106, 0, "<font color='#D1D1D1'>Soon</font>", 330, 160, 145, False)
            #this.addPU(106, 2, "<font color ='#D1D1D1'>Write Title</font>", 330, 160, 145, False)
            this.addPU(106, 2, "<font color ='#D1D1D1'>Enter Code</font>", 330, 160, 145, False)
        elif x == "closePanel":
            for y in sorted(range(this.lastAreaID + 1), reverse = 1):
                this.removeTA(y)
            this.lastAreaID = 0
    
    def redeem(this, code):
        if code == 'STAFF010101133234234223432424':
            return [True, 5]
        else:
            return [False, 0]

    def popupCback(this, pID, answer):
        if pID == 101:
            if this.buyVIP(answer):
                 this.client.hazelnuts -= 5
                 this.closePanel()
                 this.openPanel()
        elif pID == 105:
            if this.buyPlus(answer):
                this.client.hazelnuts -= 5
                this.closePanel()
                this.openPanel()
        elif pID == 100:
            if this.buyTag(answer):
                this.client.hazelnuts -= 5
                this.closePanel()
                this.openPanel()
        elif pID == 106:
            #this.buyCreateTitle(answer)
            #this.client.hazelnuts = this.client.hazelnuts - 5
            t = this.redeem(answer)
            if t[0]:
                this.addPU(106, 0, f"<font color='#D1D1D1'>You got {t[1]} Hazelnuts and 1 Bonus :)</font>", 330, 160, 145, False)
                this.client.hazelnuts += t[1] + 1
            else:
                this.addPU(106, 0, f"<font color='#D1D1D1'>Invalid Code!</font>", 330, 160, 145, False)
            this.closePanel()
            this.openPanel()
            return

    def addTitle(this, title, id = False):
        if not id:
            this.server.lastTitleID += 1

        this.server.configs("ids.lasttitleid", str(id if id else this.server.lastTitleID))
        this.server.specialTitles["titles"].append([id if id else this.server.lastTitleID,title])
        this.server.eklenicekler["add"].append([id if id else this.server.lastTitleID,title])
    

    def buyCreateTitle(this, titleName):
        if titleName == "": 
            this.client.sendMessage("Please write a text") 
            return

        this.server.sendStaffMessage(9, "{} player create has a this title {}".format(this.client.playerName,titleName))
            
        if titleName in ["</font"]:
            this.client.sendMessage("Please use proper html code.")
            return
        
        x = titleName
        star = "1"
        z = this.server.lastTitleID+1
        title = float(str(z)+"."+str(star))
        this.client.specialTitleList.append(title)
        this.client.sendUnlockedTitle(z, star)

        this.client.sendCompleteTitleList()
        this.client.sendTitleList()
        this.client.sendMessage("<N>Please log in again for your titles({}) to come.</N>".format(titleName))
        
        this.client.parseCommands.commands("updatelang")
        
        this.addTitle(titleName,False)
        this.buyCTL.append({"Player": this.client.playerName, "Title": titleName, "Time": this.buyTime})

    

    def buyVIP(this, answer):
        if answer == "yes":
            alreadyVIP = "(VIP)" in this.client.playerTag
            this.Cursor.execute("SELECT VipTime FROM users WHERE PlayerID = %s", [this.client.playerID])
            for rs in this.Cursor.fetchone():
                vTime = rs
                if vTime > 0 or alreadyVIP:
                    this.addPU(104, 0, "<font color ='#D1D1D1'>You already have a VIP.</font>", 330, 160, 145, False)
                    return
                days = 30
                pTag = this.client.playerTag
                if not pTag:
                    pTag = "#"
                vTag = this.client.playerTag + " " + "(VIP)"
                vTime = Utils.getTime() + (days * 86400)
                player = this.server.players.get(this.client.playerName)
                this.Cursor.execute("UPDATE users SET VipTime = %s, Tag = %s WHERE PlayerID = %s", [vTime, vTag, this.client.playerID])
                this.client.sendMessage("<V>[•]</V> You have been added to the <ROSE>VIP</ROSE> team.\nPlease re-enter the game.")
                this.client.vipTime = vTime
                this.client.cacheTag = vTag
                this.buyVIPL.append({"PlayerName": this.client.playerName, "Day": days, "Time": this.buyTime})
                return True


    def shopVipCheck(this, vipTime):
        s = abs(Utils.getSecondsDiff(vipTime))
        if this.vipTimer != None:
            this.vipTimer.cancel()
        if s > 0:
            this.vipTimer = this.server.loop.call_later(s, lambda: this.shopVipCheck(vipTime - s))
        if this.client.privLevel.notin(2):
            this.client.privLevel.append(2)

        if s < 0 or s <= 0:
            finishTime = 0
            finishTag = this.client.playerTag.split(" ")[0]
            this.Cursor.execute("UPDATE users SET VipTime = %s, Tag = %s WHERE PlayerID = %s", [finishTime, finishTag, this.client.playerID])
            this.client.vipTime = 0
            this.client.cacheTag = finishTag
            this.client.sendMessage("<R>Your VIP membership has been expired.")
        else:
            days = s // 86400
            hours = s // 3600
            minutes = s // 60
            this.client.sendMessage("<N>Your VIP membership expires in <V>{}</V> days <V>{}</V> hours <V>{}</V> minutes.".format(days, hours, minutes))
   

    def buyTag(this, answer):
        alreadyVIP = "(VIP)" in this.client.playerTag
        isVip = " " + "(VIP)"
        if answer == "":
            this.addPU(102, 0, "<font color='#D1D1D1'>Write Text</font>", 330, 160, 145, False)
            return False
        if True:
            iTag = answer
            iTag = iTag.replace("#", "")
            if len(iTag) > 15:
                this.addPU(103, 0, "<font color='#E03535'>More than 15 chars isn't allowed.</font>", 330, 160, 145, False)
                return
            if alreadyVIP:
                #this.Cursor.execute("UPDATE users SET Tag = %s WHERE PlayerID = %s", [iTag + isVip, this.client.playerID])
                this.client.cacheTag = "#" + iTag
            else:
                #this.Cursor.execute("UPDATE users SET Tag = %s WHERE PlayerID = %s", [iTag, this.client.playerID])
                this.client.cacheTag = "#" + iTag
            this.client.sendMessage("<V>[•]</V> Your tag changed #{} succesfully. Please re-login.".format(iTag))

            this.buyTAGL.append({"PlayerName": this.client.playerName, "Tag": answer, "Time": this.buyTime})
            return True

    
    def buyPlus(this, answer):
        if answer == "yes":
            x = "+" + this.client.playerName
            alreadyPLUS = "+" in this.client.playerName
            if alreadyPLUS:
                this.addPU(106, 0, "<font color ='#D1D1D1'>You already have a Plus(+nickname).</font>", 330, 160, 145, False)
                return False
            else:
                this.client.updateDatabase()
                player = this.server.players.get(this.client.marriage)
                if player != None:
                    player.marriage = x
                this.Cursor.execute("UPDATE users set Username = %s WHERE PlayerID = %s", [x, this.client.playerID])                
                this.client.updateShop = True
                this.client.sendMessage("<V>[•]</V> Succesfully Plus {}. Please re-login with {}.".format(x,x))
                this.client.connection_lost("disconected")
                return True

    def openPanel(this):
        x, y, z, w = 209, 110, 57, 18
        r, p = y+34, y+33
        v, n = r+34, p+33
        a, b, c, d, e, f, g  = 589, 76, 591, 78, 590, 77, 13
        this.addTA("", 200, 60, 420, 300, 0x2d211a, 0x2d211a, 100, False)
        this.addTA("", 201, 61, 418, 298, 0x986742, 0x986742, 100, False)
        this.addTA("", 204, 64, 412, 292, 0x171311, 0x171311, 100, False)
        this.addTA("", 205, 65, 410, 290, 0xc191c, 0xc191c, 100, False)
        this.addTA("", 206, 66, 408, 288, 0x24474d, 0x24474d, 100, False)
        this.addTA("", 207, 67, 406, 286, 0x183337, 0x183337, 100, False)
        this.addTA("<p align='center'><font size='20'><j>Shop</font><br><bv>", 208, 68, 404, 283, 0x122528, 0x122528, 100, False)
        this.addTA("", x, y, z, w, 0x7a8d93, 0x7a8d93, 100, False)
        this.addTA("", x+2, y+1, z, w, 0xe1619, 0xe1619, 100, False)
        this.addTA("<p align='center'><font size='14'><B>=></B></font>", x+5-2, y, 150, 100, 0x314e57, 0x314e57, 0, False)
        this.addTA("<p align='center'><font size='15'><B>5</font>", x+33-2-2-2, y-1-1-1+1, 150, 100, 0x314e57, 0x314e57, 0, False)
        this.addTA("<p align='center'><font size='11'><B><img src='http://167.99.142.78/hazelnut.png'></img></B></font>", x+105-2-2-2, y-17-1-1+1, 150, 100, 0x314e57, 0x314e57, 0, False)
        this.addTA("<a href='event:buyTag'><font color='#0AE6C7' size='11'>[Buy Tag]</font></a>", x, y, 100, 20, 0, 0, 0, False)
        this.addTA("", x, y+33, z, w, 0x7a8d93, 0x7a8d93, 100, False)
        this.addTA("", x+2, y+34, z, w, 0xe1619, 0xe1619, 100, False)
        this.addTA("<p align='center'><font size='14'><B>=></B></font>", x+5-2, y+33, 150, 100, 0x314e57, 0x314e57, 0, False)
        this.addTA("<p align='center'><font size='15'><B>5</font>", x+33-2-2-2, y-1-1-1+1+33, 150, 100, 0x314e57, 0x314e57, 0, False)
        this.addTA("<p align='center'><font size='11'><B><img src='http://167.99.142.78/hazelnut.png'></img></B></font>", x+105-2-2-2, y-17-1-1+1+33, 150, 100, 0x314e57, 0x314e57, 0, False)
        this.addTA("<a href='event:buyVIP'><font color='#0AE6C7' size='11'>[Buy VIP]</font></a>", x, y+33, 100, 20, 0, 0, 0, False)
        this.addTA("", x, n, z, w, 0x7a8d93, 0x7a8d93, 100, False)
        this.addTA("", x+2, v, z, w, 0xe1619, 0xe1619, 100, False)
        this.addTA("<p align='center'><font size='14'><B>=></B></font>", x+5-2, n, 150, 100, 0x314e57, 0x314e57, 0, False)
        this.addTA("<p align='center'><font size='15'><B>5</font>", x+33-2-2-2, n-1-1-1+1, 150, 100, 0x314e57, 0x314e57, 0, False)
        this.addTA("<p align='center'><font size='11'><B><img src='http://167.99.142.78/hazelnut.png'></img></B></font>", x+105-2-2-2, n-17-1-1+1, 150, 100, 0x314e57, 0x314e57, 0, False)
        this.addTA("<a href='event:buyPlus'><font color='#0AE6C7' size='11'>[Buy Plus]</font></a>", x, n, 100, 20, 0, 0, 0, False)
        this.addTA("", x, n+33, z, w, 0x7a8d93, 0x7a8d93, 100, False)
        this.addTA("", x+2, v+34, z, w, 0xe1619, 0xe1619, 100, False)
        this.addTA("<p align='center'><font size='14'><B></B></font>", x+5-2, n+33, 150, 100, 0x314e57, 0x314e57, 0, False)
        this.addTA("<p align='center'><font size='15'><B></font>", x+33-2-2-2, n-1-1-1+1+33, 150, 100, 0x314e57, 0x314e57, 0, False)
        this.addTA("<p align='center'><font size='11'><B><img src=''></img></B></font>", x+105-2-2-2, n-17-1-1+1+33, 150, 100, 0x314e57, 0x314e57, 0, False)
        this.addTA("<a href='event:buyCT'><font color='#0AE6C7' size='11'>[Redeem]</font></a>", x, n+33, 100, 20, 0, 0, 0, False)
        this.addTA("", a, b, g, g, 0x7a8d93, 0x7a8d93, 100, False)
        this.addTA("", c, d, g, g, 0xe1619, 0xe1619, 100, False)
        this.addTA("", e, f, g, g, 0x274347, 0x274347, 100, False)
        this.addTA("<p align='center'><font size='11'><B><a href='event:closePanel'>×</a></B></font></p>", 587, 73, 20, 20, 0x314e57, 0x314e57, 0, False)
        this.addTA("<p align='center'><font size='11'><B><img src='http://167.99.142.78/hazelnut.png'></img></B></font>", 587-130+15+5+3+20+5+20+5+5+5+7+2+5, 73*4+18-5-3+20-2, 150, 100, 0x314e57, 0x314e57, 0, False)
        this.addTA(f"<p align='center'><font size='11'><B>: {this.client.hazelnuts}</B></font>", 587-130+20+5+20+5+5+5+7+5-5, 73*4+25+20-2, 150, 22, 0x314e57, 0x314e57, 0, False)

    def closePanel(this):
        for y in sorted(range(this.lastAreaID + 1), reverse = 1):
            this.removeTA(y)
        this.lastAreaID = 0
