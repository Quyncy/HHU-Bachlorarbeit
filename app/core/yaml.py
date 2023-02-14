"""
tutor.yml Datei erstellen
"""

import yaml

with open('tutor_hours.yml', 'r') as file:
    data = yaml.load(file, Loader=yaml.FullLoader)

tutor = data['tutor']
print(tutor[0]['tutor_id'])
print(tutor[0]['hours'])

# Update Daten
tutor[0]['hours'] = 10

# Schreibe die Daten in eine yml Datei
with open('tutor.yml', 'w') as file:
    yaml.dump(data, file)


# oder 

import yaml
import requests

response = requests.get('https://127.0.0.1:8000/list_tutor/')
tutor_info = response.json()

tutor = [{'name': tutor['matrikelnummer'], 'hours': tutor['arbeitsstunden']} for tutor in tutor_info]
data = {'tutor': tutor}

with open('tutor.yml', 'w') as file:
    yaml.dump(data, file)