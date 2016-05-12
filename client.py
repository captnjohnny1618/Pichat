import sys
import socket
import select

class client():

    #SERVER_IP='192.168.2.4'
    SERVER_IP='127.0.0.1'
    PORT=8000
    BUFF_SIZE=4096
    
    def __init__(self):
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
        try:
            sock.connect((self.SERVER_IP,self.PORT))
        except:
            print("Could not connect")
            sys.exit()

        print("Connected to server %s on port %i" % (self.SERVER_IP, self.PORT));
        
        while True:
            socket_list=[sys.stdin, sock]

            (readable,writable,[])=select.select(socket_list,[],[],0)

            for s in readable:
                if s==sock:
                    ## Socket should receive data
                    data=sock.recv(self.BUFF_SIZE)
                    if data=='':
                        print('Disconnected from server')
                        sys.exit()
                    else:
                        sys.stdout.write('\b\b\b\b\b');
                        sys.stdout.write(data)
                        sys.stdout.write('[ME] ')
                        sys.stdout.flush()                                         
                else:
                    ## User is writing data 
                    msg=sys.stdin.readline()
                    sock.send(msg)
                    sys.stdout.write('[Me] ')
                    sys.stdout.flush()

if __name__=='__main__':
    client()
                    
