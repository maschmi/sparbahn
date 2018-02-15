from bahn.bahn import Sparbahn, TripData
from datetime import datetime, timedelta, date


def allweekdays(start_date, weekday, weeks):
   d = start_date                  # January 1st
   d += timedelta(days = weekday - d.weekday())  # First Sunday
   max_date = d + timedelta(days = 7*weeks)
   while d  <= max_date:
      if d >= datetime.now().date():
        yield d
      d += timedelta(days = 7)

#weekdays 3 = Thu, 4=Fri, 5=Sat, 6=Sun

start = 'Dresden Hbf'
target = 'N'
future_weeks = 4
datesTo = list(allweekdays(datetime.now().date(),3,future_weeks))
datesTo.extend(list(allweekdays(datetime.now().date(),4,future_weeks)))
datesBack = list(allweekdays(datetime.now().date(),5,future_weeks))
datesBack.extend(list(allweekdays(datetime.now().date(),6,future_weeks)))

for i in range(0,future_weeks*2):
    #print(datesTo[i])
    #print(datesBack[i])
    trip = Sparbahn(start = start, target = target, fast = False, tripType='return', dateTo=datesTo[i], dateBack=datesBack[i])
    trip.getData()
    trip.writeToFile()

import json
#trips = trip.toData
with open('from_Dresden Hbf_to_N_at_16.02.2018_2018-02-15 17:59:29.501384.json','r') as datafile:
    trips = json.loads(datafile.read())
tripdata = TripData()
tripdata.readTrip(trips)

filteredtrips = tripdata.findFilter(dateTo,arrival_time="23:59",max_price = 100)


print(filteredtrips)





