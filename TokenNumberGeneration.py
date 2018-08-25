import json
import psycopg2
import datetime
from flask import Flask,request,jsonify
import sys
sys.stdout.flush()
app = Flask(__name__)
#app.route('/token',methods=['POST'])
def tokengeneration(request):

     business_id = request.json['business_id']
     customer_appointment_date = request.json['appointment_date']
     customer_email = request.json['customer_email']
     try:
      con = psycopg2.connect(user='quywvejawxhnse',password='065fe8ac62d76caa061d1e517b2f0107b5776f767037c2e29cad16c259a771cf',host='ec2-176-34-113-15.eu-west-1.compute.amazonaws.com',port='5432',database='d3opaj0jiqsm0h')
      cur = con.cursor()
     except psycopg2.Error :
       return (json.dumps({'Status': 'Failure','Message':'DB connection Error'}, sort_keys=True, indent=4)) 
     sql = ("select customer_token_num from customer_details where customer_appointment_date = '"+customer_appointment_date+"' and business_id ="+business_id+" and customer_email='"+customer_email+"'")
     print(sql)
     tokennum=0
     result =''   
     cur.execute(sql)
     result = cur.fetchall()
     print(result)
     for field in result:
        print(field)
        for tokennum in field:
          tokennum = int(tokennum)
          print(tokennum,type(tokennum))
     if tokennum > 0  :
          #tokennum = 0
          return json.dumps({'Message': 'AlreadyExists', 'Status': 'success','TokenNumber':tokennum}, sort_keys=True, indent=4)
     elif len(result)== 0:
          return json.dumps({'Message': 'DataNotExists', 'Status': 'failure','TokenNumber':tokennum}, sort_keys=True, indent=4)
     elif tokennum  == 0 or tokennum is None :
          sql = "select count(*)from token_generation where business_id="+business_id+" and appointment_date='"+customer_appointment_date+"'"
          print(sql)
          cur.execute(sql)
          i = cur.fetchone()
          for table_count in i :
            table_count = int(table_count)
            print(table_count)
          if table_count is 0 :
             sql = "insert into  token_generation VALUES ("+business_id+",'0','"+customer_appointment_date+"')"
             print(sql)
             cur.execute(sql)
             con.commit()
     sql= "select token_number from token_generation where appointment_date='"+customer_appointment_date+"' and business_id="+business_id+""
     cur.execute(sql)
     i = cur.fetchone()
     for no in i: 
         print(no,type(no))
         no = int(no)
     no+=1
     print(no,type(no))
     no = str(no)
     sql = ("update token_generation set token_number='"+no+"' where appointment_date='"+customer_appointment_date+"' and business_id="+business_id+"")
     print(sql)
     cur.execute(sql)
     con.commit()
     #no = str(no)
     psql = ("update customer_details set customer_token_num = '"+no+"'  where customer_appointment_date = '"+customer_appointment_date+"' and business_id = "+business_id+" and customer_email='"+customer_email+"'")
     print(psql)
     cur.execute(psql)
     con.commit()
     return json.dumps({'Message': 'Token Generated', 'Status': 'success','TokenNumber':no}, sort_keys=True, indent=4)
     con.close()
 
 
    


#if __name__ == "__main__":
        #app.run(debug=True)
   #app.run(host='192.168.1.3',port='5000')
