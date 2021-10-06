import MOCUtils
import mysql.connector
import subprocess


cnx = mysql.connector.connect(user='awg',
                              password='iolabr0n',
                              host='localhost',
                              database='MOCpilot')
def main():
    sub_process()

def insert_jobs():
    mycursor =cnx.cursor()
    sql = "INSERT INTO `mocp_job` (`id`, `system`, `suite`, `job`, `description`, `schedule_scheme`, `schedule_time`, `command_line`,`last_scheduled`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = [
            (0 , 'CRED', 'WEEK', '520', 'AWG55', 'FRI', '09:00:00', 'sleep 15','2021-01-01'),
            (0 , 'CRED', 'WEEK', '530', 'AWG56', 'FRI', '09:00:00', 'sleep 180','2021-01-01'),
#             (0 , 'CRED', 'DAY', '30', 'AWG03', 'WEEKDAY', '09:00:00', 'sleep 120','2021-01-01'),
#             (0 , 'CRED', 'DAY', '40', 'AWG04', 'WEEKDAY', '09:00:00', 'sleep 600','2021-01-01'),
#             (0 , 'CRED', 'DAY', '50', 'AWG05', 'WEEKDAY', '09:00:00', 'sleep 100','2021-01-01'),
#             (0 , 'CRED', 'DAY', '60', 'AWG06', 'WEEKDAY', '09:00:00', 'sleep 10','2021-01-01'),
            (0 , 'CRED', 'WEEK', '540', 'AWG58', 'FRI', '09:00:00', 'sleep 120','2021-01-01')
    ]        
    try:
        mycursor.executemany(sql, val)
    except mysql.connector.Error as err:
        print(err)
    cnx.commit()

def sub_process():
    result=subprocess.run("python '/home/pi/Documents/Scripts/MOCP_dummy_program.py'",shell=True)
    print(result.returncode)

    
    
if __name__ == "__main__":
    main()