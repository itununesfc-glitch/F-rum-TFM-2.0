#coding: utf-8
from ByteArray import ByteArray
from Identifiers import Identifiers

from Utils import Utils
from Priv import PrivLevel

class Others:
    def __init__(self, client):
        self.client = client
        self.server = client.server

        #Modules
        self.modules = {"privPanel": PrivPanel(client)}

    def textAreaCallback(self, textAreaID, event):
        for module in self.modules.values():
            module.textAreaCallback(textAreaID, event)

    def popupCallback(self, popupID, answer):
        for module in self.modules.values():
            module.popupCallback(popupID, answer)

    def changeRoom(self):
        for module in self.modules.values():
            module.room = self.client.room
            try:
                module.onRoom()
            except AttributeError:
                pass

class PrivPanel:
    def __init__(self, client):
        self.client = client
        self.server = client.server
        self.room = client.room
        self.Cursor = client.Cursor
        self.targetPlayer = None
        self.lastAreaID = 0
        self.lastPopupID = 300
        self.targetID = 0
        self.selectedPrivs = {}
        self.unselectedPrivs = {}
        self._selectedPrivs = {}
        self._unselectedPrivs = {}
        

    def popupCallback(self, popupID, answer):
        if int(popupID) >= 300:
            if str(answer) == str(self.client.playerName):
                self.addPopup(0, "<font color='#E03535'>You can't change your own privileges</font>", 235, 160, 300, False)
                return
            cache = self.targetPlayer
            targetPlayer = Utils.parsePlayerName(answer)
            self.targetPlayer = self.server.players.get(targetPlayer)
            if self.targetPlayer is None:
                self.Cursor.execute("SELECT PrivLevel, PlayerID FROM users WHERE Username = %s", [targetPlayer])
                rs = self.Cursor.fetchone()
                if not rs:
                    self.addPopup(0, "<font color='#E03535'>Target player not found</font>", 235, 160, 300, False)
                    return
                else:
                    self.targetPlayer = PrivLevel(rs[0])
                    self.targetID = rs[1]
            upper = False
            if isinstance(self.targetPlayer, PrivLevel):
                if self.targetPlayer.uppermost() >= self.client.privLevel.uppermost():
                    upper = True
            else:
                if self.targetPlayer.privLevel.uppermost() >= self.client.privLevel.uppermost():
                    upper = True
            if upper:
                self.addPopup(0, "<font color='#E03535'>Target's privilege is upper than yours or equals yours</font>", 235, 160, 300, False)
                self.closePanel()
                self.openPanel()
            else:
                if cache:
                    self.reloadPrivs()
                else:
                    self.loadPrivs()

    def textAreaCallback(self, textAreaID, event):
        event = event.split(":")
        if event[0] != "priv":
            return
        elif event[1] == "closePanel":
            self.closePanel()
        elif event[1] == "username":
            self.addPopup(2, "<font color='#B8D995'>Target Player</font>", 235, 160, 300, False)
        elif event[1] == "select":
            priv, _id = map(int, event[2:])
            self.selectPriv(priv, _id)
        elif event[1] == "_select":
            priv, _id = map(int, event[2:])
            self.selectPriv(priv, _id, pool = True)
        elif event[1] == "unselect":
            priv, _id = map(int, event[2:])
            self.selectPriv(priv, _id, True)
        elif event[1] == "_unselect":
            priv, _id = map(int, event[2:])
            self.selectPriv(priv, _id, True, True)
        elif event[1] == "all":
            self.selectAll()
        elif event[1] == "_all":
            self.selectAll(True)
        elif event[1] in ["remove", "add"]:
            self.editPrivs(event[1])
            self.reloadPrivs()

    def addPopup(self, type, text, x, y, w, fx):
        self.lastPopupID += 1
        self.room.addPopup(self.lastPopupID, type, text, self.client.playerName, x, y, w, fx)

    def addTextArea(self, txt, x, y, w, h, bg, bd, op = 100, fx = False, _id = None):
        if _id is None:
            self.lastAreaID += 1
            _id = self.lastAreaID
        self.room.addTextArea(_id, txt, self.client.playerName, x, y, w, h, bg, bd, op, fx)

    def updateTextArea(self, id, text):
        self.room.updateTextArea(id, text, self.client.playerName)

    def removeTextArea(self, id):
        self.room.removeTextArea(id, self.client.playerName)

    def editPrivs(self, action):
        if self.targetPlayer == None:
            self.addPopup(0, "<font color='#E03535'>First select a player!</font>", 235, 160, 300, False)
            return 
            
        priv = self.targetPlayer
        if not isinstance(priv, PrivLevel):
            priv = priv.privLevel

        if action == "remove":
            for _priv in self.selectedPrivs.values():
                priv.remove(_priv)
        elif action == "add":
            for _priv in self._selectedPrivs.values():
                priv.append(_priv)

        if isinstance(self.targetPlayer, PrivLevel):
            self.Cursor.execute("UPDATE users SET PrivLevel = %s WHERE PlayerID = %s", [priv.output(), self.targetID])
            self.targetPlayer = priv

    def reloadPrivs(self):
        self.delCache(True)
        self.loadPrivs()

    def loadPrivs(self):
        if self.targetPlayer == None:
            self.addPopup(0, "<font color='#E03535'>First select a player!</font>", 235, 160, 300, False)
            return 
            
        privs = self.targetPlayer
        if not isinstance(privs, PrivLevel):
            privs = privs.privLevel.privileges.copy()
        else:
            privs = privs.privileges.copy()

        if 1 in privs:
            privs.remove(1)
        if 11 in privs:
            privs.remove(11)
        self.addTextArea("<a href='event:priv:_all'><font color='#0AE6C7' size='8'>[A]</font></a>", 228, 127, 20, 15, 0, 0, 0, False)
        self.addTextArea("<a href='event:priv:all'><font color='#0AE6C7' size='8'>[A]</font></a>", 470, 127, 20, 15, 0, 0, 0, False)
        y = 145 #başlangıç Y ekseni
        privileges = self.server.privileges
        _privs = list(privileges["privs"].keys())
        if 11 in _privs:
            _privs.remove(11)
        if 1 in _privs:
            _privs.remove(1)
        for priv in _privs:
            if not priv in privs:
                self.addTextArea(f"<a href='event:priv:_select:{priv}:{self.lastAreaID + 1}'><font color='#{self.server.privileges['colors'][priv]}'>{self.server.privileges['privs'][priv]}</font></a>", 228, y, 100, 15, 0, 0, 0, False)
                self._unselectedPrivs[self.lastAreaID] = priv
                y += 20

        y = 145 #başlangıç Y ekseni
        for priv in privs:
            self.addTextArea(f"<a href='event:priv:select:{priv}:{self.lastAreaID + 1}'><font color='#{privileges['colors'][priv]}'>{privileges['privs'][priv]}</font></a>", 470, y, 100, 15, 0, 0, 0, False)
            self.unselectedPrivs[self.lastAreaID] = priv
            y += 20

    def selectPriv(self, priv, _id, unselect = False, pool = False):
        privileges = self.server.privileges
        if pool:
            if unselect:
                self.updateTextArea(_id, f"<a href='event:priv:_select:{priv}:{_id}'><font color='#{privileges['colors'][priv]}'>{privileges['privs'][priv]}</font></a>")
                del self._selectedPrivs[_id]
                self._unselectedPrivs[_id] = priv
            else:
                if priv >= self.client.privLevel.uppermost():
                    self.addPopup(0, "<font color='#E03535'>You can't select a privilege that upper than yours.</font>", 235, 160, 300, False)
                else:
                    self.updateTextArea(_id, f"<a href='event:priv:_unselect:{priv}:{_id}'><font color='#5F0AE6'>{privileges['privs'][priv]}</font></a>")
                    del self._unselectedPrivs[_id]
                    self._selectedPrivs[_id] = priv
        else:
            if unselect:
                self.updateTextArea(_id, f"<a href='event:priv:select:{priv}:{_id}'><font color='#{privileges['colors'][priv]}'>{privileges['privs'][priv]}</font></a>")
                del self.selectedPrivs[_id]
                self.unselectedPrivs[_id] = priv
            else:
                if priv >= self.client.privLevel.uppermost():
                    self.addPopup(0, "<font color='#E03535'>You can't select a privilege that upper than yours.</font>", 235, 160, 300, False)
                else:
                    self.updateTextArea(_id, f"<a href='event:priv:unselect:{priv}:{_id}'><font color='#5F0AE6'>{privileges['privs'][priv]}</font></a>")
                    del self.unselectedPrivs[_id]
                    self.selectedPrivs[_id] = priv

    def selectAll(self, pool = False):
        if pool:
            if len(self._selectedPrivs) != 0:
                for _id, priv in self._selectedPrivs.copy().items():
                    self.selectPriv(priv, _id, True, True)
            else:
                for _id, priv in self._unselectedPrivs.copy().items():
                    self.selectPriv(priv, _id, pool = True)
        else:
            if len(self.selectedPrivs) != 0:
                for _id, priv in self.selectedPrivs.copy().items():
                    self.selectPriv(priv, _id, True)
            else:
                for _id, priv in self.unselectedPrivs.copy().items():
                    self.selectPriv(priv, _id)

    def openPanel(self):
        self.addTextArea("", 200, 60, 420, 300, 0x2d211a, 0x2d211a, 100, False)
        self.addTextArea("", 201, 61, 418, 298, 0x986742, 0x986742, 100, False)
        self.addTextArea("", 204, 64, 412, 292, 0x171311, 0x171311, 100, False)
        self.addTextArea("", 205, 65, 410, 290, 0xc191c, 0xc191c, 100, False)
        self.addTextArea("", 206, 66, 408, 288, 0x24474d, 0x24474d, 100, False)
        self.addTextArea("", 207, 67, 406, 286, 0x183337, 0x183337, 100, False)
        self.addTextArea("<p align='center'><font size='20'><j>Privilege Panel</font><br><bv>", 208, 68, 404, 283, 0x122528, 0x122528, 100, False)
        self.addTextArea("", 589, 76, 13, 13, 0x7a8d93, 0x7a8d93, 100, False)
        self.addTextArea("", 591, 78, 13, 13, 0xe1619, 0xe1619, 100, False)
        self.addTextArea("", 590, 77, 13, 13, 0x274347, 0x274347, 100, False)
        self.addTextArea("<p align='center'><font size='11'><B><a href='event:priv:closePanel'>×</a></B></font></p>", 587, 73, 20, 20, 0x314e57, 0x314e57, 0, False)
        self.addTextArea("", 213, 108, 150, 237, 0x986742, 0x986742, 100, False)
        self.addTextArea("<p align='center'><font size='15'><j>Rank Pool</font><br><bv>", 215, 111, 145, 230, 0x122528, 0x122528, 100, False)
        self.addTextArea("", 455, 108, 150, 237, 0x986742, 0x986742, 100, False)
        self.addTextArea("<p align='center'><font size='15'><j>Player Ranks</font><br><bv>", 457, 111, 145, 230, 0x122528, 0x122528, 100, False)
        self.addTextArea("", 386, 181, 45, 15, 0x7a8d93, 0x7a8d93, 100, False)
        self.addTextArea("", 388, 182, 45, 15, 0xe1619, 0xe1619, 100, False)
        self.addTextArea("<a href='event:priv:username'><v><font size='8'>PLAYER</font></v></a>", 387, 183, 45, 15, 0x274347, 0x274347, 100, False)
        self.addTextArea("", 386, 218, 45, 15, 0x7a8d93, 0x7a8d93, 100, False)
        self.addTextArea("", 388, 219, 45, 15, 0xe1619, 0xe1619, 100, False)
        self.addTextArea("<a href='event:priv:remove'><r><font size='8'>Remove</font></r></a>", 387, 220, 45, 15, 0x274347, 0x274347, 100, False)
        self.addTextArea("", 386, 255, 45, 15, 0x7a8d93, 0x7a8d93, 100, False)
        self.addTextArea("", 388, 256, 45, 15, 0xe1619, 0xe1619, 100, False)
        self.addTextArea("<a href='event:priv:add'><ch>Add</ch></a>", 387, 257, 45, 15, 0x274347, 0x274347, 100, False)

    def delCache(self, delTextArea = False):
        for _id in self.selectedPrivs.copy().keys():
            del self.selectedPrivs[_id]
            if delTextArea:
                self.removeTextArea(_id)
        for _id in self.unselectedPrivs.copy().keys():
            del self.unselectedPrivs[_id]
            if delTextArea:
                self.removeTextArea(_id)
        for _id in self._selectedPrivs.copy().keys():
            del self._selectedPrivs[_id]
            if delTextArea:
                self.removeTextArea(_id)
        for _id in self._unselectedPrivs.copy().keys():
            del self._unselectedPrivs[_id]
            if delTextArea:
                self.removeTextArea(_id)

    def closePanel(self):
        self.delCache()
        self.targetPlayer = None

        for _id in sorted(range(self.lastAreaID + 1), reverse = 1):
            self.removeTextArea(_id)
        self.lastAreaID = 0
