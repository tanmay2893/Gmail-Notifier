'''import sys
import imaplib
import getpass
import email
import datetime
def process_mailbox(M):
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print "No messages found!"
        return
    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print "ERROR getting message", num
            return
    msg = email.message_from_string(data[0][1])
    print 'Message %s: %s' % (num, msg['Subject'])
    print 'Raw Date:', msg['Date']
    date_tuple = email.utils.parsedate_tz(msg['Date'])
    if date_tuple:
        local_date = datetime.datetime.fromtimestamp(
            email.utils.mktime_tz(date_tuple))
        print "Local Date:", \
            local_date.strftime("%a, %d %b %Y %H:%M:%S")
M = imaplib.IMAP4_SSL('imap.gmail.com')
try:
    M.login('tanmay2893@gmail.com','')
except imaplib.IMAP4.error:
    print "LOGIN FAILED!!! "
rv, data = M.select("INBOX")
if rv == 'OK':
    print "Processing mailbox...\n"
    process_mailbox(M) # ... do something with emails, see below ...
    M.close()
M.logout()

'''
import unirest,getpass,time
import imaplib,email,math,datetime
import ConfigParser
import os,re
from pprint import pprint
list_response_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')
def open_connection(verbose=False):
    # Read the config file
    config = ConfigParser.ConfigParser()
    config.read([os.path.expanduser('~/.pymotw')])
    # Connect to the server
    #hostname = config.get('server', 'hostname')
    hostname='imap.gmail.com'
    if verbose: print 'Connecting to', hostname
    connection = imaplib.IMAP4_SSL(hostname)

    # Login to our account
    username = '******@gmail.com'
    password = ''
    if verbose: print 'Logging in as', username
    connection.login(username, password)
    return connection

def parse_list_response(line):
    flags, delimiter, mailbox_name = list_response_pattern.match(line).groups()
    mailbox_name = mailbox_name.strip('"')
    return (flags, delimiter, mailbox_name)
def msg_from_user(email):
    c.select('INBOX', readonly=True)
    (t,msg)=c.search(None,'(UNSEEN)')
    if t=='OK':
        k=int(msg[0].split(' ')[-1])
        for i in range(k, k-11,-1):
            typ, msg_data = c.fetch(str(i), '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    for header in [ 'subject', 'to', 'from' ]:
                        print '%-8s: %s' % (header.upper(), msg[header])
if __name__ == '__main__':
    while True:
        try:
            c = open_connection()
            break
        except:
            print 'Network Issues'
            print 'Retrying ......'
            continue
    DATA=0
    ht=[]
    name=''
    date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
    r=0
    while True:
        r+=1
        if r!=1:
            print('Will Search Again after 1 minute')
            time.sleep(60)
        try:
            print 'Searching ....'
            friends='*********@gmail.com'
            friends=friends.split(' ')
            x=''
            for i in friends:
                x+='(FROM "'+i+'")'
            c.select('INBOX',readonly=True)
            (t,msg)=c.search(None, '(UNSEEN)','(SENTSINCE {0})'.format(date))
            print msg
            msg = [int(i) for i in msg[0].split()]
            msg_copy=list(reversed(msg))
            #z=msg_copy[:5]
            z=msg_copy[:2]
            y=msg_copy[0]
            x=len(msg)
            if y<=DATA:
                DATA=y
                continue
            else:
                if ht!=[]:
                    m=list(set(z)-set(ht))
                    print m
                    print '*****'
                else:
                    m=z
                DATA=msg_copy[0]
            if x<2:
                k=x
            else:
                k=2
            t=[]
            g=0
            print m
            ht+=m\
            for i in m:
                if g==2:
                    break
                g+=1
                s=''
                s+=str(g)+' --        '
                typ, msg_data = c.fetch(str(i), '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_string(response_part[1])
                        for header in [ 'subject', 'from' ]:
                            s+=str(header.upper())+' : '+str(msg[header])+'      '
                            print '%-8s: %s' % (header.upper(), msg[header])
                print '************'
                t+=[s]
            for i in t:
                while True:
                    try:
                        response = unirest.get("https://site2sms.p.mashape.com/index.php?msg="+i+"&phone="+phone+"&pwd="+pwd+"&uid=************",headers={"X-Mashape-Key": "**************************************"})
                        print response
                        break
                    except:
                        print 'Error in Sending Message'
                        continue
            
        finally:
            print ''

