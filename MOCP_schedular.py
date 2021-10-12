
import MOCPsettings
import mysql.connector
import datetime
import logging
import sys

from time import sleep
from MOCUtils import get_schedule_date, date_properties, insert_log_entry

properties=[]
schedule_date=''




logging.basicConfig(level=logging.DEBUG,
                    filename='/home/pi/log/MOCP_Schedular.log',filemode='a',
                    format='%(asctime)s - %(name)s -%(levelname)s: %(message)s')
logger=logging.getLogger('MOCP Schedular')


def main():
    initialise()
    while True:
        process()
    cnx.close()
    logger.info('Schedular Finishing')
    
def initialise():
    global schedule_date, properties
    schedule_date=get_schedule_date()
    if schedule_date == 'Not defined':
        print('Schedule date not defined')
        sys.exit(1)
    print('Schedule date = {}'.format(schedule_date))

    properties=date_properties( schedule_date)
    print(properties)

    logger.info('Schedular Starting')
    logger.info('Schedule date = {}'.format(schedule_date))
    logger.info('Date Properties = {}'.format(properties))
    


    
def process():
    global schedule_date, properties
    cnx = mysql.connector.connect(user=MOCPsettings.DB_USER,
                                  password=MOCPsettings.DB_PASSWORD,
                                  host='localhost',
                                  database='MOCpilot')
    logger.info('Updating Schedule')
    mycursor= cnx.cursor()

    try:
        sql = """SELECT  id,
                         system,
                         suite,
                         job,
                         schedule_scheme,
                         schedule_time,
                         last_scheduled       
                 FROM mocp_job
                 WHERE last_scheduled != '{}'""".format(schedule_date)
        
        mycursor.execute(sql)

    except mysql.connector.Error as err:
        logger.error(sql)
        logger.error(err)
        sys.exit(1)
    else:    
        jobs=mycursor.fetchall()

        for (job_id,
             job_system,
             job_suite,
             job,
             job_scheme,
             job_time,
             job_last_scheduled
                                ) in jobs:
#            print(job)
            if job_scheme in properties:
                sql = """INSERT INTO `mocp_schedule_job` (  `id`,
                                                            `system`,
                                                            `suite`,
                                                            `job`,
                                                            `status`,
                                                            `schedule_date`,
                                                            `schedule_time`)
                                                         
                         VALUES ({}, '{}', '{}', {}, '{}', '{}', '{}')""".format(
                                0, job_system, job_suite, job, "SQ", schedule_date, job_time)
                
                logger.info("Inserting {}".format(job))
                try:
                    mycursor.execute(sql)
                except mysql.connector.Error as err:
                    logger.error(sql)
                    logger.error(err)
                    sys.exit(1)
                else:    
                    sql = """INSERT INTO `mocp_log` (       `system`,
                                                            `suite`,
                                                            `job`,
                                                            `job_id`,
                                                            `action`,
                                                            `schedule_date`,
                                                            `schedule_status`)
                                                     
                             VALUES ('{}', '{}', '{}', {}, '{}', '{}', '{}')""".format(
                                     job_system, job_suite, job, job_id ,'Added to schedule' , schedule_date, 'SQ')

                    try:
                        mycursor.execute(sql)
                    except mysql.connector.Error as err:
                        logger.error(sql)
                        logger.error(err)
                        sys.exit(1)
                    else:
                        sql = """UPDATE mocp_job set last_scheduled = '{}' WHERE id = {}""".format(schedule_date, job_id)
                        try:
                            mycursor.execute(sql)
                        except mysql.connector.Error as err:
                            logger.error(sql)
                            logger.error(err)
                            sys.exit(1)


            # log= {  'system' : job_system,
                    # 'suite' : job_suite,
                    # 'job' : job,
                    # 'job_id' : 0,
                    # 'action' : 'Added to schedule',
                    # 'schedule_date': schedule_date,
                    # 'schedule_status' : 'SQ'}
            
         
            # result=insert_log_entry(log, MOCPsettings.system_user_id, MOCPsettings.system_token)
              
            # sql = """UPDATE mocp_job set last_scheduled = '{}' WHERE id = {}""".format(schedule_date, job_id)
            # try:
                # mycursor.execute(sql)
            # except mysql.connector.Error as err:
                # logger.error(sql)
                # logger.error(err)
       

    cnx.commit()

    mycursor.close() 
    sleep(60)
    
if __name__ == "__main__":
    main()