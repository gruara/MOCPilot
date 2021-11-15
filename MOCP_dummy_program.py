import random
from time import sleep

def main():
#   use current time to seed random
    random.seed()
    
    run_time=random.randint(30, 600)
    print("Run time {} seconds".format(run_time)) 
    sleep(run_time)
    
    result=random.randint(0,9)

    if result > 8:
        exit(result)
    else:
        exit(0)


if __name__ == "__main__":
    main()