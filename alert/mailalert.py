import json
import smtplib
from email.mime.text import MIMEText

class mailalert:

    def __init__(self, tripdata):        
        self.sender = ""
        self.to = ""
        self.server = ""
        self.user = ""
        self.password = ""
        self.message = None
        self.smtp = None        
        self.tripdata = tripdata
    
    def createMessage(self, sender, to):
        text = ""        
        for trip in self.tripdata.trips:
            text += "Für {} von {} um {} nach {} (Ankunft {}) in {} Studen und {}mal umsteigen.\n".format(trip['price'],
                                                                                                    self.tripdata.tripStart,
                                                                                                    trip['departure'],
                                                                                                    self.tripdata.tripEnd,
                                                                                                    trip['arrival'],
                                                                                                    trip['duration'],
                                                                                                    trip['changes'])
        self.message = MIMEText(text)
        self.message["Subject"] = "{}: Sparpreise von {} nach {}".format(self.tripdata.TripDate, self.tripdata.tripStart, self.tripdata.tripEnd)
        self.to = to
        self.message["To"] = self.to
        self.sender = sender
        self.message["From"] = self.sender
    
    def sendMessage(self, server, username = None, password = None):
        self.server = smtplib.SMTP_SSL(host="mail.immernurwollen.de")
        if username is not None and password is not None:
            self.server.login(username,password)            
        self.server.send_message(self.message)

        


