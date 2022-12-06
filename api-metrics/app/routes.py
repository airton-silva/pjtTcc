from ast import Str
from crypt import methods
from dataclasses import replace
from hmac import new
from importlib import metadata
from os import times
from this import s
from urllib import response
import time
import json
# from urllib import response
from flask import Flask, Response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Float
from datetime import datetime, timedelta
from flask_cors import CORS
from main import coletar_dados_prometheus, criar_requisicao_prometheus_2
from main import getTargets
from main import search_metric, buscar, gerarMetadata, gerarQueryPreferences, conf_data_source, search_metric_opc
from alerts import getAlertByPod

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

class ModelDataSources(db.Model):
    __tablename__ = 'data_source'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    url = db.Column(db.String(50))
    authType = db.Column(db.String(50))



    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'url':self.url,
            'authType': self.authType
        }
db.create_all()

class ModelAlerts(db.Model):
    __tablename__ ='alerts_fails'
    id = db.Column(db.Integer, primary_key=True)
    pod = db.Column(db.String(50))
    mtype = db.Column(db.String(20))
    type = db.Column(db.String(50))
    alert = db.Column(db.String(50))
    time = db.Column(db.String(20))
    value = db.Column(db.String(20))
    create_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'pod': self.pod,
            'mtype':self.mtype,
            'type': self.type,
            'alert':self.alert,
            'time': self.time,
            'value': self.value,
            'create_at': self.create_at
        }
db.create_all()


class ModelCargas(db.Model):
    __tablename__ = 'cargas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    latencia_mean = db.Column(db.Float)
    latencia_total = db.Column(db.Float)
    mean_bytes_in = db.Column(db.Float)
    request_duration = db.Column(db.Float)
    wait = db.Column(db.Float)
    requests = db.Column(db.Integer)
    throughput = db.Column(db.Float)
    status_cod_success = db.Column(db.Integer)
    status_cod_bad_requset = db.Column(db.Integer)
    status_cod_sever = db.Column(db.Integer)
    errors = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'latencia_mean': self.latencia_mean,
            'latencia_total': self.latencia_total,
            'mean_bytes_in':self.mean_bytes_in,
            'request_duration': self.request_duration,
            'wait': self.wait,
            'requests': self.requests,
            'throughput' : self.throughput,
            'status_cod_success': self.status_cod_success,
            'status_cod_bad_requset': self.status_cod_bad_requset,
            'status_cod_sever': self.status_cod_sever,
            'errors': self.errors
        }
 
db.create_all()

#teste de carga
@app.route('/carga', methods=['POST'])
def create_valuesCarga():
    data = request.get_json()
    print(data['latencies']['mean'])
    try:
        tstcarga = ModelCargas(
            name = data['name'],
            latencia_mean=data['latencies']['mean'],
            latencia_total=data['latencies']['total'],
            mean_bytes_in=data['bytes_in']['mean'],
            request_duration=data['duration'],
            wait=data['wait'],
            requests=data['requests'],
            throughput =data['throughput'],
            status_cod_success=data['status_codes']['200'],
            status_cod_bad_requset=data['status_codes']['400'],
            status_cod_sever=data['status_codes']['500'],
            errors=data['errors']

        )
        db.session.add(tstcarga)
        db.session.commit()
        return jsonify(tstcarga.to_dict())
        
    except Exception as e:
        return jsonify(str(e))

#datasource
@app.route('/data_sources', methods=['GET'])
def get_dataSources():
    dataSources = ModelDataSources.query.all()
    data = [dataSource.to_dict() for dataSource in dataSources]
    return jsonify(data)

@app.route('/prometheus', methods=['GET'])
def mydatasources():
    dt_source = ModelDataSources.query.filter_by(name='Prometheus').first()
    # dt_source = ModelDataSources.query.all()
    d = conf_data_source(dt_source.to_dict())
    # for row in dt_source:
    #     print(row.name)
  
    if dt_source:
        return jsonify(dt_source.to_dict())
    else:
        return jsonify({'message': 'dt_source not found'})

