from bahn.bahn import Sparbahn, TripData

start = 'Dresden Hbf'
target = 'N'
dateTo = '22.02.2018'
dateBack = '31.03.2018'
#trip = Sparbahn(start = start, target = target, fast = False, tripType='return', dateTo=dateTo, dateBack=dateBack)
#trip.getData()
#trip.writeToFile()

import json
trips = {}
with open('back_2018-02-13 19:45:10.552781.json', 'r') as infile:
    trips = json.loads(infile.read())

tripdata = TripData()
tripdata.readTrip(trips)
print("yay")