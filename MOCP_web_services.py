import mysql.connector
import logging
import json
import hashlib
import uuid
import datetime
import MOCPsettings

from flask import (Flask, request, jsonify)


cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                              password=MOCPsettings.DB_PASSWORD,
                              host='localhost',
                              database='MOCpilot')
logging.basicConfig(level=logging.DEBUG,
                    filename='/home/pi/log/MOCP_Web_Services.log',filemode='a',
                    format='%(asctime)s - %(name)s - %(threadName)s %(levelname)s: %(message)s')
logger=logging.getLogger('MOCP Web Services')
logger.info('Job Runner Starting')

app=Flask("MOCP_web_services")

token=''

@app.route("/api/v1.0/MOCP/user", methods=['GET', 'PUT'])
def login():
    global token
    sys_message = 'None'
    payload=request.get_json()
    if not payload:
        response = 400
    else:
        user=payload.get('user_id')
        password=payload.get('password')
        new_password=payload.get('new_password')
        if request.method == 'GET' and user and password and not new_password:
        
            logger.info('Log in request')
            response, sys_message=login_user(user, password)
        elif request.method == 'PUT' and user and password and new_password:
            logger.info('Change password request')
            response, sys_message=change_password(user, password, new_password)
        else:
            response = 400
            
    if response == 200:
        return_payload = {'payload' : {
                        'token' : token
                        }}
        reply = {'http_reply' :{
                    'http_code' : 200,
                    'http_message' : 'Success',
                    'system_message' : sys_message}}
        return jsonify(return_payload, reply), response
    else:
        reply=response_message(response, sys_message)        

        return jsonify(reply), response
        
def login_user(user, password):
    global token
    mycursor= cnx.cursor()

    sql = """SELECT user_id, password FROM mocp_user WHERE user_id = '{}'""".format(user.lower())
    try:
        mycursor.execute(sql)
    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)
 
        return 500, 'None'
    rec=mycursor.fetchone()
    if mycursor.rowcount < 1:
        return 404, 'Invalid user/password'
    rec_user, rec_password=rec

    in_password=password.encode()
    h = hashlib.new('sha512-256')   
    h.update(in_password)
    hash=h.hexdigest()

    if hash != rec_password:
        return 404, 'Invalid user/password'
    token = uuid.uuid4()
    token_expiry = datetime.datetime.now() + \
                        datetime.timedelta(minutes=MOCPsettings.TOKEN_EXPIRY)

    sql = """UPDATE mocp_user set token = '{}', token_expiry = '{}' WHERE user_id = '{}'""".format(token, token_expiry, user.lower())
    try:
        mycursor.execute(sql)
    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)
        return 500, 'None'


    cnx.commit()
    return 200, 'Logged in'
    
def change_password(user, password, new_password):
    global token
    mycursor= cnx.cursor()

    sql = """SELECT user_id, password FROM mocp_user WHERE user_id = '{}'""".format(user.lower())
    try:
        mycursor.execute(sql)
    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)
 
        return 500, 'None'
    rec=mycursor.fetchone()
    if mycursor.rowcount < 1:
        return 404, 'Invalid user/password'

    rec_user, rec_password=rec

    if password != 'NULL':
        in_password=password.encode()
        h = hashlib.new('sha512-256')   
        h.update(in_password)
        hash=h.hexdigest()

        if hash != rec_password:
            return 404,'Invalid user/password'
    else:
        if rec_password != '':
        
            return 505, 'None'
            
    in_new_password=new_password.encode()
    h = hashlib.new('sha512-256')   
    h.update(in_new_password)
    new_hash=h.hexdigest()
    token = uuid.uuid4()
    token_expiry = datetime.datetime.now() + \
                        datetime.timedelta(minutes=MOCPsettings.TOKEN_EXPIRY)
                        
    sql = """UPDATE mocp_user set password= '{}', token = '{}', token_expiry = '{}' WHERE user_id = '{}'""".format(new_hash, token, token_expiry, user.lower())
    try:
  
        mycursor.execute(sql)
    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)
        return 500, 'None'


    cnx.commit()
    return 200, 'Password Changed'
    
