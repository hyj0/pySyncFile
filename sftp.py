import paramiko


class Sftp:
    def __init__(self, host, user, password, servPort=22):
        self.connect = paramiko.Transport((host, servPort))
        self.connect.connect(
                None, username=user, password=password,
        )
        self.sftp = paramiko.SFTPClient.from_transport(self.connect)

    def uploadFile(self, localFile, servFile):
        print("upload", localFile, "-->", servFile)
        self.sftp.put(localFile, servFile)

    def mkdir(self, servDir):
        self.sftp.mkdir(servDir)
        print("mkdir", servDir)

    def delete(self, servFile):
        self.sftp.remove(servFile)


if __name__ == "__main__":
    sftp = Sftp("192.168.200.132", "hyj", "123456")

    # dirlist on remote host
    dirlist = sftp.sftp.listdir('.')
    print("Dirlist: %s" % dirlist)

    sftp.sftp.mkdir("/home/hyj/pySyncFile/aa/bb/")

    sftp.uploadFile("./sftp.py", "/home/hyj/pySyncFile/sftp.py")
