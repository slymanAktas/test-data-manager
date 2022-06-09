import paramiko


class Paramiko:
    # http://docs.paramiko.org/en/2.1/api/sftp.html#paramiko.sftp_attr.SFTPAttributes
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(hostname=self.host, username=self.username, password=self.password, timeout=5)
        # self.ssh_client.connect(hostname=self.host, port=22, username=self.username, password=self.password)

    def close_connection(self):
        self.ssh_client.close()

    def run_command(self, command):
        self.ssh_client.invoke_shell()
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        # return stdout.readline()
        return stdout.readlines()

    def download_from_remote_machine(self, remotefilepath, localfilepath):
        ftp_client = self.ssh_client.open_sftp()
        ftp_client.get(remotefilepath, localfilepath)
        ftp_client.close()

    def upload_to_remote_machine(self, localfilepath, remotefilepath):
        ftp_client = self.ssh_client.open_sftp()
        ftp_client.put(localfilepath, remotefilepath)
        ftp_client.close()

    def write_pass(self, command, password):
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        stdin.write(password)
        self.ssh_client.close()
        if stderr:
            return stderr.readlines()
        else:
            return stdout.readlines()

    def get_size_of_file(self, remotefilepath):
        ftp_client = self.ssh_client.open_sftp()
        size = ftp_client.stat(remotefilepath).st_size
        ftp_client.close()
        return size

    def remove_file(self, remotefilepath):
        ftp_client = self.ssh_client.open_sftp()
        ftp_client.remove(remotefilepath)
        ftp_client.close()

    def remove_dir(self, remotefilepath):
        ftp_client = self.ssh_client.open_sftp()
        ftp_client.rmdir(remotefilepath)
        ftp_client.close()

    def rename(self, oldpath, newpath):
        ftp_client = self.ssh_client.open_sftp()
        ftp_client.rename(oldpath, newpath)
        ftp_client.close()

    def mkdir(self, remotefilepath, mode=777):
        ftp_client = self.ssh_client.open_sftp()
        ftp_client.mkdir(remotefilepath, mode)
        ftp_client.close()

    def file(self, remotefilepath, mode='r'):
        ftp_client = self.ssh_client.open_sftp()
        ftp_client.file(remotefilepath, mode)
        ftp_client.close()



