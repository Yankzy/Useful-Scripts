''' Python script to monitor changes in files on your computer and send email to you using crontab.'''
import hashlib
import glob
import json
import smtplib
from email.message import EmailMessage

hasher = hashlib.md5()
size = 65536 #to read large files in chunks 
list_of_files = glob.glob('./*.csv') #absolute path for crontab

def send_email():

    '''
    Toggle to True if running the script for the first time.
    It will create a json file with hashes of your files.
    '''
    first_time = False 

    if first_time:

        first_hashes = {}
        for x in list_of_files:

            with open(x, 'rb') as f:
                buf = f.read(size)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = f.read(size)
                    first_hashes[x] = hasher.hexdigest()

        with open('hash.json', 'w') as file:
             file.write(json.dumps(first_hashes, indent=2))
    else:
        check_hash = {} 
        with open('hash.json') as f: #absolute path for crontab
             data = json.load(f)

        for x in list_of_files:

            with open(x, 'rb') as f:
                buf = f.read(size)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = f.read(size)
                    new_hash = hasher.hexdigest()
                    #if a hash match with one in data, that file has not changed
                    if new_hash in data.values():
                        check_hash[x] = new_hash
                    data[x] = new_hash


        #update our hashes
        with open('hash.json', 'w') as file:  #absolute path for crontab
             file.write(json.dumps(data, indent=2))

        if len(check_hash) > 0: 

            filename="check_hash.txt" #absolute path for crontab

            
            with open(filename, 'w') as f: #absolute path for crontab
                f.write(json.dumps(check_hash, indent=2))

            
            EMAIL_ADDRESS = 'SMTPAddress@gmail.com' 
            EMAIL_PASSWORD = 'SMTPPassWord'

            msg = EmailMessage()

            msg['Subject'] = 'Unupdated files'
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = 'receive@gmail.com'
            msg.set_content('These file(s) did not update:')
            msg.add_attachment(open(filename, "r").read(), filename=filename)



            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
     
if __name__ == "__main__":
    send_email()