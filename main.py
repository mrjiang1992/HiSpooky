from flask import Flask, request, redirect
from twilio.rest import TwilioRestClient
import twilio.twiml
 
app = Flask(__name__)
"""People in the Queue"""
cur=[] 
"""Count of going over people!"""
a=0
"""This it the output message"""
message=""
account_sid = "AC36c5c6423b5cc522e118a8915a0ba81b"
auth_token = "8c2c310fb78dbe50c1afe54211a48f3f"
client = TwilioRestClient(account_sid, auth_token)
storyTime= False;"""False means that people are being added"""
@app.route("/", methods=['GET', 'POST'])
def getCall():
    global a
    global message
    global account_sid
    global auth_token
    global client
    global storyTime
    global cur
    resp = twilio.twiml.Response()
    """ for blank case"""
    if (request.values.get('Body',None)):
        """The starting procedure"""
        if (request.values.get('Body',None).lower() == "start" ):
            """if there is room then keep adding to Queue"""
            if(len(cur)==4 and str(request.values.get('From', None)) not in cur):
                """This is where we start the story because we add the 10th person"""
                cur.append(request.values.get('From', None))
                storyTime=True;
                client.messages.create(to=cur[0], from_="+1585-270-7626",body="You will begin the Spooky Story please keep it within 140 characters! ") 
                resp.message("You have entered the Queue You are Number "+str(len(cur) )+" Please wait for your turn!")
                
            elif(len(cur)<5):
        
                if str(request.values.get('From', None)) in cur:
                    resp.message("You are in the Queue already!")
            
                else:
                    cur.append(request.values.get('From', None))
                    resp.message("You have entered the Queue You are Number "+str(len(cur))+" Please wait for your turn!")
            else:
                    resp.message("Please try again later when another story is happenning ")
                    
        else:
            
            """You are in queue and have a message other then Start"""
            if str(request.values.get('From', None)) in cur:
                """finds the index"""
                c=0
                while c<len(cur):
                    if cur[c]== request.values.get('From', None):
                        break;
                    c+=1
                    
                if (c==a):
                    """Add message to the array increment a"""
                    message+=request.values.get('Body',None)+" "
                    a+=1
                    resp.message("Your message is added to the story please wait for it to finish!")
                    """Message the next person that it is their turn """
                    if(c==4):
                       
                        x=0
                        while x<len(cur):
                            client.messages.create(to=cur[x], from_="+1585-270-7626",body="Here is the Spooky Story!") 
                            client.messages.create(to=cur[x], from_="+1585-270-7626",body=message)
                            client.messages.create(to=cur[x], from_="+1585-270-7626",body="Thanks for playing!")  
                            x+=1
                        message =""
                        storyTime=not storyTime
                        a=0
                        cur=[]  
                         
                    else:
                        client.messages.create(to=cur[a], from_="+1585-270-7626",body="Continue the story and please limit it to 140 characters. Here is the story so far:") 
                        client.messages.create(to=cur[a], from_="+1585-270-7626",body=message) 

                elif(c<a):
                    """Have already gone and are in queue"""
                    resp.message("Please wait till everyone has gone.")
                else:
                    """Still have to go in queue"""
                    resp.message("Please wait untill it is your turn for the story.")
                    
            else:
                """ERROR: not in queue"""
                
                resp.message("ERROR: To join queue say start")
                    
    
    return str(resp)
    
if __name__ == "__main__":
    app.run(debug=True)