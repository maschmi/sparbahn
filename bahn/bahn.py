import json        
from requests import Request, Session    
from bs4 import BeautifulSoup as bs
from .nocookie import NoCookie



class TripData():

    def __init__(self):
        self.tripJson = None
        self.trips = []
        self.tripStart = None
        self.tripEnd = None
        self.tripDate = None        
        
    def readTrip(self, tripJson):
        self.tripJson = tripJson
        


class Sparbahn:

    def __init__(self, start, target, fast, tripType, dateTo, dateBack):
        # = 'Dresden Hbf', target = 'N', fast = False, tripType='return', dateTo, dateBack):
        #setup session to use
        self.reqsession = Session()
        self.reqsession.cookies.set_policy(NoCookie())
        self.tripType = tripType
        self.start = start
        self.dateTo = dateTo
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
        base_url = "https://ps.bahn.de/preissuche/preissuche/psc_angebotssuche.post"
        # data = {"startSucheSofort":True ,
        #         "startBhfName":self.start,
        #         "startBhfId":self.startID,
        #         "startBhfLocType":"1",
        #         "zielBhfName":self.target,
        #         "schnelleVerbindungen":self.fastOnly,
        #         "klasse":"2",
        #         "tripType":self.tripType,
        #         "datumHin":self.dateTo,
        #         "sliderHinMin":"0000",
        #         "sliderHinMax":"1440",
        #         "datumRueck":self.dateBack,
        #         "sliderRueckMin":"0000",
        #         "sliderRueckMax":"1440",
        #         "travellers": self.travellers
        #         }
        
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
        base_url = 'http://ps.bahn.de/preissuche/preissuche/psc_service.go'
        travellers = self.travellers
        travellers[0]['alter'] = ''
        #reshape the payload to something like 
        #jQuery311021736690577137074_1518032530614&data=%7B%22s%22%3A%22008002549%22%2C%22d%22%3A%22008000261%22%2C%22dt%22%3A%2208.02.18%22%2C%22t%22%3A%220%3A00%22%2C%22dur%22%3A1440%2C%22pscexpires%22%3A%220702182102-5cd4e44eea411f493f507f597333c820%22%2C%22dir%22%3A1%2C%22sv%22%3Atrue%2C%22ohneICE%22%3Afalse%2C%22bic%22%3Afalse%2C%22tct%22%3A%220%22%2C%22c%22%3A%222%22%2C%22travellers%22%3A%5B%7B%22typ%22%3A%22E%22%2C%22bc%22%3A%220%22%2C%22alter%22%3A%22%22%7D%5D%7D&_=1518032530615
        #/preissuche/preissuche/psc_service.go?lang=de&country=DEU&data={"s":"008002549","d":"008000261","dt":"08.02.18","t":"0:00","dur":1440,"pscexpires":"0702182158-7e3c016f083bdef0b48b766b364ad3c420","dir":1,"sv":true,"ohneICE":false,"bic":false,"tct":"0","c":"2","travellers":[{"typ":"E","bc":"0","alter":""}]}&service=pscangebotsuche
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
            payload['data'] = json.dumps(data_back, ensure_ascii=True)
            ht = self.reqsession.get(base_url,params=payload, headers=headers)
            self.backData = ht.json()


    def writeToFile(self):
        from  datetime import datetime
        
        if self.toData is not None:
            with open('to_{}.json'.format(datetime.now()),'w') as outfile:
                json.dump(self.toData,outfile)

        if self.backData is not None:
            with open('back_{}.json'.format(datetime.now()),'w') as outfile:
                json.dump(self.backData,outfile)
