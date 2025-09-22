#!/usr/bin/env python3
"""
Simple test client to send a login packet to the game server running on 127.0.0.1:11801.
This follows the project's ByteArray.writeUTF format: unsigned short (big-endian) length + UTF-8 bytes.

Adjust `USERNAME` and `PASSWORD` to match a test account in your DB.
"""
import socket
import struct

HOST = '127.0.0.1'
PORT = 11802  # temporarily use alternate port to avoid conflicting supervisor instance on 11801

# fill in with the test user created in the DB (from the repo debugging steps)
USERNAME = 'testuser'
PASSWORD = 'testpass'
URL = ''
STARTROOM = '1;0;0;0'  # guess; server seems to accept any string for startRoom
RESULT_KEY = 0

# Packet identifiers from modules/Identifiers.py (C, Login) => C=26, Login.Login=8
C = 26
LOGIN = 8

# Informations IDs (from modules/Identifiers.py)
INFORMATIONS_C = 28
CORRECT_VERSION_CC = 3


def write_utf(s: str) -> bytes:
    b = s.encode('utf-8')
    return struct.pack('>H', len(b)) + b


def build_packet(cid: int, subcid: int, payload: bytes) -> bytes:
    # The server expects a varint length prefix (little-endian 7-bit groups with continuation bit),
    # followed by: packetID (1 byte), C (1 byte), CC (1 byte), payload.
    # packetID can be 0 from the client.
    content = bytes([0, cid, subcid]) + payload
    # length = len(content) because server's getnewlen expects length encoded as (len(data)+?)
    # In server sendData length was len(data) + 2 (for identifiers). For client we include packetID+C+CC in content,
    # so length should be len(content).
    length = len(content)
    parts = []
    calc1 = length >> 7
    while calc1 != 0:
        parts.append(((length & 127) | 128))
        length = calc1
        calc1 = calc1 >> 7
    parts.append(length & 127)
    return bytes(parts) + content


def build_correct_version_packet(version: int, lang: str, ckey: str) -> bytes:
    # payload: short(version) + UTF(lang) + UTF(ckey)
    payload = struct.pack('>H', int(version))
    payload += write_utf(lang)
    payload += write_utf(ckey)
    return build_packet(INFORMATIONS_C, CORRECT_VERSION_CC, payload)


def build_login_packet(username, password, url, startroom, result_key):
    # According to ParsePackets.Login.Login handler in the repo, it reads:
    # 1) packet.readUTF() -> parsePlayerName -> we send username
    # 2) packet.readUTF() -> password
    # 3) packet.readUTF() -> url
    # 4) packet.readUTF() -> startRoom
    # 5) packet.readInt() -> resultKey
    payload = b''
    payload += write_utf(username)
    payload += write_utf(password)
    payload += write_utf(url)
    payload += write_utf(startroom)
    payload += struct.pack('>i', int(result_key))
    return build_packet(C, LOGIN, payload)


if __name__ == '__main__':
    # First send Correct_Version handshake using info from include/files/infoSWF.json
    # Use the known values from the repository: version=626, key='MdIglcIq'
    version = 626
    lang = 'en'
    ckey = 'MdIglcIq'

    cv_pkt = build_correct_version_packet(version, lang, ckey)
    login_pkt = build_login_packet(USERNAME, PASSWORD, URL, STARTROOM, RESULT_KEY)

    print('Connecting to', HOST, PORT)
    with socket.create_connection((HOST, PORT), timeout=5) as s:
        print('Sending Correct_Version packet, length', len(cv_pkt))
        s.sendall(cv_pkt)
        try:
            s.settimeout(3.0)
            data = s.recv(4096)
            if data:
                print('Received after Correct_Version:', data)
            else:
                print('No data received after Correct_Version; server may have closed connection')
        except socket.timeout:
            print('Timed out waiting for server response to Correct_Version')

        # If server responded (or even if not), try sending login packet
        print('Sending login packet, length', len(login_pkt))
        s.sendall(login_pkt)
        try:
            s.settimeout(3.0)
            data = s.recv(4096)
            if data:
                print('Received after Login:', data)
            else:
                print('No data received after Login; server may have closed connection')
        except socket.timeout:
            print('Timed out waiting for server response to Login')
