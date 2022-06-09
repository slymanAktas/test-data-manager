import pysftp as sftp


class SFTP:
    # https://pypi.org/project/pysftp/
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.ssh_client = sftp.Connection(host=self.host, username=self.username, password=self.password)

    def close_connection(self):
        self.ssh_client.close()

    def upload_file_to_remote(self, localfilepath, remotefileth):
        try:
            self.ssh_client.put(localfilepath, remotefileth)
            self.close_connection()
        except Exception as e:
            print(e)

    def upload_dir_to_remote(self, localfilepath, remotefileth):
        try:
            self.ssh_client.put_d(localfilepath, remotefileth)
            self.close_connection()
        except Exception as e:
            print(e)

    def upload_dir_to_remote_recursively(self, localfilepath, remotefileth):
        try:
            self.ssh_client.put_r(localfilepath, remotefileth)
            self.close_connection()
        except Exception as e:
            print(e)

    def download_file_from_remote(self, remotefilepath, localfilepath):
        try:
            self.ssh_client.get(remotefilepath, localfilepath)
            self.close_connection()
        except Exception as e:
            print(e)

    def download_dir_from_remote(self, remotefilepath, localfilepath):
        try:
            self.ssh_client.get_d(remotefilepath, localfilepath)
            self.close_connection()
        except Exception as e:
            print(e)

    def download_dir_from_remote_recursively(self, remotefilepath, localfilepath):
        try:
            self.ssh_client.get_r(remotefilepath, localfilepath)
            self.close_connection()
        except Exception as e:
            print(e)

    def listdir(self, remotepath):
        list_of_directory = self.ssh_client.listdir(remotepath=remotepath)
        print(list_of_directory)
        self.close_connection()
        return list_of_directory

    def makedir(self, remotepath):
        self.ssh_client.mkdir(remotepath, mode=777)
        self.close_connection()

    def makedirs(self, remotepath):
        self.ssh_client.makedirs(remotepath, mode=777)
        self.close_connection()

    def remove_file(self, remotepath):
        self.ssh_client.remove(remotepath)
        self.close_connection()

    def remove_dir(self, remotepath):
        self.ssh_client.rmdir(remotepath)
        self.close_connection()

    def truncate(self, remotepath, remaining_bytes):
        '''

        :param remotepath: file path
        :param remaining_bytes: Örn 5 ise ilk 5 karakter'den sonrasini siler
        :return:
        '''
        self.ssh_client.truncate(remotepath, remaining_bytes)
        self.close_connection()


a = SFTP('172.20.0.196', 'selenium', '123qwe.asd')

a.upload_dir_to_remote('/Users/user/Desktop/delete_later', '/Users/selenium/Desktop/slyman/aktas')