@app.route('/prometheus/preferences', methods=['GET'])
def tst_metric():
    preferences = ModelPreferences.query.all()
    data = [preference.to_dict() for preference in preferences]
    # print(data['name'])
    rede = {}
    memory={}
    disco={}
    cpu={}
    mydict =[]
    for preference in preferences:
        # print(preference.metric+'_'+preference.name_pod)
        # print(preference.metric)
        if preference.metric == 'REDE':
            rede = {
                "%s " % preference.name_pod +":"+ "'%s'" % preference.myquery
            }
            mydict.append(rede)
            # print(rede)
        elif preference.metric == 'MEMORIA':
            memory = {
                "%s " % preference.name_pod +":"+ "'%s'" % preference.myquery
            }
            mydict.append(memory)
        elif preference.metric == 'CPU':
            cpu = {
                "%s " % preference.name_pod +":"+ "'%s'" % preference.myquery
            }
            mydict.append(cpu)
        elif preference.metric == 'DISCO':
            disco = {
                "%s " % preference.name_pod +":"+ "'%s'" % preference.myquery
            }
            mydict.append(disco)

    data = mydict
    # print(type(data) )

    class SetEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, set):
                return list(obj)
            return json.JSONEncoder.default(self, obj)
    try:
        return json.dumps(data,  cls=SetEncoder)
    #    return jsonify({'dictmetrics':data})

    except Exception as e:
        return jsonify(str(e))


@app.route('/data_sources', methods=['POST'])
def create_dataSource():
    data = request.get_json()
    try:
        dsource = ModelDataSources(
            name= data['name'],
            url= data['url'],
            authType = data['authType']

        )
        db.session.add(dsource)
        db.session.commit()
        return jsonify(dsource.to_dict())
        
    except Exception as e:
        return jsonify(str(e))

@app.route('/data_sources/<int:id>', methods=['DELETE'])
def delete_dataSource(id):
    try:
        datasource = ModelDataSources.query.get(id)
        db.session.delete(datasource)
        db.session.commit()
        return jsonify(datasource.to_dict())
    except Exception as e:
        return jsonify(str(e))

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
        preference.myquery = gerarQueryPreferences(data['name_pod']+'_'+data['type'] ,data['type'],data['metric'],data['name_pod']),
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