@app.route("/api/v1.0/MOCP/user", methods=['POST'])
def new_user(): 
    logger.info('Insert user') 
    sys_message='None'
    if not authorised():
        sys_message='Invalid token or token expired'
        response = 403
    else:    
        payload=request.get_json()
        if not payload:
            response = 400
        else:
            user_id=payload.get('user_id')
            name=payload.get('name')
            if not user_id or not name:
                response = 400
            else:
                create_date=datetime.datetime.now().strftime("%Y-%m-%d")
                token=uuid.uuid4()
                token_expiry='2000-01-01 00:00:01'
                mycursor=cnx.cursor()
                sql = """INSERT INTO `mocp_user`(`user_id`,
                                                 `name`, 
                                                 `created_on`, 
                                                 `password`, 
                                                 `token`, 
                                                 `token_expiry`) 
                            VALUES ('{}', '{}', '{}', '{}', '{}', '{}')""".format(user_id.lower(), name, create_date, '', token, token_expiry)
                try:
                    mycursor.execute(sql)
                except mysql.connector.IntegrityError as err:
                    sys_message='User already exists'
                    response = 409
                except mysql.connector.Error as err:
                    logger.error(sql)
                    logger.error(err)
                    response = 500
                else:

                    if mycursor.rowcount == 1:
                        sys_message='User inserted'
                        response = 201       
                        cnx.commit()
                    else:
                        sys_message='Unknown error'
                        response = 500
        
    reply=response_message(response, sys_message)        

    return jsonify(reply), response  

    
@app.route("/api/v1.0/MOCP/schedule_job", methods=['GET'])
def schedule_jobs():
    logger.info('Get Schedule Jobs')
    sys_message= 'None'
    if not authorised():
        sys_message='Invalid token or token expired'
        response = 403
    else:    
        payload=request.get_json()
        if not payload:
            response = 400
        else:
            system= payload.get('system')
            suite=payload.get('suite')
            job=payload.get('job')
            schedule_date=payload.get('schedule_date')
            
            if not schedule_date:
                sys_message='Schedule date must be supplied'
                response = 400
            else:
                condition="schedule_date = '{}'".format(schedule_date)
                if system:
                    condition="{} AND system = '{}'".format(condition, system)
                if suite:
                    condition="{} AND suite = '{}'".format(condition, suite)
                if job:
                    condition="{} AND job = {}".format(condition, job)
                sql="""SELECT   system, 
                                suite, 
                                job, 
                                status, 
                                schedule_date, 
                                schedule_time from mocp_schedule_job
                    WHERE {}
                    ORDER BY system, suite, job""".format(condition)
                try:
                    mycursor=cnx.cursor()

                    mycursor.execute(sql)
                except mysql.connector.Error as err:
                    logger.error(sql)
                    logger.error(err)
                    response = 500
                else:
                    if mycursor.rowcount == 0:
                        sys_message='No records with given criteria'
                        response = 404       
                    else:
                        recs=mycursor.fetchall()
                        payload=[]
                        for rec_system, rec_suite, rec_job, rec_status, rec_schedule_date, rec_schedule_time in recs:
                            date=rec_schedule_date
                            job_dict={'system' : rec_system,
                                      'suite' : rec_suite,
                                      'job' : rec_job,
                                      'status' : rec_status,
                                      'schedule_date' : date.strftime("%Y-%m-%d"),
                                      'schedule_time' : str(rec_schedule_time)}
                            
                            payload.append(job_dict)
                        return_payload = payload
                        response = 200            
                        reply = {'http_reply' :{
                                'http_code' : 200,
                                'http_message' : 'Success',
                                'system_message' : sys_message}}
                        return jsonify(return_payload, reply), response
    reply=response_message(response, sys_message)        
    return jsonify(reply), response    


