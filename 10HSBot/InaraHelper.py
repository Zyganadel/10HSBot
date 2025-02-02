import datetime
from json import JSONEncoder


class InaraHelper:
    inaraKey:str;
    spoofName = 'EDDI';
    spoofVersion = '4.0.4';
    encoder:JSONEncoder = JSONEncoder();

    # def __init__(self, key:str):
        # InaraHelper.inaraKey = key;

    @staticmethod
    def GetCMDRData(name:str):        
        header = {'appName':InaraHelper.spoofName,'appVersion':InaraHelper.spoofVersion,'APIkey':InaraHelper.inaraKey};
        dt = datetime.utcnow();
        dtString = dt.isoformat()[:19]+'Z';
        data={'eventName':'getCommanderProfile','eventTimestamp':dtString,'eventData':{'searchName':name}};
        dataFormatted={'header':header,'events':[data]};
        jsonData = InaraHelper.encoder.encode(o=dataFormatted);
        print(dataFormatted);
        print(data);
        print(jsonData);
        response = InaraHelper.requests.post('https://inara.cz/inapi/v1/', data=jsonData);
        reply = response.json();
        status = reply['header']['eventStatus'];
        pass;

    pass;

class InaraData:
    isValid:bool;
    squadronId:int;
    wingId:int;

    def __init__(self, rawData:dict):
        # we'll only be dealing with the event, so disregard the header.
        eventInfo=rawData['events'][0];
        eventData:dict = eventInfo['eventData'];

        # Determine if data is valid by checking status code, and if not, set all values to indicate invalid.
        status:int = eventInfo['eventStatus'];
        self.isValid = status == 200;

        # if data is invalid, perform error handling.
        if(not self.isValid):
            print(f'Got status of {status}, marking data as invalid for this cmdr.');
            self.squadronId=-1;
            self.wingId=-1;
            pass;

        # otherwise parse data into vars.
        else:
            if('commanderSquadron' in eventData.keys()):
                self.squadronId=eventData['commanderSquadron']['squadronID'];
                pass;
            else: self.squadronId=-1; pass;
            if('commanderWing' in eventData.keys()):
                self.wingId=eventData['commanderWing']['wingID'];
                pass;
            else: self.wingId=-1; pass;
            pass;

        pass;
    pass;



