import sys
import socket
import select
import datetime 

class user():
    name=None
    status=None
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
    body=None

    def __init__(self,data,src_username):
        # Grab timestamp
        self.timestamp=datetime.datetime.now().time().isoformat().split('.')[0]

        # Parse the data into our object
        # User is issuing a command to the server
        if data[0]=='#':
            print('server command sent')
            
        # User is sending a direct message    
        elif data[0]=='@':
            split_string=data[1:len(data)].split(' ',1);
            self.dest=split_string[0].lower();
            if len(split_string)<2:
                split_string.append('')
            self.body=split_string[1];
            
        # User is chatting with everyone (broadcast message)    
        else:
