import MOCUtils
import mysql.connector
import datetime
import logging

from time import sleep

properties=[]
#schedule_date=datetime.datetime.now().strftime("%Y-%m-%d")
schedule_date='2021-09-24'
properties=MOCUtils.date_properties( schedule_date)

cnx = mysql.connector.connect(user='awg',
                              password='iolabr0n',
                              host='localhost',
                              database='MOCpilot')

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


    logger.info('Schedular Starting')
    logger.info('Schedule date = {}'.format(schedule_date))
    logger.info('Date Properties = {}'.format(properties))
    


    
def process():
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
        
    jobs=mycursor.fetchall()

# Without commit, although strictly not needed, results from SELECT are cached and
# any additions not picked up - superceded by commit following update 

    cnx.commit()
    for (job_id,
         job_system,
         job_suite,
         job,
         job_scheme,
         job_time,
         job_last_scheduled
         ) in jobs:
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
              
            sql = """UPDATE mocp_job set last_scheduled = '{}' WHERE id = {}""".format(schedule_date, job_id)
            try:
                mycursor.execute(sql)
            except mysql.connector.Error as err:
                logger.error(sql)
                logger.error(err)
       
    mycursor.close()           
    cnx.commit()


    sleep(60)
    
if __name__ == "__main__":
    main()