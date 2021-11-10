import mysql.connector
import logging
import json
import hashlib
import uuid
import datetime
import subprocess
import MOCPsettings

from flask import (Flask, request, jsonify)



logging.basicConfig(level=logging.DEBUG,
                    filename='/home/pi/log/MOCP_Web_Services.log',filemode='a',
                    format='%(asctime)s - %(name)s - %(threadName)s %(levelname)s: %(message)s')
logger=logging.getLogger('MOCP Web Services')
logger.info('Web Services Starting')

app=Flask("MOCP_web_services")

token=''

@app.route("/file_dependency", methods=['GET'])
def get_file_dependencies():
    logger.info('Get File Dependencies')
    sys_message= 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    if not authorised():
        sys_message='Invalid token or token expired'
        response = 403
    else:    
        req_payload=request.get_json()
        if not req_payload:
            response = 400
        else:
            system= req_payload.get('system')
            suite=req_payload.get('suite')
            job=req_payload.get('job')
           
            

            condition="id > 0"
            if system:
                condition="{} AND system = '{}'".format(condition, system)
            if suite:
                condition="{} AND suite = '{}'".format(condition, suite)
            if job:
                condition="{} AND job = {}".format(condition, job)
            sql="""SELECT   system, 
                            suite, 
                            job,
                            full_path,
                            rule

                FROM mocp_file_dependency
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
                    for rec_system, rec_suite, rec_job, rec_full_path, rec_rule in recs:
            
                        job_dict={'system' : rec_system,
                                  'suite' : rec_suite,
                                  'job' : rec_job,
                                  'full_path' : rec_full_path,
                                  'rule' : rec_rule}
                        
                        payload.append(job_dict)
                    return_payload = payload
                    response = 200            
                    reply = {'http_reply' :{
                            'http_code' : 200,
                            'http_message' : 'Success',
                            'system_message' : sys_message}}
                    return jsonify(return_payload, reply), response
    cnx.commit()
    reply=response_message(response, sys_message)        
    return jsonify(reply), response 

@app.route("/job", methods=['GET'])
def get_jobs():
    logger.info('Get Jobs')
    sys_message= 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    if not authorised():
        sys_message='Invalid token or token expired'
        response = 403
    else:    
        req_payload=request.get_json()
        if not req_payload:
            response = 400
        else:
            system= req_payload.get('system')
            suite=req_payload.get('suite')
            job=req_payload.get('job')
           
            

            condition="id > 0"
            if system:
                condition="{} AND system = '{}'".format(condition, system)
            if suite:
                condition="{} AND suite = '{}'".format(condition, suite)
            if job:
                condition="{} AND job = {}".format(condition, job)
            sql="""SELECT   system, 
                            suite, 
                            job,
                            description,
                            run_on,
                            or_run_on,
                            or_run_on2,
                            but_not_on,
                            and_not_on,
                            schedule_time,
                            command_line,
                            last_scheduled   
                FROM mocp_job
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
                    for rec_system, rec_suite, rec_job, rec_desc, rec_run_on, rec_or_run_on, rec_or_run_on2, rec_but_not_on, rec_and_not_on, rec_schedule_time,rec_command_line, rec_last_scheduled in recs:
            
                        job_dict={'system' : rec_system,
                                  'suite' : rec_suite,
                                  'job' : rec_job,
                                  'description' : rec_desc,
                                  'run_on' : rec_run_on,
                                  'or_run_on' : rec_or_run_on,
                                  'or_run_on2' : rec_or_run_on2,
                                  'but_not_on' : rec_but_not_on,
                                  'and_not_on' : rec_and_not_on,
                                  'schedule_time' : str(rec_schedule_time),
                                  'command_line' : rec_command_line,
                                  'last_scheduled' : rec_last_scheduled.strftime("%Y-%m-%d")}
                        
                        payload.append(job_dict)
                    return_payload = payload
                    response = 200            
                    reply = {'http_reply' :{
                            'http_code' : 200,
                            'http_message' : 'Success',
                            'system_message' : sys_message}}
                    return jsonify(return_payload, reply), response
    cnx.commit()
    reply=response_message(response, sys_message)        
    return jsonify(reply), response    


