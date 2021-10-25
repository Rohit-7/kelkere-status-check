import requests
import json
from jinja2 import Environment, FileSystemLoader
from requests.auth import HTTPBasicAuth

app_env = Environment(loader=FileSystemLoader('./'))
template = app_env.get_template('MailTemplate.html')
json_filepath = './Server Data.json'
servers = None

with open(json_filepath,'r') as f:
    servers = json.load(f)

for comp in servers:
    for env in servers[comp]:
        url = servers[comp][env]
        url = url.strip()
        try:
            response = requests.get(url, auth=HTTPBasicAuth('',''),timeout=3)
            servers[comp][env] = response.status_code
            print(url,'->',response.status_code)
        except requests.exceptions.Timeout:
            response = None
            servers[comp][env] = 408
            print(url,'->','Timed out.')
        except requests.exceptions.ConnectionError:
            response = None
            servers[comp][env] = 502
            print(url,'->','Bad URL.')

target_filename = 'index.html'
with open(target_filename,'w') as f:
    f.write(template.render(servers=servers))