@app.route('/preferences/merge', methods=['GET'])
def get_preferences_merge():
    # consumeCpuByContainer = coletar_dados_prometheus('Pods', 'container_cpu_usage_seconds_total_teastore-webui-5d554cc97f-b9xvj')  
    # consumeMemoryByContainer = coletar_dados_prometheus('Pods', 'container_memoryWorking_set_bytes_teastore-webui-5d554cc97f-b9xvj')

    CpuMetrics ={
        'teastore-webui-5d554cc97f-b9xvj' : coletar_dados_prometheus('Pods', 'container_cpu_usage_seconds_total_teastore-webui-5d554cc97f-b9xvj')['data']['result'][0]['value'],
        'teastore-db-5d9555684f-mvzn2': coletar_dados_prometheus('Pods', 'container_cpu_usage_seconds_total_teastore-db-5d9555684f-mvzn2')['data']['result'][0]['value'],
        'teastore-image-5599565ccf-mnl5v' : coletar_dados_prometheus('Pods', 'container_cpu_usage_seconds_total_teastore-image-5599565ccf-mnl5v')['data']['result'][0]['value'],
        'teastore-persistence-d69d45b4-47bsj': coletar_dados_prometheus('Pods', 'container_cpu_usage_seconds_total_teastore-persistence-d69d45b4-47bsj')['data']['result'][0]['value'],
        'teastore-auth-775c7fc4cc-ck64p': coletar_dados_prometheus('Pods', 'container_cpu_usage_seconds_total_teastore-auth-775c7fc4cc-ck64p')['data']['result'][0]['value'],
        'teastore-recommender-8589c6d499-g96fp': coletar_dados_prometheus('Pods', 'container_cpu_usage_seconds_total_teastore-recommender-8589c6d499-g96fp')['data']['result'][0]['value'],
        # 'teastore_registry': coletar_dados_prometheus('Pods', 'container_cpu_usage_seconds_total_teastore-registry-668b87766-s7jkz')['data']['result'],

    },

    MemoryMetrics={
        'teastore-webui-5d554cc97f-b9xvj' : coletar_dados_prometheus('Pods', 'container_memoryWorking_set_bytes_teastore-webui-5d554cc97f-b9xvj')['data']['result'][0]['value'],
        'teastore-db-5d9555684f-mvzn2': coletar_dados_prometheus('Pods', 'container_memoryWorking_set_bytes_teastore-db-5d9555684f-mvzn2')['data']['result'][0]['value'],
        'teastore-image-5599565ccf-mnl5v' : coletar_dados_prometheus('Pods', 'container_memoryWorking_set_bytes_teastore-image-5599565ccf-mnl5v')['data']['result'][0]['value'],
        'teastore-persistence-d69d45b4-47bsj': coletar_dados_prometheus('Pods', 'container_memoryWorking_set_bytes_teastore-persistence-d69d45b4-47bsj')['data']['result'][0]['value'],
        'teastore-auth-775c7fc4cc-ck64p': coletar_dados_prometheus('Pods', 'container_memoryWorking_set_bytes_teastore-auth-775c7fc4cc-ck64p')['data']['result'][0]['value'],
        'teastore-recommender-8589c6d499-g96fp': coletar_dados_prometheus('Pods', 'container_memoryWorking_set_bytes_teastore-recommender-8589c6d499-g96fp')['data']['result'][0]['value'],
        # 'teastore_registry': coletar_dados_prometheus('Pods', 'container_memoryWorking_set_bytes_teastore-registry-668b87766-s7jkz')['data']['result'],

    }


    read = {
        'teastore-webui-5d554cc97f-b9xvj' : coletar_dados_prometheus('Pods', 'container_fs_reads_bytes_total_teastore-webui-5d554cc97f-b9xvj')['data']['result'][0]['value'],
        # 'teastore-db-5d9555684f-mvzn2': coletar_dados_prometheus('Pods', 'container_fs_reads_bytes_total_teastore-db-5d9555684f-mvzn2')['data']['result'][0]['value'],
        'teastore-image-5599565ccf-mnl5v' : coletar_dados_prometheus('Pods', 'container_fs_reads_bytes_total_teastore-image-5599565ccf-mnl5v')['data']['result'][0]['value'],
        'teastore-persistence-d69d45b4-47bsj': coletar_dados_prometheus('Pods', 'container_fs_reads_bytes_total_teastore-persistence-d69d45b4-47bsj')['data']['result'][0]['value'],
        'teastore-auth-775c7fc4cc-ck64p': coletar_dados_prometheus('Pods', 'container_fs_reads_bytes_total_teastore-auth-775c7fc4cc-ck64p')['data']['result'][0]['value'],
        'teastore-recommender-8589c6d499-g96fp': coletar_dados_prometheus('Pods', 'container_fs_reads_bytes_total_teastore-recommender-8589c6d499-g96fp')['data']['result'][0]['value'],
        # 'teastore_registry': coletar_dados_prometheus('Pods', 'container_fs_reads_bytes_total_teastore-registry-668b87766-s7jkz')['data']['result'],

    },
    writes = {
        'teastore-webui-5d554cc97f-b9xvj' : coletar_dados_prometheus('Pods', 'container_fs_writes_bytes_total_teastore-webui-5d554cc97f-b9xvj')['data']['result'][0]['value'],
        # 'teastore-db-5d9555684f-mvzn2': coletar_dados_prometheus('Pods', 'container_fs_writes_bytes_total_teastore-db-5d9555684f-mvzn2')['data']['result'][0]['value'],
        'teastore-image-5599565ccf-mnl5v' : coletar_dados_prometheus('Pods', 'container_fs_writes_bytes_total_teastore-image-5599565ccf-mnl5v')['data']['result'][0]['value'],
        'teastore-persistence-d69d45b4-47bsj': coletar_dados_prometheus('Pods', 'container_fs_writes_bytes_total_teastore-persistence-d69d45b4-47bsj')['data']['result'][0]['value'],
        'teastore-auth-775c7fc4cc-ck64p': coletar_dados_prometheus('Pods', 'container_fs_writes_bytes_total_teastore-auth-775c7fc4cc-ck64p')['data']['result'][0]['value'],
        'teastore-recommender-8589c6d499-g96fp': coletar_dados_prometheus('Pods', 'container_fs_writes_bytes_total_teastore-recommender-8589c6d499-g96fp')['data']['result'][0]['value'],
        # 'teastore_registry': coletar_dados_prometheus('Pods', 'container_fs_writes_bytes_total_teastore-registry-668b87766-s7jkz')['data']['result'],
    },

    transmit ={
        'teastore-webui-5d554cc97f-b9xvj' : coletar_dados_prometheus('Pods', 'container_network_transmit_bytes_total_teastore-webui-5d554cc97f-b9xvj')['data']['result'][0]['value'],
        # 'teastore-db-5d9555684f-mvzn2': coletar_dados_prometheus('Pods', 'container_network_transmit_bytes_total_teastore-db-5d9555684f-mvzn2')['data']['result'][0]['value'],
        'teastore-image-5599565ccf-mnl5v' : coletar_dados_prometheus('Pods', 'container_network_transmit_bytes_total_teastore-image-5599565ccf-mnl5v')['data']['result'][0]['value'],
        'teastore-persistence-d69d45b4-47bsj': coletar_dados_prometheus('Pods', 'container_network_transmit_bytes_total_teastore-persistence-d69d45b4-47bsj')['data']['result'][0]['value'],
        'teastore-auth-775c7fc4cc-ck64p': coletar_dados_prometheus('Pods', 'container_network_transmit_bytes_total_teastore-auth-775c7fc4cc-ck64p')['data']['result'][0]['value'],
        'teastore-recommender-8589c6d499-g96fp': coletar_dados_prometheus('Pods', 'container_network_transmit_bytes_total_teastore-recommender-8589c6d499-g96fp')['data']['result'][0]['value'],
        # 'teastore_registry': coletar_dados_prometheus('Pods', 'container_network_transmit_bytes_total_teastore-registry-668b87766-s7jkz')['data']['result'],

    },

    receive =[{
        'teastore-webui-5d554cc97f-b9xvj' : coletar_dados_prometheus('Pods', 'container_network_receive_bytes_total_teastore-webui-5d554cc97f-b9xvj')['data']['result'][0]['value'],
        # 'teastore-db-5d9555684f-mvzn2': coletar_dados_prometheus('Pods', 'container_network_receive_bytes_total_teastore-db-5d9555684f-mvzn2')['data']['result'][0]['value'],
        'teastore-image-5599565ccf-mnl5v' : coletar_dados_prometheus('Pods', 'container_network_receive_bytes_total_teastore-image-5599565ccf-mnl5v')['data']['result'][0]['value'],
        'teastore-persistence-d69d45b4-47bsj': coletar_dados_prometheus('Pods', 'container_network_receive_bytes_total_teastore-persistence-d69d45b4-47bsj')['data']['result'][0]['value'],
        'teastore-auth-775c7fc4cc-ck64p': coletar_dados_prometheus('Pods', 'container_network_receive_bytes_total_teastore-auth-775c7fc4cc-ck64p')['data']['result'][0]['value'],
        'teastore-recommender-8589c6d499-g96fp': coletar_dados_prometheus('Pods', 'container_network_receive_bytes_total_teastore-recommender-8589c6d499-g96fp')['data']['result'][0]['value'],
        # 'teastore_registry': coletar_dados_prometheus('Pods', 'container_network_receive_bytes_total_teastore-registry-668b87766-s7jkz')['data']['result'],
    }]


    disk ={
        'readNods': read,
        'writeNods': writes,

    }
    netWork ={
        'transmit_bytes' : transmit,
        'receive_bytes': receive,
    }
    MergeMetricsNodes ={
            'CPU': CpuMetrics,
            'MEMORY': [MemoryMetrics],
            'disk': disk,
            'Network': netWork,
    }

    print(disk)
        
    return MergeMetricsNodes


