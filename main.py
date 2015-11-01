from flask import Flask, request, redirect
from twilio.rest import TwilioRestClient
import twilio.twiml
 
app = Flask(__name__)
cur=[]
a=0
message=""
@app.route("/", methods=['GET', 'POST'])
def getCall():
    global a
    global message
    resp = twilio.twiml.Response()
    
    if (request.values.get('Body',None)):
        
        if (request.values.get('Body',None) == "Start" or request.values.get('Body',None) == "start"):
            
            if(len(cur)<10):
        
                if str(request.values.get('From', None)) in cur:
                    resp.message("You are in the Queue already!")
            
                else:
                    resp.message("You have entered the Queue You are Number "+str(len(cur)+1)+" Please wait for your turn!")
                    cur.append(request.values.get('From', None))
            
            else:
                resp.message("There is too many in the queue")
        else:
            """You are in queue and have a message other then Start"""
            if str(request.values.get('From', None)) in cur:
                c=0
                while c<len(cur):
                    if cur[c]== request.values.get('From', None):
                        break;
                    c+=1
                if (c==a):
                    """Add message to the array increment a"""
                    message+=request.values.get('Body',None)
                    a+=1
                    resp.message("Your message is added to the story please wait for it to finish!")
                    """Message the next person that it is their turn """
                    account_sid = "AC36c5c6423b5cc522e118a8915a0ba81b"
                    auth_token = "8c2c310fb78dbe50c1afe54211a48f3f"
                    client = TwilioRestClient(account_sid, auth_token)
                    client.messages.create(to=cur[a], from_="+1585-270-7626",body="Please continue the story and limit it to 140 characters. Here is the story so far:") 
                    client.messages.create(to=cur[a], from_="+1585-270-7626",body=message) 

                elif(c<a):
                    """Have already gone and are in queue"""
                    resp.message("Please wait till everyone has gone.")
                else:
                    """Still have to go in queue"""
                    resp.message("Please wait untill it is your turn for the story.")
                    
            else:
                """ERROR: not in queue and """
                
                resp.message("ERROR: To Join Queue say start")
                    
    
    return str(resp)
    
if __name__ == "__main__":
    app.run(debug=True)