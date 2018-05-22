import json
import psycopg2
import datetime
from flask import Flask,request,jsonify
from TokenNumberGenerationChatbots import tokengeneration
app = Flask(__name__)

#@app.route('/updateChatbots',methods=['POST'])
def updatecustomerinfochatbots(request):

    current_time = datetime.datetime.utcnow()+datetime.timedelta(hours=5, minutes=30)
    current_time = current_time.strftime('%H:%M:%S')
    current_time = str(current_time)
    print(type(current_time),current_time)
    current_datetime = datetime.datetime.utcnow()+datetime.timedelta(hours=5,minutes=30)
    current_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    current_datetime = str(current_datetime)
    print(current_datetime)
    
    Today_date = datetime.datetime.utcnow().date().strftime('%Y-%m-%d')
    print(type(Today_date),Today_date)
    business_name = request.json['business_name']
    business_name = "Dr"+" "+business_name
    try:
     con = psycopg2.connect(user='quywvejawxhnse',password='065fe8ac62d76caa061d1e517b2f0107b5776f767037c2e29cad16c259a771cf',host='ec2-176-34-113-15.eu-west-1.compute.amazonaws.com',port='5432',database='d3opaj0jiqsm0h')
     cursor = con.cursor()
    except psycopg2.Error :
       return (json.dumps({'Status': 'Failure','Message':'DB connection Error'}, sort_keys=True, indent=4))
    sqlid = "select business_id  from business_primary where business_first_name ILIKE '"+business_name+"'"
    print(sqlid)
    cursor.execute(sqlid)
    result=cursor.fetchone()
    b_id = result[0]
    print(b_id,type(b_id))
    business_id = b_id#request.json['business_id']
    business_id = str(business_id)
    customer_checkin_date = current_datetime 
    customer_access_datetime = current_datetime
    customer_name = "Chatbots"
    customer_mobile = "Chatbots"
    customer_email = request.json['customer_email']
    customer_token_num = "0"
    customer_current_status = "booked"
    customer_appointment_time = " "
    customer_latlong = "12.12458 | 13.0236"
    customer_gender = "Chatbots"
    customer_photo_url = "Chatbots"
    customer_deviceid = "Chatbots"
    customer_consolidated_activities = "loggedin"
    customer_appointment_date = Today_date
    
    sqlend = ("select business_hour_end ,business_appointment_type from business_primary where  business_id = "+business_id+"")
    print(sqlend)
    cursor.execute(sqlend)
    result=cursor.fetchone()
    business_end_time = result[0]
    b_type = result[1]
    print(business_end_time)
    print( b_type)
    if b_type in ['token']:
      if customer_appointment_date != Today_date:
          return (json.dumps({'Status': 'Success', 'StatusCode': '200','Message':"Token can't be generated other than today"}, sort_keys=True, indent=4)) 
      if business_end_time <= current_time :
          return (json.dumps({'Status': 'Success', 'StatusCode': '200','Message':'AOH'}, sort_keys=True, indent=4))
      else:
        result =''
        sqlselect = ("select customer_current_status,customer_token_num from customer_details where customer_appointment_date = '"+customer_appointment_date+"' and business_id = "+business_id+" and customer_email='"+customer_email+"'")
        print(sqlselect)
        cursor.execute(sqlselect)
        result = cursor.fetchone()
        print(result)                
        if result is None: 
           sql = "insert into customer_details VALUES ("+business_id+",'"+customer_checkin_date+"', '"+customer_access_datetime+"','"+customer_name+"','"+customer_mobile+"','"+customer_email+"',"+customer_token_num+",'"+customer_current_status+"','"+customer_appointment_time+"','"+customer_latlong+"','"+customer_gender+"','"+customer_photo_url+"','"+customer_deviceid+"','"+customer_consolidated_activities+"','"+customer_appointment_date+"')"
           print(sql)
           cursor.execute(sql)
           con.commit()
           return(tokengeneration(business_id,customer_email))
        else:

            #for field in result:
             #   print(field)
            field = result[0]
            token = result[1]
            print(field,token)
            if field in ['booked','checkedout']:
                return(json.dumps({'Status': 'Success', 'StatusCode': '200','Message': 'AlreadyExists','Token':token}, sort_keys=True, indent=4))
            elif field in ['checkedin']:
                print('i am in checked')
                pass
                return(json.dumps({'Status': 'Success', 'StatusCode': '200','Message': 'Already Checkedin Today'}, sort_keys=True, indent=4))
            elif field in ['cancelled']:
                sqlupdate = ("update customer_details set customer_access_datetime='"+customer_access_datetime+"',customer_current_status='"+field+"',customer_token_num='0' where business_id='"+business_id+"' and customer_name='"+customer_name+"' and customer_email='"+customer_email+"'and customer_appointment_date='"+customer_appointment_date+"'")
                print(sqlupdate)
                cursor.execute(sqlupdate)
                con.commit()
                #COMMENT				
                return(tokengeneration(business_id,customer_email))				
    else:
        if b_type in ['slot']:
            return(failure)
    con.close()
 
#if __name__ == "__main__":
        #app.run(debug=True)
 #  app.run(host='192.168.1.6',port='5000')