@app.route('/')
def index():
    resp = getTargets('targets?state=active')
    return resp

@app.route('/alerts/all', methods=['GET'])
def getAll_alerts():
    allAlerts = ModelAlerts.query.filter(ModelAlerts.alert=='failure')
    data = [alerts.to_dict() for alerts in allAlerts]
    return jsonify(data)

@app.route('/alerts/<filter>', methods=['GET'])
def getByAlerts(filter):
    allAlerts = ModelAlerts.query.filter(ModelAlerts.type==filter)
    data = [alerts.to_dict() for alerts in allAlerts]
    return jsonify(data)

@app.route('/alerts', methods=['GET'])
def get_alerts():
    objs = ModelPreferences.query.all()
    alert_fail =[]

    for ob in objs:
   
        if ob.metric =='CPU':
            resp = getAlertByPod(ob.name_pod, ob.metric, ob.type, ob.value_failure)
            cpu={
                'cpu': resp
            }
            alert_fail.append(cpu)
        if ob.metric =='MEMORIA':
            resp = getAlertByPod(ob.name_pod, ob.metric, ob.type, ob.value_failure)
            memory={
                'memory': resp
            }
            alert_fail.append(memory)
        if ob.metric =='DISCO':
            read= getAlertByPod(ob.name_pod, ob.metric, ob.type, ob.value_failure)
            write= getAlertByPod(ob.name_pod, ob.metric, ob.type, ob.value_failure)
            disk = {
                'read':read,
                'write':write
            }
            alert_fail.append(disk)
        if ob.metric =='REDE':
            receive= getAlertByPod(ob.name_pod, ob.metric, ob.type, ob.value_failure)
            send = getAlertByPod(ob.name_pod, ob.metric, ob.type, ob.value_failure)
            network = {
                'receive':receive,
                'send':send
            }
            alert_fail.append(network)

    print(alert_fail)

    for alert in alert_fail:
        # rede send
        if alert.get('send') != None:

            for al in alert.get('send'):
                try:
                    alerts = ModelAlerts(
                        pod= al['pod'],
                        mtype= 'send',
                        type= al['type'],
                        alert=al['alert'],
                        time= al['time'],
                        value= al['value'],
                        create_at= datetime.now().date()
                    )
                    db.session.add(alerts)
                    db.session.commit()
                except Exception as e:
                    return jsonify(str(e))
        # rede receive
        if alert.get('receive') != None:
            for al in alert.get('receive'):
                try:
                    alerts = ModelAlerts(
                        pod= al['pod'],
                        mtype= 'receive',
                        type= al['type'],
                        alert=al['alert'],
                        time= al['time'],
                        value= al['value'],
                        create_at= datetime.now().date()
                    )
                    db.session.add(alerts)
                    db.session.commit()
                except Exception as e:
                    return jsonify(str(e))        

        # cpu
        if alert.get('cpu') != None:

            for al in alert.get('cpu'):
                # print("**\n"+al['pod'])
                try:
                    alerts = ModelAlerts(
                        pod= al['pod'],
                        mtype= 'cpu',
                        type= al['type'],
                        alert=al['alert'],
                        time= al['time'],
                        value= al['value'],
                        create_at= datetime.now().date()
                    )
                    db.session.add(alerts)
                    db.session.commit()
                except Exception as e:
                    return jsonify(str(e))
        # memory
        if alert.get('memory') != None:

            for al in alert.get('memory'):
                # print("memory--\n"+al['pod'])
                try:
                    alerts = ModelAlerts(
                        pod= al['pod'],
                        mtype= 'memory',
                        type= al['type'],
                        alert=al['alert'],
                        time= al['time'],
                        value= al['value'],
                        create_at= datetime.now().date()
                    )
                    db.session.add(alerts)
                    db.session.commit()
                except Exception as e:
                    return jsonify(str(e))        

        # disco read
        if alert.get('read') != None:

            for al in alert.get('read'):
                try:
                    alerts = ModelAlerts(
                        pod= al['pod'],
                        mtype= 'read',
                        type= al['type'],
                        alert=al['alert'],
                        time= al['time'],
                        value= al['value'],
                        create_at= datetime.now().date()
                    )
                    db.session.add(alerts)
                    db.session.commit()
                except Exception as e:
                    return jsonify(str(e))
        # disco write
        if alert.get('write') != None:
            for al in alert.get('write'):
                try:
                    alerts = ModelAlerts(
                        pod= al['pod'],
                        mtype= 'write',
                        type= al['type'],
                        alert=al['alert'],
                        time= al['time'],
                        value= al['value'],
                        create_at= datetime.now().date()
                    )
                    db.session.add(alerts)
                    db.session.commit()
                except Exception as e:
                    return jsonify(str(e)) 
    
    return jsonify(alerts.to_dict())


