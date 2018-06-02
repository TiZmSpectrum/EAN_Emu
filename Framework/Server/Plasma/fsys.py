from time import strftime
from threading import Timer

from ConfigParser import ConfigParser

from Config import readFromConfig
from Utilities.Packet import Packet
from Utilities.RandomStringGenerator import GenerateRandomString


def HandleHello(self, data):
    SaveHelloData(self, data)

    currentTime = strftime('%b-%d-%Y %H:%M:%S UTC')

    newPacketData = ConfigParser()
    newPacketData.optionxform = str

    newPacketData.add_section("PacketData")

    newPacketData.set("PacketData", "domainPartition.domain", "eagames")
    newPacketData.set("PacketData", "messengerIp", readFromConfig("connection", "emulator_ip"))
    newPacketData.set("PacketData", "messengerPort", 0)  # Unknown data are being send to this port
    newPacketData.set("PacketData", "domainPartition.subDomain", "BFBC2")
    newPacketData.set("PacketData", "TXN", "Hello")
    newPacketData.set("PacketData", "activityTimeoutSecs",
                      0)  # We could let idle clients disconnect here automatically?
    newPacketData.set("PacketData", "curTime", currentTime)
    newPacketData.set("PacketData", "theaterIp", readFromConfig("connection", "emulator_ip"))
    newPacketData.set("PacketData", "theaterPort", readFromConfig("connection", "theater_server_port"))

    Packet(newPacketData).sendPacket(self, "fsys", 0x80000000, self.CONNOBJ.plasmaPacketID)

    self.CONNOBJ.IsUp = True

    SendMemCheck(self)


def SaveHelloData(self, data):
    self.CONNOBJ.clientString = data.get("PacketData", "clientString")
    self.CONNOBJ.sku = data.get("PacketData", "sku")
    self.CONNOBJ.locale = data.get("PacketData", "locale")
    self.CONNOBJ.clientString = data.get("PacketData", "clientString")
    self.CONNOBJ.clientVersion = data.get("PacketData", "clientVersion")
    self.CONNOBJ.SDKVersion = data.get("PacketData", "SDKVersion")
    self.CONNOBJ.protocolVersion = data.get("PacketData", "protocolVersion")
    self.CONNOBJ.fragmentSize = data.get("PacketData", "fragmentSize")
    self.CONNOBJ.clientType = data.get("PacketData", "clientType")


def SendMemCheck(self):
    newPacketData = ConfigParser()
    newPacketData.optionxform = str

    newPacketData.add_section("PacketData")

    newPacketData.set("PacketData", "TXN", "MemCheck")
    newPacketData.set("PacketData", "memcheck.[]", 0)
    newPacketData.set("PacketData", "type", 0)
    newPacketData.set("PacketData", "salt", GenerateRandomString(9))

    if self.CONNOBJ.IsUp:
        Packet(newPacketData).sendPacket(self, "fsys", 0x80000000, 0)


def HandleMemCheck(self):
    if self.CONNOBJ.memcheck_timer is None and self.CONNOBJ.ping_timer is None:  # Activate both ping and memcheck timers when we receive this
        self.CONNOBJ.memcheck_timer = Timer(500, SendMemCheck, [self, ])
        self.CONNOBJ.memcheck_timer.start()
        self.CONNOBJ.ping_timer = Timer(150, SendPing, [self, ])
        self.CONNOBJ.ping_timer.start()
    else:  # Restart timers
        self.CONNOBJ.memcheck_timer.cancel()
        self.CONNOBJ.ping_timer.cancel()

        self.CONNOBJ.memcheck_timer = Timer(500, SendMemCheck, [self, ])
        self.CONNOBJ.memcheck_timer.start()
        self.CONNOBJ.ping_timer = Timer(150, SendPing, [self, ])
        self.CONNOBJ.ping_timer.start()


def HandlePing(self):
    if self.CONNOBJ.ping_timer is None:
        self.CONNOBJ.ping_timer = Timer(150, SendPing, [self, ])
        self.CONNOBJ.ping_timer.start()
    else:
        self.CONNOBJ.ping_timer.cancel()

        self.CONNOBJ.ping_timer = Timer(150, SendPing, [self, ])
        self.CONNOBJ.ping_timer.start()


def SendPing(self):
    newPacketData = ConfigParser()
    newPacketData.optionxform = str
    newPacketData.add_section("PacketData")
    newPacketData.set("PacketData", "TXN", "Ping")

    Packet(newPacketData).sendPacket(self, "fsys", 0x80000000, 0)


def HandleGoodbye(self, data):
    reason = data.get("PacketData", "reason")
    message = data.get("PacketData", "message")

    if reason == "GOODBYE_CLIENT_NORMAL":
        self.logger.new_message("[" + self.ip + ":" + str(self.port) + '][fsys] Client disconnected normally!', 2)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + "] Unknown Goodbye reason!", 2)


def HandleGetPingSites(self):
    emuIp = readFromConfig("connection", "emulator_ip")

    newPacketData = ConfigParser()
    newPacketData.optionxform = str
    newPacketData.add_section("PacketData")
    newPacketData.set("PacketData", "TXN", "GetPingSites")

    newPacketData.set("PacketData", "pingSite.[]", "4")
    newPacketData.set("PacketData", "pingSite.0.addr", emuIp)
    newPacketData.set("PacketData", "pingSite.0.type", "0")
    newPacketData.set("PacketData", "pingSite.0.name", "gva")
    newPacketData.set("PacketData", "pingSite.1.addr", emuIp)
    newPacketData.set("PacketData", "pingSite.1.type", "1")
    newPacketData.set("PacketData", "pingSite.1.name", "nrt")
    newPacketData.set("PacketData", "pingSite.2.addr", emuIp)
    newPacketData.set("PacketData", "pingSite.2.type", "2")
    newPacketData.set("PacketData", "pingSite.2.name", "iad")
    newPacketData.set("PacketData", "pingSite.3.addr", emuIp)
    newPacketData.set("PacketData", "pingSite.3.type", "3")
    newPacketData.set("PacketData", "pingSite.3.name", "sjc")
    newPacketData.set("PacketData", "minPingSitesToPing", "0")

    Packet(newPacketData).sendPacket(self, "fsys", 0x80000000, self.CONNOBJ.plasmaPacketID)


def ReceivePacket(self, data, txn):
    if txn == 'Hello':
        HandleHello(self, data)
    elif txn == 'MemCheck':
        HandleMemCheck(self)
    elif txn == 'Ping':
        HandlePing(self)
    elif txn == 'Goodbye':
        HandleGoodbye(self, data)
    elif txn == 'GetPingSites':
        HandleGetPingSites(self)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown fsys message (' + txn + ")", 2)