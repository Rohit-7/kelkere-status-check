import requests
import json
from requests.auth import HTTPBasicAuth

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

table_style = 'border-collapse: collapse;border-radius: 0.5em;overflow: hidden;'

th_style = 'background-color: #111;background-clip: padding-box;color:white;position: sticky;margin-top:1em;top:0;padding: 0.75em 1em; border-bottom: 3px solid white;'

td_style = 'padding: 0.5em 1em; border-bottom: 3px solid white;'

td_style_border = 'border-left: 3px solid white;'

box_style = 'display: inline-block;padding: 0.5em;margin:5px;border-radius: 0.25em;'

green_box = 'background-color: #7CFC00;'

red_box = 'background-color: #FF3131;color:white;'

light_row = 'background-color: #e7e7e7;'

dark_row = 'background-color: #c7c7c7;'

html =  ''' <div style='width:auto; max-width:95%; margin:25px auto;'>
<table style="'''+ table_style +'''">
<thead>
<tr>
<th style="'''+ th_style +'''">Application</th>
<th style="'''+ th_style + td_style_border +'''">Environment</th>
</tr>
</thead>
<tbody>
'''

count = 0

for comp in servers:
    count += 1
    html +=  '<tr>\n<td style="'+ (light_row if count%2==0 else dark_row) + td_style +'">' + str(comp) + '</td>\n<td style="' + (light_row if count%2==0 else dark_row) + td_style_border + td_style + '">\n'
    for env in servers[comp]:
        html += "<div style='" + box_style + (green_box if servers[comp][env]==200 else red_box) + "'>" + str(env) + "</div>\n"
    html += '</td>\n</tr>'

html += '</tbody>\n</table>\n</div>'

target_filename = 'index.html'
with open(target_filename,'w') as f:
    f.write(html)