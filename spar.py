from bahn.bahn import Sparbahn, TripData
from datetime import datetime, timedelta, date
from alert.mailalert import Mailalert


def allweekdays(start_date, weekday, weeks):
   """generates the date for a given weekday for x weeks in the future starting from start_date"""
   d = start_date                  
   d += timedelta(days = weekday - d.weekday()) 
   max_date = d + timedelta(days = 7*weeks)
   while d  <= max_date:
      if d >= datetime.now().date():
        yield d
      d += timedelta(days = 7)



start = 'Dresden Hbf'
target = 'N'
future_weeks = 1
datesTo = list(allweekdays(datetime.now().date(),3,future_weeks))
#datesTo.extend(list(allweekdays(datetime.now().date(),4,future_weeks)))
datesBack = list(allweekdays(datetime.now().date(),5,future_weeks))
#datesBack.extend(list(allweekdays(datetime.now().date(),6,future_weeks)))

trips_to = []
trips_back = []
for i in range(0,future_weeks*2):
    trip = Sparbahn(start = start, target = target, fast = False, tripType='return', dateTo=datesTo[i], dateBack=datesBack[i])
    trip.getData()
    trip.writeToFile("testdata")
    tripdata_to = TripData()
    tripdata_to.readTrip(trip.toData)
    trips_to.append(tripdata_to)
    
    tripdata_back = TripData()
    tripdata_back.readTrip(trip.backData)    
    trips_back.append(tripdata_back)    

for tripdata in trips_to:
  tripdata.trips = tripdata.findFilter(tripdata.tripDate.strftime("%d.%m.%Y"),"15:00","21:00",30)
  alert = Mailalert(tripdata)
  alert.createMessage(...)
  alert.sendMessage(...)

for tripdata in trips_back:
  tripdata.trips = tripdata.findFilter(tripdata.tripDate.strftime("%d.%m.%Y"),"16:00","23:59",30)
  alert = Mailalert(tripdata)
  alert.createMessage(...)
  alert.sendMessage(...)



