from flask import Flask, request, redirect
import twilio.twiml
 
app = Flask(__name__)
a=[]
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""
    resp = twilio.twiml.Response()
    if(len(a)<10):
       
        resp.message("You have entered the Queue You are the"+str(len(a)))
        a.append("s")
    else:
        resp.message("Error there is too many in the queue")
   
    
    return str(resp)
    
if __name__ == "__main__":
    app.run(debug=True)