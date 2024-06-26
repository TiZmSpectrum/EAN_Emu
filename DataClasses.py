class Client:
    userID = 0
    personaID = 0
    nuid = ""
    personaName = ""

    accountSessionKey = ""
    personaSessionKey = ""

    plasmaPacketID = 0
    playerID = 0  # PID on server

    filteredServers = 0

    locale = ""

    ipAddr = None
    networkInt = None
    theaterInt = None
    IsUp = False

    ping_timer = None
    memcheck_timer = None
    
    # NFS modification - NFSC doesn't know the difference between a PlasmaServer and PlasmaClient...
    serverData = None


class Server:
    userID = 0
    personaID = 0
    nuid = ""
    personaName = ""

    accountSessionKey = ""
    personaSessionKey = ""

    serverData = None

    plasmaPacketID = 0
    startedUBRAs = 0

    clientVersion = ""
    gameID = 0
    joiningPlayers = 0
    activePlayers = 0
    newPlayerID = 0
    connectedPlayers = []

    validServers = {'nfs.server.pc@ea.com': {'password': 'Che6rEPA', 'id': 1},  # Server NUID {'password': serverPassword, 'id': userID}
                    'bfbc.server.ps3@ea.com': {'password': 'zAmeH7bR', 'id': 2},
                    'bfbc.server.xenon@ea.com': {'password': 'B8ApRavE', 'id': 3}}

    validPersonas = {"nfs.server.p": 1,  # PersonaName: PersonaID
                     "bfbc.server.ps": 2,
                     "bfbc.server.xe": 3}

    ipAddr = None
    networkInt = None
    theaterInt = None
    IsUp = False

    ping_timer = None
    memcheck_timer = None
