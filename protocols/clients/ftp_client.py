'''

This is the ftp client code

'''


class Client:

    def __init__(self, cli_object):
        self.protocol = "ftp"
        self.remote_server = cli_object.ip
        self.username = cli_object.username
        self.password = cli_object.password

    def transmit(self, data_to_transmit):

        try:
            ftp = FTP(self.remote_server)
        except socket.gaierror:
            print "[*] Error: Cannot connect to FTP server.  Checking provided ip!"
            sys.exit()

        try:
            ftp.login(self.username, self.password)
        except error_perm:
            print "[*] Error: Username or password is incorrect!  Please re-run."
            sys.exit()
            # Create file name and write out file for ftp transfer
            current_date = time.strftime("%m/%d/%Y")
            current_time = time.strftime("%H:%M:%S")
            ftp_file_name = current_date.replace("/", "") +\
                "_" + current_time.replace(":", "") + "ftp_data.txt"

        with open(helpers.ea_path() + "/data/" + ftp_file_name, 'w') as cc_temp_file:
            cc_temp_file.write(data_to_transmit)

        ftp.storlines("STOR " + ftp_file_name, open(helpers.ea_path() + "/data/" + ftp_file_name))
        ftp.quit()
        os.remove(ftp_file_name)
        print "[*] File sent!!!"
