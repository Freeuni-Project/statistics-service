import json
import time
from datetime import datetime

import pika
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

from application import db, create_app
from application.models import Stat
from run import app

sleepTime = 1
print(' [*] Sleeping for ', sleepTime, ' seconds.')
time.sleep(sleepTime)

print(' [*] Connecting *statistics-service* to server ...')
parameters = pika.ConnectionParameters(host='rabbitmq', heartbeat=0)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='stat_queue', durable=True)
channel.basic_qos(prefetch_count=1)
threads = []
print(' [*] Waiting for messages.')


def add_stat_new(data, content_type):
    try:
        stat = Stat()
        stat.project_id = data['project_id']
        stat.reporter_id = data['reporter_id']
        stat.assignee_id = data['assignee_id']
        stat.ticket_id = data['id']
        stat.ticket_status = data['status']

        with app.app_context():
            db.session.add(stat)
            db.session.commit()
    except exc.SQLAlchemyError:
        print("Unable to save new stat --- %r", content_type)


def update_stat_done(data, content_type):
    try:
        ticket_id = data['id']
        with app.app_context():
            stat = Stat.query.filter_by(ticket_id=ticket_id).first()
            stat.ticket_status = "Done"
            db.session.commit()
    except exc.SQLAlchemyError:
        print("Unable to update new stat --- %r", content_type)


def delete_stat_from_db(data, content_type):
    try:
        with app.app_context():
            ticket_id = data['ticket_id']
            Stat.query.filter_by(ticket_id=ticket_id).delete()
            db.session.commit()
    except exc.SQLAlchemyError:
        print("Unable to delete stat --- %r", content_type)


add_stats = ['new_ticket', 'done_ticket']
delete_stats = ['delete_ticket']


def callback(ch, method, properties, body):
    data = json.loads(body)
    if properties.content_type == 'new_ticket':
        add_stat_new(data, properties.content_type)

    elif properties.content_type == 'done_ticket':
        update_stat_done(data, properties.content_type)

    elif properties.content_type == 'delete_ticket':
        delete_stat_from_db(data, properties.content_type)


channel.basic_consume(queue='stat_queue', on_message_callback=callback, auto_ack=True)

print('Started consuming')

channel.start_consuming()

