import os
import os.path
import commands
import argparse
import time

def goOut(path):
    ignore_file = 'ignore.txt'
    ignore_file_path = os.path.join(os.path.dirname(path),ignore_file)
    if os.path.exists(path):
        with open(ignore_file_path,'a+') as f:
            f.write(os.path.basename(path) + os.linesep)
        try:
            os.remove(path)
        except Exception as e:
            print e
    else:
        print 'file not exist'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',"--cmd", help="the command [go/purge] which control the system")
    parser.add_argument('-p',"--path", help="the path of file")
    args = parser.parse_args()
    if args.cmd == 'go':
        goOut(args.path)
