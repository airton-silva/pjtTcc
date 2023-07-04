from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
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