#coding: utf-8
import random, os, time, json, sys
from struct import *

# Modules
#from ByteArray import ByteArray
from Identifiers import Identifiers

# Utils
from utils import Utils

class ByteArray:
    def __init__(this, bytes=b""):
        if type(bytes) == str:
            try:
                bytes = bytes.encode()
            except Exception as e:
                pass
        this.bytes = bytes

    def writeByte(this, value):
        this.write(pack("!B", int(value) & 0xFF))
        return this

    def writeShort(this, value):
        this.write(pack("!H", int(value) & 0xFFFF))
        return this
    
    def writeInt(this, value):
        this.write(pack("!I", int(value) & 0xFFFFFFFF))
        return this

    def writeBool(this, value):
        return this.writeByte(1 if bool(value) else 0)
        
    def writeBoolean(this, value):
        return this.writeByte(1 if bool(value) else 0)

    def writeUTF(this, value):
        value = bytes(value.encode())
        this.writeShort(len(value))
        this.write(value)
        return this

    def writeBytes(this, value):
        this.bytes += value
        return this

    def read(this, c = 1):
        found = ""
        if this.getLength() >= c:
            found = this.bytes[:c]
            this.bytes = this.bytes[c:]

        return found

    def write(this, value):
        this.bytes += value
        return this

    def readByte(this):
        value = 0
        if this.getLength() >= 1:
            value = unpack("!B", this.read())[0]
        return value

    def readShort(this):
        value = 0
        if this.getLength() >= 2:
            value = unpack("!H", this.read(2))[0]
        return value

    def readInt(this):
        value = 0
        if this.getLength() >= 4:
            value = unpack("!I", this.read(4))[0]
        return value

    def readUTF(this):
        value = ""
        if this.getLength() >= 2:
            value = this.read(this.readShort()).decode()
        return value

    def readBool(this):
        return this.readByte() > 0

    def readUTFBytes(this, size):
        value = this.bytes[:int(size)]
        this.bytes = this.bytes[int(size):]
        return value

    def getBytes(this):
        return this.bytes

    def toByteArray(this):
        return this.getBytes()

    def getLength(this):
        return len(this.bytes)

    def bytesAvailable(this):
        return this.getLength() > 0

class Missions:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        this.Cursor = client.Cursor
        
        #Int
        this.missionsCompleted = 0

    def loadMissions(this):
        if not this.client.isGuest:
            this.getMissions()
            this.activateMissions()

    def activateMissions(this):
    	this.client.sendPacket(Identifiers.send.Activate_Missions, ByteArray().writeBoolean(True).toByteArray())

    def getMissions(this):
        now, playerID = Utils.getTime(), str(this.client.playerID)
        this.Cursor.execute("select * from missions where userid = %s", [playerID])
        rs = this.Cursor.fetchone()
        if rs:
            if rs[2] > rs[2] + 86400:
                while True:
                    if len(this.client.playerMissions) == 4: break
                    this.randomMission()
                this.Cursor.execute("update missions set missions = %s, time = %s where userid = %s", [json.dumps(this.client.playerMissions), now, playerID])
            else:
                this.client.playerMissions = json.loads(rs[1])
        else:
            while True:
                if len(this.client.playerMissions) == 4:
                    break
                this.randomMission()
            this.Cursor.execute("insert into missions values (%s, %s, %s)", [playerID, json.dumps(this.client.playerMissions), now])

    def updateMissions(this, alterDB = False):
        if alterDB:
            playerID = str(this.client.playerID)
            this.Cursor.execute("update missions set missions=%s where userid=%s", [json.dumps(this.client.playerMissions), playerID])

    def randomMission(this, isTrue=False):
        missionID = random.randint(1, 7)
        while str(missionID) in this.client.playerMissions:
            missionID = random.randint(1, 7)

        missionType = 0
        reward = random.randint(15, 50)
        collect = random.randint(10, 65)

        if missionID == 2:
            missionType = random.randint(1, 3)

        if missionID == 6:
            collect = 1
        missionID = str(missionID)
        if isTrue:
            return [missionID, missionType, 0, collect, reward, True]
        else:
            this.client.playerMissions[missionID] = [missionID, missionType, 0, collect, reward, True]

    def getMission(this, missionID):
        missionID = str(missionID)
        if missionID in this.client.playerMissions:
            return this.client.playerMissions[missionID]

    def changeMission(this, missionID):
        missionID = str(missionID)
        mission = this.randomMission(True)
        
        i = 0
        while missionID == int(mission[0]):
            mission = this.randomMission(True)
            i += 1
            if i > 21:
                break
                
        if i <= 21:
            this.client.playerMissions[mission[0]] = [mission[0], mission[1], mission[2], mission[3], mission[4], True if 10 > i else False]
            

        if missionID in this.client.playerMissions:
            del this.client.playerMissions[missionID]

        """for id, mission in this.client.playerMissions.items():
            mission[5] = False"""
        this.sendMissions()

        this.updateMissions(True)

    def upMission(this, missionID):
        missionID = str(missionID)
        if missionID in this.client.playerMissions:
            mission = this.client.playerMissions[missionID]
            mission[2] += 1
            if mission[2] >= mission[3]:
                this.completeMission(missionID)
            else:
                this.client.sendPacket(Identifiers.send.Complete_Mission, ByteArray().writeShort(missionID).writeByte(0).writeShort(mission[2]).writeShort(mission[3]).writeShort(mission[4]).writeShort(0).toByteArray())
        this.updateMissions(True)
        
    def upMissionAD(this):
        if int(this.missionsCompleted) >= 20:
            this.completeMission(missionID)
        else:
            this.client.sendPacket(Identifiers.send.Complete_Mission, ByteArray().writeByte(237).writeByte(129).writeByte(0).writeShort(this.missionsCompleted).writeShort(20).writeInt(20).writeShort(1).toByteArray())
        this.updateMissions(True)

    def completeMission(this, missionID):
        if missionID in this.client.playerMissions:
            mission = this.client.playerMissions[missionID]
            this.client.cheeseCount += mission[4]
            this.client.shopCheeses += mission[4]
            this.client.sendPacket(Identifiers.send.Complete_Mission, ByteArray().writeShort(missionID).writeByte(0).writeShort(mission[2]).writeShort(mission[3]).writeShort(mission[4]).writeShort(0).toByteArray())
            del this.client.playerMissions[missionID]
            this.randomMission()
            this.updateMissions(True)
            this.missionsCompleted += 1
            this.upMissionAD()
            
    def sendMissions(this):
        missions = this.client.playerMissions
        count = len(missions)
        p = ByteArray()
        p.writeByte(count)
        IDOO = 0
        for id, mission in missions.items():
            if IDOO == 3:
                break
            p.writeShort(mission[0]) # langues -> $QJTFM_% (short)%
            p.writeByte(mission[1])
            p.writeShort(mission[2])
            p.writeShort(mission[3])
            p.writeShort(mission[4])
            p.writeShort(0)
            p.writeBoolean(mission[5])
            IDOO +=1
            
        # 4
        mission4 = this.getMission(237129)
        p.writeByte(237)
        p.writeByte(129)
        p.writeByte(0)
        p.writeShort(int(this.missionsCompleted)) # Quantidade coletada
        p.writeShort(20) # Quantidade a coletar
        p.writeInt(20) # Quantidade a receber
        p.writeBoolean(False) # Substituir missão

                
        this.client.sendPacket(Identifiers.send.Send_Missions, p.toByteArray())
