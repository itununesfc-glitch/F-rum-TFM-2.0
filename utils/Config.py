class Config:
    # String
    miceName = "Transformice"
    adventureIMG = ""
    serverURL = ""
    OP = ""

    # Bool
    isDebug = False

    # Integer
    initialCheeses = 100000
    initialFraises = 100000
    initialShamanLevel = 100
    initialShamanExpNext = (32 + (initialShamanLevel - 1) * (initialShamanLevel + 2)) if initialShamanLevel < 30 else (900 + 5 * (initialShamanLevel - 29) * (initialShamanLevel + 30)) if  initialShamanLevel < 60 else (14250 + (15 * (initialShamanLevel - 59) * (initialShamanLevel + 60) / 2))
    leastMice = 0
    adventureID = 7
    hardModeCount = 50
    divineModeCount = 50
    shamanCount = 50
    firstCount = 1
    cheeseCount = 1
    bootcampCount = 150
