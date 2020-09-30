import re
from urllib.request import urlretrieve
import os

URL_PATH = 'https://s3.amazonaws.com/tcmg476/http_access_log'
LOCAL_FILE = 'request.log'

if (os.path.isfile("local_copy.log") == False):
  print("Downloading local copy of log file...")
  local_file, headers = urlretrieve(URL_PATH, LOCAL_FILE, lambda x,y,z: print('.', end='', flush=True))
  print("Download complete! Parsing log file...")
else:
  print("Local copy of log file found! Parsing log file...")

dates = {}

from datetime import datetime, timedelta, date
import calendar
from collections import Counter

monthDict = {}
monthDict['Jan'] = 'January'
monthDict['Feb'] = 'February'
monthDict['Mar'] = 'March'
monthDict['Apr'] = 'April'
monthDict['May'] = 'May'
monthDict['Jun'] = 'June'
monthDict['Jul'] = 'July'
monthDict['Aug'] = 'August'
monthDict['Sep'] = 'September'
monthDict['Oct'] = 'October'
monthDict['Nov'] = 'November'
monthDict['Dec'] = 'December'

totalDays = {}
distinctDays = {'Monday':0, 'Tuesday':0, 'Wednesday':0, 'Thursday':0, 'Friday':0, 'Saturday':0, 'Sunday':0}

distinctWeekTotal = 0
distinctWeekDivideCount = 0

#build month dicts
monthCount = {}
for key in monthDict:
  monthCount[key] = 0

distinctMonthCount = {}
for key in monthDict:
  distinctMonthCount[key] = 0

print('monthDict is')
print(monthDict)

print('monthCount is')
print(monthCount)
print(distinctMonthCount)

previousDay = 'Monday'

# mondays,tuesdays,wednesdays,thursdays,fridays,saturdays,sundays = 0
for line in open(local_file):
  try:
    regex = re.compile(r".*\[([^:]*):(.*) \-[0-9]{4}\] \"([A-Z]+) (.+?) (HTTP.*\"|\") ([2-5]0[0-9]) .*")
    elements = regex.split(line)

    days = elements[1]
    if days not in dates:
      dates[days] = 1

    dateSplit = elements[1].split('/')
    print(dateSplit)
    day = datetime.strptime(monthDict[dateSplit[1]] + ' ' + dateSplit[0] + ' ' + dateSplit[2], '%B %d %Y').strftime('%A')
    print(day)

    month = dateSplit[1]
    monthCount[month] = monthCount[month] + 1

    if day is not previousDay:
      distinctDays[day] = distinctDays[day] + 1
      if day is 'Monday':
        distinctWeekDivideCount = distinctWeekDivideCount + 1
    
    if day not in totalDays:
      totalDays[day] = 1
    else:
      totalDays[day] = totalDays[day] + 1
    
    distinctWeekTotal = distinctWeekTotal + 1
    print(totalDays)
    print(distinctDays)

    previousDay = day
  except Exception as e:
    print('errors:', e)


for d in distinctDays:
  totalDays[d] = totalDays[d] / distinctDays[d]

print("Avg requests per day: ")
print(totalDays)

print('Avg requests per week:')
print(distinctWeekTotal/distinctWeekDivideCount)

print('Avg requests per month')
monthCount['Oct'] = monthCount['Oct'] / 2
print(monthCount)


