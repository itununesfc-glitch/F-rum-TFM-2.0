from ctypes import c_int32 as int32
from struct import *

class ByteArray:
    def __init__(self, bytes=b""):
        if isinstance(bytes, str):
            bytes = bytes.encode()
        self.bytes = bytes

    def writeByte(self, value):
        value = 255 if int(value) > 255 else int(value)
        self.write(pack("!b" if value < 0 else "!B", value))
        return self

    def writeShort(self, value):
        value = 65535 if int(value) > 65535 else int(value)
        self.write(pack("!h" if value < 0 else "!H", value))
        return self
    
    def writeInt(self, value):
        value = int(value)
        self.write(pack("!i" if value < 0 else "!I", value))
        return self

    def writeBoolean(self, value):
        return self.writeByte(1 if bool(value) else 0)

    def copy(self):
        return ByteArray(self.bytes)

    def writeUTF(self, value):
        if isinstance(value, int):
            value = str(value)
        if isinstance(value, str):
            value = value.encode()
        self.writeShort(len(value))
        self.write(value)
        return self

    def writeBytes(self, value):
        if isinstance(value, str):
            value = value.encode()
        self.bytes += value
        return self

    def read(self, c = 1):
        found = ""
        if self.getLength() >= c:
            found = self.bytes[:c]
            self.bytes = self.bytes[c:]
        return found

    def write(self, value):
        if isinstance(value, str):
            value = value.encode()
        self.bytes += value
        return self

    def readByte(self):
        value = 0
        if self.getLength() >= 1:
            value = unpack("!B", self.read())[0]
        return value

    def readShort(self):
        value = 0
        if self.getLength() >= 2:
            value = unpack("!H", self.read(2))[0]
        return value

    def readInt(self):
        value = 0
        if self.getLength() >= 4:
            value = unpack("!I", self.read(4))[0]
        return value

    def readUTF(self):
        value = ""
        if self.getLength() >= 2:
            value = self.read(self.readShort())
            if isinstance(value, bytes):
                value = value.decode()
        return value

    def readBoolean(self):
        return self.readByte() > 0

    def readUTFBytes(self, size):
        value = self.bytes[:int(size)]
        self.bytes = self.bytes[int(size):]
        return value

    def getBytes(self):
        return self.bytes

    def toByteArray(self):
        return self.getBytes()

    def getLength(self):
        return len(self.bytes)

    def bytesAvailable(self):
        return self.getLength() > 0
    
    def compute_keys(self, keys, keyword):
        nbr = 5381
        length = len(keys)
        kwlen = len(keyword)
        for i in range(length):
            nbr = int32((nbr << 5) + nbr + keys[i] + ord(keyword[i%kwlen])).value

        keys = []
        for i in range(length):
            nbr = int32(nbr ^ nbr << 13).value
            nbr = int32(nbr ^ nbr >> 17).value
            nbr = int32(nbr ^ nbr << 5).value
            keys.append(nbr)

        return keys
    
    def decode_chunks(self, v, n, keys):
        DELTA = 0X9E3779B9
        rounds = 6 + 52//n
        sum = rounds*DELTA
        y = v[0]
        for i in range(rounds):
            e = (sum >> 2) & 3
            for p in range(n-1, -1, -1):
                z = v[p-1]
                y = v[p] = (v[p] - (((z>>5^y<<2) + (y>>3^z<<4)) ^ ((sum^y) + (keys[(p&3)^e] ^ z))))&0xffffffff
            sum = (sum - DELTA) & 0xffffffff
        return v
    
    def decryptIdentification(self, keys):
        if len(self.bytes)<10:
            raise Exception()
        barray = ByteArray()
        chunks = []
        for i in range(self.readShort()):
            chunks.append(self.readUnsignedInt())
        keys = self.compute_keys(keys, "identification")
        chunks = self.decode_chunks(chunks, len(chunks), keys)
        for chunk in chunks:
            barray.writeInt(chunk)
        self.bytes = barray.bytes
        return self

    def decrypt(self, keys, packetID = None):
        if packetID == None:
            return self.decryptIdentification(keys)
            
        packetID += 1
        keys = self.compute_keys(keys, "msg")    
        self.bytes = bytes(bytearray([(byte^keys[(packetID+i)%20])&0xff for i, byte in enumerate(self.bytes)]))
        return self