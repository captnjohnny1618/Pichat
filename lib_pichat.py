import sys
import socket
import select
import datetime 
from collections import defaultdict

class user():
    name=None
    status='online'
    status_message=None
    socket=None
    ip=None
    
    def __init__(self,name,client_socket,ip):
        self.name=name.rstrip()
        self.socket=client_socket
        self.ip=ip
        self.status='online'
        self.status_message=""

    def __str__(self):
        info=  '"' +  self.name + '"' + ' located at ' + self.ip[0] + ' on port ' + str(self.ip[1])
        return info


class message():
    dest=None
    src=None
    timestamp=None
    signal=None
    body=''

    def __init__(self,data,src_username):
        # Grab timestamp and set user
        self.timestamp=datetime.datetime.now().time().isoformat().split('.')[0]
        self.src=src_username
        
        # Parse the data into our object
        # User is issuing a command to the server
        if data[0]=='#':
            cmd_dict={
                'message': 0,
                'direct_message': 1,
                'exit': 100,
                'logout': 101,
                'ip': 1000,
                'away': 9000,
                'whos': 9001,
                'help': 9002,
            }

            cmd_dict=defaultdict(lambda: -1,cmd_dict)

            print('server command sent')
            self.signal=0

            # parse a command
            command=data[1:len(data)].rstrip();
            signal=cmd_dict[command]
            self.signal=signal
            print(self.signal)
            
        # User is sending a direct message    
        elif data[0]=='@':
            split_string=data[1:len(data)].split(' ',1);
            self.dest=split_string[0].lower()
            if len(split_string)<2:
                split_string.append('')
            self.body=split_string[1]
            
        # User is chatting with everyone (broadcast message)    
        else:
            self.dest='broadcast'
            self.body=data;

    def __str__(self):
        if self.dest=='broadcast':
            header="[ " + self.src + ' ' + self.timestamp + " ] "
        else:
            header="[ " + self.src + '->' + self.dest + ' ' + self.timestamp + " ] "

        body=self.body
        return header+body
