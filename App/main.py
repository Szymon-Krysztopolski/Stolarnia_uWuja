import sys
from web_server import server_start
from multiprocessing import Process

def main():
    try:
        p1 = Process(target=server_start)
        p1.start()
        p1.join()
        
    except KeyboardInterrupt:
        print("Finish")
        sys.exit(0)

if __name__=="__main__":
    main()