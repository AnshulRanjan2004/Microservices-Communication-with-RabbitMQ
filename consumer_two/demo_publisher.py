from flask import Flask, request,redirect,render_template
import json

app=Flask(__name__)

@app.route("/create_item",methods=['POST','GET'])
def send_to_create_item():
    if request.method=='GET':
        render_template('create_item.html')

    else:  
        data=request.data
        print(json.loads(data))
        return redirect('/create_item')

if __name__=="__main__":
    app.run(debug=True)