@app.route("/api/v1.0/MOCP/schedule_job", methods=['PUT'])
def schedule_job():
    logger.info('Update Schedule Job Status {}')
    sys_message= 'None'
    if not authorised():
        sys_message='Invalid token or token expired'
        response = 403
    else:    
        payload=request.get_json()
        if not payload:
            response = 400
        else:
            system= payload.get('system')
            suite=payload.get('suite')
            job=payload.get('job')
            schedule_date=payload.get('schedule_date')
            new_status=payload.get('new_status')
            
            mycursor= cnx.cursor()

            sql = """UPDATE mocp_schedule_job set status = '{}' WHERE system = '{}' 
                                                                AND suite ='{}' 
                                                                AND job ='{}'
                                                                AND schedule_date = '{}'""".format(new_status, system, suite, job, schedule_date)
            try:
                mycursor.execute(sql)
            except mysql.connector.Error as err:
                logger.error(sql)
                logger.error(err)
                response = 500
            else:

                if mycursor.rowcount == 0:
                    sys_message='Either schedule job is not found or status is already set to supplied value'
                    response = 404
                else:
                    sql = """INSERT INTO `mocp_log` (`system`,
                                                     `suite`,
                                                     `job`,
                                                     `job_id`,
                                                     `action`,
                                                     `schedule_date`,
                                                     `schedule_status`)
                                                         
                                 VALUES ('{}', '{}', '{}', {}, '{}', '{}', '{}')""".format(
                                         system, suite, job, 0 ,'Job schedule status changed' , schedule_date, new_status) 
                    try:
                        mycursor.execute(sql)
                    except mysql.connector.Error as err:
                        logger.error(sql)
                        logger.error(err)
                        response =500
                    else:
                        cnx.commit()
                        sys_message='Status updated'
                        response = 200
    
    reply=response_message(response, sys_message)        

    return jsonify(reply), response
    
@app.route("/api/v1.0/MOCP/job", methods=['POST'])


def insert_jobs():
    logger.info('Insert Jobs')
    sys_message= 'None'
    if not authorised():
        sys_message='Invalid token or token expired'
        response = 403
    else:    
        jobs=request.get_json()
        if not jobs:
            response = 400
        else:
            insert=''
            comma=''
            for job in jobs:
                insert="""{} {} (0, '{}' , '{}', {}, '{}', '{}', '{}', "{}" , '2000-01-01' )""".format(insert,
                                                                                               comma,
                                                                                               job['system'],
                                                                                               job['suite'],
                                                                                               job['job'],
                                                                                               job['description'],
                                                                                               job['schedule_scheme'],
                                                                                               job['schedule_time'],
                                                                                               job['command_line'])
                comma=','

            sql = """INSERT INTO `mocp_job`(`id`,
                                            `system`,
                                            `suite`,
                                            `job`,
                                            `description`,
                                            `schedule_scheme`,
                                            `schedule_time`,
                                            `command_line`,
                                            `last_scheduled`) 
                     VALUES {}""".format(insert)
            try:
                mycursor=cnx.cursor()

                mycursor.execute(sql)
            except mysql.connector.IntegrityError as err:
                sys_message='Request contains duplicates - no records inserted'
                response = 409
            except mysql.connector.Error as err:
                logger.error(sql)
                logger.error(err)
                response = 500
            else:
                cnx.commit()
                sys_message='Records inserted'
                response = 200
    reply=response_message(response, sys_message)        

    return jsonify(reply), response

def response_message(response, sys_message='None'):
    if response == 200:
        reply = {'http_reply' :{
                    'http_code' : 200,
                    'http_message' : 'Success',
                    'system_message' : sys_message
                    }}
    elif response == 201:
        reply = {'http_reply' :{
                    'http_code' : 201,
                    'http_message' : 'Created',
                    'system_message' : sys_message}}
    
    elif response == 400:
        reply = {'http_reply' :{
                    'http_code' : 400,
                    'http_message' : 'Malformed request',
                    'system_message' : sys_message}}

    elif response == 403:
        reply = {'http_reply' :{
                    'http_code' : 403,
                    'http_message' : 'Forbidden',
                    'system_message' : sys_message}}
                    
    elif response == 404:
        reply = {'http_reply' :{
                    'http_code' : 404,
                    'http_message' : 'Not Found',
                    'system_message' : sys_message}}
    elif response == 409:
        reply = {'http_reply' :{
                    'http_code' : 409,
                    'http_message' : 'Duplicate/Integrity error',
                    'system_message' : sys_message}}    
    else:
        reply = {'http_reply' :{                
                    'http_code' : 500,
                    'http_message' : 'Server error',
                    'system_message' : sys_message}}
    return reply

def authorised():
    user=request.headers.get('user_id')
    in_token=request.headers.get('token')
    if not user or not in_token:
        return False
        
    mycursor= cnx.cursor()

    sql = """SELECT user_id, token, token_expiry FROM mocp_user WHERE user_id = '{}'""".format(user.lower())
    try:
        mycursor.execute(sql)
    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)
 
        return False
    rec=mycursor.fetchone()
    if mycursor.rowcount < 1:
        return False

    rec_user, rec_token, rec_token_expiry=rec

    if in_token != rec_token:
        return False
    
    
    if datetime.datetime.now() > rec_token_expiry:
        return False
    
    return True