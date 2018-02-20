from bahn.bahn import TripData
from datetime import datetime, timedelta, date
from alert.mailalert import Mailalert
import json
import os

directory = "samples"
filename = "from_Dresden Hbf_to_N_at_01.03.2018_2018-02-15 19:23:53.221568.json"
bahndata = None
with open(os.path.join(directory,filename),'r') as infile:
    bahndata = json.load(infile)
trips = TripData()
trips.readTrip(bahndata)

trips.trips = trips.findFilter(trips.tripDate.strftime("%d.%m.%Y"))

alert = Mailalert(trips)
alert.createMessage("from","to")

alert.sendMessage("server", "user","pass")