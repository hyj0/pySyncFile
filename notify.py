import os
import win32file

import win32con
from winnt import FILE_LIST_DIRECTORY


class Inotify:
    def __init__(self, watchDir):
        self.watchDir = watchDir
        self.handleDir = win32file.CreateFile(
                watchDir,
                FILE_LIST_DIRECTORY,
                win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
                None,
                win32con.OPEN_EXISTING,
                win32con.FILE_FLAG_BACKUP_SEMANTICS,
                None
        )

    def getNotifyEven(self):
        results = win32file.ReadDirectoryChangesW(
                self.handleDir,
                1024,
                True,
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                win32con.FILE_NOTIFY_CHANGE_SIZE |
                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                win32con.FILE_NOTIFY_CHANGE_SECURITY,
                None,
                None)

        retEventList = []
        for action, fileName in results:
            filePath = os.path.abspath(
                    os.path.join(self.watchDir, fileName)
            )
            retEventList.append((filePath, action))
        return retEventList
