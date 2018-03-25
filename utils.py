import os


def mapLocalFileToServFile(localMapPath, servMapPath, localPath):
    localMapPath = os.path.abspath(localMapPath)
    localPath = os.path.abspath(localPath)

    path = localPath.replace(localMapPath, "")
    path = path.replace("\\", "/")
    path = servMapPath + "/" + path
    return path
