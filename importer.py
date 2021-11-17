import LAMP
import requests
LAMP.connect() # Please set env variables!

count = 0
for researcher in LAMP.Researcher.all()['data']:
    try:
        config = LAMP.Type.get_attachment(researcher['id'], 'org.digitalpsych.redcap.importer')['data']
        count += 1
    except LAMP.ApiException:
        continue # This Researcher is not configured for imports; ignore it.
    fields = {
        'token': config['API_TOKEN'],
        'content': 'record',
        'format': 'json',
        'type': 'flat',
        'exportSurveyFields': 'true'
    }
    records = requests.post(config['API_URL'], data=fields).json()
    LAMP.Type.set_attachment(researcher['id'], 'me',
                             attachment_key='org.digitalpsych.redcap.data',
                             body=records)
    print(count)
    try:
        arr = LAMP.Type.get_attachment(researcher['id'], 'org.digitalpsych.redcap.links')["data"]
    except LAMP.ApiException:
        continue # Ignore this Researcher
    parts = []
    for study in LAMP.Study.all_by_researcher(researcher['id'])['data']:
        parts+=(p['id'] for p in LAMP.Participant.all_by_study(study['id'])['data'])
    for p in parts:
        try:
            record_id = LAMP.Type.get_attachment(p, 'org.digitalpsych.redcap.id')["data"]
        except LAMP.ApiException:
            continue # Ignore this Participant
        if record_id >= 0:
            try:
                link = LAMP.Type.get_attachment(p, 'org.digitalpsych.redcap.links')["data"]
            except LAMP.ApiException:
                links = {}
                for s in arr:
                    data = {
                        'token': config['API_TOKEN'],
                        'content': 'surveyLink',
                        'format': 'json',
                        'instrument': s,
                        'event': '',
                        'record': record_id,
                        'returnFormat': 'json'
                    }
                    r = requests.post(config['API_URL'], data=data)
                    links[s] = r.text
                LAMP.Type.set_attachment(p, 'me',
                                attachment_key='org.digitalpsych.redcap.links',
                                body=links)

print("Finished importing data.")
