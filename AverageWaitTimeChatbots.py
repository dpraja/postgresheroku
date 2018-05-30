import json
import psycopg2
import datetime
from flask import Flask,request,jsonify
app = Flask(__name__)
def avgwaittime(business_id,customer_email,no,customer_appointment_date):
    
    business_id = business_id
    Today_date = datetime.datetime.utcnow().date().strftime('%Y-%m-%d')
    print(Today_date)
    customer_appointment_date = customer_appointment_date
   
    customer_email = customer_email
    token_number = no
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
    psql = ("select customer_access_datetime from customer_details where business_id = "+business_id+" and customer_appointment_date='"+customer_appointment_date+"' and customer_email='"+customer_email+"'")
    cur.execute(psql)
    data1 = cur.fetchone()
    for accessdatetime in data1:
     accessdatetime = str(accessdatetime)
    accessdatetime = datetime.datetime.strptime(accessdatetime, '%Y-%m-%d %H:%M:%S')
    accessdatetime = accessdatetime-datetime.timedelta(seconds=1)
    print(accessdatetime,type(accessdatetime))
    accessdatetime = str(accessdatetime)
    psql2 = ("select count(*) from (select * from customer_details order by customer_access_datetime ) customer_details where business_id="+business_id+" and customer_appointment_date='"+customer_appointment_date+"' and customer_current_status in('booked')and customer_access_datetime between '"+customer_appointment_date+"' and '"+accessdatetime+"'")
    cur.execute(psql2)
    print(psql2)
    resultcount = cur.fetchone()
    print(resultcount[0])
    resultcount = int(resultcount[0])
    print(type(resultcount))
    sqlid = "select business_hour_start,business_hour_end,business_break_time_start,business_break_time_end,business_address  from business_primary where business_id="+business_id+""
    print(sqlid)
    cur.execute(sqlid)
    val = cur.fetchone()
    bhs = val[0]
    bhe = val[1]
    bbts = val[2]
    bbte = val[3]
    add = val[4]
    print(bhs,bhe,bbts,bbte,add)
    if appointment_type in ['token'] and customer_appointment_date == Today_date:
        final = resultcount * waittime
        result = str(final)
        print(result)
        return(json.dumps({'Status': 'Success', 'StatusCode': '200','Average_Wait_Time':result,'Token':token_number,'business_hour_start':bhs,'business_hour_end':bhe,'breaktime_st':bbts,'breaktime_end':bbte,'business_address':add, 'Message':'New Token','Day':'Today'}, sort_keys=True, indent=4))
    else:
      #pass
        return(json.dumps({'Status': 'Success', 'StatusCode': '200','Average_Wait_Time':'0','Token':token_number,'business_hour_start':bhs,'business_hour_end':bhe,'breaktime_st':bbts,'breaktime_end':bbte,'business_address':add, 'Message':'New Token','Day':'Tomorrow'}, sort_keys=True, indent=4))
    cur.close()
    con.close()      
 
    
 
 
 
    

