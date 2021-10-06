from time import sleep

f1line=''
f2line=''
f3line=''

f1timestamp=''
f2timestamp=''
f3timestamp=''

f1=open('/home/pi/log/MOCP_Schedular.log', 'r')
f2=open('/home/pi/log/MOCP_Job_Controller.log', 'r')
f3=open('/home/pi/log/MOCP_Job_Runner.log', 'r')
f4=open('/home/pi/log/MOCP_Merged_Log.log', 'w')


def main():
    global f1line
    global f2line
    global f3line
	
    f1line=f1.readline()
    f2line=f2.readline()
    f3line=f3.readline()

    f1timestamp=f1line[0:23]
    f2timestamp=f2line[0:23]
    f3timestamp=f3line[0:23]

    allread=False
    while not allread:
        if f1timestamp <= f2timestamp and f1timestamp <= f3timestamp:
            f1timestamp=read_file_1(f1line)
        elif f2timestamp <= f1timestamp and f2timestamp <= f3timestamp:
            f2timestamp=read_file_2(f2line)
        else:
             f3timestamp=read_file_3(f3line)
        if f1timestamp == '99999999999999999999999' and f2timestamp == '99999999999999999999999' and f3timestamp == '99999999999999999999999':
               allread=True
    f4.close()

def read_file_1(line):
    global f1line
    f4.write(line)
    f1line=f1.readline()
    if not f1line:
        f1.close()
        f1timestamp='99999999999999999999999'
    else:    
        while f1line[0:2] != '20':
            f4.write(f1line)
            f1line=f1.readline()

        f1timestamp=f1line[0:23]


    return f1timestamp

def read_file_2(line):
    global f2line
    f4.write(line)
    f2line=f2.readline()
    if not f2line:
        f2.close()
        f2timestamp='99999999999999999999999'
    else:    
        while f2line[0:2] != '20':
            f4.write(f2line)
            f2line=f2.readline()
        f2timestamp=f2line[0:23]


    return f2timestamp

    
def read_file_3(line):
    global f3line
    f4.write(line)
    f3line=f3.readline()
    if not f3line:
        f3.close()
        f3timestamp='99999999999999999999999'
    else:    
        while f3line[0:2] != '20':
            f4.write(f3line)
            f3line=f3.readline()
        f3timestamp=f3line[0:23]


    return f3timestamp
    
if __name__ == "__main__":
    main()