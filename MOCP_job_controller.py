import datetime
import logging
import os.path
import sys
from time import sleep

import mysql.connector

import MOCPsettings
from MOCUtils import date_properties, get_schedule_date, insert_log_entry

schedule_date = ''
job_dets = {}
ds = MOCPsettings.schedule_start_time
day_start = datetime.datetime.strptime(ds, "%H:%M:%S")

logging.basicConfig(level=MOCPsettings.LOGGING_LEVEL,
                    filename=MOCPsettings.LOGGING_FILE_COTROLLER, filemode='a',
                    format=MOCPsettings.LOGGING_FORMAT)
logger = logging.getLogger('MOCP Job Controller')


def main():
    schedule_info()
    while True:
        process()
    cnx.close()


def schedule_info():
    global schedule_date

    logger.debug('Job Controller Starting')
    logger.debug('Schedule date = {}'.format(schedule_date))
    schedule_date = get_schedule_date()
    if schedule_date == 'Not defined':
        print('Schedule date not defined')
        sys.exit(1)


def process():
    global schedule_date, job_dets

    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  charset='utf8',
                                  host='localhost',
                                  database='MOCpilot')

    time_now = datetime.datetime.now().strftime("%H:%M:%S")
#    time_now='21:01:00'

    mycursor = cnx.cursor()

    try:
        sql = """SELECT  id,
                         system,
                         suite,
                         job,
                         status,
                         schedule_date,
                         schedule_time       
                 FROM mocp_schedule_job
                 WHERE schedule_date = '{}'
                    AND status IN ('SQ', 'SO')
                    AND schedule_time <= '{}'""".format(schedule_date, time_now)

        mycursor.execute(sql)

    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)
        sys.exit(1)
    else:
        jobs = mycursor.fetchall()

        for (job_id, job_system, job_suite, job_job, job_status, job_schedule_date, job_schedule_time) in jobs:
            job_dets = {
                'id': job_id,
                'system': job_system,
                'suite': job_suite,
                'job': job_job,
                'status': job_status,
                'schedule_date': job_schedule_date,
                'schedule_time': job_schedule_time}
            job_ok = False
            logger.debug("Time now - {} Day start - {} Schedule time - {}".format(
                time_now, day_start, job_schedule_time))
            stime = job_schedule_time
            sched_time = datetime.datetime.strptime(str(stime), "%H:%M:%S")
            now = datetime.datetime.strptime(time_now, "%H:%M:%S")
            if ((sched_time <= day_start) and
                (now < day_start) and
                    (now > sched_time)):
                job_ok = True
            elif ((sched_time > day_start) and
                  (now > sched_time)):
                job_ok = True
            logger.debug("Run - {}".format(job_ok))
            if job_ok:
                job_depenency_met = check_job_dependency(cnx)
                if job_depenency_met:
                    file_dependency_met = check_file_dependency(cnx)
                    if file_dependency_met:
                        ready_to_run(cnx)
    cnx.commit()

    sleep(MOCPsettings.controller_sleep_time)
    schedule_info()


