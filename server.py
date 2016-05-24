import sys
import socket
import select
import cPickle as pickle
from collections import defaultdict

import lib_pichat as lp

class server():

    PORT=8000
    MAX_CLIENTS=2
    SOCKETS=[]
    BUFF_SIZE=4096
    #IP='127.0.0.1'
    IP='aurora.rip.ucla.edu'
    users=[]
    
    def __init__(self):

        server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            server_socket.bind((self.IP,self.PORT))
        except:
            self.PORT+=1;
            server_socket.bind((self.IP,self.PORT))

        server_socket.listen(self.MAX_CLIENTS)

        self.SOCKETS.append(server_socket)
        self.users.append(lp.user("Server",server_socket,(self.IP,self.PORT)))
        
        print('----------------------')
        print('Pichat Server Started!')
        print('----------------------')

        while True:
            (readable,writable,[])=select.select(self.SOCKETS,[],[],0)

            for sock in readable:
                if sock==server_socket:
                    # Server has received a new connection
                    # Handle connection and let connected users know
                    (client_socket,ip)=server_socket.accept();
                    self.SOCKETS.append(client_socket);
                    print("New client connected");                    
                    u=client_socket.recv(self.BUFF_SIZE)
                    try:
                        u=pickle.loads(u)
                        u.socket=client_socket
                        u.ip=ip;
                        self.users.append(u)
                        print(u)
                    except:
                        print('User tried to connect with incorrect protocol.  Dropping.')
                        client_socket.send('You must connect with the pichat client\n');
                        client_socket.close()
                        self.SOCKETS.remove(client_socket)
                    
                else:
                    # Server has received data
                    # Prepare message object then send
                    data=sock.recv(self.BUFF_SIZE);
                    
                    if data=='':
                        m=lp.message('User "' + self.socket2name(sock) + '" disconnected\n','Server');
                        print(str(m).rstrip())
                        self.send_message(server_socket,sock,m);
                        self.remove_client(sock);
                        
                    else:
                        try:
                            m=pickle.loads(data);
                        except:
                            print('Received non-pichat data, ignoring')

                        if m.signal:
                            m.dest=m.src;
                            if (m.signal==9000 or m.signal==8000):
                                m.dest='broadcast'
                            m.src='Server'
                            print("Signal received : " + str(m.signal))
                            m.body=self.handle_signal(sock,m);

                        print(str(m).rstrip())
                        self.send_message(server_socket,sock,m);

    def send_message(self,server_sock,sock,m):
        if m.dest=='broadcast':
            for s in self.SOCKETS:
                if (s != server_sock) & (s != sock):
                    try:
                        s.send(pickle.dumps(m));
                    except:
                        if s in self.SOCKETS:
                            self.remove_client(s);                            
        else:
            s=self.name2socket(m.dest)
            try:
                s.send(pickle.dumps(m));
            except:
                if s in self.SOCKETS:
                    self.remove_client(s);
            
    def socket2name(self,socket):
        idx=self.SOCKETS.index(socket)
        return self.users[idx].name

    def name2socket(self,username):
        socket=None
        for i in range(0,len(self.users)):
            if self.users[i].name==username:
                u=self.users[i]
                socket=u.socket
                #socket=self.users[i].socket;
                break
        return socket

    def remove_client(self,sock):
        print('Could not reach client. Removing them from client list.');
        idx=self.SOCKETS.index(sock);
        self.SOCKETS.remove(sock);
        self.users.remove(self.users[idx])

    def handle_signal(self,socket,m):

#                      'message': 0,
#                      'direct_message': 1,
#                      'exit': 100,
#                      'logout': 101,
#                      'ip': 1000,
#                      'away': 9000,
#                      'whos': 9001,
#                      'help': 9002,

        u=self.users[self.SOCKETS.index(socket)];

        signal=m.signal
        body=''
        if signal==1: # disconnect the user but don't exit program
            print('Send user direct message')            
        elif signal==2: # dunno what I was thinking here
            print('Nothing yet')
        elif signal==100: # exit code
            print('Client is exiting');
        elif signal==101: # exit code
            print('Tell client to logout, but not exit')
        elif signal==1000: # ip
            print(u.name + ' requested their IP. Sending...')
            body='Connected to server at ip: ' + u.ip[0] + ' on port ' + str(u.ip[1]) + '.\n'
        elif signal==8000: # back
            self.users[self.SOCKETS.index(socket)].status="online"
            body=body + u.name + ' is now online.\n'
        elif signal==9000: # away
            print('set the user status to away and set away message')
            self.users[self.SOCKETS.index(socket)].status="away"
            body=body + u.name + ' is now away.\n'
        elif signal==9001: # whos
            print(u.name + ' wants to know who is connected.  Sending...');
            body="\n\n"
            for i in range(0,len(self.users)):
                if (self.users[i].name!='Server' and self.users[i].name!=u.name):
                    body=body + self.users[i].name + ' is connected and ' + str(self.users[i].status) + '.\n'
            body=body+"\n"
        elif signal==9002: # help
            print('Tell the user what the heck is going on!')
        else:
            print('Something went wrong')

        return body
    
if __name__=='__main__':
    server()
