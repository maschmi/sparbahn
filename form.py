import requests
import json
from pprint import pprint
from bs4 import BeautifulSoup as bs

base_url = "https://ps.bahn.de/preissuche/preissuche/psc_angebotssuche.post"

data = {"startSucheSofort":True ,
            "startBhfName":"Dresden Hbf",
            "startBhfId":"008010085",
            "startBhfLocType":"1",
            "zielBhfName":"N",
            "schnelleVerbindungen":True,
            "klasse":"2",
            "tripType":"return",
            "datumHin":"06.02.18",
            "sliderHinMin":"0000",
            "sliderHinMax":"1440",
            "datumRueck":"07.02.18",
            "sliderRueckMin":"0000",
            "sliderRueckMax":"1440",
            "travellers": [ 
                {"typ":"E",
                "bc":"2"}
                ]
            }
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
ht = requests.get(base_url,data=payload)

soup = bs(ht.text,'html.parser')
session = soup.find(id='pscExpires').attrs['value']


base_url = 'https://ps.bahn.de/preissuche/preissuche/psc_service.go'
data['pscexpires'] = session
#reshape the payload to something like 
#jQuery311021736690577137074_1518032530614&data=%7B%22s%22%3A%22008002549%22%2C%22d%22%3A%22008000261%22%2C%22dt%22%3A%2208.02.18%22%2C%22t%22%3A%220%3A00%22%2C%22dur%22%3A1440%2C%22pscexpires%22%3A%220702182102-5cd4e44eea411f493f507f597333c820%22%2C%22dir%22%3A1%2C%22sv%22%3Atrue%2C%22ohneICE%22%3Afalse%2C%22bic%22%3Afalse%2C%22tct%22%3A%220%22%2C%22c%22%3A%222%22%2C%22travellers%22%3A%5B%7B%22typ%22%3A%22E%22%2C%22bc%22%3A%220%22%2C%22alter%22%3A%22%22%7D%5D%7D&_=1518032530615
#/preissuche/preissuche/psc_service.go?lang=de&country=DEU&data={"s":"008002549","d":"008000261","dt":"08.02.18","t":"0:00","dur":1440,"pscexpires":"0702182158-7e3c016f083bdef0b48b766b364ad3c420","dir":1,"sv":true,"ohneICE":false,"bic":false,"tct":"0","c":"2","travellers":[{"typ":"E","bc":"0","alter":""}]}&service=pscangebotsuche

payload['data'] = json.dumps(data, ensure_ascii=True)
payload['service'] = 'pscangebotsuche'
payload['callback'] = 'jQuery311021736690577137074_1518032530614'
payload['_'] = '1518032530615'

headers = {
    'Host': 'ps.bahn.de',
    'Referer': 'https://ps.bahn.de/preissuche/preissuche/psc_angebotssuche.post?lang=de&country=DEU',
    'Connection': 'close',
    'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest'
}

ht = requests.get(base_url,data=payload, headers=headers)
pass

