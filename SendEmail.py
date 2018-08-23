import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask,request,jsonify
app = Flask(__name__)
#@app.route('/sendemail',methods=['POST'])
def sendemail(request):
 sender = request.json['sender']
 receiver = request.json['receiver']
 message_no = request.json
 #data = request.json['message']
 print(message_no)
 val1 = message_no['name']
 val2 = message_no['message']
 val3 = message_no['token_num']
 val4 = message_no['wait_time']
 val5 = message_no['bus_hour']
 val6 = message_no['break_time']
 val7 = message_no['address']
 val8 = message_no['hospital']

 subject = request.json['subject']
 msg = MIMEMultipart()
 msg['from'] = sender
 msg['to'] = receiver
 msg['subject'] = subject
 # Create the body of the message (a plain-text and an HTML version)
 html = """\
 <html>
  <head></head>
  <body>
    <dl>
    <dt>
    <p><font size="2" color="black">"""+val1+"""</font></p>
    <p><font size="4" color="blue">"""+val2+"""</font></p>
    <dd>
    <p><font size="2" color="black">"""+val3+"""</font></p>
    <p><font size="2" color="black">"""+val4+"""</font></p>
    <p><font size="2" color="black">"""+val5+"""</font></p>
    <p><font size="2" color="black">"""+val6+"""</font></p>
    <p><i><font size="2" color="blue">"""+val7+"""</font></i></p>
    <p><font size="4" color="blue">"""+val8+"""</font></p>
    </dd>
    </dl>

  </body>
 </html>
 """
 
 #msg.attach(MIMEText(msg['subject'],'plain'))
 msg.attach(MIMEText(html,'html'))
 
 gmailuser = 'infocuit.testing@gmail.com'
 password = 'infocuit@123'
 server = smtplib.SMTP('smtp.gmail.com',587)
 server.starttls()
 server.login(gmailuser,password)
 text = msg.as_string()
 server.sendmail(sender,receiver,text)
 print ("the message has been sent successfully")
 server.quit()
 return(json.dumps({'Message': 'Message Send Successfully','Returncode':'MSS'}, sort_keys=True, indent=4))
#if __name__ == "__main__":
 #   app.run(debug=True)
 # app.run(host="192.168.1.5",port="5000")
