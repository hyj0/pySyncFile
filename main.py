import ConfigParser
import os

import utils
from notify import Inotify
from sftp import Sftp


def isIgoreFile(file, ignoreList):
    for ignoreStr in ignoreList:
        if filePath.find(ignoreStr.strip()) >= 0:
            return True
    return False


if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read("./config.ini")
    localDir = config.get("map", "localDir")
    localDir = os.path.abspath(localDir)
    servDir = config.get("map", "servDir")

    if not os.path.exists(localDir) \
            or not os.path.isdir(localDir):
        print("localDir err path=", localDir)
        exit(1)

    host = config.get("serv", "host")
    user = config.get("serv", "userName")
    password = config.get("serv", "password")
    sftp = Sftp(host, user, password)

    ignoreList = config.get("map", "ignore").split(";")

    inotify = Inotify(localDir)

    print("start sync", localDir, host + ":" + servDir)
    while True:
        eventList = inotify.getNotifyEven()
        for filePath, action in eventList:
            #
            if isIgoreFile(filePath, ignoreList):
                continue

            servFile = utils.mapLocalFileToServFile(localDir, servDir, filePath)
            if action == 1:
                print(filePath, "Created")
                if os.path.isdir(filePath):
                    sftp.mkdir(servFile)
                elif os.path.isfile(filePath):
                    sftp.uploadFile(filePath, servFile)

            elif action == 2:
                print(filePath, "Deleted")
            elif action == 3:
                print(filePath, "updated")
                if os.path.isfile(filePath):
                    sftp.uploadFile(filePath, servFile)

            elif action == 4:
                print(filePath, "Renamed from ")
            elif action == 5:
                print(filePath, "Renamed to")
                if os.path.isfile(filePath):
                    sftp.uploadFile(filePath, servFile)
            else:
                pass
