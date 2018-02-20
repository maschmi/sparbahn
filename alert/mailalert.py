import json
import smtplib
from email.mime.text import MIMEText


class Mailalert:

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
            text += "Für {}€ um {:%H:%M} von {} nach {} (Ankunft {:%H:%M}) in {} Stunden mit {}mal umsteigen.\n".format(trip['price'],                                                                                                    
                                                                                                    trip['departure'],
                                                                                                    self.tripdata.tripStart,
                                                                                                    self.tripdata.tripEnd,
                                                                                                    trip['arrival'],
                                                                                                    trip['duration'],
                                                                                                    trip['changes'])
        if text != "":
            self.message = MIMEText(text)        
            self.message["Subject"] = "{}: Sparpreise von {} nach {}".format(self.tripdata.tripDate, self.tripdata.tripStart, self.tripdata.tripEnd)
            self.to = to        
            self.message["To"] = self.to
            self.sender = sender
            self.message["From"] = self.sender
    
    def sendMessage(self, server, username = None, password = None):
        if self.message is not None:
            self.server = smtplib.SMTP_SSL(host=server)
            if username is not None and password is not None:
                self.server.login(username,password)            
            self.server.send_message(self.message)

        


