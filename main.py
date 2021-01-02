import json
import time
from urllib.request import urlopen
from urllib.parse import quote
import requests


def decoder(resp):
    decoded = ''
    for line in resp:
        decoded += line.decode('utf-8')
    return decoded


token = '1424395773:AAH6kqLhCT91Giq4njcR-dQlqslPFwGxmEA'
URL = f'https://api.telegram.org/bot{token}/'

command = 'getme'
respons = requests.get(f'{URL}{command}')
responsDecoded = decoder(respons)
gtm = json.loads(responsDecoded)


status = True
while status:
    command = 'getUpdates'
    respons = urlopen(URL + command)
    responsDecoded = decoder(respons)
    updates = json.loads(responsDecoded)

    hasUpdate = len(updates['result']) > 0
    if hasUpdate:
        message = updates["result"][0]["message"]
        chat_id = str(message['chat']['id'])

        if 'text' in message:
            text = quote(message['text'].encode('utf-8'))
            command = 'sendmessage'
            respons = urlopen(f'{URL}{command}?chat_id={chat_id}&text={text}')

            responsDecoded = decoder(respons)
            responsToDict = json.loads(responsDecoded)
            sendMessageValid = responsToDict['ok'] is True

            if sendMessageValid:
                updateId = updates['result'][0]['update_id']
                command = 'getUpdates'
                urlopen(f'{URL}{command}?offset={updateId + 1}')    

    else:
        print('waiting!')
        time.sleep(1)
