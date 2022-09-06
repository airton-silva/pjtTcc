from ast import Str
from crypt import methods
from dataclasses import replace
from hmac import new
from importlib import metadata
from os import times
from this import s
from urllib import response
import time
# from urllib import response
from flask import Flask, Response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_cors import CORS
from main import coletar_dados_prometheus
from main import getTargets
from main import search_metric, buscar, gerarMetadata, gerarQueryPreferences

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
    name = db.Column(db.String(50))
    name_pod = db.Column(db.String(50))
    metric = db.Column(db.String(50))
    type = db.Column(db.String(50))
    value_failure = db.Column(db.String(20))
    period_time = db.Column(db.String(20))
    myquery = db.Column(db.String(255))
    create_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'name_pod':self.name_pod,
            'metric': self.metric,
            'type': self.type,
            'value_failure': self.value_failure,
            'period_time' : self.period_time,
            'myquery': self.myquery,
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
    print(data)
    try:
        preference = ModelPreferences(
            name= data['name'],
            name_pod= data['name_pod'],
            metric=data['metric'],
            type=data['type'],
            value_failure = data['value_failure'],
            period_time = data['period_time'],
            myquery= gerarQueryPreferences(data['name_pod']+'_'+data['type'] ,data['type'],data['metric'],data['name_pod']),
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
        preference.name= data['name'],
        preference.name_pod= data['name_pod']
        preference.metric = data['metric'],
        preference.type = data['type']
        preference.value_failure = data['value_failure'],
        preference.period_time = data['period_time'],
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

# @app.route('/preferences/fail', methods=['GET'])
# def get_preferences_Fail():

    # preferenceCPU = ModelPreferences.query.filter_by(metric='CPU').all()
    # print(preferenceCPU)
    # if preferenceCPU:
    #     return jsonify(preferenceCPU.to_dict())
    # else:
    #     return jsonify({'message': 'Preference not found'})

# Fim Routes Preferences
@app.route('/preferences/merge', methods=['GET'])
def get_preferences_merge():
    consumeCpuByContainer = coletar_dados_prometheus('CPU', 'container_cpu_usage_seconds_total_teastore-webui-5d9c74d9d6-9lrw5')  
    consumeMemoryByContainer = coletar_dados_prometheus('Memory', 'container_memoryWorking_set_bytes_teastore-webui-5d9c74d9d6-9lrw5')

 
    FileSystem ={
        'reads': coletar_dados_prometheus('FileSystem', 'container_fs_reads_bytes_total_teastore-webui-5d9c74d9d6-9lrw5')['data']['result'],
        'writes':coletar_dados_prometheus('FileSystem', 'container_fs_writes_bytes_total_teastore-webui-5d9c74d9d6-9lrw5')['data']['result']

    }
    netWork ={
        'transmit_bytes' : coletar_dados_prometheus('rede', 'container_network_transmit_bytes_total')['data']['result'],
        'receive_bytes': coletar_dados_prometheus('rede', 'container_network_receive_bytes_total')['data']['result']
    }
    teastore_webui_5d9c74d9d6_9lrw5 ={'teastore_webui_5d9c74d9d6_9lrw5': {
            'CPU': consumeCpuByContainer['data']['result'],
            'MEMORY': consumeMemoryByContainer['data']['result'],
            'FileSystem': FileSystem,
            'Network': netWork,
            }
        }
    return teastore_webui_5d9c74d9d6_9lrw5


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
    consumeBycontainer = coletar_dados_prometheus('CPU', 'consume_cpu_by_container')    
    resp ={'cpu_consume': consumeBycontainer['data']['result']}
    return resp

@app.route('/pods', methods=['GET'])
def pods():
    # data = datetime.now()
    # timesStamp = (time.mktime(data.timetuple()))
    resp = coletar_dados_prometheus('Pods', 'kube_pod_labels', '')
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

@app.route('/filesystem/ct', methods=['GET'])
def filesystem_ct():
    resp = coletar_dados_prometheus('FileSystem', 'container_fs_writes_bytes_total', '')
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
    resp = coletar_dados_prometheus('Request', 'http_requests_total',' ')
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

@app.route('/metadata', methods=['GET'])
def metadatas():
    resp = gerarMetadata()
    return resp

# @app.route('/', methods=['GET'])    
# def discoveredLabel():
#     resp = getTargets('targets?discoveredLabels?__meta_kubernetes_endpoints_name')
#     return resp

app.run()