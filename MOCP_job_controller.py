import MOCPsettings
import mysql.connector
import datetime
import os.path
import logging
import sys
from time import sleep
from MOCUtils import get_schedule_date, date_properties, insert_log_entry


schedule_date=''
job_dets={}

logging.basicConfig(level=logging.DEBUG,
                    filename='/home/pi/log/MOCP_Job_Controller.log',filemode='a',
                    format='%(asctime)s - %(name)s -%(levelname)s: %(message)s')
logger=logging.getLogger('MOCP Job Controller')


def main():
    schedule_info()
    while True:
        process()
    cnx.close()
    
def schedule_info():
    global schedule_date

    logger.info('Job Controller Starting')
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

#    time_now=datetime.datetime.now().strftime("%H:%M:%S")
    time_now='21:01:00' 
    logger.info("Checking schedule - {}".format(time_now))
    mycursor= cnx.cursor()
# TO DO - select doesn't work for non standard schedule daya eg 06:00 to 05:59, jobs
#         with a schedule time 00:00 to 05:59 will be picked up previous day!

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
        jobs=mycursor.fetchall()


        for (job_id, job_system, job_suite, job_job, job_status, job_schedule_date, job_schedule_time)  in jobs:
            job_dets = {
                        'id' : job_id,
                        'system' : job_system,
                        'suite' : job_suite,
                        'job' : job_job,
                        'status' : job_status,
                        'schedule_date' : job_schedule_date,
                        'schedule_time' : job_schedule_time}
                        
            job_depenency_met=check_job_dependency(cnx)
            if job_depenency_met:
                file_dependency_met=check_file_dependency(cnx)
                if file_dependency_met:
                    ready_to_run(cnx)
    cnx.commit()              

    sleep(MOCPsettings.controller_sleep_time)
    schedule_info()



def check_job_dependency(cnx):
    global schedule_date, job_dets
    mycursor= cnx.cursor()
    
    logger.info('Checking dependencies for job - {}'.format(job_dets['job']))
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
        dep_jobs=mycursor.fetchall()
        dependencies=mycursor.rowcount
        dep_met=0
        
        if mycursor.rowcount == 0:
            pass
        else:
    #            print(mycursor.rowcount)
            for i in dep_jobs:
    #                print(i)                
                met_if_not_scheduled=i[7]
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
                                AND status = 'RF'""".format(i[4], i[5], i[6],schedule_date)
        
                    mycursor.execute(sql)


                except mysql.connector.Error as err:
                    logger.error(sql)
                    logger.error(err)
                    sys.exit(1)
                else:
                    jobs=mycursor.fetchall()
        #               print(mycursor.rowcount)
                    if mycursor.rowcount == 1:
                        dep_met+=1
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
                            jobs=mycursor.fetchall()
                            if mycursor.rowcount == 0 and met_if_not_scheduled == 'Y':
                                dep_met+=1   
                        
        logger.info('No dependencies {} no met {}'.format(dependencies, dep_met))

    if dependencies==dep_met:
        return True
    else:
        return False

def check_file_dependency(cnx):
    global schedule_date, job_dets

    mycursor= cnx.cursor()
    
    logger.info('Checking file dependencies for job - {}'.format(job_dets['job']))
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
        dep_files=mycursor.fetchall()
        dependencies=mycursor.rowcount
        dep_met=0
    #    print(dependencies, dep_met)
        if mycursor.rowcount == 0:
            pass
        else:
    #            print(mycursor.rowcount)
            for i in dep_files:
                if os.path.exists(i[4]):
                    if i[5] == 'EXISTS':
                        dep_met+=1
                else:
                    if i[5] == 'NOTEXISTS':
                        dep_met+=1
 
    if dependencies==dep_met:
        return True
    else:
        return False

def ready_to_run(cnx):
    global schedule_date, job_dets
    mycursor= cnx.cursor()
    
    sql = """UPDATE mocp_schedule_job set status = 'RQ'
            WHERE system = '{}'
            AND   suite = '{}'
            AND   job   =  {}
            AND   schedule_date = '{}'""".format(job_dets['system'], job_dets['suite'], job_dets['job'], job_dets['schedule_date'])
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
                             job_dets['system'], job_dets['suite'], job_dets['job'], 0 ,'Dependencies met' , job_dets['schedule_date'], 'RQ')
        try:
            mycursor.execute(sql)
        except mysql.connector.Error as err:
            logger.error(sql)
            logger.error(err)
            sys.exit(1)

if __name__ == "__main__":
    main()