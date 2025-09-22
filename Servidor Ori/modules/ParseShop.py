#coding: utf-8
import binascii

from ByteArray import ByteArray
from Identifiers import Identifiers

class ParseShop:
    def __init__(self, player, server):
        self.client = player
        self.server = player.server
        self.Cursor = player.Cursor

    def getShopLength(self):
        return 0 if self.client.shopItems == "" else len(self.client.shopItems.split(","))

    def checkUnlockShopTitle(self):
        if self.getShopLength() in self.server.shopTitleList:
            title = self.server.shopTitleList[self.getShopLength()]
            self.client.checkAndRebuildTitleList("shop")
            self.client.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
            self.client.sendCompleteTitleList()
            self.client.sendTitleList()

    def checkAndRebuildBadges(self):
        rebuild = False
        for badge in self.server.shopBadges.items():
            if not badge[0] in self.client.shopBadges and self.checkInShop(badge[0]):
                self.client.shopBadges.append(str(badge[1]))
                rebuild = True

        if rebuild:
            badges = map(int, self.client.shopBadges)
            self.client.shopBadges = []
            for badge in badges:
                if not badge in self.client.shopBadges:
                    self.client.shopBadges.append(badge)

    def checkUnlockShopBadge(self, itemID):
        if not self.client.isGuest:
            if itemID in self.server.shopBadges:
                unlockedBadge = self.server.shopBadges[itemID]
                self.sendUnlockedBadge(unlockedBadge)
                self.checkAndRebuildBadges()

    def checkInShop(self, checkItem):
        if not self.client.shopItems == "":
            for shopItem in self.client.shopItems.split(","):
                if checkItem == int(shopItem.split("_")[0] if "_" in shopItem else shopItem):
                    return True
        else:
            return False

    def checkInShamanShop(self, checkItem):
        if not self.client.shamanItems == "":
            for shamanItems in self.client.shamanItems.split(","):
                if checkItem == int(shamanItems.split("_")[0] if "_" in shamanItems else shamanItems):
                    return True
        else:
            return False

    def checkInPlayerShop(self, type, playerName, checkItem):
        self.Cursor.execute("select %s from Users where Username = ?" %(type), [playerName])
        for rs in self.Cursor.fetchall():
            items = rs[type]
            if not items == "":
                for shopItem in items.split(","):
                    if checkItem == int(shopItem.split("_")[0] if "_" in shopItem else shopItem):
                        return True
            else:
                return False

    def getItemCustomization(self, checkItem, isShamanShop):
        items = self.client.shamanItems if isShamanShop else self.client.shopItems
        if not items == "":
            for shopItem in items.split(","):
                itemSplited = shopItem.split("_")
                custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                if int(itemSplited[0]) == checkItem:
                    return "" if custom == "" else ("_" + custom)
        else:
            return ""

    def getShamanItemCustom(self, code):
        item = self.client.shamanItems.split(",")
        if "_" in item:
            itemSplited = item.split("_")
            custom = (itemSplited[1] if len(itemSplited) >= 2 else "").split("+")
            if int(itemSplited[0]) == code:
                packet = ByteArray().writeByte(len(custom))
                x = 0
                while x < len(custom):
                    packet.writeInt(int(custom[x], 16))
                    x += 1
                return packet.toByteArray()
        return chr(0)

    def getShopItemPrice(self, fullItem):
        itemCat = (0 if fullItem // 10000 == 1 else fullItem // 10000) if fullItem > 9999 else fullItem // 100
        item = fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (100 * itemCat) if fullItem > 99 else fullItem
        return self.getItemPromotion(itemCat, item, self.server.shopListCheck[str(itemCat) + "|" + str(item)][1])

    def getShamanShopItemPrice(self, fullItem):
        return self.server.shamanShopListCheck[str(fullItem)][1]

    def getItemPromotion(self, itemCat, item, price):
        for promotion in self.server.shopPromotions:
            if promotion[0] == itemCat and promotion[1] == item:
                return int(promotion[2] // 100.0 * price)
        return price

    def sendShopList(self):
        self.sendShopList(True)

    def sendShopList(self, sendItems=True):
        shopItems = [] if self.client.shopItems == "" else self.client.shopItems.split(",")

        packet = ByteArray().writeInt(self.client.shopCheeses).writeInt(self.client.shopFraises).writeUTF(self.client.playerLook).writeInt(len(shopItems))
        for item in shopItems:
            if "_" in item:
                itemSplited = item.split("_")
                realItem = itemSplited[0]
                custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")
                packet.writeByte(len(realCustom)+1).writeInt(int(realItem))
                x = 0
                while x < len(realCustom):
                    packet.writeInt(int(realCustom[x], 16))
                    x += 1
            else:
                packet.writeByte(0).writeInt(int(item))

        shop = self.server.shopList if sendItems else []
        packet.writeInt(len(shop))
        for item in shop:
            packet.writeShort(item["category"]).writeShort(item["id"]).writeByte(item["customs"]).writeBoolean(item["new"]).writeBoolean("purchasable" in item).writeInt(item["cheese"]).writeInt(item["fraise"]).writeShort(0)

        looks = self.server.shopOutfits if sendItems else []
        packet.writeByte(len(looks))
        for item in looks:
            packet.writeShort(item["id"])
            packet.writeUTF("".join(item["look"]))
            packet.writeByte(item["bg"])

        packet.writeShort(len(self.client.clothes))
        for clothe in self.client.clothes:
            clotheSplited = clothe.split("/")
            packet.writeUTF(clotheSplited[1] + ";" + clotheSplited[2] + ";" + clotheSplited[3])

        shamanItems = [] if self.client.shamanItems == "" else self.client.shamanItems.split(",")
        packet.writeShort(len(shamanItems))
        for item in shamanItems:
            if "_" in item:
                itemSplited = item.split("_")
                realItem = itemSplited[0]
                custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")
                packet.writeShort(int(realItem))
                packet.writeBoolean(item in self.client.shamanLook.split(",")).writeByte(len(realCustom)+1)
                x = 0
                while x < len(realCustom):
                    packet.writeInt(int(realCustom[x], 16))
                    x += 1
            else:
                packet.writeShort(int(item)).writeBoolean(item in self.client.shamanLook.split(",")).writeByte(0)

        shamanShop = self.server.shamanShopList if sendItems else []
        packet.writeShort(len(shamanShop))
        for item in shamanShop:
            packet.writeInt(item["id"]).writeByte(item["customs"]).writeBoolean(item.get("new")).writeByte(item.get("flag")).writeInt(item["cheese"]).writeShort(item["fraise"])
        self.client.sendPacket(Identifiers.send.Shop_List, packet.toByteArray())

    def sendShamanItems(self):
        shamanItems = [] if self.client.shamanItems == "" else self.client.shamanItems.split(",")

        packet = ByteArray().writeShort(len(shamanItems))
        for item in shamanItems:
            if "_" in item:
                custom = item.split("_")[1] if len(item.split("_")) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")
                packet.writeShort(int(item.split("_")[0])).writeBoolean(item in self.client.shamanLook.split(",")).writeByte(len(realCustom) + 1)
                x = 0
                while x < len(realCustom):
                    packet.writeInt(int(realCustom[x], 16))
                    x += 1
            else:
                packet.writeShort(int(item)).writeBoolean(item in self.client.shamanLook.split(",")).writeByte(0)
        self.client.sendPacket(Identifiers.send.Shaman_Items, packet.toByteArray())

    def sendLookChange(self):
        look = self.client.playerLook.split(";")
        packet = ByteArray().writeShort(int(look[0]))

        for item in look[1].split(","):
            if "_" in item:
                custom = item.split("_")[1] if len(item.split("_")) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")
                packet.writeInt(int(item.split("_")[0])).writeByte(len(realCustom))

                x = 0
                while x < len(realCustom):
                    packet.writeInt(int(realCustom[x], 16))
                    x += 1
            else:
                packet.writeInt(int(item)).writeByte(0)

        i = 0
        while i < 10:
            packet.writeByte(0)
            i += 1

        try:
            packet.writeInt(int(self.client.mouseColor, 16))
        except:
            packet.writeInt(int("78583A", 16))
        self.client.sendPacket(Identifiers.send.Look_Change, packet.toByteArray())

    def sendShamanLook(self):
        items = ByteArray()

        count = 0
        for item in self.client.shamanLook.split(","):
            realItem = int(item.split("_")[0]) if "_" in item else int(item)
            if realItem != 0:
                items.writeShort(realItem)
                count += 1
        self.client.sendPacket(Identifiers.send.Shaman_Look, ByteArray().writeShort(count).writeBytes(items.toByteArray()).toByteArray())

    def sendItemBuy(self, fullItem):
        self.client.sendPacket(Identifiers.send.Item_Buy, ByteArray().writeInt(fullItem).writeByte(0).toByteArray())

    def sendUnlockedBadge(self, badge):
        self.client.room.sendAll(Identifiers.send.Unlocked_Badge, ByteArray().writeInt(self.client.playerCode).writeShort(badge).toByteArray())

    def sendGiftResult(self, type, playerName):
        self.client.sendPacket(Identifiers.send.Gift_Result, ByteArray().writeByte(type).writeByte(0).writeUTF(playerName).writeByte(0).writeShort(0).toByteArray())

    def equipClothe(self, packet):
        clotheID = packet.readByte()
        for clothe in self.client.clothes:
            values = clothe.split("/")
            if values[0] == "%02d" %(clotheID):
                self.client.playerLook = values[1]
                self.client.mouseColor = values[2]
                self.client.shamanColor = values[3]
                break
        self.sendLookChange()
        self.sendShopList(False)

    def saveClothe(self, packet):
        clotheID = packet.readByte()
        for clothe in self.client.clothes:
            values = clothe.split("/")
            if values[0] == "%02d" %(clotheID):
                values[1] = self.client.playerLook
                values[2] = self.client.mouseColor
                values[3] = self.client.shamanColor
                self.client.clothes[self.client.clothes.index(clothe)] = "/".join(values)
                break

        self.sendShopList(False)

    def sendShopInfo(self):
        self.client.sendPacket(Identifiers.send.Shop_Info, ByteArray().writeInt(self.client.shopCheeses).writeInt(self.client.shopFraises).toByteArray())

    def equipItem(self, packet):
        fullItem = packet.readInt()
        itemCat = (fullItem - 10000) // 10000 if fullItem > 9999 else fullItem // 100
        item = fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (100 * itemCat) if fullItem > 99 else fullItem
        lookList = self.client.playerLook.split(";")
        lookItems = lookList[1].split(",")
        lookCheckList = lookItems[:]
        i = 0
        while i < len(lookCheckList):
            lookCheckList[i] = lookCheckList[i].split("_")[0] if "_" in lookCheckList[i] else lookCheckList[i]
            i += 1

        if itemCat <= 10:
            lookItems[itemCat] = "0" if lookCheckList[itemCat] == str(item) else str(item) + self.getItemCustomization(fullItem, False)
        elif itemCat == 21:
            lookList[0] = "1"
            color = "bd9067" if item == 0 else "593618" if item == 1 else "8c887f" if item == 2 else "dfd8ce" if item == 3 else "4e443a" if item == 4 else "e3c07e" if item == 5 else "272220" if item == 6 else "78583a"
            self.client.mouseColor = "78583a" if self.client.mouseColor == color else color
        else:
            lookList[0] = "1" if lookList[0] == str(item) else str(item)
            self.client.mouseColor = "78583a"

        self.client.playerLook = lookList[0] + ";" + ",".join(map(str, lookItems))
        self.sendLookChange()

    def buyItem(self, packet):
        fullItem, withFraises = packet.readInt(), packet.readBoolean()
        itemCat = (fullItem - 10000) // 10000 if fullItem > 9999 else fullItem // 100
        item = fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (100 * itemCat) if fullItem > 99 else fullItem
        self.client.shopItems += str(fullItem) if self.client.shopItems == "" else "," + str(fullItem)
        price = self.getItemPromotion(itemCat, item, self.server.shopListCheck[str(itemCat) + "|" + str(item)][1 if withFraises else 0])
        if withFraises:
            self.client.shopFraises -= price
        else:
            self.client.shopCheeses -= price

        self.sendItemBuy(fullItem)
        self.sendShopList(False)
        self.client.sendAnimZelda(0, fullItem)
        self.checkUnlockShopTitle()
        self.checkUnlockShopBadge(fullItem)

    def customItemBuy(self, packet):
        fullItem, withFraises = packet.readInt(), packet.readBoolean()

        items = self.client.shopItems.split(",")
        for shopItem in items:
            item = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(item):
                items[items.index(shopItem)] = shopItem + "_"
                break

        self.client.shopItems = ",".join(items)
        if withFraises:
            self.client.shopFraises -= 20
        else:
            self.client.shopCheeses -= 2000

        if len(self.client.custom) == 1:
            if not fullItem in self.client.custom:
                self.client.custom.append(fullItem)
        else:
            if not str(fullItem) in self.client.custom:
                self.client.custom.append(str(fullItem))

        self.sendShopList(False)

    def customItem(self, packet):
        fullItem, length = packet.readInt(), packet.readByte()
        custom = length
        customs = list()

        i = 0
        while i < length:
            customs.append(packet.readInt())
            i += 1

        items = self.client.shopItems.split(",")
        for shopItem in items:
            sItem = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(sItem):
                newCustoms = map(lambda color: "%06X" %(0xffffff & color), customs)

                items[items.index(shopItem)] = sItem + "_" + "+".join(newCustoms)
                self.client.shopItems = ",".join(items)

                itemCat = (0 if fullItem // 10000 == 1 else fullItem // 10000) if fullItem > 9999 else fullItem // 100
                item = fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (100 * itemCat) if fullItem > 99 else fullItem
                equip = str(item) + self.getItemCustomization(fullItem, False)
                lookList = self.client.playerLook.split(";")
                lookItems = lookList[1].split(",")

                if "_" in lookItems[itemCat]:
                    if lookItems[itemCat].split("_")[0] == str(item):
                        lookItems[itemCat] = equip

                elif lookItems[itemCat] == str(item):
                    lookItems[itemCat] = equip
                self.client.playerLook = lookList[0] + ";" + ",".join(lookItems)
                self.sendShopList(False)
                self.sendLookChange()
                break

    def buyShamanItem(self, packet):
        fullItem, withFraises = packet.readShort(), packet.readBoolean()
        price = self.server.shamanShopListCheck[str(fullItem)][1 if withFraises else 0]
        self.client.shamanItems += str(fullItem) if self.client.shamanItems == "" else "," + str(fullItem)

        if withFraises:
            self.client.shopFraises -= price
        else:
            self.client.shopCheeses -= price

        self.sendShopList(False)
        self.client.sendAnimZelda(1, fullItem)

    def equipShamanItem(self, packet):
        fullItem = packet.readInt()
        item = str(fullItem) + self.getItemCustomization(fullItem, True)
        itemStr = str(fullItem)
        itemCat = int(itemStr[:len(itemStr)-2])
        index = itemCat if itemCat <= 4 else itemCat - 1 if itemCat <= 7 else 7 if itemCat == 10 else 8 if itemCat == 17 else 9
        index -= 1
        lookItems = self.client.shamanLook.split(",")

        if "_" in lookItems[index]:
            if lookItems[index].split("_")[0] == itemStr:
                lookItems[index] = "0"
            else:
                lookItems[index] = item

        elif lookItems[index] == itemStr:
            lookItems[index] = "0"
        else:
            lookItems[index] = item

        self.client.shamanLook = ",".join(lookItems)
        self.sendShamanLook()

    def customShamanItemBuy(self, packet):
        fullItem, withFraises = packet.readInt(), packet.readBoolean()

        items = self.client.shamanItems.split(",")
        for shopItem in items:
            item = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(item):
                items[items.index(shopItem)] = shopItem + "_"
                break

        self.client.shamanItems = ",".join(items)
        if withFraises:
            self.client.shopFraises -= 150
        else:
            self.client.shopCheeses -= 4000

        self.sendShopList(False)

    def customShamanItem(self, packet):
        fullItem, length = packet.readInt(), packet.readByte()
        customs = []
        i = 0
        while i < length:
            customs.append(packet.readInt())
            i += 1

        items = self.client.shamanItems.split(",")
        for shopItem in items:
            sItem = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(sItem):
                newCustoms = map(lambda color: "%06X" %(0xFFFFFF & color), customs)

                items[items.index(shopItem)] = sItem + "_" + "+".join(newCustoms)
                self.client.shamanItems = ",".join(items)

                item = str(fullItem) + self.getItemCustomization(fullItem, True)
                itemStr = str(fullItem)
                itemCat = int(itemStr[len(itemStr)-2:])
                index = itemCat if itemCat <= 4 else itemCat - 1 if itemCat <= 7 else 7 if itemCat == 10 else 8 if itemCat == 17 else 9
                index -= 1
                lookItems = self.client.shamanLook.split(",")

                if "_" in lookItems[index]:
                    if lookItems[index].split("_")[0] == itemStr:
                        lookItems[index] = item

                elif lookItems[index] == itemStr:
                    lookItems[index] = item

                self.client.shamanLook = ",".join(lookItems)
                self.sendShopList()
                self.sendShamanLook()
                break

    def buyClothe(self, packet):
        clotheID, withFraises = packet.readByte(), packet.readBoolean()
        self.client.clothes.append("%02d/1;0,0,0,0,0,0,0,0,0/78583a/%s" %(clotheID, "fade55" if self.client.shamanSaves >= 1000 else "95d9d6"))
        if withFraises:
            self.client.shopFraises -= 5 if clotheID == 0 else 50 if clotheID == 1 else 100
        else:
            self.client.shopFraises -= 40 if clotheID == 0 else 1000 if clotheID == 1 else 2000 if clotheID == 2 else 4000

        self.sendShopList(False)

    def sendGift(self, packet):
        playerName, isShamanItem, fullItem, message = packet.readUTF(), packet.readBoolean(), packet.readInt(), packet.readUTF()
        if not self.server.checkExistingUser(playerName):
            self.sendGiftResult(1, playerName)
        else:
            player = self.server.players.get(playerName)
            if player != None:
                if (player.parseShop.checkInShamanShop(fullItem) if isShamanItem else player.parseShop.checkInShop(fullItem)):
                    self.sendGiftResult(2, playerName)
                else:
                    self.server.lastGiftID += 1
                    player.sendPacket(Identifiers.send.Shop_Gift, ByteArray().writeInt(self.server.lastGiftID).writeUTF(self.client.playerName).writeUTF(self.client.playerLook).writeBoolean(isShamanItem).writeInt(fullItem).writeUTF(message).writeBoolean(False).toByteArray())
                    self.sendGiftResult(0, playerName)
                    self.server.shopGifts[self.server.lastGiftID] = [self.client.playerName, isShamanItem, fullItem]
                    self.client.shopFraises -= self.getShamanShopItemPrice(fullItem) if isShamanItem else self.getShopItemPrice(fullItem)
                    self.sendShopList()
            else:
                gifts = ""
                if (self.checkInPlayerShop("ShamanItems" if isShamanItem else "ShopItems", playerName, fullItem)):
                    self.sendGiftResult(2, playerName)
                else:
                    self.Cursor.execute("select Gifts from Users where Username = ?", [playerName])
                    rs = self.Cursor.fetchone()
                    gifts = rs[0]

                gifts += ("" if gifts == "" else "/") + binascii.hexlify("|".join(map(str, [self.client.playerName, self.client.playerLook, isShamanItem, fullItem, message])))
                self.Cursor.execute("update Users set Gifts = ? where Username = ?", [gifts, playerName])
                self.sendGiftResult(0, playerName)

    def giftResult(self, packet):
        giftID, isOpen, message, isMessage = packet.readInt(), packet.readBoolean(), packet.readUTF(), packet.readBoolean()
        if isOpen:
            values = self.server.shopGifts[int(giftID)]
            player = self.server.players.get(str(values[0]))
            if player != None:
                player.sendLangueMessage("", "$DonItemRecu", self.client.playerName)

            isShamanItem = bool(values[1])
            fullItem = int(values[2])
            if isShamanItem:
                self.client.shamanItems += str(fullItem) if self.client.shamanItems == "" else ",%s" %(fullItem)
                self.sendShopList(False)
                self.client.sendAnimZelda(1, fullItem)
            else:
                self.client.shopItems += str(fullItem) if self.client.shopItems == "" else ",%s" %(fullItem)
                self.client.sendAnimZelda(0, fullItem)
                self.checkUnlockShopTitle()
                self.checkUnlockShopBadge(fullItem)

        elif not message == "":
            values = self.server.shopGifts[int(giftID)]
            player = self.server.players.get(str(values[0]))
            if player != None:
                player.sendPacket(Identifiers.send.Shop_Gift, ByteArray().writeInt(giftID).writeUTF(self.client.playerName).writeUTF(self.client.playerLook).writeBoolean(bool(values[1])).writeShort(int(values[2])).writeUTF(message).writeBoolean(True).toByteArray())
            else:
                messages = ""
                self.Cursor.execute("select Messages from Users where Username = ?", [str(values[0])])
                rs = self.Cursor.fetchone()
                messages = rs[0]

                messages += ("" if messages == "" else "/") + binascii.hexlify("|".join(map(str, [self.client.playerName, self.client.playerLook, values[1], values[2], message])))
                self.Cursor.execute("update Users set Messages = ? where Username = ?", [messages, str(values[0])])

    def checkGiftsAndMessages(self, lastReceivedGifts, lastReceivedMessages):
        needUpdate = False
        gifts = lastReceivedGifts.split("/")
        for gift in gifts:
            if not gift == "":
                values = binascii.unhexlify(gift).split("|", 4)
                self.server.lastGiftID += 1
                self.client.sendPacket(Identifiers.send.Shop_Gift, ByteArray().writeInt(self.server.lastGiftID).writeUTF(values[0]).writeUTF(values[1]).writeBoolean(bool(values[2])).writeShort(int(values[3])).writeUTF(values[4] if len(values) > 4 else "").writeBoolean(False).toByteArray())
                self.server.shopGifts[self.server.lastGiftID] = [values[0], bool(values[2]), int(values[3])]
                needUpdate = True

        messages = lastReceivedMessages.split("/")
        for message in messages:
            if not message == "":
                values = binascii.unhexlify(message).split("|", 4)
                self.client.sendPacket(Identifiers.send.Shop_GIft, ByteArray().writeShort(0).writeShort(0).writeUTF(values[0]).writeBoolean(bool(values[1])).writeShort(int(values[2])).writeUTF(values[4]).writeUTF(values[3]).writeBoolean(True).toByteArray())
                needUpdate = True

        if needUpdate:
            self.Cursor.execute("update Users set Gifts = '', Messages = '' where Username = ?", [self.client.playerName])