def check_job_dependency(cnx):
    global schedule_date, job_dets
    mycursor = cnx.cursor()

    logger.info('Checking dependencies for job - {} {} {}'.format(
        job_dets['system'], job_dets['suite'], job_dets['job']))
    try:
        sql = """SELECT  id,
                         system,
                         suite,
                         job,
                         dep_system,
                         dep_suite,
                         dep_job,
                         met_if_not_scheduled       
                 FROM mocp_job_dependency
                 WHERE  system = '{}'
                    AND suite  = '{}'
                    AND job    = {}""".format(job_dets['system'], job_dets['suite'], job_dets['job'])
        mycursor.execute(sql)

    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)
        sys.exit(1)
    else:
        dep_jobs = mycursor.fetchall()
        dependencies = mycursor.rowcount
        dep_met = 0

        if mycursor.rowcount == 0:
            pass
        else:
            #            print(mycursor.rowcount)
            for i in dep_jobs:
                #                print(i)
                met_if_not_scheduled = i[7]
    #            print('Dependency {}'.format(i[6]))
                try:
                    sql = """SELECT  id,
                                     system,
                                     suite,
                                     job,
                                     status,
                                     schedule_date,
                                     schedule_time       
                             FROM mocp_schedule_job
                             WHERE system = '{}'
                                AND suite  = '{}'
                                AND job    = {}
                                AND schedule_date = '{}'
                                AND status = 'RF'""".format(i[4], i[5], i[6], schedule_date)

                    mycursor.execute(sql)

                except mysql.connector.Error as err:
                    logger.error(sql)
                    logger.error(err)
                    sys.exit(1)
                else:
                    jobs = mycursor.fetchall()
        #               print(mycursor.rowcount)
                    if mycursor.rowcount == 1:
                        dep_met += 1
                    else:
                        try:
                            sql = """SELECT  id,
                                         system,
                                         suite,
                                         job,
                                         status,
                                         schedule_date,
                                         schedule_time       
                                 FROM mocp_schedule_job
                                 WHERE system = '{}'
                                    AND suite  = '{}'
                                    AND job    = {}
                                    AND schedule_date = '{}'""".format(i[4], i[5], i[6], schedule_date)

                            mycursor.execute(sql)
                        except mysql.connector.Error as err:
                            logger.error(sql)
                            logger.error(err)
                            sys.exit(1)
                        else:
                            jobs = mycursor.fetchall()
                            if mycursor.rowcount == 0 and met_if_not_scheduled == 'Y':
                                dep_met += 1

        logger.info('No dependencies {} no met {}'.format(
            dependencies, dep_met))

    if dependencies == dep_met:
        return True
    else:
        return False


def check_file_dependency(cnx):
    global schedule_date, job_dets

    mycursor = cnx.cursor()

    logger.info('Checking file dependencies for job - {} {} {}'.format(
        job_dets['system'], job_dets['suite'], job_dets['job']))
    try:
        sql = """SELECT  id,
                         system,
                         suite,
                         job,
                         full_path,
                         rule
                 FROM mocp_file_dependency
                 WHERE  system = '{}'
                    AND suite  = '{}'
                    AND job    = {}""".format(job_dets['system'], job_dets['suite'], job_dets['job'])
        mycursor.execute(sql)

    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)
        sys.exit(1)
    else:
        dep_files = mycursor.fetchall()
        dependencies = mycursor.rowcount
        dep_met = 0
    #    print(dependencies, dep_met)
        if mycursor.rowcount == 0:
            pass
        else:
            #            print(mycursor.rowcount)
            for i in dep_files:
                if os.path.exists(i[4]):
                    if i[5] == 'EXISTS':
                        dep_met += 1
                else:
                    if i[5] == 'NOTEXISTS':
                        dep_met += 1

    if dependencies == dep_met:
        return True
    else:
        return False


def ready_to_run(cnx):
    global schedule_date, job_dets
    mycursor = cnx.cursor()

    sql = """UPDATE mocp_schedule_job set status = 'RQ'
            WHERE id = '{}'""".format(job_dets['id'])
    try:
        mycursor.execute(sql)
    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)
        sys.exit(1)
    else:

        sql = """INSERT INTO `mocp_log` (`system`,
                                         `suite`,
                                         `job`,
                                         `job_id`,
                                         `action`,
                                         `schedule_date`,
                                         `schedule_status`)
                                             
                     VALUES ('{}', '{}', '{}', {}, '{}', '{}', '{}')""".format(
            job_dets['system'], job_dets['suite'], job_dets['job'], 0, 'Dependencies met', job_dets['schedule_date'], 'RQ')
        try:
            mycursor.execute(sql)
        except mysql.connector.Error as err:
            logger.error(sql)
            logger.error(err)
            sys.exit(1)


if __name__ == "__main__":
    main()
