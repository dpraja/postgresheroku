import json
import datetime
import psycopg2
import arrow
import calendar
from flask import Flask,request,jsonify
app = Flask(__name__)
#@app.route('/GetBusinessReportAllDate',methods=['GET'])     
def getbusinessreportalldate(request):
     business_group = request.args['business_group']
     
     if request.args.get('business_group') and request.args.get('date_from') and request.args.get('date_to'):
        date_from = request.args['date_from']
        date_to = request.args['date_to']
     elif request.args.get('business_group'):
        Today_date = datetime.datetime.utcnow().date().strftime('%Y-%m-%d')
        date_from = Today_date
        date_to = Today_date
     a = arrow.get(date_from)
     b = arrow.get(date_to)
     delta = (b-a)
     delta = delta.days +1
     #print (delta)
     try:
      con = psycopg2.connect(user='quywvejawxhnse',password='065fe8ac62d76caa061d1e517b2f0107b5776f767037c2e29cad16c259a771cf',host='ec2-176-34-113-15.eu-west-1.compute.amazonaws.com',port='5432',database='d3opaj0jiqsm0h')
      cur = con.cursor()
     except psycopg2.Error :
       return (json.dumps({'Status': 'Failure','Message':'DB connection Error'}, sort_keys=True, indent=4))
     sql = "select business_id,business_first_name from business_primary where business_group= '"+business_group+"'"
     cur.execute(sql)
     result = cur.fetchall()
     val,business_id,business_name,values,d,e = [],[],[],[[]],{},{}
     y=1
     for i in result: 
       for a in i:
        if y % 2 == 0:  
           business_name.append(a)
        else:
           business_id.append(a)  
        y+=1
     #print("name",business_name)   
     business_group=[]
     no = 0
     for b_id in business_id:
         groups,lable = {},{}
         count,b_dates = [],[]
         b_id = str(b_id)
         #print(b_id)
         groups['name'] = business_name[no]
         #print("groups",groups)
         count_date = date_from
         
         while count_date <= date_to:
              
           sql1 = "select count(*) from customer_details where business_id='"+b_id+"' and customer_appointment_date ='"+count_date+"'and customer_current_status in ('checkedout')"
           count_date = datetime.datetime.strptime(count_date, '%Y-%m-%d')
           b_dates.append((calendar.day_name[count_date.weekday()][0:3]+"("+count_date.strftime("%d")+" "+calendar.month_name[count_date.month][0:3]+")"))
           count_date += datetime.timedelta(days=1)
           count_date = datetime.datetime.strftime(count_date, '%Y-%m-%d')
           
           #print(sql1)
           cur.execute(sql1)
           result = cur.fetchone()
           #print("result",result)
           for i in result:
              count.append(i)
         groups['values'] = count
         groups['lable'] = b_dates
         #business_group.append(b_)
         business_group.append(groups)
         no+=1     
         #print(count)
     
     print("business_group",business_group)
     #groups['Business_Group'] = request.args['business_group']
     #business_group.append({'Business_Group':request.args['business_group']})
     return(json.dumps({"Business_Group":request.args['business_group'],"Business_Members":business_group},indent =2))    
     con.close()    

