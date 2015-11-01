from flask import Flask, request, redirect
import twilio.twiml
 
app = Flask(__name__)
cur=[]
message=[]
@app.route("/", methods=['GET', 'POST'])
def getCall():
    
    resp = twilio.twiml.Response()
    if(len(cur)<10):
        
        if str(request.values.get('From', None)) in cur:
            resp.message("You are in the Queue already!")
        else:
            resp.message("You have entered the Queue You are Number "+str(len(cur)+1)+" Please wait for your turn!")
            cur.append(request.values.get('From', None))
    else:
        resp.message("Error there is too many in the queue")
   
    
    return str(resp)
    
if __name__ == "__main__":
    app.run(debug=True)