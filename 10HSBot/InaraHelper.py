import datetime
from json import JSONEncoder


class InaraHelper:
    inaraKey:str;
    spoofName = 'EDDI';
    spoofVersion = '4.0.4';
    encoder:JSONEncoder = JSONEncoder();

    def __init__(self, key:str):
        InaraHelper.inaraKey = key;

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




