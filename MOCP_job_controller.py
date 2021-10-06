import mysql.connector
import datetime
import os.path
import logging
from time import sleep


#schedule_date=datetime.datetime.now().strftime("%Y-%m-%d")

schedule_date='2021-09-24'

cnx = mysql.connector.connect(user='awg',
                              password='iolabr0n',
                              host='localhost',
                              database='MOCpilot')
logging.basicConfig(level=logging.DEBUG,
                    filename='/home/pi/log/MOCP_Job_Controller.log',filemode='a',
                    format='%(asctime)s - %(name)s -%(levelname)s: %(message)s')
logger=logging.getLogger('MOCP Job Controller')


def main():
    initialise()
    while True:
        process()
    cnx.close()
    
def initialise():
    logger.info('Job Controller Starting')
    logger.info('Schedule date = {}'.format(schedule_date))
    
def process():
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
    jobs=mycursor.fetchall()

# Without commit, although strictly not needed, results from SELECT are cached and
# any changes/additions not picked up - superceded by commit following update 

    cnx.commit()
    for (job_id, job_system, job_suite, job_job, job_status, job_schedule_date, job_schedule_time)  in jobs:
        job_depenency_met=check_job_dependency(job_system, job_suite, job_job)
        if job_depenency_met:
            file_dependency_met=check_file_dependency(job_system, job_suite, job_job)
            if file_dependency_met:
                ready_to_run(job_id, job_system, job_suite, job_job, job_schedule_date, job_schedule_time)
    sleep(60)



def check_job_dependency(system, suite, job):
    mycursor= cnx.cursor()
    
    logger.info('Checking dependencies for job - {}'.format(job))
    try:
        sql = """SELECT  id,
                         system,
                         suite,
                         job,
                         dep_system,
                         dep_suite,
                         dep_job,
                         met_if_not_scheduled       
                 FROM mocp_job_dependancy
                 WHERE  system = '{}'
                    AND suite  = '{}'
                    AND job    = {}""".format(system, suite, job)    
        mycursor.execute(sql)
        

    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)
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
                if mycursor.rowcount == 0 and met_if_not_scheduled == 'Y':
                    dep_met+=1   
                jobs=mycursor.fetchall()
        logger.info('No dependencies {} no met {}'.format(dependencies, dep_met))
    cnx.commit()              

    if dependencies==dep_met:
        return True
    else:
        return False

def check_file_dependency(system, suite, job):
    mycursor= cnx.cursor()
    
    logger.info('Checking file dependencies for job - {}'.format(job))
    try:
        sql = """SELECT  id,
                         system,
                         suite,
                         job,
                         full_path,
                         rule
                 FROM mocp_file_dependancy
                 WHERE  system = '{}'
                    AND suite  = '{}'
                    AND job    = {}""".format(system, suite, job)    
        mycursor.execute(sql)
        

    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)
    dep_files=mycursor.fetchall()
    dependencies=mycursor.rowcount
    dep_met=0
    print(dependencies, dep_met)
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
                
                


    cnx.commit()              

    if dependencies==dep_met:
        return True
    else:
        return False

def ready_to_run(id, system, suite, job, schedule_date, schedule_time):
    mycursor= cnx.cursor()
    
    sql = """UPDATE mocp_schedule_job set status = 'RQ' WHERE id = {}""".format(id)
    sql = """UPDATE mocp_schedule_job set status = 'RQ'
            WHERE system = '{}'
            AND   suite = '{}'
            AND   job   =  {}
            AND   schedule_date = '{}'""".format(system, suite, job, schedule_date)
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
                         system, suite, job, 0 ,'Dependencies met' , schedule_date, 'RQ')
    try:
        mycursor.execute(sql)
    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)

if __name__ == "__main__":
    main()