#@app.route("/api/v1.0/MOCP/job", methods=['POST'])
@app.route("/job", methods=['POST'])
def insert_jobs():
    logger.info('Insert Jobs')
    sys_message= 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

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
                insert="""{} {} (0, '{}' , '{}', {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', "{}" , '2000-01-01' )""".format(insert,
                                                                                               comma,
                                                                                               job['system'],
                                                                                               job['suite'],
                                                                                               job['job'],
                                                                                               job['description'],
                                                                                               job['run_on'],
                                                                                               job['or_run_on'],
                                                                                               job['or_run_on2'],
                                                                                               job['but_not_on'],
                                                                                               job['and_not_on'],
                                                                                               job['schedule_time'],
                                                                                               job['command_line'])
                comma=','

            sql = """INSERT INTO `mocp_job`(`id`,
                                            `system`,
                                            `suite`,
                                            `job`,
                                            `description`,
                                            `run_on`,
                                            `or_run_on`,
                                            `or_run_on2`,
                                            `but_not_on`,
                                            `and_not_on`,
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


@app.route("/job_dependency", methods=['GET'])
def get_job_dependencies():
    logger.info('Get Job Dependencies')
    sys_message= 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    if not authorised():
        sys_message='Invalid token or token expired'
        response = 403
    else:    
        req_payload=request.get_json()
        if not req_payload:
            response = 400
        else:
            system= req_payload.get('system')
            suite=req_payload.get('suite')
            job=req_payload.get('job')
           
            

            condition="id > 0"
            if system:
                condition="{} AND system = '{}'".format(condition, system)
            if suite:
                condition="{} AND suite = '{}'".format(condition, suite)
            if job:
                condition="{} AND job = {}".format(condition, job)
            sql="""SELECT   system, 
                            suite, 
                            job,
                            dep_system,
                            dep_suite,
                            dep_job,
                            met_if_not_scheduled

                FROM mocp_job_dependency
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
                    for rec_system, rec_suite, rec_job, rec_dep_system, rec_dep_suite, rec_dep_job, rec_met_if_not_scheduled in recs:
            
                        job_dict={'system' : rec_system,
                                  'suite' : rec_suite,
                                  'job' : rec_job,
                                  'dep_system' : rec_dep_system,
                                  'dep_suite' : rec_dep_suite,
                                  'dep_job' : rec_dep_job,
                                  'met_if_not_scheduled' : rec_met_if_not_scheduled}
                        
                        payload.append(job_dict)
                    return_payload = payload
                    response = 200            
                    reply = {'http_reply' :{
                            'http_code' : 200,
                            'http_message' : 'Success',
                            'system_message' : sys_message}}
                    return jsonify(return_payload, reply), response
    cnx.commit()
    reply=response_message(response, sys_message)        
    return jsonify(reply), response  

@app.route("/job_dependency", methods=['POST'])
def insert_job_dependency():
    logger.info('Insert Job Dependencies')
    sys_message= 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    if not authorised():
        sys_message='Invalid token or token expired'
        response = 403
    else:    
        dependencies=request.get_json()
        if not dependencies:
            response = 400
        else:
            insert=''
            comma=''
            for dependency in dependencies:
                insert="""{} {} (0, '{}' , '{}', {}, '{}', '{}', {}, "{}" , '{}' )""".format(  insert,
                                                                                               comma,
                                                                                               dependency['system'],
                                                                                               dependency['suite'],
                                                                                               dependency['job'],
                                                                                               dependency['dep_system'],
                                                                                               dependency['dep_suite'],
                                                                                               dependency['dep_job'],
                                                                                               '',
                                                                                               dependency['met_if_not_scheduled'])
                comma=','

            sql = """INSERT INTO `mocp_job_dependency`(`id`,
                                                       `system`,
                                                       `suite`,
                                                       `job`,
                                                       `dep_system`,
                                                       `dep_suite`,
                                                       `dep_job`,
                                                       `dep_type`,
                                                       `met_if_not_scheduled`)
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

@app.route("/log", methods=['POST'])
def insert_log(): 
    logger.info('Insert log') 
    sys_message='None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    if not authorised():
        sys_message='Invalid token or token expired'
        response = 403
    else:    
        payload=request.get_json()
        if not payload:
            response = 400
        else:
            system=payload.get('system')
            suite=payload.get('suite')
            job=payload.get('job')
            job_id=payload.get('job_id')
            action=payload.get('action')
            schedule_date=payload.get('schedule_date')
            schedule_status=payload.get('schedule_status')
            mycursor=cnx.cursor()
            sql = """INSERT INTO `mocp_log` (       `system`,
                                                    `suite`,
                                                    `job`,
                                                    `job_id`,
                                                    `action`,
                                                    `schedule_date`,
                                                    `schedule_status`)
                                             
                     VALUES ('{}', '{}', '{}', {}, '{}', '{}', '{}')""".format(
                             system, suite, job, job_id ,action , schedule_date, schedule_status)
            try:
                mycursor.execute(sql)
            except mysql.connector.Error as err:
                logger.error(sql)
                logger.error(err)
                response = 500
            else:

                if mycursor.rowcount == 1:
                    sys_message='Log entry inserted'
                    response = 201       
                    cnx.commit()
                else:
                    sys_message='Unknown error'
                    response = 500
        
    reply=response_message(response, sys_message)        

    return jsonify(reply), response  
    
    
@app.route("/schedule_date", methods=['GET'])
def get_schedule_date():
    logger.info('Get Schedule date')
    sys_message= 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    mycursor=cnx.cursor()
    sql = """SELECT * FROM `mocp_schedule` WHERE 1"""

    try:
        mycursor.execute(sql)
        rec=mycursor.fetchone()

    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)
        response = 500
    else:
        if mycursor.rowcount == 1:
            schedule_date=str(rec[1])
            response = 200
        else:
            sys_message='Unknown error'
            response = 404
    if response == 200:
        return_payload = {'payload' : {
                        'schedule_date' : schedule_date
                        }}
        reply = {'http_reply' :{
                    'http_code' : 200,
                    'http_message' : 'Success',
                    'system_message' : sys_message}}
        return jsonify(return_payload, reply), 200 
    else:
        reply=response_message(response, sys_message)        
        return jsonify(reply), response


@app.route("/schedule_job", methods=['GET'])
def schedule_jobs():
    logger.info('Get Schedule Jobs')
    sys_message= 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    if not authorised():
        sys_message='Invalid token or token expired'
        response = 403
    else:    
        req_payload=request.get_json()
        if not req_payload:
            response = 400
        else:
            system= req_payload.get('system')
            suite=req_payload.get('suite')
            job=req_payload.get('job')
            schedule_date=req_payload.get('schedule_date')
            
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
                    ORDER BY schedule_date, schedule_time, system, suite, job""".format(condition)
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
    cnx.commit()
    reply=response_message(response, sys_message)        
    return jsonify(reply), response    



