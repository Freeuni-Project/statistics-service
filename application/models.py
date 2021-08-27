# application/models.py
from . import db
from datetime import datetime


class Stat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, unique=False, nullable=False)
    ticket_id = db.Column(db.Integer, unique=False, nullable=False)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    ticket_status = db.Column(db.String(25), unique=False, nullable=False, default='In progress')
    project_status = db.Column(db.String(25), unique=False, nullable=False, default='Ongoing')
    date_updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<project %r, user%r, ticket%r>' % (self.project_id, self.user_id, self.ticket_id)

    def to_json(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'ticket_id': self.ticket_id,
            'user_id': self.user_id,
            'ticket_status': self.ticket_status,
            'project_status': self.project_status,
            'date_updated': self.date_updated
        }