@app.route('/percent-cpu', methods=['GET'])
def percentCpu():
    resp = coletar_dados_prometheus('CPU', 'consumo_percent_cpu',' ')
    return resp
    #consumo_percent_cpu    

@app.route('/cpu', methods=['GET'])
def home():
    resp = coletar_dados_prometheus('CPU', 'machine_cpu_cores')
    return resp

@app.route('/cpu/host', methods=['GET'])
def cpuHost():
    cpuHostMetrics ={
        'machine_cpu_cores': coletar_dados_prometheus('CPU', 'machine_cpu_cores'),
        'consumo_percent_cpu': coletar_dados_prometheus('CPU', 'consumo_percent_cpu'),
    }
    resp = cpuHostMetrics
    return resp

@app.route('/cpu/<type>', methods=['GET'])
def metricCpu(type):
    print(type)
    resp = coletar_dados_prometheus('CPU', type)
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

@app.route('/graf/<metric>', methods=['GET'])
def getByRange(metric):
    data = datetime.now() # intante atual
    nowForm = (str(data).replace(' ', 'T'))
    startAt = nowForm[:23]+'Z'

    interval = datetime.now() - timedelta(minutes=5) #subtraindo 5 minutos do instante atual
    intvalForm = (str(interval).replace(' ', 'T'))
    endAt = intvalForm[:23]+'Z'

    print("start", intvalForm)

    print("stop", startAt)
    
    rangeTime = '&start='+endAt+'&end='+startAt+'&step=15s'  

    metricsRange = search_metric('CPU', metric , rangeTime)
    return metricsRange


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

