import json
import psycopg2
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask,request,jsonify
app = Flask(__name__)
#@app.route('/sendemailall',methods=['POST'])
def callfn(sql):
 try:
      con = psycopg2.connect(user='quywvejawxhnse',password='065fe8ac62d76caa061d1e517b2f0107b5776f767037c2e29cad16c259a771cf',host='ec2-176-34-113-15.eu-west-1.compute.amazonaws.com',port='5432',database='d3opaj0jiqsm0h')
      cur = con.cursor()
 except psycopg2.Error :
      return (json.dumps({'Status': 'Failure','Message':'DB connection Error'}, sort_keys=True, indent=4))
 sender = request.json['sender']   
 mail = []   
 cur.execute(sql)
 result = cur.fetchall()
 for field in result:
     for test in field:
         if test  not in mail:
            mail.append(test)
 #print(mail)
 
 len_mail = len(mail)    
 #receiver = request.json['receiver']
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
 x=0
 #for receiver in email:
 while len_mail != x:
 #for  email in mail[x]:
     #print(mail[x])
     msg['to'] = mail[x]
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
     server.sendmail(sender,mail[x],text)
     x+=1
     server.quit()
 print ("the message has been sent successfully") 

 return(json.dumps({'Message': 'Message Send Successfully','Returncode':'MSS'}, sort_keys=True, indent=4))
def sendemailall(request):

 customer_appointment_date_from = request.json['appointment_date_from'] 
 customer_appointment_date_to = request.json['appointment_date_to']     
 business_id = request.json['business_id']
 if len(customer_appointment_date_from) is 0:
      Today_date = datetime.datetime.utcnow().date().strftime('%Y-%m-%d')
      customer_appointment_date_from = Today_date 
      customer_appointment_date_to = Today_date
 if request.json.get('status'):
     status = request.json['status']
     sql = ("select customer_email from customer_details where business_id = "+business_id+" and customer_appointment_date between '"+customer_appointment_date_from+"' and '"+customer_appointment_date_to+"' and customer_current_status in ('"+status+"')")
     print(sql)
     return(callfn(sql))
 else:
     sql = ("select customer_email from customer_details where business_id = "+business_id+" and customer_appointment_date between '"+customer_appointment_date_from+"' and '"+customer_appointment_date_to+"'")
     print(sql)
     return(callfn(sql))
