import datetime
import hashlib
# import json
import logging
import subprocess
import uuid

import mysql.connector
from flask import Flask, jsonify, request

import MOCPsettings

logging.basicConfig(level=MOCPsettings.LOGGING_LEVEL,
                    filename=MOCPsettings.LOGGING_FILE_WEB_SERVICES, filemode='a',
                    format='%(asctime)s - %(name)s - %(threadName)s %(levelname)s: %(message)s')  # MOCPsettings.LOGGING_FORMAT)
logger = logging.getLogger('MOCP Web Services')
logger.debug('Web Services Starting')

app = Flask("MOCP_web_services")

token = ''


@app.route("/file_dependency", methods=['GET'])
def get_file_dependencies():
    logger.debug('Get File Dependencies')
    sys_message = 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    if not authorised():
        sys_message = 'Invalid token or token expired'
        response = 403
    else:
        req_payload = request.get_json()
        if not req_payload:
            response = 400
        else:
            system = req_payload.get('system')
            suite = req_payload.get('suite')
            job = req_payload.get('job')

            condition = "id > 0"
            if system:
                condition = "{} AND system = '{}'".format(condition, system)
            if suite:
                condition = "{} AND suite = '{}'".format(condition, suite)
            if job:
                condition = "{} AND job = {}".format(condition, job)
            sql = """SELECT   system, 
                            suite, 
                            job,
                            full_path,
                            rule

                FROM mocp_file_dependency
                WHERE {}
                ORDER BY system, suite, job""".format(condition)
            try:
                mycursor = cnx.cursor()

                mycursor.execute(sql)
            except mysql.connector.Error as err:
                logger.error(sql)
                logger.error(err)
                response = 500
            else:
                if mycursor.rowcount == 0:
                    sys_message = 'No records with given criteria'
                    response = 404
                else:

                    recs = mycursor.fetchall()
                    payload = []
                    for rec_system, rec_suite, rec_job, rec_full_path, rec_rule in recs:

                        job_dict = {'system': rec_system,
                                    'suite': rec_suite,
                                    'job': rec_job,
                                    'full_path': rec_full_path,
                                    'rule': rec_rule}

                        payload.append(job_dict)
                    return_payload = payload
                    response = 200
                    reply = {'http_reply': {
                        'http_code': 200,
                        'http_message': 'Success',
                        'system_message': sys_message}}
                    return jsonify(return_payload, reply), response
    cnx.commit()
    return_payload = {}
    reply = response_message(response, sys_message)
    return jsonify(return_payload, reply), response


