# application/models.py
from . import db
from datetime import datetime


class Stat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, unique=False, nullable=False)
    ticket_id = db.Column(db.Integer, unique=False, nullable=False)
    reporter_id = db.Column(db.Integer, unique=False, nullable=False)
    assignee_id = db.Column(db.Integer, unique=False, nullable=False)
    ticket_status = db.Column(db.String(25), unique=False, nullable=False, default='In progress')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_finished = db.Column(db.DateTime, onupdate=datetime.utcnow, default=None)

    def __repr__(self):
        return '<project %r, user%r, ticket%r>' % (self.project_id, self.user_id, self.ticket_id)

    def to_json(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'ticket_id': self.ticket_id,
            'reporter_id': self.reporter_id,
            'assignee_id': self.assignee_id,
            'ticket_status': self.ticket_status,
            'date_created': self.date_created,
            'date_finished': self.date_finished
        }
