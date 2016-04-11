import httplib
import os
import time
import sys
import getopt
import signal

class bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[31m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    BGRED = '\033[41m'
    WHITE = '\033[37m'


def t():
    current_time = time.localtime()
    ctime = time.strftime('%H:%M:%S', current_time)
    return "["+ ctime + "]"
def shutdown():
	print ""
	print bcolors.BGRED + bcolors.WHITE + t() + "[info] shutting down CPSCAN" + bcolors.ENDC +"\n\n"
	sys.exit()
def usage():
    print bcolors.RED + bcolors.BOLD
    print """
              _______  ___ _______ ____
             / __/ _ \(_-</ __/ _ `/ _ \.
             \__/ .__/___/\__/\_,_/_//_/
               /_/ v 1.0 - susmithHCK
    """
    print bcolors.ENDC
    print """
        USAGE:
         -t  --target   - Target web server "example.com"
         -v  --verbose  - Enable verbose mode
         -h  --help     - show this menu

        EXAMPLE:
          python cpscan.py -t targetsite.com -v
    """
    sys.exit()

def check(host, path):
        try:
            conn = httplib.HTTPConnection(host)
            conn.request("HEAD", path)
            return conn.getresponse().status
        except StandardError:
            return "unknown"


def final_result():
    print t() + "[info] scan complete"
    if len(result_array)==0:
        print bcolors.RED + bcolors.BOLD + t() + "[critical] sorry! CPSCAN could not find any possible directories" + bcolors.ENDC
    else:
        print bcolors.GREEN + bcolors.BOLD
        print t() + "[info] Found " + str(len(result_array)) + " possible directory"
        for count in result_array:
            print count
        print bcolors.ENDC
    shutdown()

def sigint_handler(signum, frame):
    print '\n user interrupt ! shutting down'
    shutdown()

signal.signal(signal.SIGINT, sigint_handler)

v=0
f=0

opts, args = getopt.getopt(sys.argv[1:], 't:hv', ['target=','help''verbose'])


for opt, arg in opts:
    if opt in ('-h','--help'):
        usage()
    elif opt in ('-t', '--target'):
        host = arg
    elif opt in ('-v', '--verbose'):
        v=1
    else:
        usage()
if 'host' not in locals():
    usage()

print bcolors.RED + bcolors.BOLD
print """
              _______  ___ _______ ____
             / __/ _ \(_-</ __/ _ `/ _ \.
             \__/ .__/___/\__/\_,_/_//_/
               /_/ v 1.0 - susmithHCK
"""
print bcolors.ENDC

print t() + "[info] Checking connection to target server"


ccode = check(host,"/")

if (ccode < 400):
	print bcolors.BOLD + t() + "[info] Target server is up and running" + bcolors.ENDC
else:
	print bcolors.RED + bcolors.BOLD + t() + "[warning] Target server seems to be down. check your internet connection or proxy settings. see misspelled words if any " + bcolors.ENDC
	shutdown()

print t() + "[info] Initiating scan loading directory list"

f = open( "dir", "r" )
directory = []
for line in f:
    directory.append(line)

print t() + "[info] Ruinning directory scan to the target server."
maxlen=len(directory)
if (v==0):
    print t() + "[info] "+ str(maxlen) + " Directories loaded This may take a while pls wait.. use option -v for verbose mode"
else:
    print t() + "[info] "+ str(maxlen) + " Directories loaded This may take a while pls wait.."
i=0
result_array = []
for i in range (maxlen):
    c_dir=directory[i].rstrip('\n')
    rcode=check(host,c_dir)
    code=str(rcode)

    if (v==True and rcode >= 400):
        print t() + "[response]" + bcolors.YELLOW + "["+code+"]" + bcolors.ENDC +" =>  "+ host + c_dir

    if (rcode <400 ):
        print bcolors.GREEN + bcolors.BOLD + t() + "[response]" + "["+code+"]" +" =>  "+ host + c_dir + bcolors.ENDC
        num=0
        result="[response]" + "["+code+"]" +" =>  "+ host + c_dir
        result_array.insert(num,result)
        num = num+1
        reply = str(raw_input(bcolors.BOLD +' Do you want to continue scan for more possible results? (y/n): ')).lower().strip()
        print bcolors.ENDC
        if (reply == 'n'):
            final_result()
final_result()
