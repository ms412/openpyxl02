import paramiko
import time
import os
import csv

from library.msgbus import msgbus

class WrapperRemote():

    def __init__(self,config):

        self._config = config

        self._host = config.get('HOST',None)
        self._user = config.get('USER',None)
        self._passwd = config.get('PASSWD',None)
        self._path = config.get('PATH',None)
        self._filefilter = config.get('FILE_FILTER',None)
        self._tempfile = config.get('TMP_DIR',None)

        self._sshClient = paramiko.SSHClient()
        self._sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._sftp = None
        print('Create Object',self._host,self._user,self._passwd)
        self.connect(self._host,self._user,self._passwd)

    def __del__(self):
        self._sftp.close()

    def connect(self,host,user,passwd):

        try:
            self._sshClient.connect(host, username=user, password=passwd)
            self._sftp = self._sshClient.open_sftp()
            print('connected')
        except paramiko.SSHException:
            print ("Connection Failed")
            quit()
        return True

    def chdir(self,directory):
        self._sftp.chdir(directory)
        return True


    def fileinRemoteDirLatest(self,filefilter):
        latest = 0
        latestfile = None
       # sftp = self._sshClient.open_sftp()
        #sftp.chdir('/opt')
      #  print (sftp.listdir_attr())

        for fileattr in self._sftp.listdir_attr():
         #   print('xx',fileattr.filename,fileattr.st_mtime)
            if fileattr.filename.startswith(filefilter) and fileattr.st_mtime > latest:
                latest = fileattr.st_mtime
                latestfile = fileattr.filename

        print('latest',latestfile)
        return latestfile, latest

    def getFile(self,localdir,filename):
        print('TEst',localdir+'/'+filename,self._path+'/'+filename)
        self._sftp.get(self._path+'/'+filename,localdir+'/'+filename)


class remote(msgbus):

    def __init__(self,config):
        self._host = config.get('HOST',None)
        self._user = config.get('USER',None)
        self._passwd = config.get('PASSWD',None)
        self._path = config.get('PATH',None)
        self._filefilter = config.get('FILE_FILTER',None)
        self._tempfile = config.get('TMP_DIR',None)

        self._sshClient = paramiko.SSHClient()
        self._sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print('Create Object')

    def __del__(self):
        self._sshClient.close()
        print("delete myself")

    def connect(self,host,user,passwd):

        try:
            self._sshClient.connect(host, username=user, password=passwd)
            print('connected')
        except paramiko.SSHException:
            print ("Connection Failed")
            quit()
        return True

    def filesinRemoteDir(self,path):
        print(path)
        filelist = []
        stdin, stdout, stderr = self._sshClient.exec_command("ls " + path)
        #filelist = stdout.read().splitlines()
   #     print (stdout.read())
        for item in stdout.read().splitlines():
            filelist.append(item.decode("utf-8"))
        return filelist

    def filesinRemoteDirFilter(self):
        filelist = []
        templist = self.filesinRemoteDir()
        for item in templist:
            filelist.append= item.startwith(self._filefilter)

        return filelist

    def fileinRemoteDirLatest(self,filefilter):
        latest = 0
        latestfile = None

        for fileattr in self._sshClient.listdir_attr():
            if fileattr.filename.startswith(filefilter) and fileattr.st_mtime > latest:
                latest = fileattr.st_mtime
                latestfile = fileattr.filename

        return latestfile

    def chdir(self,path):
        self._sshClient.chdir(path)
        return True

    def listdir(self,path = None):
        filelist = []
        if not path:
            filelist = self._sshClient.listdir(path=',')
        else:
            filelist = self._sshClient.exec_command(path =  path)

        return filelist

    def listdir_attr(self,path = None):
        if path:
            self.chdir(path)
        return self._sshClient.listdir_attr()

    def listdir_filname(self,name,path=None):
        if path:
            self.chdir(path)


    def get(self,localdir,filelist):

        ftp = self._sshClient.open_sftp()
        for afile in filelist:
            print('afile',afile)
            (head, filename) = os.path.split(afile)
            print('Filename', filename)
            print('localfile',localdir+filename)
            ftp.get(afile, localdir +filename)
            #ftp.get(afile, './'+filename)
        ftp.close()
