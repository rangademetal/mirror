import ftplib
from Model.Secret import FTP_HOSTNAME, FTP_USERNAME, FTP_PASSWORD


class ftp_ionos:
    def __init__(self, hostname, username, password):
        self.FTP_SERVER = ftplib.FTP(hostname, username, password)

    def show_folder(self):
        return self.FTP_SERVER.dir()
    
    def cwd_folder(self, path):
        self.FTP_SERVER.cwd(path)
    
    def download_ftp(self, filename):
        with open(filename, "wb") as file:
            self.FTP_SERVER.retrbinary(f"RETR {filename}", file.write)



# ftp = ftp_ionos(FTP_HOSTNAME, FTP_USERNAME, FTP_PASSWORD)
# ftp.cwd_folder('/download/software/')
# ftp.download_ftp('setup_fraps.exe')
