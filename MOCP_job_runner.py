#
# This script needs to be executed using python3 rather than python which by default uses python2 as python2
# does not support the run method of subprocess
import MOCUtils
import threading
import subprocess
import mysql.connector
import logging

from time import sleep


cnx = mysql.connector.connect(user='awg',
                              password='iolabr0n',
                              host='localhost',
                              database='MOCpilot')

logging.basicConfig(level=logging.DEBUG,
                    filename='/home/pi/log/MOCP_Job_Runner.log',filemode='a',
                    format='%(asctime)s - %(name)s - %(threadName)s %(levelname)s: %(message)s')
logger=logging.getLogger('MOCP Job Runner')



schedule_date=''

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
    schedule_date=MOCUtils.schedule_date()
    if schedule_date == 'Not defined':
        print('Schedule date not defined')
        sys.exit(1)
    
def process():
    global schedule_date

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

    jobs=mycursor.fetchall()
#    print(mycursor.rowcount)
    cnx.commit()
    for i in jobs:
        if active_threads.count('')<4:
            run_job(i[0], i[1], i[2], i[3], i[5])

def run_job(id, system, suite, job, schedule_date):
    logger.info('Running {}'.format(job))
    mycursor= cnx.cursor()

    sql = """UPDATE mocp_schedule_job set status = 'RS' WHERE id = {}""".format(id)
    try:
        mycursor.execute(sql)
    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)
     
    sql = """INSERT INTO `mocp_log` (`system`,
                                     `suite`,
                                     `job`,
                                     `job_id`,
                                     `action`,
                                     `schedule_date`,
                                     `schedule_status`)
                                         
                 VALUES ('{}', '{}', '{}', {}, '{}', '{}', '{}')""".format(
                         system, suite, job, 0 ,'Job started' , schedule_date, 'RS')
    try:
        mycursor.execute(sql)
    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)
        
    if active_threads.count(1) == 0:
        active_threads.append(1)
#        print('Thread 1')
        t1 = threading.Thread(target=thread_run_job, args=(system, suite, job, 1))
        t1.start()
    elif active_threads.count(2) == 0:
        active_threads.append(2)
#        print('Thread 2')
        t2 = threading.Thread(target=thread_run_job, args=(system, suite, job, 2))
        t2.start()
    elif active_threads.count(3) == 0:
        active_threads.append(3)
#        print('Thread 3')
        t3 = threading.Thread(target=thread_run_job, args=(system, suite, job, 3))
        t3.start()
    elif active_threads.count(4) == 0:
        active_threads.append(4)
#        print('Thread 4')
        t4 = threading.Thread(target=thread_run_job, args=(system, suite, job,4))
        t4.start()
    else:
        logger.warning('No empty thread')
    cnx.commit()
#    clean_threads()
    
    
def thread_run_job(system, suite, job, thread):
    cnx = mysql.connector.connect(user='awg',
                              password='iolabr0n',
                              host='localhost',
                              database='MOCpilot')
    logger.info('Job {} starting'.format(job))
    mycursor=cnx.cursor()
    try:
        sql = """SELECT  id,
                         system,
                         suite,
                         job,
                         command_line,
                         last_scheduled       
                 FROM mocp_job
                 WHERE system = '{}'
                 AND   suite  = '{}'
                 AND   job    =  {}""".format(system, suite, job)
        
        mycursor.execute(sql)

    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)
        
    job_det=mycursor.fetchone()
#    print(job_det)
    result=subprocess.run(job_det[4],shell=True)
    
    if result.returncode == 0:
        status='RF'
        action='finished'
    else:
        status='RE'
        action='failed'
        
    sql = """UPDATE mocp_schedule_job set status = '{}'
            WHERE system = '{}'
            AND   suite = '{}'
            AND   job   =  {}
            AND   schedule_date = '{}'""".format(status, job_det[1], job_det[2], job_det[3], schedule_date)
    try:
        mycursor.execute(sql)
    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)
     
    sql = """INSERT INTO `mocp_log` (`system`,
                                     `suite`,
                                     `job`,
                                     `job_id`,
                                     `action`,
                                     `schedule_date`,
                                     `schedule_status`)
                                         
                 VALUES ('{}', '{}', '{}', {}, 'Job {}', '{}', '{}')""".format(
                         system, suite, job, 0 ,action , job_det[5], status)
    try:
        mycursor.execute(sql)
    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)

    logger.info('Job {} {} '.format(job,action))
    cnx.commit()
    active_threads.remove(thread)

if __name__ == "__main__":
    main()