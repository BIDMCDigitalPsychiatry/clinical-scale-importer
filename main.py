import os 
import requests  
records = requests.post(os.getenv('API_URL', ''), data={
  'token': os.getenv('API_TOKEN', ''),
  'content': 'record',
  'format': 'json',
  'type': 'flat',
  'exportSurveyFields': 'true'
}).json()
print(records[0:2])