@app.route("/schedule_job", methods=['PUT'])
def schedule_job():
    logger.info('Update Schedule Job Status {}')
    sys_message= 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

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


@app.route("/sysinfo", methods=['GET'])
def get_sys_info():  
    logger.info('Get System Information')
    sys_message= 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    if not authorised():
        sys_message='Invalid token or token expired'
        response = 403
    else: 
        mycursor=cnx.cursor()
        sql = """SELECT * FROM `mocp_schedule` WHERE 1"""

        try:
            mycursor.execute(sql)
            rec=mycursor.fetchone()

        except mysql.connector.Error as err:
            logger.error(sql)
            logger.error(err)
            response = 500
        else:
        
            if mycursor.rowcount != 1:
                schedule_date = 'unknown'
            else:
                schedule_date=str(rec[1])
                processes=subprocess.run('ps -ef',capture_output=True,text=True,shell=True).stdout
                if 'apache2' in processes :
                    apache = 'Running'
                else:
                    apache = 'Not running'
                   
                if 'MOCP_schedular' in processes :
                    schedular = 'Running'
                else:
                    schedular = 'Not running'

                if 'MOCP_job_controller' in processes :
                    job_controller = 'Running'
                else:
                    job_controller = 'Not running'              
                if 'MOCP_job_runner' in processes :
                    job_runner = 'Running'
                else:
                    job_runner = 'Not running'
                return_payload = {'payload' : {
                                  'schedule_date' : schedule_date,
                                  'apache' : apache,
                                  'schedular' : schedular,
                                  'job_controller' : job_controller,
                                  'job_runner' : job_runner
                                }}
                reply = {'http_reply' :{
                            'http_code' : 200,
                            'http_message' : 'Success',
                            'system_message' : sys_message}}
                logger.info(return_payload)
                return jsonify(return_payload, reply), 200 
    reply=response_message(response, sys_message)        
    return jsonify(reply), response   
    

        
    
@app.route("/user", methods=['GET', 'PUT'])
def login():
    global token
    sys_message = 'None'
    payload=request.get_json()
    if not payload:
        print('No Json')
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
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

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
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

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

    
@app.route("/user", methods=['POST'])
def new_user(): 
    logger.info('Insert user') 
    sys_message='None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

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
#
#   header id changed from user_id to user as underscore caused header to be ignored by Apache wsgi
#
    user=request.headers.get('user')
    in_token=request.headers.get('token')
    if not user or not in_token:
        logger.info("No user or token")
        return False
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')
        
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
        logger.info("No user rec returned")
        return False

    rec_user, rec_token, rec_token_expiry=rec

    if in_token != rec_token:
        logger.info("Token does not match")
        return False
    
    
    if datetime.datetime.now() > rec_token_expiry:
        logger.info("Token expired")
        return False
    
    return True