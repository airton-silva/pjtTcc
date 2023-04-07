from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
 
# db.create_all()

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
# db.create_all()

class ModelAlerts(db.Model):
    __tablename__ ='alerts_fails'
    id = db.Column(db.Integer, primary_key=True)
    pod = db.Column(db.String(50))
    mtype = db.Column(db.String(20))
    type = db.Column(db.String(50))
    alert = db.Column(db.String(50))
    time = db.Column(db.String(20))
    value = db.Column(db.Float)
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
# db.create_all()

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
 
# db.create_all()