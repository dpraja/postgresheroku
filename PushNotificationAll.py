from pushjack import GCMClient
from flask import Flask,request
import json
app = Flask(__name__)

#@app.route('/pushnotificationall',methods=['POST'])
def pushnotificationall(request):
    Title = request.json['title']
    Body = request.json['body']

    client = GCMClient(api_key='AIzaSyAQDQSMLhW0ihrRWaDASWPUi-U078lUn4c')

    registration_id = '/topics/my_little_topic'
    alert = 'Hello world.'
    notification = {'title': Title, 'body': Body, 'icon': 'icon'}

    # Send to single device.
    # NOTE: Keyword arguments are optional.
    res = client.send(registration_id,
                      alert,
                      notification=notification,
                      collapse_key='collapse_key',
                      delay_while_idle=True,
                      time_to_live=604800)

    # Send to multiple devices by passing a list of ids.
    client.send([registration_id], alert)

    return(json.dumps({'Status': 'Success', 'StatusCode': '200','Message': 'Push Notification sent'}, sort_keys=True, indent=4))

#if __name__ == '__main__':
   #app.run()
 #  app.run(host="192.168.1.5",port=5000)

   
