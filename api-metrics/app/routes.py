from ast import Str
from crypt import methods
from dataclasses import replace
from hmac import new
from os import times
# from urllib import response
from flask import Flask, Response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_cors import CORS
from main import coletar_dados_prometheus
from main import getTargets
from main import search_metric, buscar

# from main import gerar_response


# from ModelPreferences import ModelPreferences


app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/monitor'

db=SQLAlchemy(app)

class ModelPreferences(db.Model):
    __tablename__ = 'preferences'
    id = db.Column(db.Integer, primary_key=True)
    metric = db.Column(db.String(100))
    type = db.Column(db.String(100))
    create_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'metric': self.metric,
            'type': self.type,
            'create_at': self.create_at,
            'update_at': self.update_at
        }
 
db.create_all()

# Inicio Routes Preferences
@app.route('/preferences', methods=['GET'])
def get_preferences():
    preferences = ModelPreferences.query.all()
    data = [preference.to_dict() for preference in preferences]
    return jsonify(data)

#create a new preference  
@app.route('/preferences', methods=['POST'])
def create_preferences():
    data = request.get_json()
    try:
        preference = ModelPreferences(
            metric=data['metric'],
            type=data['type'],
            create_at=data['create_at'],
            update_at=data['update_at']
        )
        db.session.add(preference)
        db.session.commit()
        return jsonify(preference.to_dict())
    except Exception as e:
        return jsonify(str(e))

#update a preference
@app.route('/preferences/<int:id>', methods=['PUT'])
def update_preferences(id):
    data = request.get_json()
    try:
        preference = ModelPreferences.query.get(id)
        preference.metric = data['metric']
        preference.type = data['type']
        preference.create_at = data['create_at']
        preference.update_at = data['update_at']
        db.session.commit()
        return jsonify(preference.to_dict())
    except Exception as e:
        return jsonify(str(e))

#delete a preference
@app.route('/preferences/<int:id>', methods=['DELETE'])
def delete_preferences(id):
    try:
        preference = ModelPreferences.query.get(id)
        db.session.delete(preference)
        db.session.commit()
        return jsonify(preference.to_dict())
    except Exception as e:
        return jsonify(str(e))

#get a preference by id
@app.route('/preferences/<int:id>', methods=['GET'])
def get_preferences_id(id):
    preference = ModelPreferences.query.get(id)
    if preference:
        return jsonify(preference.to_dict())
    else:
        return jsonify({'message': 'Preference not found'})

# Fim Routes Preferences

@app.route('/')
def index():
    resp = getTargets('targets?state=active')
    return resp

@app.route('/percent-cpu', methods=['GET'])
def percentCpu():
    resp = coletar_dados_prometheus('CPU', 'consumo_percent_cpu',' ')
    return resp   
    #consumo_percent_cpu    

@app.route('/cpu', methods=['GET'])
def home():
    resp = coletar_dados_prometheus('CPU', 'machine_cpu_cores')
    return resp

@app.route('/cpu-usage', methods=['GET'])
def cpuConsumoTotal():

    resp = coletar_dados_prometheus('CPU', 'consumo_total_cpu',' ')
    return resp    

@app.route('/cpu/container', methods=['GET'])
def cpuBycontainer():
    resp = coletar_dados_prometheus('CPU', 'consume_cpu_by_container')
    return resp

@app.route('/Pods', methods=['GET'])
def pods():
    resp = coletar_dados_prometheus('Pods', 'cpu_usage_seconds_total',' ')
    return resp

@app.route('/percent-memory', methods=['GET'])
def percentMemory():
    resp = coletar_dados_prometheus('Memory', 'consumo_percent_memory',' ')
    return resp

@app.route('/memory', methods=['GET'])
def memory():
    resp = coletar_dados_prometheus('Memory', 'machine_memory_bytes',' ')
    return resp
@app.route('/memory-usage', methods=['GET'])
def memory_usage():
    resp = coletar_dados_prometheus('Memory', 'container_memoryWorking_set_bytes',' ')
    return resp

@app.route('/filesystem_percent', methods=['GET'])
def percentFilesystem():
    resp = coletar_dados_prometheus('FileSystem', 'consumo_percent_filesystem')
    return resp

@app.route('/filesystem_usage', methods=['GET'])
def filesystemConsume():
    resp = coletar_dados_prometheus('FileSystem', 'consumo_total_filesystem', '')
    return resp
#container_fs_limit_bytes

@app.route('/filesystem', methods=['GET'])
def filesystem():
    resp = coletar_dados_prometheus('FileSystem', 'container_fs_limit_bytes', '')
    return resp

@app.route('/memoria/<metric>', methods=['GET'])
def memory_metric(metric):
    print("q = ",metric)
    resp = search_metric('Memory', metric, '&time=1654190349.862')
    return resp

@app.route('/network/<metric>/', methods=['GET'])
def rede_metric(metric):
    data = datetime.now() # intante atual
    nowForm = (str(data).replace(' ', 'T'))
    startAt = nowForm[:23]+'Z'

    interval = datetime.now() - timedelta(minutes=5) #subtraindo 5 minutos do instante atual
    intvalForm = (str(interval).replace(' ', 'T'))
    endAt = intvalForm[:23]+'Z'

    print("start", intvalForm)

    print("stop", startAt)
    
    rangeTime = '&start='+endAt+'&end='+startAt+'&step=15s'  

    resp = search_metric('rede', metric, rangeTime)
    return resp

@app.route('/network/io/', methods=['GET'])
def rede_io():
    data = datetime.now() # intante atual
    nowForm = (str(data).replace(' ', 'T'))
    startAt = nowForm[:23]+'Z'

    interval = datetime.now() - timedelta(minutes=5) #subtraindo 5 minutos do instante atual
    intvalForm = (str(interval).replace(' ', 'T'))
    endAt = intvalForm[:23]+'Z'

    print("start", intvalForm)

    print("stop", startAt)
    
    rangeTime = '&start='+endAt+'&end='+startAt+'&step=15s'  

    receive = search_metric('rede', 'receive', rangeTime)
    sent = search_metric('rede', 'sent', rangeTime)
    
    result ={'receive': receive['data']['result'], 'sent':sent['data']['result']}

    return result
    

@app.route('/rede', methods=['GET'])
def rede():
    resp = coletar_dados_prometheus('rede', 'recebido',' ')
    return resp

@app.route('/request', methods=['GET'])
def requests():
    resp = coletar_dados_prometheus('Request', 'request_duration_seconds_count',' ')
    return resp

@app.route('/histograma', methods=['GET'])
def histograma():
    resp = coletar_dados_prometheus('histograma', 'histograma',' ')
    return resp

@app.route('/nodes/', methods=['GET'])
def nodes():
    resp = coletar_dados_prometheus('node', 'kube_node_info',' ')
    return resp   

@app.route('/namespaces/', methods=['GET']) 
def namespaces():
    resp = coletar_dados_prometheus('namespace', 'kube_namespace_labels',' ')
    return resp

@app.route('/source/<query>', methods=['GET'])
def source(query):
    resp = buscar(query)
    return resp
    
app.run()