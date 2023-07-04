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
