import urllib.request
import time
import json
import datetime
import psycopg2
from flask import Flask,request,jsonify
app = Flask(__name__)


try:
  con = psycopg2.connect(user='quywvejawxhnse',password='065fe8ac62d76caa061d1e517b2f0107b5776f767037c2e29cad16c259a771cf',host='ec2-176-34-113-15.eu-west-1.compute.amazonaws.com',port='5432',database='d3opaj0jiqsm0h')
  cur = con.cursor()
except psycopg2.Error :
     pass
   #return (json.dumps({'Status': 'Failure','Message':'DB connection Error'}, sort_keys=True, indent=4))

def aws(business_id,customer_appointment_date,customer_email):
     
     sql = ("select business_avg_wait_time_min,business_appointment_type from business_primary where business_id="+str(business_id)+"")
     cur.execute(sql)
     wait_time = cur.fetchone()
     print(type(wait_time[0]),wait_time[0])
     print(type(wait_time[1]),wait_time[1])
     waittime = wait_time[0]
     appointment_type = wait_time[1]
     psql = ("select customer_token_num from customer_details where business_id = "+str(business_id)+" and customer_appointment_date='"+customer_appointment_date+"' and customer_email='"+customer_email+"'")
     cur.execute(psql)
     data1 = cur.fetchone()
     for token_num in data1:
        print(type(token_num),token_num)
        token_num = int(token_num)
        tokennumber = token_num
     subtoken = token_num - 1
     subtoken = str(subtoken)
    
     print(subtoken,type(subtoken))
 
     psql2 = ("select count(*) from (select * from customer_details order by case when substring(customer_token_num from '^\d+$') is null then 9999 else cast(customer_token_num as integer) end,customer_token_num) customer_details where business_id="+str(business_id)+" and customer_appointment_date='"+customer_appointment_date+"' and customer_current_status in('booked')and customer_token_num between '0' and '"+subtoken+"'")
     cur.execute(psql2)
     print(psql2)
     resultcount = cur.fetchone()
     print(resultcount[0])
     resultcount = int(resultcount[0])
     print(type(resultcount))
     if appointment_type in ['token']:
        final = resultcount * waittime
        result = str(final)
        print(result)
        return(result)

def sendsmsivr(request):
    
          mobile = request.json['mobile']
          date = request.json['date']
          
          sql = ("select * from customer_details where customer_appointment_date = '"+date+"' and customer_email = '"+mobile+"'")
          cur.execute(sql)
          print(sql)
          def myconverter(o):
                    if isinstance(o, datetime.date):
                         return o.__str__()  

          columns = cur.description
          final = [{columns[index][0]:column for index, column in enumerate(value)}   for value in cur.fetchall()]
          result = json.dumps(final,indent=3,default=myconverter)
          result = json.loads(result)
          print("res",result,type(result))
          
          business_id = request.json['business_id']
          cc = request.json['cc']#result[0]['business_id']
          query = "select business_first_name from business_primary where business_id = "+str(business_id)+""
          cur.execute(query)
          data = cur.fetchone()
          print(type(data),data)
          docid = ''.join(data)
          print(docid,type(docid))
          token = result[0]['customer_token_num']
          app_date = result[0]['customer_appointment_date']
          docid = docid[3:]
          print(docid)
          awt = aws(business_id,app_date,mobile)
          #d['Today_business_name'] = docid
          message = "Your Appointment is Confirmed with Dr. "+docid+", Token Number: "+token+" , Appointment Date: "+app_date+", Average Wait Time: "+awt+". "
          print(message)
          url = "https://control.msg91.com/api/sendhttp.php?authkey=195833ANU0xiap5a708d1f&mobiles="+mobile+"&message="+message+"&sender=InfoIt&route=4&country="+cc+""
          req = urllib.request.Request(url)
          with urllib.request.urlopen(req) as response:
             the_page = response.read()
             the_page = the_page[1:]
             print(the_page)
             the_page = str(the_page)
          return(json.dumps({"Message":"SMS Sent Sucessfully","Key":the_page},indent =2))
