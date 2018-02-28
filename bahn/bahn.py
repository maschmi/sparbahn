import json        
from  datetime import datetime,date
from requests import Request, Session    
from bs4 import BeautifulSoup as bs
from .nocookie import NoCookie
import os



class TripData():

    def __init__(self):        
        self.trips = []
        self.tripStart = None
        self.tripEnd = None
        self.tripDate = None   
        self.daysToTrip = None     
        
    def readTrip(self, tripJson):
        
        angebotDict = tripJson['angebote']

        priceDict = {}
        
        for angebot in angebotDict:
            price = angebotDict[angebot]['p']
            for id in angebotDict[angebot]['sids']:
                priceDict[id] = price.replace(',','.')

        tripDict = tripJson['verbindungen']
        
        for trip in tripDict:
            nr_trains = len(tripDict[trip]['trains'])
            singleTrip = {
                'changes': tripDict[trip]['nt'],
                'duration': tripDict[trip]['dur'],
                'price': priceDict[tripDict[trip]['sid']],
                'departure': datetime.strptime( "{} {}".format(tripDict[trip]['trains'][0]['dep']['d'],
                                                tripDict[trip]['trains'][0]['dep']['t']),
                                                '%d.%m.%y %H:%M'),            
                'arrival': datetime.strptime( "{} {}".format(tripDict[trip]['trains'][nr_trains-1]['arr']['d'],
                                                            tripDict[trip]['trains'][nr_trains-1]['arr']['t']),
                                                    '%d.%m.%y %H:%M'),
                
            }
            self.trips.append(singleTrip)
        
        self.tripDate = self.trips[0]['departure'].date()
        self.tripEnd = tripJson['dbf'][0]['name']
        self.tripStart = tripJson['sbf'][0]['name']
        self.daysToTrip = datetime.now().date() - self.tripDate

    def findFilter(self, traveldate, departure_time = "16:00", arrival_time = "21:00", max_price = 25):
        min_time = datetime.strptime("{} {}".format(traveldate,departure_time),
                                                '%d.%m.%Y %H:%M')
        max_time = datetime.strptime("{} {}".format(traveldate,arrival_time),
                                                '%d.%m.%Y %H:%M')
        journeys = [t for t in self.trips if float(t['price']) < max_price and t['departure'] > min_time and t['arrival'] < max_time]
        return journeys

class Sparbahn:

    def __init__(self, start, target, fast, tripType, dateTo, dateBack):
        # = 'Dresden Hbf', target = 'N', fast = False, tripType='return', dateTo, dateBack):
        #setup session to use
        self.reqsession = Session()
        self.reqsession.cookies.set_policy(NoCookie())
        self.tripType = tripType
        self.start = start
        if isinstance(dateTo,date):
            self.dateTo = dateTo.strftime('%d.%m.%Y')
        else:
            self.dateTo = dateTo
        if isinstance(dateBack,date):
            self.dateBack = dateBack.strftime('%d.%m.%Y')
        else:
            self.dateBack = dateBack      
        self.fastOnly = fast
        self.start = start
        self.target = target
        self.travellers = [ {"typ":"E", "bc":"2"}]
        self.session = None
        self.bhfId = {'N':'008000284', 'Dresden Hbf': '008010085'}
        try:
            self.startID = self.bhfId[start]
            self.endID = self.bhfId[target]
        except KeyError:
            raise KeyError("Bahnhofnamen nicht in bhfID gefunden. Bitte eintragen.")
        self.toData = None
        self.backData = None
                    

    def getPSCcode(self):
        """gets a PSCCode from a hidden field needed for the XHR"""
        base_url = "https://ps.bahn.de/preissuche/preissuche/psc_angebotssuche.post"
        
        lang = "de"
        country = "DEU"

        headers = {
            'Host': 'ps.bahn.de',
            'Connection': 'close',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.97 Safari/537.36 Vivaldi/1.94.1008.34',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
            }

        payload = {"country":country,"lang":lang}
        payload

        ht = self.reqsession.post(base_url,data=payload,headers=headers)

        soup = bs(ht.text,'html.parser')
        self.session = soup.find(id='pscExpires').attrs['value']

    def getData(self):
        """runs a XHR request get (round)trip and pricing data in JSON"""
        base_url = 'http://ps.bahn.de/preissuche/preissuche/psc_service.go'
        travellers = self.travellers
        travellers[0]['alter'] = ''
        
        if not self.session:
            self.getPSCcode()

        data_to = {
            "s":self.startID,
            "d":self.endID,
            "dt":self.dateTo,
            "t":"0:00",
            "dur":"1440",
            "pscexpires": self.session,
            "dir":"1",
            "sv":self.fastOnly,
            "ohneICE":"false",
            "bic":"false",
            "tct":"0",
            "c":"2",
            "travellers": travellers
            }        
        
        payload = { 'data': json.dumps(data_to, ensure_ascii=True),
                    'service':'pscangebotsuche'}
        
        headers = {
            'Host': 'ps.bahn.de',
            'Referer': 'https://ps.bahn.de/preissuche/preissuche/psc_angebotssuche.post?lang=de&country=DEU',
            'Connection': 'close',
            'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.97 Safari/537.36 Vivaldi/1.94.1008.34',

        }
        ht = self.reqsession.get(base_url,params=payload, headers=headers)
        self.toData = ht.json()

        if self.tripType == 'return':
            data_back = {
            "s":self.endID,
            "d":self.startID,
            "dt":self.dateBack,
            "t":"0:00",
            "dur":"1440",
            "pscexpires": self.session,
            "dir":"2",
            "sv":self.fastOnly,
            "ohneICE":"false",
            "bic":"false",
            "tct":"0",
            "c":"2",
            "travellers": travellers
            }

            payload['data'] = json.dumps(data_back, ensure_ascii=True)
            ht = self.reqsession.get(base_url,params=payload, headers=headers)
            self.backData = ht.json()


    def writeToFile(self,directory="."):       
        
        if self.toData is not None:
            with open(os.path.join(directory,'from_{}_to_{}_at_{}_{}.json'.format(self.start, self.target, self.dateTo, datetime.now()) ),'w') as outfile:
                json.dump(self.toData,outfile)

        if self.backData is not None:
            with open(os.path.join(directory,'from_{}_to_{}_at_{}_{}.json'.format(self.target, self.start, self.dateBack,  datetime.now())),'w') as outfile:
                json.dump(self.backData,outfile)
