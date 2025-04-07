import twint, time, datetime, pyAesCrypt

def FirePayload(filePath, encryptPass):
    print("ACTIVATED PAYLOAD")
    bufferSIZE = 64 * 1024
    pyAesCrypt.encryptFile(filePath, (filePath+'.aes'), encryptPass, bufferSIZE)

    print("SWITCH ACTIVATED - LOCKDOWN MODE ENTERED")
    exit()

def CheckKey(c, delaTime, filePath, encryptPass, targetTime):
    try:
        twint.run.Search(c)
    except ValueError:
        print("Something bad happened")
        GetTargets()
    tweets = twint.output.tweets_list
    if not tweets:
        if(time.time() >= targetTime): FirePayload(filePath, encryptPass)
        else:
            print("No results, trying again after delay")
            time.sleep(delaTime)
            CheckKey(c, delaTime, filePath, encryptPass, targetTime)
    else:
        print("Deadswitch De-Activated, Entered Safe Mode")
        exit()

def GetTargets():
    c=twint.Config()
    startTime = input("Date to start searching from (YYYY-MM-DD):\n ")
    try: datetime.datetime.strptime(startTime, '%Y-%m-%d')
    except ValueError:
        print("That's not a date, try again (YYYY-MM-DD)")
        GetTargets()
    c.Since = startTime
    c.Search = input("keyphrase to disarm switch?\n")
    c.Username = input("Twitter account to watch?\n")
    delayTime = int(input("Time in seconds to wait between checking the account\n"))
    filePath = input("File to encrypt if switch fires?\n")
    encryptPass = input("Password to encrypt file?\n")
    targetTime = (time.time() + (int(input("How many minutes to run before firing?\n"))*60))
    c.Hide_output = True
    c.Store_object = True
    CheckKey(c, delayTime, filePath, encryptPass, targetTime)

GetTargets()