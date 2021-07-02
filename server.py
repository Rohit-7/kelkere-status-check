from flask import Flask, render_template, jsonify, request
from datetime import date
import pandas as pd
import time
import socket

app = Flask(__name__)
app.config.from_pyfile('./config.py')
server_list = []

@app.route('/',methods=['GET'])
def index_page():    
    filepath = app.config['SERVERS_FILE_LOCATION']
    excel_data_frame = pd.read_excel(filepath, sheet_name=0)
    excel_data = excel_data_frame.to_dict(orient='records')
    for server in excel_data:
        server_list.append(server)
        server['Status'] = -1
        # server.pop('Server',None)
        # server.pop('Port',None)

    return render_template("StatusCheck.html",servers=excel_data)

@app.route('/get-status',methods=['POST'])
def test_conn():
    application = request.get_json()['Application']
    component = request.get_json()['Component']
    environment = request.get_json()['Environment']
    server = None
    port = None
    for item in server_list:
        if item['Application'] == application:
            if item['Component'] == component:
                if item['Environment'] == environment:
                    server = item['Server']
                    port = item['Port']
    if server is not None and port is not None:
        # print(server,port)
        status = None
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((server,port))
        sock.settimeout(2)
        if result == 0:
            # print('Port is open.')
            status = 1
        else:
            # print('Port is closed.')
            status = 0
        sock.close()
        return jsonify({'Status':status})
    
    else:
        return "Unknown"

if __name__ == '__main__':
    app.run(debug=True,port=5000)