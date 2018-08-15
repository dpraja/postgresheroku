import json
import psycopg2
import datetime
from flask import Flask,request,jsonify
app = Flask(__name__)
#@app.route("/averagewait",methods=['GET'])
def avgwaittime():
    if request.args.get('business_id'):
        business_id = request.args['business_id'] 
    if request.args.get('appointment_date'):
        customer_appointment_date = request.args['appointment_date']
    if request.args.get('customer_email'):
        customer_email = request.args['customer_email']
    try:
     con = psycopg2.connect(user='quywvejawxhnse',password='065fe8ac62d76caa061d1e517b2f0107b5776f767037c2e29cad16c259a771cf',host='ec2-176-34-113-15.eu-west-1.compute.amazonaws.com',port='5432',database='d3opaj0jiqsm0h')
     cur = con.cursor()  
    except psycopg2.Error :
       return (json.dumps({'Status': 'Failure','Message':'DB connection Error'}, sort_keys=True, indent=4)) 
    
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
        return(json.dumps({'Status': 'Success', 'StatusCode': '200','Average_Wait_Time':result}, sort_keys=True, indent=4))
    else:
      pass
    cur.close()
    con.close()      
 

 
    

