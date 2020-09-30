import re
#Import the file 
from urllib.request import urlretrieve
import os

URL_PATH = 'https://s3.amazonaws.com/tcmg476/http_access_log'
LOCAL_FILE = 'request.log'

# Alt.: supply an anonmymous callback function to print a simple progress bar to screen
if (os.path.isfile("request.log") == False):
  print("Downloading request copy of log file...")
  local_file, headers = urlretrieve(URL_PATH, LOCAL_FILE, lambda x,y,z: print('.', end='', flush=True))
  print("Download complete! Parsing log file...")
else:
  print("Request copy of log file found! Parsing log file...")

# Create this generate output into a percentage 
def print_nicely(number, fours, threes, total):
    four_perc, three_perc = fours/total, threes/total
    print("There were a total of %d request." %total)
    print("%f percent were not successful and %f were redirected." %(four_perc,three_perc))
    keys = keywithmaxval(number)
    print("The most requested file was %s." %keys[0])
    print("The least requested file was %s." %keys [1]) 

#split log files in order to find answers 
def keywithmaxval (d):
    v=list(d.values())
    k=list(d.keys())
    return k[v.index(max(v))], k[v.index(min(v))],

# Break down all the request into one line 
def main(): 
    regex = re.compile(r".*\[([^:]*):(.*) \-[0-9]{4}\] \"([A-Z]+) (.+?) (HTTP.*\"|\") ([2-5]0[0-9]) .*")
    redirected = 0 
    not_successful = 0 
    total_request = 0
    file_dict = {}
    
    with open('./request.log') as fp: 
        for line in fp: 
            try:
                #
                match = re.search(regex, line)
                total_request +=1
                if match.group(6) in file_dict.keys():
                    file_dict[match.group(6)] += 1
                else: 
                    file_dict[match.group(6)] = 1 
                code = (int(match.group(6)))
                if code >= 400:
                     not_successful += 1
                elif code >= 300 and code <= 399:
                     redirected += 1
            except AttributeError:
                continue

#Close loop and print 
    print_nicely(file_dict, not_successful, redirected, total_request)

if __name__ == "__main__":
    main()

