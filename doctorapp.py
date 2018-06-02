import json
import datetime
import psycopg2
from flask import Flask,request,jsonify
app = Flask(__name__)
#@app.route('/Getlivefeeddoctorapp',methods=['POST'])
try:
  con = psycopg2.connect(user='quywvejawxhnse',password='065fe8ac62d76caa061d1e517b2f0107b5776f767037c2e29cad16c259a771cf',host='ec2-176-34-113-15.eu-west-1.compute.amazonaws.com',port='5432',database='d3opaj0jiqsm0h')
  cur = con.cursor()
except psycopg2.Error :
     pass
   #return (json.dumps({'Status': 'Failure','Message':'DB connection Error'}, sort_keys=True, indent=4))
def current_token(business_id):
     
     psql = ("select customer_token_num from customer_details where DATE(customer_appointment_date) = DATE(NOW()) and business_id = "+business_id+" and customer_current_status in('cancelled','checkedout') order by   customer_access_datetime desc limit 1")
     cur.execute(psql)
     token_status = cur.fetchone()
     
     #token_status = ''.join(token_status)
     #print(token_status)
     return(token_status)
def aws(business_id,customer_appointment_date,customer_email):
     
     sql = ("select business_avg_wait_time_min,business_appointment_type from business_primary where business_id="+business_id+"")
     cur.execute(sql)
     wait_time = cur.fetchone()
     print(type(wait_time[0]),wait_time[0])
     print(type(wait_time[1]),wait_time[1])
     waittime = wait_time[0]
     appointment_type = wait_time[1]
     psql = ("select customer_token_num from customer_details where business_id = "+business_id+" and customer_appointment_date='"+customer_appointment_date+"' and customer_email='"+customer_email+"'")
     cur.execute(psql)
     data1 = cur.fetchone()
     for token_num in data1:
        print(type(token_num),token_num)
        token_num = int(token_num)
        tokennumber = token_num
     subtoken = token_num - 1
     subtoken = str(subtoken)
    
     print(subtoken,type(subtoken))
 
     psql2 = ("select count(*) from (select * from customer_details order by case when substring(customer_token_num from '^\d+$') is null then 9999 else cast(customer_token_num as integer) end,customer_token_num) customer_details where business_id="+business_id+" and customer_appointment_date='"+customer_appointment_date+"' and customer_current_status in('booked')and customer_token_num between '0' and '"+subtoken+"'")
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
def getlivetokenrecord(request):
   
     customer_email = request.json['customer_email']
     Today_date = datetime.datetime.utcnow().date().strftime('%Y-%m-%d')
     print(type(Today_date),Today_date)
     Tomorrow_date = datetime.datetime.utcnow().date()+ datetime.timedelta(days=1)
     Tomorrow_date = Tomorrow_date.strftime('%Y-%m-%d')
     print(Tomorrow_date)
     sql = ("select * from customer_details where customer_appointment_date in ('"+Today_date+"','"+Tomorrow_date+"') and customer_email = '"+customer_email+"'")
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
     d = {}
     for i in result:
          print(i)
          if i['customer_appointment_date'] == Today_date:
               
               d['Today_customer_appointment_date'] = "Today"
               d['Today_customer_token_num'] = i['customer_token_num']
               business_id = i['business_id']
               business_id = str(i['business_id'])
               query = "select business_first_name from business_primary where business_id = "+business_id+""
               cur.execute(query)
               data = cur.fetchone()
               print(type(data),data)
               docid = ''.join(data)
               print(docid,type(docid))
               docid = docid[3:]
               d['Today_business_name'] = docid
               d['Today_awt'] = aws(business_id,i['customer_appointment_date'],customer_email)
               d['Today_current_token'] = current_token(business_id)
          elif i['customer_appointment_date'] == Tomorrow_date:
               d['Tomorrow_date_customer_appointment_date'] = "Tomorrow"
               d['Tomorrow_date_token_num'] = i['customer_token_num']
               business_id = i['business_id']
               business_id = str(i['business_id'])
               query = "select business_first_name from business_primary where business_id = "+business_id+""
               cur.execute(query)
               data = cur.fetchone()
               print(type(data),data)
               docid = ''.join(data)
               print(docid,type(docid))
               docid = docid[3:]
               d['Tomorrow_business_name'] = docid
               d['Tomorrow_awt'] = aws(business_id,i['customer_appointment_date'],customer_email)
     print(d)          
     return(json.dumps(d))
'''     
     for i in result:
         
         print("business_id",i['business_id'])
         print("customer_appointment_date", i['customer_appointment_date'])
         print("customer_token_num",i['customer_token_num'])
     customer_token_num = i['customer_token_num']
     customer_appointment_date = i['customer_appointment_date']
     business_id = str(i['business_id'])
     query = "select business_first_name from business_primary where business_id = "+business_id+""
     cur.execute(query)
     data = cur.fetchone()
     
     print(type(data),data)
     docid = ''.join(data)
     print(docid,type(docid))


     psql = ("select customer_token_num from customer_details where DATE(customer_appointment_date) = DATE(NOW()) and business_id = "+business_id+" and customer_current_status in('cancelled','checkedout') order by   customer_access_datetime desc limit 1")
     cur.execute(psql)
     token_status = cur.fetchone()
     
     token_status = ''.join(token_status)
     print(token_status)

     sql = ("select business_avg_wait_time_min,business_appointment_type from business_primary where business_id="+business_id+"")
     cur.execute(sql)
     wait_time = cur.fetchone()
     print(type(wait_time[0]),wait_time[0])
     print(type(wait_time[1]),wait_time[1])
     waittime = wait_time[0]
     appointment_type = wait_time[1]
     psql = ("select customer_token_num from customer_details where business_id = "+business_id+" and customer_appointment_date='"+customer_appointment_date+"' and customer_email='"+customer_email+"'")
     cur.execute(psql)
     data1 = cur.fetchone()
     for token_num in data1:
        print(type(token_num),token_num)
        token_num = int(token_num)
        tokennumber = token_num
     subtoken = token_num - 1
     subtoken = str(subtoken)
    
     print(subtoken,type(subtoken))
 
     psql2 = ("select count(*) from (select * from customer_details order by case when substring(customer_token_num from '^\d+$') is null then 9999 else cast(customer_token_num as integer) end,customer_token_num) customer_details where business_id="+business_id+" and customer_appointment_date='"+customer_appointment_date+"' and customer_current_status in('booked')and customer_token_num between '0' and '"+subtoken+"'")
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
        #return(json.dumps({'Status': 'Success', 'StatusCode': '200','Average Wait Time':result}, sort_keys=True, indent=4))
     Today_date = datetime.datetime.utcnow().date().strftime('%Y-%m-%d')
     print(type(Today_date),Today_date)
     Tomorrow_date = datetime.datetime.utcnow().date()+ datetime.timedelta(days=1)
     Tomorrow_date = Tomorrow_date.strftime('%Y-%m-%d')
     print(Tomorrow_date)
     if customer_appointment_date == Today_date:
          return(json.dumps({'Day':'Today','Token':customer_token_num,'Doctorname':docid,'Business_id':business_id,'Current_Token':token_status,'Averagewaittime':result}, indent = 4))
     else:
          return(json.dumps({'Day':'Tomorrow','Token':customer_token_num,'Doctorname':docid,'Business_id':business_id}, indent = 4))
     #return (json.dumps(result))   
 
'''     



#if __name__ == "__main__":
    #app.run(debug=True)
    #app.run(host='192.168.99.1',port=5000)

    
