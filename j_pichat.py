import datetime as dt

class pi_user():
    name=""
    status="online"
    msg_history=[]

class pi_message():

    sender=""
    destination=""
    timestamp=""
    body=""

    def __init__(self,user,message):
        self.sender=user.name
        self.body=message
        self.timestamp=dt.datetime.now()
        self.destination="broadcast";
    
class pi_client():
    user
    status
    server_ip

class pi_server():
    connected_users=[]
