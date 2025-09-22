# coding: utf-8
import re, time, random, string, time as thetime

# Library
from datetime import datetime

class Utils:
    @staticmethod
    def getLangues(langueID=None):
        datas = {0:"EN", 1:"FR", 2:"FR", 3:"BR", 4:"ES", 5:"CN", 6:"TR", 7:"VK", 8:"PL", 9:"HU", 10:"NL", 11:"RO", 12:"ID", 13:"DE", 14:"E2", 15:"AR", 16:"PH", 17:"LT", 18:"JP", 19:"CH", 20:"FI", 21:"CZ", 22:"SK", 23:"HR", 24:"BU", 25:"LV", 26:"HE", 27:"IT", 29:"ET", 30:"AZ", 31:"PT"}
        if langueID:
            return datas[langueID]
        return datas
    @staticmethod
    def getLangueID(langue=None):
        datas = {"EN":0, "FR":1, "FR":2, "BR":3, "ES":4, "CN":5, "TR":6, "VK":7, "PL":8, "HU":9, "NL":10, "RO":11, "ID":12, "DE":13, "E2":14, "AR":15, "PH":16, "LT":17, "JP":18, "CH":19, "FI":20, "CZ":21, "SK":22, "HR":23, "BU":24, "LV":25, "HE":26, "IT":27, "ET":29, "AZ":30, "PT":31}
        if langue:
            return datas[langue]
        return 0
    
    @staticmethod
    def buildMap(*elems):
        m = {}
        i = 0
        while i < len(elems):
            m[elems[i]] = elems[i + 1]
            i += 2
        return m

    @staticmethod
    def getTime():
        return int(time.time())

    @staticmethod
    def getValue(*array):
        return random.choice(array)

    @staticmethod
    def getHoursDiff(endTimeMillis):
        t = Utils.getTime()
        startTime = datetime.fromtimestamp(float(t))
        try:
            endTime = datetime.fromtimestamp(float(endTimeMillis))
        except:
            endTime = datetime(1997, 3, 4, 0, 0, 0, 0)
        result = endTime - startTime
        seconds = (result.microseconds + (result.seconds + result.days * 24 * 3600) * 10 ** 6) // float(10 ** 6)
        hours = int(int(seconds) // 3600) + 1
        return hours

    @staticmethod
    def getSecondsDiff(endTimeMillis):
        return int(time.time() - endTimeMillis)

    @staticmethod
    def getRandomChars(size):
        return "".join(random.choice(string.digits + string.ascii_uppercase + string.ascii_lowercase) for x in range(size))

    @staticmethod
    def getDaysDiff(endTimeMillis):
        startTime = datetime.fromtimestamp(float(Utils.getTime()))
        endTime = datetime.fromtimestamp(float(endTimeMillis))
        result = endTime - startTime
        return result.days + 1

    @staticmethod
    def parsePlayerName(playerName):
        return (playerName[0] + playerName[1:].lower().capitalize()) if playerName.startswith("*") or playerName.startswith("+") else playerName.lower().capitalize()

    @staticmethod
    def joinWithQuotes(list):
        return "\"" + "\", \"".join(list) + "\""

    @staticmethod
    def getYoutubeID(url):
        matcher = re.compile(".*(?:youtu.be\\/|v\\/|u\\/\\w\\/|embed\\/|watch\\?v=)([^#\\&\\?]*).*").match(url)
        return matcher.group(1) if matcher else None

    @staticmethod
    def Duration(duration):
        time = re.compile('P''(?:(?P<years>\d+)Y)?''(?:(?P<months>\d+)M)?''(?:(?P<weeks>\d+)W)?''(?:(?P<days>\d+)D)?''(?:T''(?:(?P<hours>\d+)H)?''(?:(?P<minutes>\d+)M)?''(?:(?P<seconds>\d+)S)?'')?').match(duration).groupdict()
        for key, count in time.items():
            time[key] = 0 if count is None else time[key]
        return (int(time["weeks"]) * 7 * 24 * 60 * 60) + (int(time["days"]) * 24 * 60 * 60) + (int(time["hours"]) * 60 * 60) + (int(time["minutes"]) * 60) + (int(time["seconds"]) - 1)
