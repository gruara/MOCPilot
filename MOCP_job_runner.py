#
# This script needs to be executed using python3 rather than python which by default uses python2 as python2
# does not support the run method of subprocess
import MOCPsettings
import threading
import subprocess
import mysql.connector
import logging
from MOCUtils import get_schedule_date, date_properties, insert_log_entry

from time import sleep


logging.basicConfig(level=logging.DEBUG,
                    filename='/home/pi/log/MOCP_Job_Runner.log',filemode='a',
                    format='%(asctime)s - %(name)s - %(threadName)s %(levelname)s: %(message)s')
logger=logging.getLogger('MOCP Job Runner')



schedule_date=''
job_dets={}

active_threads=[]



def main():
    initialise()
    while True:
        process()
        sleep(60)#
#        clean_threads()
    cnx.close()
    
def initialise():
    global schedule_date
    logger.info('Job Runner Starting')
    logger.info('Schedule date = {}'.format(schedule_date))
    schedule_date=get_schedule_date()
    if schedule_date == 'Not defined':
        print('Schedule date not defined')
        sys.exit(1)
    
def process():
    global schedule_date, job_dets
    
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')

    mycursor= cnx.cursor()
# TO DO - select doesn't work for non standard schedule daya eg 06:00 to 05:59, jobs
#         with a schedule time 00:00 to 05:59 will be picked up previous day!

    try:
        sql = """SELECT  id,
                         system,
                         suite,
                         job,
                         status,
                         schedule_date
                 FROM mocp_schedule_job
                 WHERE schedule_date = '{}'
                    AND status IN ('RQ')""".format(schedule_date)
        
        mycursor.execute(sql)
    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)
        sys.exit(1)
    else:
        jobs=mycursor.fetchall()
    #    print(mycursor.rowcount)
        for job_id, job_system, job_suite, job_job, job_status, job_schedule_date in jobs:
            job_dets = {
                        'id' : job_id,
                        'system' : job_system,
                        'suite' : job_suite,
                        'job' : job_job,
                        'status' : job_status,
                        'schedule_date' : job_schedule_date}
            if active_threads.count('')<4:
                run_job(cnx)
    cnx.commit()


def run_job(cnx):
    global schedule_date, job_dets

    logger.info('Running {}'.format(job_dets['job']))
    mycursor= cnx.cursor()

    sql = """UPDATE mocp_schedule_job set status = 'RS' WHERE id = {}""".format(job_dets['id'])
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
                             job_dets['system'], job_dets['suite'], job_dets['job'], 0 ,'Job started' , job_dets['schedule_date'], 'RS')
        try:
            mycursor.execute(sql)
        except mysql.connector.Error as err:
            logger.error(sql)
            logger.error(err)
        else:   
            if active_threads.count(1) == 0:
                active_threads.append(1)
        #        print('Thread 1')
                t1 = threading.Thread(target=thread_run_job, args=(job_dets['system'], job_dets['suite'], job_dets['job'],'1'))
                t1.start()
            elif active_threads.count(2) == 0:
                active_threads.append(2)
        #        print('Thread 2')
                t2 = threading.Thread(target=thread_run_job, args=(job_dets['system'], job_dets['suite'], job_dets['job'],'2'))
                t2.start()
            elif active_threads.count(3) == 0:
                active_threads.append(3)
        #        print('Thread 3')
                t3 = threading.Thread(target=thread_run_job, args=(job_dets['system'], job_dets['suite'], job_dets['job'],'3'))
                t3.start()
            elif active_threads.count(4) == 0:
                active_threads.append(4)
        #        print('Thread 4')
                t4 = threading.Thread(target=thread_run_job, args=(job_dets['system'], job_dets['suite'], job_dets['job'],'4'))
                t4.start()
            else:
                logger.warning('No empty thread')

#    clean_threads()
    
    
def thread_run_job(system, suite, job, thread):
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')
                                  
    logger.info('Job {} starting'.format(job))
    mycursor=cnx.cursor()
    try:
        sql = """SELECT command_line
                 FROM mocp_job
                 WHERE system = '{}'
                 AND   suite  = '{}'
                 AND   job    =  {}""".format(system, suite, job)
        
        mycursor.execute(sql)

    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)
        sys.exit(1)
    else:    
        command_line=mycursor.fetchone()
    #    print(job_det)
        result=subprocess.run(command_line,shell=True)
        
        if result.returncode == 0:
            status='RF'
            action='finished'
        else:
            status='RE'
            action='failed'
        logger.info('Job {} {} '.format(job, action))
            
        sql = """UPDATE mocp_schedule_job set status = '{}'
                WHERE system = '{}'
                AND   suite = '{}'
                AND   job   =  {}
                AND   schedule_date = '{}'""".format(status, system, suite, job, schedule_date)
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
                                             
                     VALUES ('{}', '{}', '{}', {}, 'Job {}', '{}', '{}')""".format(
                             system, suite, job, 0 ,action , schedule_date, status)
            try:
                mycursor.execute(sql)
            except mysql.connector.Error as err:
                logger.error(sql)
                logger.error(err)
    cnx.commit()
    active_threads.remove(int(thread))

if __name__ == "__main__":
    main()