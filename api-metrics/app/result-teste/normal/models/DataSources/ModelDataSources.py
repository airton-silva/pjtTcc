from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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