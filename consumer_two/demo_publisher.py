from flask import Flask, request,redirect,render_template
import json
import pika

app=Flask(__name__)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='create_item')

@app.route("/create_item",methods=['POST','GET'])
def send_to_create_item():
    if request.method=='GET':
        return render_template('create_item.html')

    elif request.method=='POST':  
        itemName=request.form["itemName"]
        itemDescription=request.form["itemDescription"]
        itemPrice=request.form["itemPrice"]
        item={"itemName":itemName,"itemDescription":itemDescription,"itemPrice":itemPrice}
        item_json=json.dumps(item)
        print(item_json)
        
        channel.basic_publish(exchange='',
                      routing_key='create_item',
                      body=item_json) #publish the message to the queue
        return redirect('/create_item')

if __name__=="__main__":
    app.run(debug=True)