@app.route("/job", methods=['GET'])
def get_jobs():
    logger.debug('Get Jobs')
    sys_message = 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    if not authorised():
        sys_message = 'Invalid token or token expired'
        response = 403
    else:
        req_payload = request.get_json()
        if not req_payload:
            response = 400
        else:
            system = req_payload.get('system')
            suite = req_payload.get('suite')
            job = req_payload.get('job')

            condition = "id > 0"
            if system:
                condition = "{} AND system = '{}'".format(condition, system)
            if suite:
                condition = "{} AND suite = '{}'".format(condition, suite)
            if job:
                condition = "{} AND job = {}".format(condition, job)
            sql = """SELECT   system, 
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
                mycursor = cnx.cursor()

                mycursor.execute(sql)
            except mysql.connector.Error as err:
                logger.error(sql)
                logger.error(err)
                response = 500
            else:
                recs = mycursor.fetchall()
                if mycursor.rowcount == 0:
                    sys_message = 'No records with given criteria'
                    response = 404
                else:

                    payload = []
                    for rec_system, rec_suite, rec_job, rec_desc, rec_run_on, rec_or_run_on, rec_or_run_on2, rec_but_not_on, rec_and_not_on, rec_schedule_time, rec_command_line, rec_last_scheduled in recs:
                        stime = rec_schedule_time
                        job_dict = {'system': rec_system,
                                    'suite': rec_suite,
                                    'job': rec_job,
                                    'description': rec_desc,
                                    'run_on': rec_run_on,
                                    'or_run_on': rec_or_run_on,
                                    'or_run_on2': rec_or_run_on2,
                                    'but_not_on': rec_but_not_on,
                                    'and_not_on': rec_and_not_on,
                                    'schedule_time': str(datetime.datetime.strptime(str(stime), "%H:%M:%S").time()),
                                    'command_line': rec_command_line,
                                    'last_scheduled': rec_last_scheduled.strftime("%Y-%m-%d")}

                        payload.append(job_dict)
                    return_payload = payload
                    response = 200
                    reply = {'http_reply': {
                        'http_code': 200,
                        'http_message': 'Success',
                        'system_message': sys_message}}
                    return jsonify(return_payload, reply), response
    cnx.commit()
    return_payload = {}
    reply = response_message(response, sys_message)
    return jsonify(return_payload, reply), response


# @app.route("/api/v1.0/MOCP/job", methods=['POST'])
@app.route("/job", methods=['POST'])
def insert_jobs():
    logger.debug('Insert Jobs')
    sys_message = 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    if not authorised():
        sys_message = 'Invalid token or token expired'
        response = 403
    else:
        jobs = request.get_json()
        if not jobs:
            response = 400
        else:
            insert = ''
            comma = ''
            for job in jobs:
                insert = """{} {} (0, '{}' , '{}', {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', "{}" , '2000-01-01' )""".format(insert,
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
                comma = ','

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
                mycursor = cnx.cursor()

                mycursor.execute(sql)
            except mysql.connector.IntegrityError as err:
                sys_message = 'Request contains duplicates - no records inserted'
                response = 409
            except mysql.connector.Error as err:
                logger.error(sql)
                logger.error(err)
                response = 500
            else:
                cnx.commit()
                sys_message = 'Records inserted'
                response = 200
    return_payload = {}
    reply = response_message(response, sys_message)

    return jsonify(return_payload, reply), response


@app.route("/job", methods=['PUT'])
def update_job():
    logger.debug('Update Job')
    sys_message = 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')
    if not authorised():
        sys_message = 'Invalid token or token expired'
        response = 403
    else:
        req_payload = request.get_json()
        if not req_payload:
            response = 400
        else:
            system = req_payload.get('system')
            suite = req_payload.get('suite')
            job = req_payload.get('job')
            description = req_payload.get('description')
            run_on = req_payload.get('run_on')
            or_run_on = req_payload.get('or_run_on')
            or_run_on2 = req_payload.get('or_run_on2')
            but_not_on = req_payload.get('but_not_on')
            and_not_on = req_payload.get('and_not_on')
            schedule_time = req_payload.get('schedule_time')
            command_line = req_payload.get('command_line')
            last_scheduled = req_payload.get('last_scheduled')

            sql = """UPDATE `mocp_job` SET  `description` = "{}",
                                            `run_on` = '{}',
                                            `or_run_on` = '{}',
                                            `or_run_on2` = '{}',
                                            `but_not_on` = '{}',
                                            `and_not_on` = '{}',
                                            `schedule_time` = '{}',
                                            `command_line` = "{}",
                                            `last_scheduled` = '{}'
                     WHERE  `system` = '{}' AND
                            `suite` = '{}' AND
                            `job` = {}""".format(description,
                                                 run_on,
                                                 or_run_on,
                                                 or_run_on2,
                                                 but_not_on,
                                                 and_not_on,
                                                 schedule_time,
                                                 command_line,
                                                 last_scheduled,
                                                 system,
                                                 suite,
                                                 job)
            logger.debug(sql)
            try:
                mycursor = cnx.cursor()

                mycursor.execute(sql)
            except mysql.connector.IntegrityError as err:
                sys_message = 'Request contains duplicates - no records inserted'
                response = 409
            except mysql.connector.Error as err:
                logger.error(sql)
                logger.error(err)
                response = 500
            else:
                cnx.commit()
                sys_message = 'Record updated'
                response = 200
    return_payload = {}
    reply = response_message(response, sys_message)

    return jsonify(return_payload, reply), response


@app.route("/job_dependency", methods=['GET'])
def get_job_dependencies():
    logger.debug('Get Job Dependencies')
    sys_message = 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    if not authorised():
        sys_message = 'Invalid token or token expired'
        response = 403
    else:
        req_payload = request.get_json()
        if not req_payload:
            response = 400
        else:
            system = req_payload.get('system')
            suite = req_payload.get('suite')
            job = req_payload.get('job')

            condition = "id > 0"
            if system:
                condition = "{} AND system = '{}'".format(condition, system)
            if suite:
                condition = "{} AND suite = '{}'".format(condition, suite)
            if job:
                condition = "{} AND job = {}".format(condition, job)
            sql = """SELECT   system, 
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
                mycursor = cnx.cursor()

                mycursor.execute(sql)
            except mysql.connector.Error as err:
                logger.error(sql)
                logger.error(err)
                response = 500
            else:
                if mycursor.rowcount == 0:
                    sys_message = 'No records with given criteria'
                    response = 404
                else:
                    recs = mycursor.fetchall()
                    payload = []
                    for rec_system, rec_suite, rec_job, rec_dep_system, rec_dep_suite, rec_dep_job, rec_met_if_not_scheduled in recs:

                        job_dict = {'system': rec_system,
                                    'suite': rec_suite,
                                    'job': rec_job,
                                    'dep_system': rec_dep_system,
                                    'dep_suite': rec_dep_suite,
                                    'dep_job': rec_dep_job,
                                    'met_if_not_scheduled': rec_met_if_not_scheduled}

                        payload.append(job_dict)
                    return_payload = payload
                    response = 200
                    reply = {'http_reply': {
                        'http_code': 200,
                        'http_message': 'Success',
                        'system_message': sys_message}}
                    return jsonify(return_payload, reply), response
    cnx.commit()
    return_payload = {}
    reply = response_message(response, sys_message)
    return jsonify(return_payload, reply), response


@app.route("/job_dependency", methods=['POST'])
def insert_job_dependency():
    logger.debug('Insert Job Dependencies')
    sys_message = 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    if not authorised():
        sys_message = 'Invalid token or token expired'
        response = 403
    else:
        dependencies = request.get_json()
        if not dependencies:
            response = 400
        else:
            insert = ''
            comma = ''
            for dependency in dependencies:
                insert = """{} {} (0, '{}' , '{}', {}, '{}', '{}', {}, "{}" , '{}' )""".format(insert,
                                                                                               comma,
                                                                                               dependency['system'],
                                                                                               dependency['suite'],
                                                                                               dependency['job'],
                                                                                               dependency['dep_system'],
                                                                                               dependency['dep_suite'],
                                                                                               dependency['dep_job'],
                                                                                               '',
                                                                                               dependency['met_if_not_scheduled'])
                comma = ','

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
                mycursor = cnx.cursor()

                mycursor.execute(sql)
            except mysql.connector.IntegrityError as err:
                sys_message = 'Request contains duplicates - no records inserted'
                response = 409
            except mysql.connector.Error as err:
                logger.error(sql)
                logger.error(err)
                response = 500
            else:
                cnx.commit()
                sys_message = 'Records inserted'
                response = 200
    return_payload = {}
    reply = response_message(response, sys_message)

    return jsonify(return_payload, reply), response


@app.route("/log", methods=['GET'])
def get_log_entries():
    logger.debug('Get Log Entries')

    sys_message = 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    if not authorised():
        sys_message = 'Invalid token or token expired'
        response = 403
    else:
        req_payload = request.get_json()
        if not req_payload:
            response = 400
        else:

            system = req_payload.get('system')
            suite = req_payload.get('suite')
            job = req_payload.get('job')
            schedule_date = req_payload.get('schedule_date')

            condition = "timestamp > 0"
            if system:
                condition = "{} AND system = '{}'".format(condition, system)
            if suite:
                condition = "{} AND suite = '{}'".format(condition, suite)
            if job:
                condition = "{} AND job = {}".format(condition, job)
            if schedule_date:
                condition = "{} AND schedule_date = '{}'".format(
                    condition, schedule_date)

            sql = """SELECT   timestamp,
                            system, 
                            suite, 
                            job,
                            action,
                            schedule_date,
                            schedule_status
                FROM mocp_log
                WHERE {}
                ORDER BY timestamp """.format(condition)

            try:

                mycursor = cnx.cursor()

                mycursor.execute(sql)
            except mysql.connector.Error as err:
                logger.error(sql)
                logger.error(err)
                response = 500
            else:
                recs = mycursor.fetchall()
                if mycursor.rowcount == 0:
                    sys_message = 'No records with given criteria'
                    logger.info(sql)
                    response = 404
                else:

                    payload = []
                    for rec_timestamp, rec_system, rec_suite, rec_job, rec_action, rec_schedule_date, rec_status in recs:
                        #
                        job_dict = {'timestamp': rec_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                                    'system': rec_system,
                                    'suite': rec_suite,
                                    'job': rec_job,
                                    'action': rec_action,
                                    'schedule_date': rec_schedule_date.strftime("%Y-%m-%d"),
                                    'status': rec_status
                                    }

                        payload.append(job_dict)
                    return_payload = payload
                    response = 200
                    reply = {'http_reply': {
                        'http_code': 200,
                        'http_message': 'Success',
                        'system_message': sys_message}}
                    return jsonify(return_payload, reply), response
    cnx.commit()
    return_payload = {}

    reply = response_message(response, sys_message)
    return jsonify(return_payload, reply), response


@app.route("/log", methods=['POST'])
def insert_log():
    logger.debug('Insert log')
    sys_message = 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    if not authorised():
        sys_message = 'Invalid token or token expired'
        response = 403
    else:
        payload = request.get_json()
        if not payload:
            response = 400
        else:
            system = payload.get('system')
            suite = payload.get('suite')
            job = payload.get('job')
            job_id = payload.get('job_id')
            action = payload.get('action')
            schedule_date = payload.get('schedule_date')
            schedule_status = payload.get('schedule_status')
            mycursor = cnx.cursor()
            sql = """INSERT INTO `mocp_log` (       `system`,
                                                    `suite`,
                                                    `job`,
                                                    `job_id`,
                                                    `action`,
                                                    `schedule_date`,
                                                    `schedule_status`)
                                             
                     VALUES ('{}', '{}', '{}', {}, '{}', '{}', '{}')""".format(
                system, suite, job, job_id, action, schedule_date, schedule_status)
            try:
                mycursor.execute(sql)
            except mysql.connector.Error as err:
                logger.error(sql)
                logger.error(err)
                response = 500
            else:

                if mycursor.rowcount == 1:
                    sys_message = 'Log entry inserted'
                    response = 201
                    cnx.commit()
                else:
                    sys_message = 'Unknown error'
                    response = 500
    return_payload = {}
    reply = response_message(response, sys_message)

    return jsonify(return_payload, reply), response


@app.route("/schedule_date", methods=['GET'])
def get_schedule_date():
    #    logger.debug('Get Schedule date')
    sys_message = 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    mycursor = cnx.cursor()
    sql = """SELECT * FROM `mocp_schedule` WHERE 1"""

    try:
        mycursor.execute(sql)
        rec = mycursor.fetchone()

    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)
        response = 500
    else:
        if mycursor.rowcount == 1:
            schedule_date = str(rec[1])
            response = 200
        else:
            sys_message = 'Unknown error'
            response = 404
    if response == 200:
        return_payload = {
            'schedule_date': schedule_date
        }
        reply = {'http_reply': {
            'http_code': 200,
            'http_message': 'Success',
            'system_message': sys_message}}
        return jsonify(return_payload, reply), 200
    else:
        reply = response_message(response, sys_message)
        return_payload = {}
        return jsonify(return_payload, reply), response


@app.route("/schedule_date", methods=['PUT'])
def update_schedule_date():
    logger.debug('Update Schedule Date')
    sys_message = 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')
    if not authorised():
        sys_message = 'Invalid token or token expired'
        response = 403
    else:
        req_payload = request.get_json()
        if not req_payload:
            response = 400
        else:
            schedule_date = req_payload.get('schedule_date')

            sql = """UPDATE `mocp_schedule` SET  `schedule_date` = '{}'""".format(
                schedule_date)

            logger.debug(sql)
            try:
                mycursor = cnx.cursor()

                mycursor.execute(sql)
            except mysql.connector.IntegrityError as err:
                sys_message = 'Request contains duplicates - no records inserted'
                response = 409
            except mysql.connector.Error as err:
                logger.error(sql)
                logger.error(err)
                response = 500
            else:
                cnx.commit()
                sys_message = 'Record updated'
                response = 200
    return_payload = {}
    reply = response_message(response, sys_message)

    return jsonify(return_payload, reply), response


@app.route("/schedule_job", methods=['GET'])
def get_schedule_jobs():
    logger.debug('Get Schedule Jobs')
    sys_message = 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    if not authorised():
        sys_message = 'Invalid token or token expired'
        response = 403
    else:
        req_payload = request.get_json()
        if not req_payload:
            response = 400
        else:
            system = req_payload.get('system')
            suite = req_payload.get('suite')
            job = req_payload.get('job')
            schedule_date = req_payload.get('schedule_date')

            if not schedule_date:
                sys_message = 'Schedule date must be supplied'
                response = 400
            else:
                condition = "schedule_date = '{}'".format(schedule_date)
                if system:
                    condition = "{} AND system = '{}'".format(
                        condition, system)
                if suite:
                    condition = "{} AND suite = '{}'".format(condition, suite)
                if job:
                    condition = "{} AND job = {}".format(condition, job)
                sql = """SELECT id,
                                system, 
                                suite, 
                                job, 
                                status, 
                                schedule_date, 
                                schedule_time,
                                last_update from mocp_schedule_job
                    WHERE {}
                    ORDER BY schedule_date, schedule_time, system, suite, job""".format(condition)
                try:
                    mycursor = cnx.cursor()

                    mycursor.execute(sql)
                except mysql.connector.Error as err:
                    logger.error(sql)
                    logger.error(err)
                    response = 500
                else:
                    recs = mycursor.fetchall()
                    if mycursor.rowcount == 0:
                        sys_message = 'No records with given criteria'
                        response = 404
                    else:

                        payload = []
                        for rec_id, rec_system, rec_suite, rec_job, rec_status, rec_schedule_date, rec_schedule_time, rec_last_update in recs:
                            sdate = rec_schedule_date
                            stime = rec_schedule_time
                            job_dict = {'id' : rec_id,
                                        'system': rec_system,
                                        'suite': rec_suite,
                                        'job': rec_job,
                                        'status': rec_status,
                                        'schedule_date': sdate.strftime("%Y-%m-%d"),
                                        'schedule_time': str(datetime.datetime.strptime(str(stime), "%H:%M:%S").time()),
                                        'last_update' :  rec_last_update.strftime("%Y-%m-%d %H:%M:%S")
                                        }

                            payload.append(job_dict)
                        return_payload = payload
                        response = 200
                        reply = {'http_reply': {
                            'http_code': 200,
                            'http_message': 'Success',
                            'system_message': sys_message}}
                        return jsonify(return_payload, reply), response
    cnx.commit()
    return_payload = {}
    reply = response_message(response, sys_message)
    return jsonify(return_payload, reply), response


@app.route("/schedule_job", methods=['POST'])
def insert_schedule_job():
    logger.debug('Insert schedule job')
    sys_message = 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    if not authorised():
        sys_message = 'Invalid token or token expired'
        response = 403
    else:
        payload = request.get_json()
        if not payload:
            response = 400
        else:
            system = payload.get('system')
            suite = payload.get('suite')
            job = payload.get('job')
            status = payload.get('status')
            schedule_date = payload.get('schedule_date')
            schedule_time = payload.get('schedule_time')
            mycursor = cnx.cursor()
            sql = """INSERT INTO `mocp_schedule_job` (`id`,
                                                    `system`,
                                                    `suite`,
                                                    `job`,
                                                    `status`,
                                                    `schedule_date`,
                                                    `schedule_time`)
                                             
                     VALUES (0, '{}', '{}', '{}', '{}', '{}',  '{}')""".format(
                system, suite, job, status, schedule_date, schedule_time)
            try:
                logger.debug(sql)
                mycursor.execute(sql)
            except mysql.connector.Error as err:
                logger.error(sql)
                logger.error(err)
                response = 500
            else:

                if mycursor.rowcount == 1:
                    sys_message = 'Record inserted'
                    response = 201
                    cnx.commit()
                else:
                    sys_message = 'Unknown error'
                    response = 500
    return_payload = {}
    reply = response_message(response, sys_message)

    return jsonify(return_payload, reply), response


@app.route("/schedule_job", methods=['PUT'])
def update_schedule_job():
    logger.debug('Update Schedule Job Status')
    sys_message = 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    if not authorised():
        sys_message = 'Invalid token or token expired'
        response = 403
    else:
        payload = request.get_json()
        if not payload:
            response = 400
        else:
            system = payload.get('system')
            suite = payload.get('suite')
            job = payload.get('job')
            schedule_date = payload.get('schedule_date')
            status = payload.get('status')
            schedule_time = payload.get('schedule_time')

            mycursor = cnx.cursor()
            if schedule_time == '':
                sql = """UPDATE mocp_schedule_job set status = '{}'                                               
                                                    WHERE system = '{}' 
                                                    AND suite ='{}' 
                                                    AND job ='{}'""".format(status, system, suite, job, schedule_date)
            else:
                sql = """UPDATE mocp_schedule_job set status = '{}',
                                                    schedule_time = '{}'
                                                        WHERE system = '{}' 
                                                        AND suite ='{}' 
                                                        AND job ='{}'
                                                        AND schedule_date = '{}'""".format(status, schedule_time, system, suite, job, schedule_date)
            try:
                mycursor.execute(sql)
            except mysql.connector.Error as err:
                logger.error(sql)
                logger.error(err)
                response = 500
            else:

                if mycursor.rowcount == 0:
                    sys_message = 'Either schedule job is not found or status is already set to supplied value'
                    logger.debug(sql)
                    response = 404
                else:
                    if schedule_time == '':
                        action = 'Job schedule status changed'
                    else:
                        action = 'Job expediated'
                    sql = """INSERT INTO `mocp_log` (`system`,
                                                     `suite`,
                                                     `job`,
                                                     `job_id`,
                                                     `action`,
                                                     `schedule_date`,
                                                     `schedule_status`)
                                                         
                                 VALUES ('{}', '{}', '{}', {}, '{}', '{}', '{}')""".format(
                        system, suite, job, 0, action, schedule_date, status)
                    try:
                        mycursor.execute(sql)
                    except mysql.connector.Error as err:
                        logger.error(sql)
                        logger.error(err)
                        response = 500
                    else:
                        cnx.commit()
                        sys_message = 'Status updated'
                        response = 200

    reply = response_message(response, sys_message)
    return_payload = {}

    return jsonify(return_payload, reply), response


@app.route("/sysinfo", methods=['GET'])
def get_sys_info():
    logger.debug('Get System Information')
    sys_message = 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    if not authorised():
        sys_message = 'Invalid token or token expired'
        response = 403
    else:
        mycursor = cnx.cursor()
        sql = """SELECT * FROM `mocp_schedule` WHERE 1"""

        try:
            mycursor.execute(sql)
            rec = mycursor.fetchone()

        except mysql.connector.Error as err:
            logger.error(sql)
            logger.error(err)
            response = 500
        else:

            if mycursor.rowcount != 1:
                schedule_date = 'unknown'
            else:
                schedule_date = str(rec[1])
                processes = subprocess.run(
                    "ps -ef ", capture_output=True, text=True, shell=True).stdout
                if 'apache2' in processes:
                    apache = 'Running'
                else:
                    apache = 'Not running'

                if 'MOCP_schedular' in processes:
                    schedular = 'Running'
                else:
                    schedular = 'Not running'

                if 'MOCP_job_controller' in processes:
                    job_controller = 'Running'
                else:
                    job_controller = 'Not running'
                if 'MOCP_job_runner' in processes:
                    job_runner = 'Running'
                else:
                    job_runner = 'Not running'
                return_payload = {
                    'schedule_date': schedule_date,
                    'apache': apache,
                    'schedular': schedular,
                    'job_controller': job_controller,
                    'job_runner': job_runner
                }
                reply = {'http_reply': {
                    'http_code': 200,
                    'http_message': 'Success',
                    'system_message': sys_message}}
                logger.debug(return_payload)
                return jsonify(return_payload, reply), 200
    return_payload = {}
    reply = response_message(return_payload, response, sys_message)
    return jsonify(reply), response


@app.route("/user", methods=['GET', 'PUT'])
def login():
    global token
    sys_message = 'None'
    payload = request.get_json()
    if not payload:
        print('No Json')
        response = 400
    else:
        user = payload.get('user_id')
        password = payload.get('password')
        new_password = payload.get('new_password')
        if request.method == 'GET' and user and password and not new_password:

            logger.debug('Log in request')
            response, sys_message = login_user(user, password)
        elif request.method == 'PUT' and user and password and new_password:
            logger.debug('Change password request')
            response, sys_message = change_password(
                user, password, new_password)
        else:
            response = 400

    if response == 200:
        return_payload = {
            'token': token
        }
        reply = {'http_reply': {
            'http_code': 200,
            'http_message': 'Success',
            'system_message': sys_message}}
    else:
        return_payload = {}
        reply = response_message(response, sys_message)

    return jsonify(return_payload, reply), response


def login_user(user, password):
    global token
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    mycursor = cnx.cursor()

    sql = """SELECT user_id, password FROM mocp_user WHERE user_id = '{}'""".format(
        user.lower())
    try:
        mycursor.execute(sql)
    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)

        return 500, 'None'
    rec = mycursor.fetchone()
    if mycursor.rowcount < 1:
        return 404, 'Invalid user/password'
    rec_user, rec_password = rec

    in_password = password.encode()
    h = hashlib.new('sha512-256')
    h.update(in_password)
    hash = h.hexdigest()

    if hash != rec_password:
        return 404, 'Invalid user/password'
    token = uuid.uuid4()
    token_expiry = datetime.datetime.now() + \
        datetime.timedelta(minutes=MOCPsettings.TOKEN_EXPIRY)

    sql = """UPDATE mocp_user set token = '{}', token_expiry = '{}' WHERE user_id = '{}'""".format(
        token, token_expiry, user.lower())
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

    mycursor = cnx.cursor()

    sql = """SELECT user_id, password FROM mocp_user WHERE user_id = '{}'""".format(
        user.lower())
    try:
        mycursor.execute(sql)
    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)

        return 500, 'None'
    rec = mycursor.fetchone()
    if mycursor.rowcount < 1:
        return 404, 'Invalid user/password'

    rec_user, rec_password = rec

    if password != 'NULL':
        in_password = password.encode()
        h = hashlib.new('sha512-256')
        h.update(in_password)
        hash = h.hexdigest()

        if hash != rec_password:
            return 404, 'Invalid user/password'
    else:
        if rec_password != '':

            return 505, 'None'

    in_new_password = new_password.encode()
    h = hashlib.new('sha512-256')
    h.update(in_new_password)
    new_hash = h.hexdigest()
    token = uuid.uuid4()
    token_expiry = datetime.datetime.now() + \
        datetime.timedelta(minutes=MOCPsettings.TOKEN_EXPIRY)

    sql = """UPDATE mocp_user set password= '{}', token = '{}', token_expiry = '{}' WHERE user_id = '{}'""".format(
        new_hash, token, token_expiry, user.lower())
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
    logger.debug('Insert user')
    sys_message = 'None'
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    if not authorised():
        sys_message = 'Invalid token or token expired'
        response = 403
    else:
        payload = request.get_json()
        if not payload:
            response = 400
        else:
            user_id = payload.get('user_id')
            name = payload.get('name')
            if not user_id or not name:
                response = 400
            else:
                create_date = datetime.datetime.now().strftime("%Y-%m-%d")
                token = uuid.uuid4()
                token_expiry = '2000-01-01 00:00:01'
                mycursor = cnx.cursor()
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
                    sys_message = 'User already exists'
                    response = 409
                except mysql.connector.Error as err:
                    logger.error(sql)
                    logger.error(err)
                    response = 500
                else:

                    if mycursor.rowcount == 1:
                        sys_message = 'User inserted'
                        response = 201
                        cnx.commit()
                    else:
                        sys_message = 'Unknown error'
                        response = 500
    return_payload = {}
    reply = response_message(response, sys_message)

    return jsonify(return_payload, reply), response


def response_message(response, sys_message='None'):
    if response == 200:
        reply = {'http_reply': {
            'http_code': 200,
            'http_message': 'Success',
            'system_message': sys_message
        }}
    elif response == 201:
        reply = {'http_reply': {
            'http_code': 201,
            'http_message': 'Created',
            'system_message': sys_message}}

    elif response == 400:
        reply = {'http_reply': {
            'http_code': 400,
            'http_message': 'Malformed request',
            'system_message': sys_message}}

    elif response == 403:
        reply = {'http_reply': {
            'http_code': 403,
            'http_message': 'Forbidden',
            'system_message': sys_message}}

    elif response == 404:
        reply = {'http_reply': {
            'http_code': 404,
            'http_message': 'Not Found',
            'system_message': sys_message}}
    elif response == 409:
        reply = {'http_reply': {
            'http_code': 409,
            'http_message': 'Duplicate/Integrity error',
            'system_message': sys_message}}
    else:
        reply = {'http_reply': {
            'http_code': 500,
            'http_message': 'Server error',
            'system_message': sys_message}}
    return reply


def authorised():
    #
    #   header id changed from user_id to user as underscore caused header to be ignored by Apache wsgi
    #
    user = request.headers.get('user')
    in_token = request.headers.get('token')
    if not user or not in_token:
        logger.debug("No user or token")
        return False
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    mycursor = cnx.cursor()

    sql = """SELECT user_id, token, token_expiry FROM mocp_user WHERE user_id = '{}'""".format(
        user.lower())
    try:
        mycursor.execute(sql)
    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)

        return False
    rec = mycursor.fetchone()
    if mycursor.rowcount < 1:
        logger.debug("No user rec returned")
        return False

    rec_user, rec_token, rec_token_expiry = rec

    if in_token != rec_token:
        logger.debug("Token does not match")
        return False

    if datetime.datetime.now() > rec_token_expiry:
        logger.debug("Token expired")
        return False

    return True