@app.route('/memory/host', methods=['GET'])
def memoryHost():
    metricMemoryHost ={
        'machine_memory_bytes':coletar_dados_prometheus('Memory', 'machine_memory_bytes',' '),
        'container_memoryWorking_set_bytes': coletar_dados_prometheus('Memory', 'container_memoryWorking_set_bytes',' '),
        'consumo_percent_memory': coletar_dados_prometheus('Memory', 'consumo_percent_memory',' ')
    }
    return metricMemoryHost

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

    interval = datetime.now() - timedelta(minutes=10) #subtraindo 5 minutos do instante atual
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
    data = datetime.now() # intante atual
    nowForm = (str(data).replace(' ', 'T'))
    startAt = nowForm[:23]+'Z'

    interval = datetime.now() - timedelta(minutes=5) #subtraindo 5 minutos do instante atual
    intvalForm = (str(interval).replace(' ', 'T'))
    endAt = intvalForm[:23]+'Z'
    rangeTime = '&start='+endAt+'&end='+startAt+'&step=15s' 

    resp = coletar_dados_prometheus('histograma', 'histograma', '')
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

@app.route('/source', methods=['POST'])
def source_opc():
    data = request.get_json()
    api =data['url']
    q_type = data['type']
    exp_query = data['query']
    dt = datetime.now() # instante atual
    ts = datetime.timestamp(dt)

    if(q_type == 'none'):
        mount_query = api+exp_query
    else:
         mount_query = api + q_type +'?query='+exp_query+'&time='+str(ts)
   
    resp = search_metric_opc(mount_query)
    print(resp)
    return resp



@app.route('/metadata', methods=['GET'])
def metadatas():
    resp = gerarMetadata()
    return resp


app.run()