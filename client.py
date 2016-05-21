import sys
import socket
import select
import cPickle as pickle
import lib_pichat as lp

class client():

    #SERVER_IP='192.168.2.5'
    SERVER_IP='127.0.0.1'
    PORT=8000
    BUFF_SIZE=4096
    USER=None
    
    def __init__(self):

        ### Connect to server and set up user
        print('----------------------')
        print('Pichat Client Started!')
        print('----------------------')
        print('')

        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
        try:
            sock.connect((self.SERVER_IP,self.PORT))
        except:
            self.PORT+=1;
            sock.connect((self.SERVER_IP,self.PORT))
            #print("Could not connect")
            #sys.exit()

        print("Connected to server %s on port %i" % (self.SERVER_IP, self.PORT));            
        
        username=raw_input('Please enter a username: ')
        print("Exchanging info with the Pichat server...")
        self.USER=lp.user(username,[],[]);
        sock.send(pickle.dumps(self.USER));

        print("Welcome %s!" % self.USER.name)
        sys.stdout.write('[ME] ')
        sys.stdout.flush()
        
        ### Main loop to handle sending and receiving data
        while True:
            socket_list=[sys.stdin, sock]

            (readable,writable,[])=select.select(socket_list,[],[],0)

            for s in readable:
                if s==sock:
                    ## Receiving data from server
                    data=sock.recv(self.BUFF_SIZE)
                    m=pickle.loads(data); # load into message object

                    if data=='':
                        print('Disconnected from server')
                        sys.exit()
                    else:
                        sys.stdout.write('\b\b\b\b\b');
                        sys.stdout.write(str(m))
                        sys.stdout.write('[ME] ')
                        sys.stdout.flush()                                         
                else:
                    ## User is writing data 
                    msg=sys.stdin.readline()
                    msg=lp.message(msg,self.USER.name)
                    sock.send(pickle.dumps(msg));
                    sys.stdout.write('[ME] ')
                    sys.stdout.flush()

if __name__=='__main__':
    client()
                    
