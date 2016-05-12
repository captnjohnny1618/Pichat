import sys
import socket
import select
from collections import defaultdict

def parse_data(data):
    # look at users typed message and determine if signal
    # commands always start with a "#"
    
    cmd_dict={'message': 0,
              'logout': 1,
              'user': 2,
              'exit': 99,
              'ip': 1000,
              'away': 9000,
              'whos': 9001,
              'help': 9002,
    }

    cmd_dict=defaultdict(lambda: -1,cmd_dict)
    
    if data[0]=='#':
        # parse a command
        command=data[1:len(data)].rstrip();
        signal=cmd_dict[command]
        #print('Signal received' + signal);

    else:
        # transfer the data as a message
        signal=0;

    return signal    
    
class server():

    PORT=8000
    MAX_CLIENTS=2
    SOCKETS=[]
    BUFF_SIZE=4096
    IP='127.0.0.1'
    #IP='192.168.2.4'
    users=[]
    
    def __init__(self):
        server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_socket.bind((self.IP,self.PORT))
        server_socket.listen(self.MAX_CLIENTS)

        self.SOCKETS.append(server_socket)
        self.users.append(user("Server",server_socket,(self.IP,self.PORT)))
        
        print('Socket opened')

        while True:
            (readable,writable,[])=select.select(self.SOCKETS,[],[],0)

            for sock in readable:
                if sock==server_socket:
                    (client_socket,ip)=server_socket.accept();
                    self.SOCKETS.append(client_socket);
                    print("New client connected");
                    client_socket.send("Enter a username: ")
                    name=client_socket.recv(32)
                    u=user(name,client_socket,ip)
                    self.users.append(u)
                    print(u)
                    
                else:
                    data=sock.recv(self.BUFF_SIZE);
                    username=self.get_user_from_socket(sock);
                    print('Received: "' + data.rstrip() + '" from ' + username);
                    if data=='':
                        self.SOCKETS.remove(sock);
                        self.broadcast(server_socket,sock,'A user disconnected\n');
                    else:
                        signal=parse_data(data)
                        if signal:
                            print("Signal received: " + str(signal))
                            self.handle_signal(sock,signal);
                        else:
                            self.broadcast(server_socket,sock,data);

    def broadcast(self,server_socket,sock,data):
        username=self.get_user_from_socket(sock);
        for s in self.SOCKETS:
            if (s != server_socket) & (s != sock):
                try:
                    s.send("[" + username + "]: " + data);
                except:
                    if s in self.SOCKETS:
                        self.SOCKETS.remove(s);

    def get_user_from_socket(self,socket):
        idx=self.SOCKETS.index(socket)
        return self.users[idx].name

    def handle_signal(self,socket,signal):
#        'logout': 1,
#        'user': 2,
#        'exit': 99,
#        'ip': 1000,
#        'away': 9000,
#        'whos': 9001,
#        'help': 9002, 
        if signal==1: # disconnect the user but don't exit program
            print('user disconnected')
        elif signal==2: # dunno what I was thinking here
            print('signal user?')
        elif signal==99: # exit code
            print('tell client to exit the program')
        elif signal==1000: # ip
            print('report the user and server ip+port back to the user')
        elif signal==9000: # away
            print('set the user status to away and set away message')
        elif signal==9001: # whos
            print('report to the user everyone who is connect and their status');
        elif signal==9002: # 
            print('Tell the user what the heck is going on!')
        else:
            print('Something went wrong')

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
    
if __name__=='__main__':
    server()
